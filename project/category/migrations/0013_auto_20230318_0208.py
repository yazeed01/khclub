# Generated by Django 2.2.7 on 2023-03-17 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0012_auto_20230318_0158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvaldata_category',
            name='data_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appp', to='category.Data_Category', unique=True, verbose_name='المحتوى'),
        ),
    ]
