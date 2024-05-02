from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from lynkpage.portfolio.api.views import (
    PersonalCategoryViewSet,
    PersonalDataViewSet,
)

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("personal/data", PersonalDataViewSet)
router.register("personal/categories", PersonalCategoryViewSet)


app_name = "api"
urlpatterns = router.urls
