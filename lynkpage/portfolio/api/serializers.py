# from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    CharField,
    ImageField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    ValidationError,
)

from lynkpage.portfolio.models.personal import PersonalCategory, PersonalData
from lynkpage.users.api.serializers import (
    SkillsSerializer,
    SocialLinksSerializer,
)
from lynkpage.users.models import User


# ---------------------- personal categories serializer ---------------------- #
class PersonalCategorySerializer(ModelSerializer):
    """_summary_ :

    Args:
        serializers (_type_): _description_
    """

    user = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """_summary_"""

        model = PersonalCategory
        # get all fields from model
        fields = ["id", "name", "user"]


# ------------------------- Personal data serializer ------------------------- #
class PersonalDataSerializer(ModelSerializer):
    """_summary_ :

    Args:
        serializers (_type_): _description_
    """

    # user = PrimaryKeyRelatedField(read_only=True)
    image = SerializerMethodField("get_image")
    category = CharField(source="category.name")

    class Meta:
        """_summary_"""

        model = PersonalData
        fields = [
            "id",
            "category",
            "title",
            "embeded_item",
            "image",
            "link",
        ]

    def get_image(self, obj) -> str:
        """_summary_

        Args:
            obj (_type_): _description_

        Returns:
            _type_: _description_
        """
        if obj.image:
            return obj.get_image()

    # def create(self, validated_data):
    #     print("vd: ", validated_data)
    #     category_name = validated_data.pop("category")
    #     category_name = category_name.pop("name")
    #     user = validated_data.pop("user")
    #     category, _ = PersonalCategory.objects.get_or_create(
    #         name=category_name, user=user
    #     )

    #     personal_data = PersonalData.objects.create(
    #         category=category, user=user, **validated_data
    #     )
    #     return personal_data


class PersonalDataWriteSerializer(ModelSerializer):
    """_summary_ :

    Args:
        serializers (_type_): _description_
    """

    # user = PrimaryKeyRelatedField()
    category = CharField(source="category.name")
    max_image_size = 1024 * 1024 * 5  # 5MB
    image = ImageField(
        max_length=None,
        allow_empty_file=False,
        allow_null=False,
        required=False,
    )

    # validating the image
    def validate_image(self, value):
        valid_formats = [
            "image/jpeg",
            "image/png",
            "image/jpg",
        ]  # Add other acceptable formats

        if value.content_type not in valid_formats:
            raise ValidationError("Image Format not allowed.")

        if value.size > self.max_image_size:
            raise ValidationError("Image size is too large.")

        return value

    class Meta:
        """_summary_"""

        model = PersonalData
        fields = [
            "id",
            "user",
            "category",
            "title",
            "embeded_item",
            "image",
            "link",
        ]

    def create(self, validated_data):
        # print("vd: ", validated_data)
        category_name = validated_data.pop("category")
        category_name = category_name.pop("name")
        user = validated_data.pop("user")
        # user = User.objects.get(id=user_id)
        category, _ = PersonalCategory.objects.get_or_create(
            name=category_name, user=user
        )

        personal_data = PersonalData.objects.create(
            category=category, user=user, **validated_data
        )
        return personal_data

    def update(self, instance, validated_data):
        # Handle the update logic for the fields with dotted sources manually
        category_name = validated_data.pop("category")
        category_name = category_name.pop("name")
        user = instance.user

        category, _ = PersonalCategory.objects.get_or_create(
            name=category_name, user=user
        )

        instance.category = category
        # instance.user = user

        # Update the other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# new personal serializer
class UserDataSerializerView(ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """

    data = PersonalDataSerializer(
        source="personaldata_set", many=True, read_only=True
    )

    class Meta:
        """_summary_"""

        model = PersonalCategory
        fields = ["id", "name", "data"]


class PersonalSerializerView(ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """

    user_data = UserDataSerializerView(
        source="personalcategory_set", many=True, read_only=True
    )
    skills = SkillsSerializer(many=True, read_only=True)
    social_links = SocialLinksSerializer(many=True, read_only=True)

    class Meta:
        """_summary_"""

        model = User
        fields = [
            "username",
            "full_name",
            "image",
            "thumbnail",
            "occupation",
            "is_premium",
            "skills",
            "social_links",
            "email",
            "about",
            "theme_name",
            "user_data",
        ]
