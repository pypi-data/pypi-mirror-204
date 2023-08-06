from uuid import uuid4

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from drf_spectacular.utils import (
    OpenApiTypes,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users import schemas
from users.forms import PasswordChangeForm
from users.serializers import (
    ChangeEmailSerializer,
    ChangePasswordSerializer,
    RemindPasswordSerializer,
    SocialAuthSerializer,
    StandardLoginSerializer,
    StandardRegistrationSerializer,
    TokenSerializer,
)
from users.tasks import (
    delete_account,
    send_auth_email,
    send_change_password_email,
)
from users.utils import FacebookAuthorization, GoogleAuthorization, get_hash

User = get_user_model()


@extend_schema_view(
    post=extend_schema(
        request=None,
        responses={
            201: TokenSerializer,
        },
    )
)
class BackgroundRegistrationView(APIView):
    def post(self, request):
        users_count = User.objects.count()
        username_uuid = "{}-{}".format(users_count + 1, uuid4())

        user = User.objects.create(
            username=username_uuid, account_type=User.Type.anonymous
        )
        serializer = TokenSerializer(user.auth_token)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    post=extend_schema(
        request=None,
        parameters=schemas.STANDARD_REGISTRATION_POST_PARAMETERS,
        responses={201: TokenSerializer, 400: StandardRegistrationSerializer},
    )
)
class StandardRegistrationView(APIView):
    def post(self, request):
        serializer = StandardRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            send_auth_email.delay(user.pk, request.scheme, request.get_host())

            token_serializer = TokenSerializer(user.auth_token)
            return Response(
                token_serializer.data, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        request=None,
        parameters=schemas.STANDARD_LOGIN_POST_PARAMETERS,
        responses={200: TokenSerializer, 400: OpenApiTypes.OBJECT},
        examples=[
            schemas.ACCOUNT_LOGIN_FAILED_RESPONSE,
        ],
    )
)
class StandardLoginView(APIView):
    @classmethod
    def get_response_serializer_class(self):
        LOGIN_RESPONSE_SERIALIZER_PATH = getattr(
            settings, "LOGIN_RESPONSE_SERIALIZER_PATH", None
        )

        if LOGIN_RESPONSE_SERIALIZER_PATH:
            try:
                return import_string(LOGIN_RESPONSE_SERIALIZER_PATH)
            except ImportError:
                raise ImproperlyConfigured("Module cannot be resolved.")

        return TokenSerializer

    def post(self, request):
        serializer = StandardLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=serializer.data["email"])
            if not user.is_active:
                return Response(
                    {"error_code": "02", "error_msg": _("User not active")},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"error_code": "01", "error_msg": _("User not found")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(
            username=serializer.data["email"],
            password=serializer.data["password"],
        )

        if user is not None:
            serializer_class = self.get_response_serializer_class()
            response_data = serializer_class(user.auth_token).data
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error_code": "00", "error_msg": _("Login failed!")},
                status=status.HTTP_400_BAD_REQUEST,
            )


