import json
import uuid

from django.conf import settings as debugsetting
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

import config.settings.base as settings
from config.settings.base import MEDIA_URL
from config.settings.base import REST_AUTH
from lynkpage.users.views import validate_client_token

JWT_AUTH_COOKIE = REST_AUTH["JWT_AUTH_COOKIE"]
JWT_AUTH_REFRESH_COOKIE = REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]
VERIFY_PATH = "/auth/token/verify/"
REFRESH_PATH = "/auth/token/refresh/"


class MoveJWTCookieIntoTheBody(MiddlewareMixin):
    """
    for Django Rest Framework JWT's POST "/token-refresh" endpoint
    check for a 'token' in the request.COOKIES
    and if, add it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path == VERIFY_PATH and JWT_AUTH_COOKIE in request.COOKIES:
            if request.body != b"":
                data = json.loads(request.body)
                data["token"] = request.COOKIES[JWT_AUTH_COOKIE]
                request._body = json.dumps(data).encode("utf-8")  # noqa: SLF001
            else:
                # I cannot create a body if it is not passed
                # so the client must send '{}'
                pass


class MoveJWTRefreshCookieIntoTheBody(MiddlewareMixin):
    """
    for Django Rest Framework JWT's POST "/token-refresh" endpoint
    check for a 'token' in the request.COOKIES
    and if, add it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path == REFRESH_PATH and JWT_AUTH_REFRESH_COOKIE in request.COOKIES:
            if request.body != b"":
                data = json.loads(request.body)
                data["refresh"] = request.COOKIES[JWT_AUTH_REFRESH_COOKIE]
                request._body = json.dumps(data).encode("utf-8")  # noqa: SLF001
            else:
                # I cannot create a body if it is not passed
                # so the client must send '{}'
                pass


def vue_get_csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


class ClientAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if debugsetting.DEBUG:  # if the debug mode is on, skip the client token check
            return self.get_response(request)

        client_token = request.headers.get("x-client-token")

        # Check if the request is made to the admin site
        resolved = resolve(request.path_info)
        app_name = resolved.app_name
        url_name = resolved.url_name

        media_url_prefix = MEDIA_URL if hasattr(settings, "MEDIA_URL") else "/media/"

        if (
            app_name == "admin"
            or (url_name in ["api-schema", "api-docs"])
            or request.path_info.startswith(media_url_prefix)
        ):
            # Skip authentication checks for the admin site
            return self.get_response(request)

        if not client_token:
            return HttpResponseForbidden("Client token is missing")

        try:
            uuid.UUID(client_token, version=4)
        except ValueError:
            return HttpResponseForbidden("Invalid client token")

        if not validate_client_token(client_token):
            return HttpResponseForbidden("Invalid client token")

        return self.get_response(request)
