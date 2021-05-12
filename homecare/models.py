from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Test(models.Model):
    name = models.CharField(max_length=100)
    attempts = models.IntegerField(help_text='set the value to 0.') # this value will auto increase with each each user who take test
    Difficulty = models.CharField(max_length=100, help_text='options are: easy, medium, difficult,N/A')
    num_questions = models.IntegerField(help_text='enter the number of questions')

    def __str__(self):
        return self.name


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.TextField(help_text="enter the question here")
    optionA = models.CharField(max_length=100)
    optionB = models.CharField(max_length=100)
    optionC = models.CharField(max_length=100)
    optionD = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class TrainingVideo(models.Model):
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=100, help_text='if no topic put N/A')
    duration = models.IntegerField(help_text='input time takes to complete training in mins')
    img = models.ImageField(upload_to='images/')
    video_link = models.CharField(max_length=300, help_text='enter link to youtube video')

    def __str__(self):
        return self.name


class TrainingPpt(models.Model):
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=100, help_text='if no topic put N/A')
    duration = models.IntegerField(help_text='input time takes to complete training in mins')
    img = models.ImageField(upload_to='images/')
    ppt = models.CharField(max_length=300, help_text='enter link to ppt in Onedrive')

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pretest_completion = models.BooleanField(default=False)
    pretest_grade = models.IntegerField(blank=True, null=True, help_text='this grade is presented as percentage')
    postest_completion = models.BooleanField(default=False)
    training_completion = models.BooleanField(default=False)
    postest_grade = models.IntegerField(blank=True, null=True, help_text='this grade is presented as percentage')

    def __str__(self):
        return self.user.last_name


class HomeSlides(models.Model):
    name = models.CharField(max_length=100)
    header_description = models.TextField(help_text='enter the heading text for caption')
    body_description = models.TextField(help_text='enter the summary description')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

