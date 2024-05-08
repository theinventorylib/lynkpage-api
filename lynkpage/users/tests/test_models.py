from rest_framework.test import APITestCase

from lynkpage.users.models import Skills
from lynkpage.users.models import SocialLinks
from lynkpage.users.models import User
from lynkpage.users.tests.factories import UserFactory

# fixing out magice values
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
        assert isinstance(user.last_name, str)


# -------------------------- Testing Social link Factory ------------------------- #
class TestSocialLinkModel(APITestCase):
    def test_social_link_model(self):
        social_lnk = SocialLinks.objects.create(
            user=UserFactory(),
            name="test",
            link="https://test.com",
            display=True,
        )
        assert isinstance(social_lnk, SocialLinks)
        # test name is a string
        assert isinstance(social_lnk.name, str)
        # test link is a string
        assert isinstance(social_lnk.link, str)
        # test display is a boolean
        assert isinstance(social_lnk.display, bool)


# --------------------------- Testing Skills Factory -------------------------- #
class TestSkillsModel(APITestCase):
    def test_skills_model(self):
        skills = Skills.objects.create(user=UserFactory(), name="test")
        assert isinstance(skills, Skills)
        # test name is a string
        assert isinstance(skills.name, str)
        # test user is a user
        assert isinstance(skills.user, User)
