# Generated by Django 4.0.3 on 2022-04-18 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_alter_category_options_alter_data_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data_category',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='العنوان (اختياري)'),
        ),
    ]
