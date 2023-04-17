# Generated by Django 3.2.18 on 2023-03-25 03:47

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_newsslide_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsslide',
            name='image',
            field=models.ImageField(help_text='المقاس المناسب للصورة هو (428 * 1108)', upload_to='news_slide', validators=[main.models.validate_image], verbose_name='صورة'),
        ),
    ]
