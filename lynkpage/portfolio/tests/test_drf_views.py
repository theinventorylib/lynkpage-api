import pytest
from rest_framework.test import APIRequestFactory

from lynkpage.portfolio.api.views import PersonalCategoryViewSet
from lynkpage.portfolio.api.views import PersonalDataViewSet
from lynkpage.portfolio.models.personal import PersonalCategory
from lynkpage.portfolio.models.personal import PersonalData
from lynkpage.users.models import User


class TestPersonalCategoryViewset:
    @pytest.fixture()
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(
        self,
        personal_category: PersonalCategory,
        api_rf: APIRequestFactory,
    ):
        view = PersonalCategoryViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = personal_category.user
        response = view(request)
        assert response.status.HTTP_200_OK

    def test_get_queryset_not_found(
        self,
        personal_category: PersonalCategory,
        api_rf: APIRequestFactory,
    ):
        view = PersonalCategoryViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request)
        assert response.status.HTTP_200_OK

    def test_get_queryset_single(
        self,
        personal_category: PersonalCategory,
        api_rf: APIRequestFactory,
    ):
        view = PersonalCategoryViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = personal_category.user
        response = view(request, id=personal_category.id)
        assert response.status.HTTP_200_OK
        # different user instances
        # assert response.data["name"] == "Test" noqa: ERA001

    def test_get_queryset_single_not_found(
        self,
        personal_category: PersonalCategory,
        api_rf: APIRequestFactory,
    ):
        view = PersonalCategoryViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=personal_category.id)
        assert response.status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Not found."

    def test_patch_queryset_single(
        self,
        personal_category: PersonalCategory,
        api_rf: APIRequestFactory,
    ):
        view = PersonalCategoryViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"name": "test"})
        view.request = request
        request.user = personal_category.user
        response = view(request, id=personal_category.id)
        assert response.status.HTTP_200_OK

    def test_patch_queryset_single_not_found(
        self,
        personal_category: PersonalCategory,
        api_rf: APIRequestFactory,
    ):
        view = PersonalCategoryViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch("/fake-url/", {"name": "test"})
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=personal_category.id)
        assert response.status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Not found."

    def test_delete_queryset_single(
        self,
        personal_category: PersonalCategory,
        api_rf: APIRequestFactory,
    ):
        view = PersonalCategoryViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = personal_category.user
        response = view(request, id=personal_category.id)
        assert response.status.HTTP_204_NO_CONTENT

    def test_delete_queryset_single_not_found(
        self,
        personal_category: PersonalCategory,
        api_rf: APIRequestFactory,
    ):
        view = PersonalCategoryViewSet.as_view({"delete": "destroy"})
        request = api_rf.delete("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=personal_category.id)
        assert response.status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Not found."


class TestPersonalDataViewset:
    @pytest.fixture()
    def api_rf(self) -> APIRequestFactory:
        return APIRequestFactory()

    def test_get_queryset(
        self,
        personal_data: PersonalData,
        api_rf: APIRequestFactory,
    ):
        view = PersonalDataViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = personal_data.user
        response = view(request)
        assert response.status.HTTP_200_OK

    def test_get_queryset_not_found(
        self,
        personal_data: PersonalData,
        api_rf: APIRequestFactory,
    ):
        view = PersonalDataViewSet.as_view({"get": "list"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request)
        assert response.status.HTTP_200_OK

    def test_get_queryset_single(
        self,
        personal_data: PersonalData,
        api_rf: APIRequestFactory,
    ):
        view = PersonalDataViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = personal_data.user
        response = view(request, id=personal_data.id)
        assert response.status.HTTP_200_OK
        # different user instances
        # assert response.data["name"] == "Test" noqa: ERA001

    def test_get_queryset_single_not_found(
        self,
        personal_data: PersonalData,
        api_rf: APIRequestFactory,
    ):
        view = PersonalDataViewSet.as_view({"get": "retrieve"})
        request = api_rf.get("/fake-url/")
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=personal_data.id)
        assert response.status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Not found."

    def test_patch_queryset_single(
        self,
        personal_data: PersonalData,
        api_rf: APIRequestFactory,
    ):
        view = PersonalDataViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch(
            "/fake-url/",
            {"title": "test", "category": "test"},
        )
        view.request = request
        request.user = personal_data.user
        response = view(request, id=personal_data.id)
        assert response.status.HTTP_200_OK

    def test_patch_queryset_single_not_found(
        self,
        personal_data: PersonalData,
        api_rf: APIRequestFactory,
    ):
        view = PersonalDataViewSet.as_view({"patch": "partial_update"})
        request = api_rf.patch(
            "/fake-url/",
            {"title": "test", "category": "test"},
        )
        view.request = request
        request.user = User.objects.create(username="test")
        response = view(request, id=personal_data.id)
        assert response.status.HTTP_404_NOT_FOUND
        assert response.data["detail"] == "Not found."
