# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from drf_spectacular.views import (  # SpectacularRedocView,
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# extra
from lynkpage.portfolio.api.views import PortfolioViewSet
from lynkpage.users.api.views import UserDeleteView

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]

# API URLS
urlpatterns += [
    # API base url
    path(
        "api/v1/portfolio/<str:username>",
        PortfolioViewSet.as_view(),
        name="portfolio",
    ),
    path("api/v1/portfolio/", include("config.api_router")),
    path("api/v1/account/", include("dj_rest_auth.urls")),
    path("api/v1/account/", include("lynkpage.users.urls")),
    path(
        "api/v1/account/delete/<str:username>",
        UserDeleteView.as_view(),
        name="user-delete",
    ),
    path(
        "api/v1/account/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/account/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/account/registration/",
        include("dj_rest_auth.registration.urls"),
    ),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]


# def trigger_error(request):
#     division_by_zero = 1 / 0


# if not settings.DEBUG:
#     urlpatterns = [
#         path("sentry-debug/", trigger_error),
#     ] + urlpatterns

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
