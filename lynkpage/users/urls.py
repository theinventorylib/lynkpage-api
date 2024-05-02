from django.conf import settings
from django.urls import path  # noqa
from rest_framework.routers import DefaultRouter, SimpleRouter

from lynkpage.users.api.views import (
    SkillsViewSet,
    SocialLinksViewSet,
    validate_email,
    validate_username,
)

app_name = "users"

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("social_links", SocialLinksViewSet)
router.register("skills", SkillsViewSet)

urlpatterns = [
    path("validate/username/", validate_username, name="validate_username"),
    path("validate/email/", validate_email, name="validate_email"),
]

urlpatterns += router.urls
