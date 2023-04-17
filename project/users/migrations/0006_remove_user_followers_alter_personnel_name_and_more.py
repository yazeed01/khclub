# Generated by Django 4.0.3 on 2022-03-27 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20220319_0329'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.AlterField(
            model_name='personnel',
            name='name',
            field=models.CharField(max_length=80, verbose_name='الاسم'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='السيرة الذاتية'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='user-image', verbose_name='الصورة'),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=30, verbose_name='الاسم كامل'),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
