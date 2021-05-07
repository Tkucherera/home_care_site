from django.shortcuts import render, redirect
from .models import *
# Create your views here.
# index view


def index(request):
    # tests = Test.objects.all()
    # also create new user in userinfo table
    user_id = request.user.id
    if user_id:
        if not UserInfo.objects.get(user_id=user_id):
            user_info = UserInfo(user_id=user_id)
            user_info.save()

        stats = get_userinfo(user_id)

        return render(request, 'index.html', {'stats': stats})

    return render(request, 'index.html')


def test(request):
    # get the tests
    tests = Test.objects.all()
    # get the questions
    # get the test id that the user selected

    if request.method == 'GET':
        required_test = request.GET.get('pk')
        print('Required test: ', required_test)
        if required_test is not None:
            questions = Question.objects.all().filter(test_id=required_test)
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

                counter += 1
                json_q.append(data_input)

            return render(request, 'Tests.html', {'questions': json_q, 'pk': required_test})

    elif request.method == 'POST':
        # first get the correct answers
        test_id = request.POST['test_submit']
        questions = Question.objects.all().filter(test_id=test_id)
        correct_answers = []

        score = 0
        print('checking answers...')
        n = 1
        for question in questions:
            if request.POST[f"question{n}"] == question.correct_answer:
                score += 1
            n += 1
        print('The score is: ', score)

        return render(request, 'Tests.html', {'score': score})

            # TODO update score the the user profile
            # TODO refine the code
            #  TODO Differentiate between Pre/Post test


    else:

        return render(request, 'Tests.html')


def training(request):
    return render(request, 'Training.html')


def get_userinfo(pk):  # grab users information from user_info table
    user_information = UserInfo.objects.get(user_id=pk)
    pretest_completion = {'completion': 'Take Test', 'color': 'red'}
    postest_completion = {'completion': 'Take Test', 'color': 'red'}
    training_completion = {'completion': 'Train', 'color': 'red'}
    if user_information.pretest_completion:
        pretest_completion['completion'] = 'Complete'
        pretest_completion['color'] = 'green'

    if user_information.postest_completion:
        postest_completion['completion'] = 'Complete'
        pretest_completion['color'] = 'green'

    if user_information.training_completion:
        training_completion['color'] = 'green'
        training_completion['completion'] = 'Complete'

    stats = {
        'pretest_completion': pretest_completion,
        'postest_completion': postest_completion,
        'training_completion': training_completion
    }

    return stats


def calculate_percentage(score, num_questions):
    percentage = (score/num_questions)*100
    # parse percentage to get suggestion
    db_scores = {
        'A': 90,
        'B': (80, 89),
        'C': (70, 79),
        'Fail': (0, 69)
    }
    if percentage > 69:
        user_score = {
            'score': score,
            'percentage': percentage,
            'grade': 'pass',
            'color': 'green',
            'message': 'congratulations you passed'
        }
    else:
        user_score = {
            'score': score,
            'percentage': percentage,
            'grade': 'fail',
            'color': 'red',
            'message': 'Unfortunately you failed'
        }

    return user_score

