from rest_framework.test import APITestCase

from lynkpage.portfolio.models.personal import PersonalCategory
from lynkpage.portfolio.models.personal import PersonalData
from lynkpage.portfolio.tests.factories import PersonalCategoryFactory
from lynkpage.portfolio.tests.factories import PersonalDataFactory
from lynkpage.portfolio.tests.factories import UserFactory
from lynkpage.users.models import User

# Gettin rid of magic values
_short_username_len = 3
_long_username_len = 20


# ---------------------------- Testing User Factory ---------------------------- #
class TestUserModel(APITestCase):
    def test_user_model(self):
        user = UserFactory()
        assert isinstance(user, User)
        # test username is a string bewteen 3 and 20 characters
        assert isinstance(user.username, str)
        assert len(user.username) >= _short_username_len
        assert len(user.username) <= _long_username_len
        # test email is a string
        assert isinstance(user.email, str)
        # other details are strings
        assert isinstance(user.full_name, str)
        assert isinstance(user.occupation, str)
        assert isinstance(user.last_name, str)


# ---------------------- Testing PersonalCategoryFactory --------------------- #
class TestPersonalCategoryModel(APITestCase):
    def test_personal_category_model(self):
        personal_category = PersonalCategoryFactory()
        assert isinstance(personal_category, PersonalCategory)
        # test name is a string
        assert isinstance(personal_category.name, str)
        # test user is a user
        assert isinstance(personal_category.user, User)


# ------------------------ Testing PersonalDataFactory ----------------------- #
class TestPersonalDataModel(APITestCase):
    def test_personal_data_model(self):
        personal_data = PersonalDataFactory()
        assert isinstance(personal_data, PersonalData)
        # test title is a string
        assert isinstance(personal_data.title, str)
        # test description is a string
        # assert isinstance(personal_data.description, str) noqa: ERA001
        # test link is a string
        assert isinstance(personal_data.link, str)
        # test user is a user
        assert isinstance(personal_data.user, User)
        # test category is a category
        assert isinstance(personal_data.category, PersonalCategory)
