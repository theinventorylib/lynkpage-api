from rest_framework.serializers import (
    CharField,
    EmailField,
    ImageField,
    ModelSerializer,
    ValidationError,
)

from lynkpage.users.models import Skills, SocialLinks, User

# User = get_user_model()


class SocialLinksSerializer(ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = [
            "id",
            "name",
            "link",
            "display",
        ]


class SocialLinksWriteSerializer(ModelSerializer):
    class Meta:
        model = SocialLinks
        fields = [
            "id",
            "name",
            "link",
            "display",
        ]

    def create(self, validated_data):
        user = validated_data.pop("user")
        social_lnk = SocialLinks.objects.create(user=user, **validated_data)
        return social_lnk

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.link = validated_data.get("link", instance.link)
        instance.display = validated_data.get("display", instance.display)
        instance.save()
        return instance


class SkillsSerializer(ModelSerializer):
    class Meta:
        model = Skills
        fields = [
            "id",
            "name",
        ]


class SkillsWriteSerializer(ModelSerializer):
    class Meta:
        model = Skills
        fields = [
            "id",
            "name",
        ]

    # def create(self, validated_data):
    #     user = validated_data.pop("user")
    #     skill = Skills.objects.create(user=user, **validated_data)
    #     data = {"id": skill.id, "name": skill.name}
    #     return data

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class UserSerializer(ModelSerializer[User]):
    # image = SerializerMethodField("get_image")
    skills = SkillsSerializer(many=True, read_only=True)
    social_links = SocialLinksSerializer(many=True, read_only=True)
    email = EmailField(read_only=True)
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
            "social_link_count",
            "skill_count",
            "category_count",
            "item_count",
        ]

    # get the user image first
    # the obj is the user object
    # def get_image(self, obj) -> str:
    #     if obj.image:
    #         return obj.get_image()


class UserDisplaySerializer(ModelSerializer[User]):
    # image = SerializerMethodField("get_image")
    skills = SkillsSerializer(many=True, read_only=True)
    social_links = SocialLinksSerializer(many=True, read_only=True)
    email = EmailField(read_only=True)

    class Meta:
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
        ]


class UserRegSerializer(ModelSerializer):
    password2 = CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "full_name",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    # save the user object
    def save(self, request):
        # convert the username to lowercase
        lower_username = self.validated_data["username"].lower()
        self.validated_data["username"] = lower_username
        # check if user name is shorter than 3 char or longer than 20 char
        if (
            len(self.validated_data["username"]) < 3
            or len(self.validated_data["username"]) > 20
        ):
            raise ValidationError(
                {"username": "Username must be between 3 and 20 characters."}
            )

        # check if password and password2 are the same
        if self.validated_data["password"] != self.validated_data["password2"]:
            raise ValidationError({"password": "Passwords must match."})
        else:
            del self.validated_data["password2"]

        # should check if the username already exists and
        # if it does, raise an error and tell the user
        try:
            user = User.objects.get(username=lower_username)
            raise ValidationError({"username": "Username already exists."})
        except User.DoesNotExist:
            user = User.objects.create_user(**self.validated_data)

        return user
