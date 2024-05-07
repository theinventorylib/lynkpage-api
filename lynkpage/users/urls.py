from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from lynkpage.users.api.views import SkillsViewSet
from lynkpage.users.api.views import SocialLinksViewSet
from lynkpage.users.api.views import validate_email
from lynkpage.users.api.views import validate_username

app_name = "users"

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("social_links", SocialLinksViewSet)
router.register("skills", SkillsViewSet)

urlpatterns = [
    path("validate/username/", validate_username, name="validate_username"),
    path("validate/email/", validate_email, name="validate_email"),
]

urlpatterns += router.urls
