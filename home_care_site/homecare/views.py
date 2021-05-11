from django.shortcuts import render, redirect
from .models import *
# Create your views here.
# index view
import datetime
import json


def index(request):
    slides = HomeSlides.objects.all()
    # also create new user in userinfo table
    user_id = request.user.id
    if user_id:
        # save new user
        if UserInfo.objects.filter(user_id=user_id).exists():
            stats = get_userinfo(user_id)

            return render(request, 'index.html', {'stats': stats, 'slides': slides})

        else:
            user_info = UserInfo(user_id=user_id)
            user_info.save()
            print(' new user saved!')
            try:
                stats = get_userinfo(user_id)
                return render(request, 'index.html', {'stats': stats, 'slides': slides})
            except'Internal Server Error':
                return render(request, 'index.html')

    return render(request, 'index.html', {'slides': slides})


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

    if request.method == 'POST':
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
        results = calculate_percentage(score, n-1, test_id)

        # start working to update
        user_id = request.user.id
        update = update_db(results, test_id, user_id)

        # if the user has passed post test print certificate
        print(update)

        return render(request, 'Tests.html', {'score': results})

            # TODO refine the code

    return render(request, 'Tests.html', {'test': tests})


def training(request):
    videos = TrainingVideo.objects.all()

    return render(request, 'Training.html', {'videos': videos})


def get_userinfo(pk):  # grab users information from user_info table
    if UserInfo.objects.get(user_id=pk):
        user_information = UserInfo.objects.get(user_id=pk)
        pretest_completion = {'completion': 'Take Test', 'color': 'red'}
        postest_completion = {'completion': 'Take Test', 'color': 'red'}
        training_completion = {'completion': 'Train', 'color': 'red'}
        if user_information.pretest_completion:
            pretest_completion['completion'] = 'Complete'
            pretest_completion['color'] = 'green'

        if user_information.postest_completion:
            postest_completion['completion'] = 'Complete'
            postest_completion['color'] = 'green'
            print('color changed to green')

        if user_information.training_completion:
            training_completion['color'] = 'green'
            training_completion['completion'] = 'Complete'

        stats = {
            'pretest_completion': pretest_completion,
            'postest_completion': postest_completion,
            'training_completion': training_completion
        }

        return stats
    return None


def calculate_percentage(score, num_questions, test_id):
    percentage = round((score/num_questions)*100, 0)
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
            'message': 'congratulations you passed',
            'test': test_id,
            'num_questions': num_questions
        }
    else:
        user_score = {
            'score': score,
            'percentage': percentage,
            'grade': 'fail',
            'color': 'red',
            'message': 'Unfortunately you failed',
            'test': test_id,
            'num_questions': num_questions
        }

    return user_score


def update_db(score, test_name, user_id):  # this function will update the db
    percentage = score['percentage']
    if test_name == '2':
        UserInfo.objects.filter(user_id=user_id).update(postest_grade=percentage, postest_completion=True)

        return 'updated post-test'
    else:
        UserInfo.objects.filter(user_id=user_id).update(pretest_completion=True, pretest_grade=percentage)

        return 'updated pre-test'


def certificate(request):
    if request.method == 'POST':
        post = request.POST['certificate']
        # convert from str back to dict
        score = eval(post)
        fullname = request.user.get_full_name
        date = datetime.date.today()

        return render(request, 'certificate.html', {'fullname': fullname, 'date': date, 'score': score} )

