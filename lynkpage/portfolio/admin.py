from django.contrib import admin

from .models.personal import PersonalCategory
from .models.personal import PersonalData

# from .models.professional


# Register your models here.
@admin.register(PersonalCategory)
class PersonalCategoryAdmin(admin.ModelAdmin):
    list_display = ("user", "name")


@admin.register(PersonalData)
class UserDataModelAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "link")
