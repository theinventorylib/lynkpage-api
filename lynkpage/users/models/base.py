import uuid
from pathlib import Path

from django.conf.urls.static import static
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import ForeignKey
from django.db.models import ImageField
from django.db.models import IntegerField
from django.db.models import Model
from django.db.models import TextField
from django.db.models import UUIDField
from django.utils.translation import gettext_lazy as _


# image handling(renaming)
def upload_image(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return Path("user_images") / filename


# get default image from static
def get_default_image():
    return static("img/default.png")


class User(AbstractUser):
    """
    Default custom user model for lynkpage.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    username = CharField(
        _("Username of User"),
        blank=True,
        max_length=20,
        unique=True,
    )

    full_name = CharField(_("Full name"), blank=True, max_length=255)
    image = ImageField(upload_to=upload_image, blank=True)
    thumbnail = ImageField(upload_to="user_thumbnails", blank=True)
    occupation = CharField(max_length=100, blank=True, default="")
    is_premium = BooleanField(default=False)
    email = EmailField(max_length=100, unique=True)
    about = TextField(blank=True, default="")
    # name of hte user theme
    theme_name = CharField(max_length=100, default="cupcake")
    # free users can only have 3 social links
    social_link_count = IntegerField(default=3)
    # free users can only have 5 skills
    skill_count = IntegerField(default=5)
    # free user can only have 3 categories
    category_count = IntegerField(default=3)
    # free users can only create 15 items (five for each category)
    item_count = IntegerField(default=15)


class SocialLinks(Model):
    user = ForeignKey(User, related_name="social_links", on_delete=CASCADE)
    name = CharField(max_length=100, blank=False)
    link = CharField(max_length=500, blank=False)
    display = BooleanField(default=False)

    def __str__(self):
        return self.name


class Skills(Model):
    user = ForeignKey(User, related_name="skills", on_delete=CASCADE)
    name = CharField(max_length=200, blank=False)

    class Meta:
        verbose_name = "skill"

    def __str__(self):
        return self.name


class ClientToken(Model):
    token = UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.token)
