from http import HTTPStatus
from typing import Any
from django.views.generic import View
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetCompleteView, PasswordResetConfirmView
from django.urls.exceptions import NoReverseMatch
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters


class AcceptJsonMixin:
    """
    Adds method to detect if JSON was requested in the Accept header
    """

    def json_response_requested(self: View) -> bool:
        """ does the request want JSON content back?"""
        if "HTTP_ACCEPT" in self.request.META:
            return self.request.META["HTTP_ACCEPT"] == "application/json"
        return False


def manifest(request: HttpRequest) -> HttpResponse:
    """Return a json encoded dictionary {name: path} for views offered
    by Django Accounts API

    :param request: the Django http request
    :type request: HttpRequest
    :return: json encoded name: path dictionary
    :rtype: HttpResponse
    """
    return JsonResponse(dict(
        login=reverse("django_accounts_api:login"),
        logout=reverse("django_accounts_api:logout"),
        password_change=reverse("django_accounts_api:password_change"),
    ))


def _user_details(user: DjangoUser) -> dict:
    """The details of the user to return on success"""
    return dict(
        id=user.pk,
        name=user.get_full_name(),
    )


def login_check(request) -> HttpResponse:
    """
    Deprecated (use Login view with Accept application/json)
    200 and details if logged in, 401 if not
    """
    user: DjangoUser = request.user
    if (user.is_authenticated):
        return JsonResponse(_user_details(user))
    else:
        return HttpResponse(status=401)


@method_decorator(ensure_csrf_cookie, name='get')
@method_decorator(sensitive_post_parameters(), name='dispatch')
class Login(AcceptJsonMixin, LoginView):
    '''
    Override the Django login view to be API friendly for json or partial html
    '''
    template_name = "django_accounts_api/login.html"

    def form_valid(self, form):
        """Override redirect behavior to return JSON user details"""
        _repressed_redirect = super().form_valid(form)  # noqa: F841
        return JsonResponse(
            _user_details(self.request.user),
            status=201
        )

    def form_invalid(self, form):
        """Override redirect behavior if json is requested return json errors"""
        if self.json_response_requested():
            return JsonResponse(dict(errors=form.errors), status=400)
        else:
            return super().form_invalid(form)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Override the get behavior if json requested return user details"""
        if self.json_response_requested():
            if (request.user.is_authenticated):
                return JsonResponse(_user_details(request.user))
            else:
                return JsonResponse({}, status=HTTPStatus.NO_CONTENT)
        else:
            return super().get(request, *args, **kwargs)


class Logout(LogoutView):
    ''' Override the Django logout view to NOT redirect on successful login
    GET - actually calls POST, but will error in Django 5
    POST - logs out, returns 200
    '''

    def post(self, request, *args, **kwargs):
        _repressed_redirect_or_render = super().post(request, *args, **kwargs)  # noqa: F841
        return HttpResponse(
            status=200
        )


@method_decorator(sensitive_post_parameters(), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class PasswordChange(AcceptJsonMixin, PasswordChangeView):
    ''' Override the Django change password view to support API use
    GET - renders a partial change password form - can be accessed without auth
    '''
    template_name = "django_accounts_api/password_change.html"

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        """Django's PasswordChangeView is login required and redirects, we suppress this and 401"""
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Override the get behavior if json requested return user details"""
        if request.user.is_authenticated:
            if (self.json_response_requested()):
                return JsonResponse(_user_details(request.user))
            else:
                return super().post(request, *args, **kwargs)

    def post(self, *args, **kwargs):
        if self.json_response_requested():
            if self.request.user.is_authenticated:
                return super().post(*args, **kwargs)
        else:
            return super().post(*args, **kwargs)

    def form_invalid(self, form):
        """Override redirect behavior if json is requested return json errors"""
        if self.json_response_requested():
            return JsonResponse(dict(errors=form.errors), status=400)
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        try:
            _repressed_redirect = super().form_valid(form)  # noqa: F841
        except NoReverseMatch:
            pass
        return HttpResponse(status=200)


@method_decorator(sensitive_post_parameters(), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class PasswordReset(AcceptJsonMixin, PasswordResetView):
    ''' Override the Django password reset view to support API use
    GET - renders a password reset form - can be accessed without auth
    '''

    template_name = "django_accounts_api/password_reset.html"

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch method to include CSRF and sensitive post parameters protection"""
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Override the get behavior if json requested return user details"""
        if self.json_response_requested():
            return JsonResponse(_user_details(request.user))
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests and sends a password reset email if the email is available
        in the DB, or returns "email not found" otherwise.
        """
        email = request.POST.get('email')
        Users = get_user_model()
        user = Users.objects.filter(email=email).first()
        if user:
            form = self.get_form()
            if form.is_valid():
                form.save(
                    subject_template_name='registration/password_reset_subject.txt',
                    email_template_name='registration/password_reset_email.html',
                    use_https=request.is_secure(),
                    from_email=None,
                    request=request,
                )
                if self.json_response_requested():
                    response_data = {
                        "message": "Password reset email has been sent."}
                    return JsonResponse(response_data)
                else:
                    return self.form_valid(form)
            else:
                if self.json_response_requested():
                    response_data = {
                        "message": "Invalid data provided.", "errors": form.errors}
                    return JsonResponse(response_data, status=400)
                else:
                    return self.form_invalid(form)
        else:
            if self.json_response_requested():
                response_data = {"message": "Email not found."}
                return JsonResponse(response_data)
            else:
                form = self.get_form()
                return self.form_invalid(form)

    def form_invalid(self, form):
        """Override redirect behavior if json is requested return json errors"""
        if self.json_response_requested():
            return JsonResponse(dict(errors=form.errors), status=400)
        else:
            return super().form_invalid(form)

    def form_valid(self, form):
        """Override form_valid method to return HttpResponse with status code"""
        try:
            _repressed_redirect = super().form_valid(form)  # noqa: F841
        except NoReverseMatch:
            pass
        return HttpResponse(status=200)


@method_decorator(sensitive_post_parameters(), name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class PasswordResetConfirm(AcceptJsonMixin, PasswordResetConfirmView):
    """
    Custom PasswordResetConfirmView to support API use
    """
    template_name = 'django_accounts_api/password_reset_confirm.html'

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not self.valid_link(request):
            return HttpResponse(status=400)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.json_response_requested():
            return JsonResponse({'message': 'Password reset confirmed'}, status=200)
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.json_response_requested():
            return JsonResponse({'message': 'Password reset confirmed'}, status=200)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        If the form is valid, redirect to the supplied URL.
        """
        if self.json_response_requested():
            return JsonResponse({'message': 'Password reset confirmed'}, status=200)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, re-render the context data with the
        data-filled form and errors.
        """
        if self.json_response_requested():
            return JsonResponse({'errors': form.errors}, status=400)
        return super().form_invalid(form)


class PasswordResetComplete(PasswordResetCompleteView):
    """
    Custom PasswordResetCompleteView to support API use
    """
    template_name = 'password_reset_complete.html'

    def render_to_response(self, context, **response_kwargs):
        if self.json_response_requested():
            return JsonResponse({'message': 'Password reset successful.'}, status=200)
        else:
            return super().render_to_response(context, **response_kwargs)
