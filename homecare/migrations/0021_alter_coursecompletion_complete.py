# Generated by Django 3.2.2 on 2021-05-24 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homecare', '0020_module_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecompletion',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
