# Generated by Django 3.2 on 2021-05-05 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_userinfo_postest_grade'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserInfo',
        ),
    ]
