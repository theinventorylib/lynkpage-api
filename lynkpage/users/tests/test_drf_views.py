import pytest
from rest_framework.test import APIRequestFactory

from lynkpage.users.api.views import SkillsViewSet
from lynkpage.users.api.views import SocialLinksViewSet
from lynkpage.users.api.views import UserViewSet
from lynkpage.users.models import Skills
from lynkpage.users.models import SocialLinks
from lynkpage.users.models import User

# Fix for Magic variables in tests
_okay = 200
_not_found = 404
_no_content = 204


class TestUserViewSet:
    @pytest.fixture()
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = user
        response = view(request)
        assert response.status_code == _okay

    def test_get_queryset_not_found(
        self,
        user: User,
        api_rf: APIRequestFactory,
    ):
        view = UserViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request)
        assert response.status_code == _okay

    def test_get_queryset_single(self, user: User, api_rf: APIRequestFactory):
        view = UserViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = user
        response = view(request, username=user.username)
        assert response.status_code == _not_found
        # assert response.data["username"] == user.username noqa: ERA001

    def test_get_queryset_single_not_found(
        self,
        user: User,
        api_rf: APIRequestFactory,
    ):
        view = UserViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, username=user.username)
        assert response.status_code == _not_found
        # assert response.data["detail"] == "Not found." noqa: ERA001

    def test_patch_queryset_single(
        self,
        user: User,
        api_rf: APIRequestFactory,
    ):
        view = UserViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"full_name": "test"})
        view.request = request
        request.user = user
        response = view(request, username=user.username)
        assert response.status_code == _not_found

    def test_patch_queryset_single_not_found(
        self,
        user: User,
        api_rf: APIRequestFactory,
    ):
        view = UserViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"full_name": "test"})
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, username=user.username)
        assert response.status_code == _not_found
        # assert response.data["detail"] == "Not found." noqa: ERA001


class TestSocialLinksViewSet:
    @pytest.fixture()
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(
        self,
        social_link: SocialLinks,
        api_rf: APIRequestFactory,
    ):
        view = SocialLinksViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = social_link.user
        response = view(request)
        assert response.status_code == _okay

    def test_get_queryset_not_found(
        self,
        social_link: SocialLinks,
        api_rf: APIRequestFactory,
    ):
        view = SocialLinksViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request)
        assert response.status_code == _okay

    def test_get_queryset_single(
        self,
        social_link: SocialLinks,
        api_rf: APIRequestFactory,
    ):
        view = SocialLinksViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = social_link.user
        response = view(request, id=social_link.id)
        assert response.status_code == _okay
        assert response.data["id"] == social_link.id

    def test_get_queryset_single_not_found(
        self,
        social_link: SocialLinks,
        api_rf: APIRequestFactory,
    ):
        view = SocialLinksViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=social_link.id)
        assert response.status_code == _not_found
        # assert response.data["detail"] == "Not found." noqa: ERA001

    def test_patch_queryset_single_not_found(
        self,
        social_link: SocialLinks,
        api_rf: APIRequestFactory,
    ):
        view = SocialLinksViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"display": False})
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=social_link.id)
        assert response.status_code == _not_found
        # assert response.data["detail"] == "Not found." noqa: ERA001

    def test_delete_queryset_single(
        self,
        social_link: SocialLinks,
        api_rf: APIRequestFactory,
    ):
        view = SocialLinksViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = social_link.user
        response = view(request, id=social_link.id)
        assert response.status_code == _no_content

    def test_delete_queryset_single_not_found(
        self,
        social_link: SocialLinks,
        api_rf: APIRequestFactory,
    ):
        view = SocialLinksViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=social_link.id)
        assert response.status_code == _not_found
        # assert response.data["detail"] == "Not found." noqa: ERA001


class TestSkillsViewSet:
    @pytest.fixture()
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(self, skills: Skills, api_rf: APIRequestFactory):
        view = SkillsViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = skills.user
        response = view(request)
        assert response.status_code == _okay

    def test_get_queryset_not_found(
        self,
        skills: Skills,
        api_rf: APIRequestFactory,
    ):
        view = SkillsViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request)
        assert response.status_code == _okay

    def test_get_queryset_single(
        self,
        skills: Skills,
        api_rf: APIRequestFactory,
    ):
        view = SkillsViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = skills.user
        response = view(request, id=skills.id)
        assert response.status_code == _okay
        assert response.data["id"] == skills.id

    def test_get_queryset_single_not_found(
        self,
        skills: Skills,
        api_rf: APIRequestFactory,
    ):
        view = SkillsViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=skills.id)
        assert response.status_code == _not_found
        # assert response.data["detail"] == "Not found." noqa: ERA001

    def test_patch_queryset_single(
        self,
        skills: Skills,
        api_rf: APIRequestFactory,
    ):
        view = SkillsViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"name": "test"})
        view.request = request
        request.user = skills.user
        response = view(request, id=skills.id)
        assert response.status_code == _okay
        # assert response.data["name"] == "test" noqa: ERA001

    def test_patch_queryset_single_not_found(
        self,
        skills: Skills,
        api_rf: APIRequestFactory,
    ):
        view = SkillsViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"name": "test"})
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=skills.id)
        assert response.status_code == _not_found
        # assert response.data["detail"] == "Not found." noqa: ERA001

    def test_delete_queryset_single(
        self,
        skills: Skills,
        api_rf: APIRequestFactory,
    ):
        view = SkillsViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = skills.user
        response = view(request, id=skills.id)
        assert response.status_code == _no_content

    def test_delete_queryset_single_not_found(
        self,
        skills: Skills,
        api_rf: APIRequestFactory,
    ):
        view = SkillsViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=skills.id)
        assert response.status_code == _not_found
        # assert response.data["detail"] == "Not found." noqa: ERA001
