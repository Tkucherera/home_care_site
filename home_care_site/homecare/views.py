from django.shortcuts import render, redirect
from .models import *
# Create your views here.

# index view


def index(request):
    # tests = Test.objects.all()
    questions = Question.objects.all()
    return render(request, 'index.html', {'questions': questions})


def test(request):
    # get the tests
    tests = Test.objects.all()
    # get the questions
    questions = Question.objects.all()
    # assign unique identifier to each answer
    json_q = []
    counter = 1
    for question in questions:
        # put data in json and append it to json_q
        data_input = {
            'name': f"question{counter}",
            'question': question.question,
            'optionA': (question.optionA, f"{counter}A"),
            'optionB': (question.optionB, f"{counter}B"),
            'optionC': (question.optionC, f"{counter}C"),
            'optionD': (question.optionD, f"{counter}D"),
            'correct_answer': (question.correct_answer, f"{counter}correct")
        }
        counter+=1
        json_q.append(data_input)
        print('score')
        if request.method == 'POST':
            correct = ['2', '6', '8']  # get the correct answers for all the problems
            score = 0
            print('checking answers...')
            n = 1
            for answer in correct:
                if request.POST[f"question{n}"] == answer:
                    score += 1
                n += 1
            print('The score is: ', score)

            # TODO update score the the user profile
            # TODO refine the code
            #  TODO Differentiate between Pre/Post test

    return render(request, 'Tests.html', {'questions': json_q})


def training(request):
    return render(request, 'Training.html')
