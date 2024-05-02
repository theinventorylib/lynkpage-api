from django.core.cache import cache
from rest_framework import status

# from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, schema
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from lynkpage.users.models import Skills, SocialLinks, User

from .serializers import (
    SkillsSerializer,
    SkillsWriteSerializer,
    SocialLinksSerializer,
    SocialLinksWriteSerializer,
    UserDisplaySerializer,
)

# User = get_user_model()


class UserViewSet(
    RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet
):
    cache_key = "user"
    serializer_class = UserDisplaySerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.user.id

        # Check if the queryset is cached
        assert isinstance(user_id, int)

        # Check if the queryset is cached
        cached_query = cache.get(f"{self.cache_key}_{user_id}")
        if cached_query:
            return cached_query

        # If not cached, retrieve the queryset and cache it
        queryset = (
            self.queryset.filter(id=user_id).only("id", "username", "email"),
        )
        cache.set(
            f"{self.cache_key}_{user_id}", queryset, timeout=60 * 15
        )  # Cache for 15 minutes
        return queryset

    # deleting and updating cache if deleted or updated
    def perform_update(self, serializer):
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        serializer.save()

    def perform_destroy(self, instance):
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        instance.delete()


# Delete account
class UserDeleteView(APIView):
    cache_key = "user"

    def delete(self, request, username=None, format=None):
        try:
            user = self.request.user
            # the user is must be authenticated
            assert isinstance(user, User)

            # checking if user and username matches
            assert user.username == username

            cache.delete(f"{self.cache_key}_{self.request.user.id}")
            cache.delete(f"portfolio_{self.request.user.username}")
            user.delete()

            # send 204 code
            return Response(
                status=204, data={"message": "User deleted successfully."}
            )
        except Exception:
            return Response(
                status=400,
                data={
                    "message": "Something went wrong, please try again later."
                },
            )


class SocialLinksViewSet(ModelViewSet):
    # social links can also be fetched from the user cache
    cache_key = "social_links"
    queryset = SocialLinks.objects.select_related("user").all()
    serializer_class = SocialLinksSerializer
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action in ("retrieve", "destroy"):
            return SocialLinksSerializer

        if self.action in ("create", "update", "partial_update"):
            return SocialLinksWriteSerializer

        return SocialLinksSerializer

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.user.id

        # Check if the queryset is cached
        assert isinstance(user_id, int)

        # Check if the queryset is cached
        cached_query = cache.get(f"{self.cache_key}_{user_id}")
        if cached_query:
            return cached_query

        # If not cached, retrieve the queryset and cache it
        queryset = self.queryset.filter(user=user_id).only("id", "user")
        cache.set(f"{self.cache_key}_{user_id}", queryset, timeout=60 * 15)
        return queryset

        # assert isinstance(self.request.user.id, int)
        # return self.queryset.filter(user=self.request.user.id)

    def perform_create(self, serializer):
        # clear the cache
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        # update the social_inks count on the user
        user = self.request.user
        if not user.is_premium and user.social_link_count > 0:
            user.social_link_count -= 1
            user.save()
        else:
            return Response(
                {"detail": "You have reached your social link limit."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(user=user)

    def perform_update(self, serializer):
        # clear the cache
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        serializer.save(user=self.request.user)

    # clearing the cache on delete
    def perform_destroy(self, instance):
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        # update the social link count on the user
        user = self.request.user
        if not user.is_premium and user.social_link_count < 4:
            user.social_link_count += 1
            user.save()
        instance.delete()


class SkillsViewSet(ModelViewSet):
    # skills can also be fetched from the user cache
    cache_key = "skills"
    queryset = Skills.objects.select_related("user").all()
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action in ("retrieve", "destroy"):
            return SkillsSerializer

        if self.action in ("create", "update", "partial_update"):
            return SkillsWriteSerializer

        return SkillsSerializer

    def get_queryset(self, *args, **kwargs):
        user_id = self.request.user.id

        # Check if the queryset is cached
        assert isinstance(user_id, int)

        # Check if the queryset is cached
        cached_query = cache.get(f"{self.cache_key}_{user_id}")
        if cached_query:
            return cached_query

        # If not cached, retrieve the queryset and cache it
        queryset = self.queryset.filter(user=user_id).only("id", "user")
        cache.set(f"{self.cache_key}_{user_id}", queryset, timeout=60 * 15)
        return queryset

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        # clear the cache
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        # update the skill count on the user
        user = self.request.user
        if not user.is_premium and user.skill_count > 0:
            user.skill_count -= 1
            user.save()
        else:
            return Response(
                {"detail": "You have reached your skill limit."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(user=user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        # clear the cache
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        serializer.save(user=self.request.user)

    # clearing the cache on delete
    def perform_destroy(self, instance):
        cache.delete(f"{self.cache_key}_{self.request.user.id}")
        cache.delete(f"portfolio_{self.request.user.username}")
        # update the skill count on the user
        user = self.request.user
        if not user.is_premium and user.skill_count < 6:
            user.skill_count += 1
            user.save()
        instance.delete()


# Signup dynamics
# checking if username or email is already taken
@api_view(["POST"])
@schema(None)
def validate_username(request):
    username = request.data.get("username", None)
    if username is None:
        return Response({"message": "Username is required."})
    else:
        username = username.strip().lower()
    data = {
        "is_taken": User.objects.filter(username__iexact=username).exists()
    }
    if data["is_taken"]:
        data["message"] = "A user with this username already exists."
    elif len(username) < 3:
        data["message"] = "Username must be at least 3 characters long."
    elif len(username) > 20:
        data["message"] = "Username must be less than 20 characters."
    else:
        data["message"] = "Username is available"
    return Response(data)


@api_view(["POST"])
@schema(None)
def validate_email(request):
    email = request.data.get("email", None)
    if email is None:
        return Response({"message": "Email is required."})
    data = {"is_taken": User.objects.filter(email__iexact=email).exists()}
    if data["is_taken"]:
        data["message"] = "A user with this email already exists."
    else:
        data["message"] = "Email is available."
    return Response(data)
