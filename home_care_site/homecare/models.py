from django.db import models

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


class Training(models.Model):
    name = models.CharField(max_length=200)
    topic = models.CharField(max_length=100, help_text='if no topic put N/A')
    duration = models.IntegerField(help_text='input time takes to complete training in mins')

    def __str__(self):
        return self.name

