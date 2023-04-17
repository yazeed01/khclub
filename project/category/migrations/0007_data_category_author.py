# Generated by Django 4.0.3 on 2022-08-07 01:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0006_alter_category_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='data_category',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='الكاتب'),
            preserve_default=False,
        ),
    ]