# Generated by Django 3.2.2 on 2021-05-18 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homecare', '0015_rename_modules_completed_coursecompletion_modules'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homecare.module'),
        ),
        migrations.AlterField(
            model_name='trainingvideo',
            name='module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='homecare.module'),
        ),
    ]
