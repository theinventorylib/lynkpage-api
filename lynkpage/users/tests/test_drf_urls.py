from rest_framework import status
from rest_framework.test import APITestCase

from lynkpage.users.tests.factories import SkillsFactory
from lynkpage.users.tests.factories import SocialLinksFactory
from lynkpage.users.tests.factories import UserFactory


# ------------------------ Testing User api endpoints ------------------------ #
class TestUserModelUrls(APITestCase):
    def test_user_detail(self):
        user = UserFactory()
        url = str("api/v1/account/user/" + user.username)
        response = self.client.get(url)
        # user not verified
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_detail_not_found(self):
        url = "api/v1/account/user/unknown"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_login(self):
        user = UserFactory()
        url = "api/v1/account/login/"
        data = {"username": user.username, "password": "password"}
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ----------------------- Testing SocialLinks api endpoints ---------------------- #
class TestSocialLinksModelUrls(APITestCase):
    def test_social_links_list(self):
        url = "api/v1/account/social_links/"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_social_links_detail(self):
        social_lnk = SocialLinksFactory()
        url = str("api/v1/account/social_links/" + str(social_lnk.id))
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_social_link_detail_not_found(self):
        url = "api/v1/account/social_links/0"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND


# ------------------------ Testing Skills api endpoints ----------------------- #
class TestSkillsModelUrls(APITestCase):
    def test_skills_list(self):
        url = "api/v1/account/skills/"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_skills_detail(self):
        skills = SkillsFactory()
        url = str("api/v1/account/skills/" + str(skills.id))
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_skills_detail_not_found(self):
        url = "api/v1/account/skills/0"
        response = self.client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
