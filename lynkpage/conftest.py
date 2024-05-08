import pytest

from lynkpage.portfolio.tests.factories import PersonalCategoryFactory
from lynkpage.portfolio.tests.factories import PersonalDataFactory
from lynkpage.users.models import Skills
from lynkpage.users.models import SocialLinks
from lynkpage.users.models import User
from lynkpage.users.tests.factories import SkillsFactory
from lynkpage.users.tests.factories import SocialLinksFactory
from lynkpage.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture()
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def social_link(db) -> SocialLinks:
    return SocialLinksFactory()


@pytest.fixture()
def skills(db) -> Skills:
    return SkillsFactory()


@pytest.fixture()
def personal_category(db) -> PersonalCategoryFactory:
    return PersonalCategoryFactory()


@pytest.fixture()
def personal_data(db) -> PersonalDataFactory:
    return PersonalDataFactory()
