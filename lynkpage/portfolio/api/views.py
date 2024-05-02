from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from lynkpage.portfolio.api.serializers import (
    PersonalCategorySerializer,
    PersonalDataSerializer,
    PersonalDataWriteSerializer,
    PersonalSerializerView,
)
from lynkpage.portfolio.models.personal import PersonalCategory, PersonalData
from lynkpage.users.models import User as PortfolioUser

# PortfolioUser = get_user_model()

# TODO: turn cache functions to wrapper??


# ------------------------------ professional Portfolio View ------------------------------ #
class PortfolioViewSet(RetrieveAPIView):
    cache_key = "portfolio"
    serializer_class = PersonalSerializerView

    def get_object(self):
        username = self.kwargs.get("username")
        try:
            # for cache to work, it needs to be cleared on updates from the user and the user's data
            # cached_user = cache.get(f"{self.cache_key}_{username}")
            # if cached_user:
            #     user = cached_user
            # else:
            user = get_object_or_404(PortfolioUser, username=username)
            cache.set(
                f"{self.cache_key}_{username}",
                user,
                timeout=60 * 15,
            )
            return user
        except PortfolioUser.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


# ---------------------------- personal data view ---------------------------- #
class PersonalDataViewSet(ModelViewSet):
    cache_key = "personal_data"
    queryset = PersonalData.objects.all()
    parser_classes = (MultiPartParser, FormParser)  # Add these parser classes
    lookup_field = "id"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cached_query = cache.get(
                f"{self.cache_key}_{self.request.user.id}"
            )
            if cached_query:
                return cached_query

            data = PersonalData.objects.filter(
                user=self.request.user
            ).select_related(
                "category",
                "user",
            )
            cache.set(
                f"{self.cache_key}_{self.request.user.id}",
                data,
                timeout=60 * 15,
            )
            return data
        return (
            PersonalData.objects.none()
        )  # Return an empty queryset if the user is not authenticated

    def get_serializer_class(self):
        if self.action in ("retrieve", "destroy"):
            return PersonalDataSerializer

        if self.action in ("create", "update", "partial_update"):
            return PersonalDataWriteSerializer

        return PersonalDataSerializer

    # # create a new data
    def create(self, request, *args, **kwargs):
        """_summary_"""

        if not request.user.is_authenticated:
            return Response(
                {"detail": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        copied_data = request.data.copy()  # avoiding immutable dict error

        copied_data["user"] = request.user.id

        # update the item count on the user
        if not request.user.is_premium and request.user.item_count > 0:
            user = request.user
            user.item_count -= 1
            user.save()
        else:
            return Response(
                {"detail": "You have reached your item limit."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=copied_data)
        serializer.is_valid(raise_exception=True)

        # save the data
        serializer.save()

        # update the cache
        cache.delete(f"{self.cache_key}_{request.user.id}")
        cache.delete(f"portfolio_{request.user.username}")
        cache.set(
            f"{self.cache_key}_{request.user.id}",
            self.get_queryset(),
            timeout=60 * 15,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # clearing the cache on update
    def perform_update(self, serializer):
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        serializer.save()

    # clearing the cache on delete
    def perform_destroy(self, instance):
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        # update the item count on the user
        if (
            not self.request.user.is_premium
            and self.request.user.item_count < 16
        ):
            user = self.request.user
            user.item_count += 1
            user.save()
        instance.delete()


# -------------------------- Personal Category view -------------------------- #
class PersonalCategoryViewSet(ModelViewSet):
    cache_key = "personal_category"
    queryset = PersonalCategory.objects.all()
    serializer_class = PersonalCategorySerializer
    lookup_field = "id"

    def get_queryset(self):
        # Filter the queryset based on the username provided in the request
        if self.request.user.is_authenticated:
            cached_query = cache.get(
                f"{self.cache_key}_{self.request.user.id}"
            )
            if cached_query:
                return cached_query

            data = PersonalCategory.objects.filter(
                user=self.request.user
            ).select_related(
                "user",
            )
            cache.set(
                f"{self.cache_key}_{self.request.user.id}",
                data,
                timeout=60 * 15,
            )
            return data
        return (
            PersonalCategory.objects.none()
        )  # Return an empty queryset if the user is not authenticated

    # # create a new category
    def create(self, request, *args, **kwargs):
        """_summary_"""
        # get the user object
        request_user_id = self.request.user.id
        user_id = request_user_id if request_user_id else request.data["user"]

        # get the user object
        user = PortfolioUser.objects.get(id=user_id)

        # check if the user is premium
        if not user.is_premium and user.category_count > 0:
            user.category_count -= 1
            user.save()
        else:
            return Response(
                {"detail": "You have reached your category limit."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create the category
        name = request.data["name"]
        category = PersonalCategory.objects.create(user=user, name=name)

        # update the cache
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"personal_data_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        cache.set(
            f"{self.cache_key}_{self.request.user.id}",
            self.get_queryset(),
            timeout=60 * 15,
        )

        data = {
            "id": category.id,
            "name": category.name,
            "user": category.user.id,
        }
        return Response(status=status.HTTP_201_CREATED, data=data)

    # clearing the cache on update
    def perform_update(self, serializer):
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"personal_data_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        serializer.save()

    # clearing the cache on delete
    def perform_destroy(self, instance):
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"personal_data_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        # update the category count on the user
        if (
            not self.request.user.is_premium
            and self.request.user.category_count < 4
        ):
            user = self.request.user
            user.category_count += 1
            user.save()
        instance.delete()
