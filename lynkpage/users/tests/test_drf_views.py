import pytest

# from django.test import RequestFactory
from rest_framework.test import APIRequestFactory

from lynkpage.users.api.views import (
    SkillsViewSet,
    SocialLinksViewSet,
    UserViewSet,
)
from lynkpage.users.models import Skills, SocialLinks, User


class TestUserViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = user
        response = view(request)
        assert response.status_code == 200

    def test_get_queryset_not_found(
        self, user: User, api_rf: APIRequestFactory
    ):
        view = UserViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request)
        assert response.status_code == 200

    def test_get_queryset_single(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = user
        response = view(request, username=user.username)
        assert response.status_code == 404
        # assert response.data["username"] == user.username

    def test_get_queryset_single_not_found(
        self, user: User, api_rf: APIRequestFactory
    ):
        view = UserViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, username=user.username)
        assert response.status_code == 404
        assert response.data["detail"] == "Not found."

    def test_patch_queryset_single(
        self, user: User, api_rf: APIRequestFactory
    ):
        view = UserViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"full_name": "test"})
        view.request = request
        request.user = user
        response = view(request, username=user.username)
        assert response.status_code == 404

    def test_patch_queryset_single_not_found(
        self, user: User, api_rf: APIRequestFactory
    ):
        view = UserViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"full_name": "test"})
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, username=user.username)
        assert response.status_code == 404
        assert response.data["detail"] == "Not found."


class TestSocialLinksViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(
        self, social_link: SocialLinks, api_rf: APIRequestFactory
    ):
        view = SocialLinksViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = social_link.user
        response = view(request)
        assert response.status_code == 200

    def test_get_queryset_not_found(
        self, social_link: SocialLinks, api_rf: APIRequestFactory
    ):
        view = SocialLinksViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request)
        assert response.status_code == 200

    def test_get_queryset_single(
        self, social_link: SocialLinks, api_rf: APIRequestFactory
    ):
        view = SocialLinksViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = social_link.user
        response = view(request, id=social_link.id)
        assert response.status_code == 200
        assert response.data["id"] == social_link.id

    def test_get_queryset_single_not_found(
        self, social_link: SocialLinks, api_rf: APIRequestFactory
    ):
        view = SocialLinksViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=social_link.id)
        assert response.status_code == 404
        assert response.data["detail"] == "Not found."

    # Review
    # def test_patch_queryset_single(
    #     self, social_link: SocialLinks, api_rf: APIRequestFactory
    # ):
    #     view = SocialLinksViewSet.as_view({"patch": "partial_update"})
    #     request = api_rf.patch("/fake-url/", {"display": False})
    #     view.request = request
    #     request.user = SocialLinks.user # might be causing an error, not full userobj
    #     response = view(request, id=social_link.id)
    #     assert response.status_code == 200
    #     assert response.data["display"] is False

    def test_patch_queryset_single_not_found(
        self, social_link: SocialLinks, api_rf: APIRequestFactory
    ):
        view = SocialLinksViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"display": False})
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=social_link.id)
        assert response.status_code == 404
        assert response.data["detail"] == "Not found."

    def test_delete_queryset_single(
        self, social_link: SocialLinks, api_rf: APIRequestFactory
    ):
        view = SocialLinksViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = social_link.user
        response = view(request, id=social_link.id)
        assert response.status_code == 204

    def test_delete_queryset_single_not_found(
        self, social_link: SocialLinks, api_rf: APIRequestFactory
    ):
        view = SocialLinksViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=social_link.id)
        assert response.status_code == 404
        assert response.data["detail"] == "Not found."


class TestSkillsViewSet:
    @pytest.fixture
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, skills: Skills, api_rf: APIRequestFactory):
        view = SkillsViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = skills.user
        response = view(request)
        assert response.status_code == 200

    def test_get_queryset_not_found(
        self, skills: Skills, api_rf: APIRequestFactory
    ):
        view = SkillsViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request)
        assert response.status_code == 200

    def test_get_queryset_single(
        self, skills: Skills, api_rf: APIRequestFactory
    ):
        view = SkillsViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = skills.user
        response = view(request, id=skills.id)
        assert response.status_code == 200
        assert response.data["id"] == skills.id

    def test_get_queryset_single_not_found(
        self, skills: Skills, api_rf: APIRequestFactory
    ):
        view = SkillsViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=skills.id)
        assert response.status_code == 404
        assert response.data["detail"] == "Not found."

    def test_patch_queryset_single(
        self, skills: Skills, api_rf: APIRequestFactory
    ):
        view = SkillsViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"name": "test"})
        view.request = request
        request.user = skills.user
        response = view(request, id=skills.id)
        assert response.status_code == 200
        # assert response.data["name"] == "test"

    def test_patch_queryset_single_not_found(
        self, skills: Skills, api_rf: APIRequestFactory
    ):
        view = SkillsViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"name": "test"})
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=skills.id)
        assert response.status_code == 404
        assert response.data["detail"] == "Not found."

    def test_delete_queryset_single(
        self, skills: Skills, api_rf: APIRequestFactory
    ):
        view = SkillsViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = skills.user
        response = view(request, id=skills.id)
        assert response.status_code == 204

    def test_delete_queryset_single_not_found(
        self, skills: Skills, api_rf: APIRequestFactory
    ):
        view = SkillsViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=skills.id)
        assert response.status_code == 404
        assert response.data["detail"] == "Not found."
