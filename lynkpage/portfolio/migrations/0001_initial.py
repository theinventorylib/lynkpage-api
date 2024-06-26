# Generated by Django 4.2.11 on 2024-05-01 22:59

from django.db import migrations, models
import django.db.models.deletion
import lynkpage.portfolio.models.personal


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Personal Categories',
            },
        ),
        migrations.CreateModel(
            name='PersonalData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('embeded_item', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to=lynkpage.portfolio.models.personal.upload_image)),
                ('link', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portfolio.personalcategory')),
            ],
        ),
    ]
