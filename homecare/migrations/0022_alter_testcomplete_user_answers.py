# Generated by Django 3.2.2 on 2021-05-24 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homecare', '0021_alter_coursecompletion_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcomplete',
            name='user_answers',
            field=models.TextField(blank=True),
        ),
    ]