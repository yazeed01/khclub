# Generated by Django 2.2.7 on 2022-03-19 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20220318_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partners',
            name='display',
            field=models.BooleanField(default=True, verbose_name='إظهار؟'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='display',
            field=models.BooleanField(default=True, help_text='إظهار العنصر او إخفاء.', verbose_name='إظهار؟'),
        ),
        migrations.AlterField(
            model_name='personnel',
            name='type_user',
            field=models.CharField(help_text='مثل: مؤسس , عضو , رئيس , ..', max_length=40, verbose_name='الفئة'),
        ),
    ]
