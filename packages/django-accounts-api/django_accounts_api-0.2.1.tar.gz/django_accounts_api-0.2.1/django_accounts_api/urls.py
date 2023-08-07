from django.urls import path
from .views import (
    Login,
    Logout,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirmView,
    PasswordResetComplete,
    login_check,
    manifest
)

app_name = 'django_accounts_api'
urlpatterns = [
    path('', manifest, name='manifest'),
    path('check', login_check, name='login_check'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('password_change', PasswordChange.as_view(), name='password_change'),
    path('password_reset', PasswordReset.as_view(), name='password_reset'),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('reset/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),
]
