# Generated by Django 4.0.3 on 2022-04-22 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_user_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partners',
            options={'verbose_name': 'شريك', 'verbose_name_plural': 'الشركاء'},
        ),
        migrations.AlterModelOptions(
            name='personnel',
            options={'verbose_name': 'عضو', 'verbose_name_plural': 'فريق العمل'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'مستخدم', 'verbose_name_plural': 'المستخدمين'},
        ),
    ]