@extend_schema_view(
    post=extend_schema(
        request=None,
        parameters=schemas.CHANGE_PASSWORD_POST_PARAMETERS,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            schemas.ACCOUNT_PASSWORD_CHANGED_RESPONSE,
            schemas.ACCOUNT_CHANGE_PASSWORD_FAILED_RESPONSE,
        ],
    )
)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if request.user.account_type != User.Type.standard:
            return Response(
                {"detail": _("Action not allowed for user's account type!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            if request.user.check_password(serializer.data["current_password"]):
                request.user.set_password(serializer.data["new_password"])
                request.user.save()
                return Response(
                    {"detail": _("Password changed successfully!")},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"detail": _("User authorization failed!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        request=None,
        parameters=schemas.CHANGE_EMAIL_POST_PARAMETERS,
        responses={
            200: OpenApiTypes.OBJECT,
            400: OpenApiTypes.OBJECT,
        },
        examples=[
            schemas.ACCOUNT_EMAIL_CHANGED_RESPONSE,
            schemas.ACCOUNT_EMAIL_CHANGED_FAILED_RESPONSE,
        ],
    )
)
class ChangeEmailView(APIView):
    def post(self, request):
        serializer = ChangeEmailSerializer(data=request.data)

        if request.user.account_type != User.Type.standard:
            return Response(
                {"detail": _("Action not allowed for user's account type!")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if serializer.is_valid():
            if User.objects.filter(
                username=serializer.data["new_email"]
            ).exists():
                return Response(
                    {"detail": _("E-mail already in use!")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.user.email = serializer.data["new_email"]
            request.user.username = serializer.data["new_email"]
            request.user.save()

            return Response(
                {"detail": _("E-mail changed successfully!")},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAccountView(TemplateView):
    template_name = get_template("verify_ok.html")

    def get(self, request, *args, **kwargs):
        user_id = request.GET.get("user", None)
        key = request.GET.get("key", None)

        if not user_id or not key:
            self.template_name = get_template("verify_error.html")

        try:
            user = User.objects.get(id=user_id)

            if key != get_hash(user):
                self.template_name = get_template("verify_error.html")
            else:
                user.is_active = True
                user.save()
        except User.DoesNotExist:
            self.template_name = get_template("verify_error.html")

        return HttpResponse(self.template_name.render())


@extend_schema_view(
    post=extend_schema(
        request=None,
        parameters=schemas.REMIND_PASSWORD_POST_PARAMETERS,
        responses={200: OpenApiTypes.OBJECT, 400: RemindPasswordSerializer},
        examples=[schemas.ACCOUNT_REMIND_PASSWORD_RESPONSE],
    )
)
class RemindPasswordView(APIView):
    def post(self, request):
        serializer = RemindPasswordSerializer(data=request.data)

        if serializer.is_valid():
            send_change_password_email.delay(
                serializer.data["email"], request.scheme, request.get_host()
            )
            return Response(
                {"detail": _("Reset password link was send!")},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemindPasswordConfirmView(FormView):
    template_name = "change_password.html"
    form_class = PasswordChangeForm

    def get_initial(self):
        initial = super().get_initial()

        user = self.request.GET.get("user", None)
        key = self.request.GET.get("key", None)

        initial.update({"user": user, "key": key})

        return initial

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        user.set_password(form.cleaned_data["password"])
        user.save()

        template = get_template("password_changed.html")
        return HttpResponse(template.render())


@extend_schema_view(
    post=extend_schema(
        request=None,
        responses={
            204: OpenApiTypes.OBJECT,
        },
        examples=[
            schemas.ACCOUNT_DELETED_RESPONSE,
        ],
    )
)
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        delete_account.delay(request.user.pk)
        return Response(
            {"detail": _("Account deleted!")}, status=status.HTTP_200_OK
        )


@extend_schema_view(
    post=extend_schema(
        request=None,
        parameters=schemas.SOCIAL_AUTH_POST_PARAMETERS,
        responses={
            200: TokenSerializer,
            400: SocialAuthSerializer,
        },
    )
)
class GoogleAuthorizationView(APIView):
    def post(self, request):
        serializer = SocialAuthSerializer(data=request.data)

        if serializer.is_valid():
            user_data = GoogleAuthorization.get_user_data(
                serializer.data["token"]
            )

            user, created = User.objects.get_or_create(
                username=user_data["email"],
                email=user_data["email"],
                is_active=True,
                account_type=User.Type.google,
            )

            token_serializer = TokenSerializer(user.auth_token)

            return Response(token_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    post=extend_schema(
        request=None,
        parameters=schemas.SOCIAL_AUTH_POST_PARAMETERS,
        responses={
            200: TokenSerializer,
            400: OpenApiTypes.OBJECT,
        },
        examples=[schemas.ACCOUNT_FACEBOOK_AUTH_FAILED_RESPONSE],
    )
)
class FacebookAuthorizationView(APIView):
    def post(self, request):
        serializer = SocialAuthSerializer(data=request.data)

        if serializer.is_valid():
            user_data = FacebookAuthorization.get_user_data(
                serializer.data["token"]
            )

            if "email" not in user_data:
                raise ParseError(_("Facebook authorization failed!"))

            user, created = User.objects.get_or_create(
                username=user_data["email"],
                email=user_data["email"],
                is_active=True,
                account_type=User.Type.facebook,
            )

            token_serializer = TokenSerializer(user.auth_token)

            return Response(token_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
