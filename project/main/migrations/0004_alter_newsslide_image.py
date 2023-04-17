# Generated by Django 3.2.18 on 2023-03-24 21:46

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_newsslide_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsslide',
            name='image',
            field=models.ImageField(help_text='المقاس المناسب للصورة هو (428 * 1108) **الرجاء الإلتزام بالمقاس**', upload_to='news_slide', validators=[main.models.validate_image], verbose_name='صورة'),
        ),
    ]
