# from django.db.models import (
#     CASCADE,
#     BooleanField,
#     CharField,
#     EmailField,
#     ForeignKey,
#     ImageField,
#     IntegerField,
#     URLField,
#     Model,
#     TextField,
#     UUIDField,
# )


# class Theme(Model):
#     name = CharField(max_length=100)

#     # Card Details
#     card_shape = CharField(max_length=50, default='rectangle')
#     card_background_color = CharField(max_length=50, default='#111827')
#     card_text_color = CharField(max_length=50, default='#000000')
#     card_border_color = CharField(max_length=50, default='#000000')
#     card_border_width = IntegerField(default=1)

#     # Background Settings
#     background_color = CharField(max_length=50, default='#111827')
#     background_image = ImageField(upload_to='backgrounds', blank=True)

#     # Colors
#     # primary_color = CharField(max_length=50, default='#6de873')
#     # secondary_color = CharField(max_length=50, default='#ec96f2')
#     # accent_color = CharField(max_length=50, default='#95edda')
#     # neutral_color = CharField(max_length=50, default='#292938')
#     # base_color = CharField(max_length=50, default='#111827')
#     # info_color = CharField(max_length=50, default='#91b3ed')
#     # success_color = CharField(max_length=50, default='#1d9575')
#     # warning_color = CharField(max_length=50, default='#f5a447')
#     # error_color = CharField(max_length=50, default='#e45553')

#     # Borders
#     border_color = CharField(max_length=50, default='#000000')
#     border_width = IntegerField(default=1)

#     def __str__(self):
#         return self.name
