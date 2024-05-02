import json
import uuid

from django.conf import settings as debugsetting
from django.http import HttpResponseForbidden, JsonResponse
from django.middleware.csrf import get_token
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

import config.settings.base as settings
from config.settings.base import MEDIA_URL, REST_AUTH  # noqa
from lynkpage.users.views import validate_client_token

# from rest_framework import exceptions


JWT_AUTH_COOKIE = REST_AUTH["JWT_AUTH_COOKIE"]
JWT_AUTH_REFRESH_COOKIE = REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]
VERIFY_PATH = "/auth/token/verify/"
REFRESH_PATH = "/auth/token/refresh/"


class MoveJWTCookieIntoTheBody(MiddlewareMixin):
    """
    for Django Rest Framework JWT's POST "/token-refresh" endpoint --- check for a 'token' in the request.COOKIES
    and if, add it to the body payload.
    """

    def __init__(self, get_response):  # noqa
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path == VERIFY_PATH and JWT_AUTH_COOKIE in request.COOKIES:
            if request.body != b"":
                data = json.loads(request.body)
                data["token"] = request.COOKIES[JWT_AUTH_COOKIE]
                request._body = json.dumps(data).encode("utf-8")  # noqa
            else:
                # I cannot create a body if it is not passed so the client must send '{}'
                pass

        return None


class MoveJWTRefreshCookieIntoTheBody(MiddlewareMixin):
    """
    for Django Rest Framework JWT's POST "/token-refresh" endpoint --- check for a 'token' in the request.COOKIES
    and if, add it to the body payload.
    """

    def __init__(self, get_response):  # noqa
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if (
            request.path == REFRESH_PATH
            and JWT_AUTH_REFRESH_COOKIE in request.COOKIES
        ):
            if request.body != b"":
                data = json.loads(request.body)
                data["refresh"] = request.COOKIES[JWT_AUTH_REFRESH_COOKIE]
                request._body = json.dumps(data).encode("utf-8")  # noqa
            else:
                # I cannot create a body if it is not passed so the client must send '{}'
                pass

        return None


def vue_get_csrf(request):
    return JsonResponse({"csrfToken": get_token(request)})


class ClientAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            debugsetting.DEBUG
        ):  # if the debug mode is on, skip the client token check
            response = self.get_response(request)
            return response
        else:  # if the debug mode is off, check the client token
            client_token = request.headers.get("x-client-token")

            # Check if the request is made to the admin site
            resolved = resolve(request.path_info)
            app_name = resolved.app_name
            url_name = resolved.url_name

            media_url_prefix = (
                MEDIA_URL if hasattr(settings, "MEDIA_URL") else "/media/"
            )

            if (
                app_name == "admin"
                or (url_name in ["api-schema", "api-docs"])
                or request.path_info.startswith(media_url_prefix)
            ):
                # Skip authentication checks for the admin site
                response = self.get_response(request)
                return response

            if not client_token:
                # raise exceptions.AuthenticationFailed("Client token is missing")
                return HttpResponseForbidden("Client token is missing")

            try:
                uuid.UUID(client_token, version=4)
            except ValueError:
                # raise HttpResponseForbidden("Invalid client token")
                return HttpResponseForbidden("Invalid client token")

            if not validate_client_token(client_token):
                # raise HttpResponseForbidden("Invalid client token")
                return HttpResponseForbidden("Invalid client token")

            response = self.get_response(request)
            return response


# checking if user is premium
class PremiumAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if debugsetting.DEBUG:
            response = self.get_response(request)
            return response
        else:
            if request.user.is_authenticated and not request.user.is_premium:
                premium_endpoints = []
                if request.path in premium_endpoints:
                    return HttpResponseForbidden("Premium access required")
                else:
                    response = self.get_response(request)
                    return response
