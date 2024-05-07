from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from lynkpage.portfolio.api.views import PersonalCategoryViewSet
from lynkpage.portfolio.api.views import PersonalDataViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("personal/data", PersonalDataViewSet)
router.register("personal/categories", PersonalCategoryViewSet)


app_name = "api"
urlpatterns = router.urls
