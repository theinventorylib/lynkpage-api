import os
import uuid

from django.conf import settings

# from django.contrib.auth import get_user_model
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    ForeignKey,
    ImageField,
    Model,
)

from lynkpage.users.models import User as PortfolioUser

# PortfolioUser = get_user_model()


# image handling(renaming)
def upload_image(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join("images/personal", filename)


class PersonalCategory(Model):
    """_summary_

    Args:
        models (_type_): _description_ : This is th ecategory for the personal portfolio
    """

    user = ForeignKey(PortfolioUser, on_delete=CASCADE)
    name = CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Personal Categories"


class PersonalData(Model):
    user = ForeignKey(PortfolioUser, on_delete=CASCADE)
    category = ForeignKey(PersonalCategory, on_delete=CASCADE)
    title = CharField(max_length=100, null=True, blank=True)
    # description = TextField(null=True, blank=True)
    embeded_item = BooleanField(default=False)
    image = ImageField(upload_to=upload_image, null=True, blank=True)
    link = CharField(max_length=100, null=True, blank=True)

    # get the image
    def get_image(self):
        if self.image:
            if settings.DEBUG:
                return f"http://localhost:8000{self.image.url}"
            else:
                return f"http://app.lynkpage.com{self.image.url}"
        return ""
