import os
import uuid
from io import BytesIO

from django.conf.urls.static import static
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    EmailField,
    ForeignKey,
    ImageField,
    IntegerField,
    Model,
    TextField,
    UUIDField,
)

# from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


# image handling(renaming)
def upload_image(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("user_images", filename)


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
        _("Username of User"), blank=True, max_length=20, unique=True
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

    # create a thumbnail maker and getter, it uses the Image function from django and Byteio to turn it into a thumb
    # get the user image first
    # Todo Remove
    def get_image(self):
        if self.image:
            return f"http://localhost:8000{self.image.url}"
        else:
            # return the image in static/image/user_default
            return ""

    # get the thumbnail
    # Todo: remove
    def get_thumbnail(self):
        if self.thumbnail:
            return f"http://0.0.0.0:8000{self.thumbnail.url}"
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return f"http://0.0.0.0:8000{self.thumbnail.url}"
            else:
                return ""

    # make a thumbnail
    # Todo: remove
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=85)

        thumbnail = File(thumb_io, name=image.name)
        return thumbnail


class SocialLinks(Model):
    user = ForeignKey(User, related_name="social_links", on_delete=CASCADE)
    name = CharField(max_length=100, blank=False)
    link = CharField(max_length=500, blank=False)
    display = BooleanField(default=False)


class Skills(Model):
    user = ForeignKey(User, related_name="skills", on_delete=CASCADE)
    name = CharField(max_length=200, blank=False)

    class Meta:
        verbose_name = "skill"


class ClientToken(Model):
    token = UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.token)
