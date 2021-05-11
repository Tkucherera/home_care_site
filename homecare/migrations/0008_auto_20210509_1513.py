# Generated by Django 3.2 on 2021-05-09 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homecare', '0007_auto_20210508_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeSlides',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('header_description', models.TextField(help_text='enter the heading text for caption')),
                ('body_description', models.TextField(help_text='enter the summary description')),
                ('image', models.ImageField(upload_to='media/')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='pretest_grade',
            field=models.IntegerField(blank=True, help_text='this grade is presented as percentage', null=True),
        ),
    ]
