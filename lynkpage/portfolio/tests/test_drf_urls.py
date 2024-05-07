from rest_framework import status
from rest_framework.test import APITestCase

from lynkpage.portfolio.tests.factories import PersonalCategoryFactory
from lynkpage.portfolio.tests.factories import PersonalDataFactory


# ---------------------- Testing PersonalCategoryFactory --------------------- #
class TestPersonalCategoryModel(APITestCase):
    def test_personal_categories_list(self):
        url = "api/v1/portfolio/personal/categories/"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_personal_categories_detail(self):
        personal_category = PersonalCategoryFactory()
        url = str(
            "api/v1/portfolio/personal/categories/" + str(personal_category.id),
        )
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_personal_categories_detail_not_found(self):
        url = "api/v1/portfolio/personal/categories/0"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ------------------------ Testing PersonalDataFactory ----------------------- #
class TestPersonalDataModel(APITestCase):
    def test_personal_data_list(self):
        url = "api/v1/portfolio/personal/data/"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_personal_data_detail(self):
        personal_data = PersonalDataFactory()
        url = str("api/v1/portfolio/personal/data/" + str(personal_data.id))
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_personal_data_detail_not_found(self):
        url = "api/v1/portfolio/personal/data/0"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
