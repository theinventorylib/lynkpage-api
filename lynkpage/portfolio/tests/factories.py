# from collections.abc import Sequence
# from typing import Any

# from django.contrib.auth import get_user_model
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from lynkpage.portfolio.models.personal import PersonalCategory, PersonalData
from lynkpage.users.tests.factories import UserFactory


# User factory for the test
# UserFactory = UserFactory()
# Personal Category Factory for the test
class PersonalCategoryFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    name = Faker("name")

    class Meta:
        model = PersonalCategory


# Personal Data Factory for the test
class PersonalDataFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    category = SubFactory(PersonalCategoryFactory)
    title = Faker("name")
    # description = Faker("text")
    # image = Faker("image")
    link = Faker("url")

    class Meta:
        model = PersonalData
