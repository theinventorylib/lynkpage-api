from collections.abc import Sequence
from typing import Any

from factory import Faker
from factory import SubFactory
from factory import post_generation
from factory.django import DjangoModelFactory

from lynkpage.users.models import Skills
from lynkpage.users.models import SocialLinks
from lynkpage.users.models import User as UserModel


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    email = Faker("email")
    full_name = Faker("first_name")
    is_active = True

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):  # noqa: FBT001
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """Save again the instance if creating and at least one hook ran."""
        if create and results and not cls._meta.skip_postgeneration_save:
            # Some post-generation hooks ran, and may have modified us.
            instance.save()

    class Meta:
        model = UserModel
        django_get_or_create = ["username"]


class SocialLinksFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    name = Faker("name")
    link = Faker("url")
    display = Faker("boolean")

    class Meta:
        model = SocialLinks


class SkillsFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    name = Faker("name")

    class Meta:
        model = Skills
