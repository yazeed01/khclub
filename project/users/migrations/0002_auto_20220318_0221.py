# Generated by Django 2.2.7 on 2022-03-17 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='partners',
            name='date_start',
            field=models.DateField(blank=True, null=True, verbose_name='تاريخ إنضمام الشريك'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='image',
            field=models.ImageField(upload_to='partners-image', verbose_name='الصوره'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='name',
            field=models.CharField(max_length=80, verbose_name='اسم الشريك'),
        ),
        migrations.AlterField(
            model_name='partners',
            name='who_i',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='معلومات عن الشريك (إختياري)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='البريد الإلكتروني'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=30, verbose_name='الاسم'),
        ),
    ]
