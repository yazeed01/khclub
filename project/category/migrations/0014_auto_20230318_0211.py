# Generated by Django 2.2.7 on 2023-03-17 23:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0013_auto_20230318_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvaldata_category',
            name='data_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Data_Category', unique=True, verbose_name='المحتوى'),
        ),
    ]