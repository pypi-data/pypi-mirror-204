from drf_spectacular.utils import OpenApiExample, OpenApiParameter

STANDARD_REGISTRATION_POST_PARAMETERS = [
    OpenApiParameter(
        name="email",
        description="E-mail",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="password",
        description="Password",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="repeat_password",
        description="Repeat password",
        required=True,
        type=str,
    ),
]

STANDARD_LOGIN_POST_PARAMETERS = [
    OpenApiParameter(
        name="email",
        description="E-mail",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="password",
        description="Password",
        required=True,
        type=str,
    ),
]

REMIND_PASSWORD_POST_PARAMETERS = [
    OpenApiParameter(
        name="email",
        description="E-mail",
        required=True,
        type=str,
    ),
]

CHANGE_PASSWORD_POST_PARAMETERS = [
    OpenApiParameter(
        name="current_password",
        description="Current user password",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="new_password",
        description="New user password",
        required=True,
        type=str,
    ),
    OpenApiParameter(
        name="repeat_new_password",
        description="Repeat current user password",
        required=True,
        type=str,
    ),
]

SOCIAL_AUTH_POST_PARAMETERS = [
    OpenApiParameter(
        name="token",
        description="Social authorization token",
        required=True,
        type=str,
    ),
]

CHANGE_EMAIL_POST_PARAMETERS = [
    OpenApiParameter(
        name="new_email",
        description="New user email",
        required=True,
        type=str,
    ),
]

ACCOUNT_EMAIL_CHANGED_RESPONSE = OpenApiExample(
    "email_changed",
    value={"detail": "E-mail changed successfully!"},
    response_only=True,
    status_codes=["200"],
)

ACCOUNT_EMAIL_CHANGED_FAILED_RESPONSE = OpenApiExample(
    "password_changed",
    value={
        "detail": [
            "E-mail already in use!",
            "Action not allowed for user's account type!",
        ],
        "serializer_field": ["field error details"],
    },
    response_only=True,
    status_codes=["400"],
)

ACCOUNT_LOGIN_FAILED_RESPONSE = OpenApiExample(
    "login_failed",
    value={
        "00": "Login failed!",
        "01": "User not found",
        "02": "User not active",
    },
    response_only=True,
    status_codes=["400"],
)

ACCOUNT_DELETED_RESPONSE = OpenApiExample(
    "account_deleted",
    value={"detail": "Account deleted!"},
    response_only=True,
    status_codes=["204"],
)

ACCOUNT_PASSWORD_CHANGED_RESPONSE = OpenApiExample(
    "password_changed",
    value={"detail": "Password changed successfully!"},
    response_only=True,
    status_codes=["200"],
)

ACCOUNT_REMIND_PASSWORD_RESPONSE = OpenApiExample(
    "password_changed",
    value={"detail": "Reset password link was send!"},
    response_only=True,
    status_codes=["200"],
)

ACCOUNT_CHANGE_PASSWORD_FAILED_RESPONSE = OpenApiExample(
    "password_changed",
    value={
        "detail": [
            "User authorization failed!",
            "Action not allowed for user's account type!",
        ],
        "serializer_field": ["field error details"],
    },
    response_only=True,
    status_codes=["400"],
)

ACCOUNT_FACEBOOK_AUTH_FAILED_RESPONSE = OpenApiExample(
    "facebook_auth_failed",
    value={
        "detail": "Facebook authorization failed!",
        "serializer_field": ["field error details"],
    },
    response_only=True,
    status_codes=["400"],
)
