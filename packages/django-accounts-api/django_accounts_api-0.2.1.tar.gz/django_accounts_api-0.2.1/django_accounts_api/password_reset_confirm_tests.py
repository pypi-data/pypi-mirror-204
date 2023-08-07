from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()
test_user_email = "admin@admin.com"


class PasswordResetTestCase(TestCase):
    """Basic tests of the partial HTML password reset view"""

    def setUp(self) -> None:
        """Get the url and create a user"""
        self.user = User.objects.create_user(
            "test", password="test", email=test_user_email
        )
        self.url = reverse(
            "django_accounts_api:password_reset_confirm",
            kwargs=dict(
                uidb64=urlsafe_base64_encode(force_bytes(self.user.pk)),
                token=default_token_generator.make_token(self.user)
            )
        )
        self.invalid_token_url = reverse(
            "django_accounts_api:password_reset_confirm",
            kwargs=dict(
                uidb64=urlsafe_base64_encode(force_bytes(self.user.pk)),
                token="invalid_token"
            )
        )
        # generate the password reset token
        return super().setUp()

    def test_password_reset_confirm_success(self):
        # prepare the data
        data = {
            'new_password1': 'newpass123',
            'new_password2': 'newpass123',
        }

        response = self.client.post(
            self.url, data,
            HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 302)

    def test_password_reset_confirm_failure(self):
        # prepare the data with invalid token
        data = {
            'new_password1': 'newpass123',
            'new_password2': 'newpass123',
        }
        response = self.client.post(
            self.invalid_token_url, data,
            HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "Password reset unsuccessful")
