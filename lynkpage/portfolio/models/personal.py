import uuid
from pathlib import Path

from django.conf import settings
from django.db.models import CASCADE
from django.db.models import BooleanField
from django.db.models import CharField
from django.db.models import ForeignKey
from django.db.models import ImageField
from django.db.models import Model

from lynkpage.users.models import User as PortfolioUser


# image handling(renaming)
def upload_image(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return Path("images/personal") / filename


class PersonalCategory(Model):
    """_summary_

    Args:
        models (_type_): _description_ : This is th ecategory for the personal portfolio
    """

    user = ForeignKey(PortfolioUser, on_delete=CASCADE)
    name = CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Personal Categories"

    def __str__(self):
        return self.name


class PersonalData(Model):
    user = ForeignKey(PortfolioUser, on_delete=CASCADE)
    category = ForeignKey(PersonalCategory, on_delete=CASCADE)
    title = CharField(max_length=100, blank=True)
    embeded_item = BooleanField(default=False)
    image = ImageField(upload_to=upload_image, null=True, blank=True)
    link = CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    # get the image
    def get_image(self):
        if self.image:
            if settings.DEBUG:
                return f"http://localhost:8000{self.image.url}"
            return f"http://app.lynkpage.com{self.image.url}"
        return ""
