from django.shortcuts import render, redirect
from .models import *
# Create your views here.
# index view
import datetime
import json


def index(request):
    slides = HomeSlides.objects.all()
    # also create new user in userinfo table

    return render(request, 'index.html', {'slides': slides})


def module(request):
    modules = Module.objects.all()
    return render(request, 'modules.html', {'module': modules})


def test(request):
    # get the tests
    tests = Test.objects.all()
    # get the questions
    # get the test id that the user selected

    if request.method == 'GET':
        required_test = request.GET.get('pk')
        print('Required test: ', required_test)
        if required_test is not None:
            req_test = Test.objects.get(id=required_test)
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

            return render(request, 'Tests.html', {'questions': json_q, 'pk': required_test, 'test':req_test})

    if request.method == 'POST':
        # first get the correct answers
        test_id = request.POST['test_submit']
        questions = Question.objects.all().filter(test_id=test_id)
        correct_answers = []
        # get the module_id
        module_id = Test.objects.get(pk=test_id).module.id
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
        update = update_db(results, test_id, user_id, module_id)

        # if the user has passed post test print certificate
        print(update)

        # Check if course if completed
        completed = check_modules(user_id)
        return render(request, 'Tests.html', {'score': results, 'completed': completed})

            # TODO refine the code

    return render(request, 'Tests.html', {'tests': tests})


def training(request):
    modules = Module.objects.all()
    videos = TrainingVideo.objects.all()
    user_id = request.user.id
    if request.method == 'GET':
        try:
            completed = ((TestComplete.objects.filter(user_id=user_id, test_completion=True).count()) / 16) * 100
            print(' the percentage is ', completed)
            return render(request, 'Training.html', {'modules': modules, 'completed': completed})
        except user_id.DoesNotExist:
            completed = False

    if request.method == 'POST':
        module = request.POST['module']
        required_test = Test.objects.filter(module_id=module)
        completed = False
        return render(request, 'Training.html', {'modules': modules, 'tests': required_test})

    return render(request, 'Training.html', {'modules': modules, 'completed': completed})

        # see how many tests of 16 are complete


'''def get_userinfo(pk):  # grab users information from user_info table
    if TestCompletion.objects.get(user_id=pk):
        user_information = TestCompletion.objects.get(user_id=pk)
        counter = 1:
        for pretest_completion in user_information:
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
    return None'''


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


def update_db(score, test_id, user_id, module_id):  # this function will update the db
    percentage = score['percentage']
    if TestComplete.objects.filter(user_id=user_id, test_id=test_id).exists():
        TestComplete.objects.filter(user_id=user_id, test_id=test_id).update(test_grade=percentage, module_id=module_id)
        # check if user has passed
        if score['grade'] == 'pass':
            TestComplete.objects.filter(user_id=user_id, test_id=test_id).update(test_completion=True)
            # update module if passed
            update = module_completion(user_id, module_id)

    else:
        TestComplete.objects.create(user_id=user_id, test_id=test_id, test_grade=percentage, module_id=module_id)
        if score['grade'] == 'pass':
            TestComplete.objects.filter(user_id=user_id, test_id=test_id, test_grade=percentage).update(test_completion=True)
            # update module if passed
            update = module_completion(user_id, module_id)

    return 'test'


def certificate(request):
    if request.method == 'POST':
        post = request.POST['certificate']
        # convert from str back to dict
        score = eval(post)
        fullname = request.user.get_full_name
        date = datetime.date.today()

        return render(request, 'certificate.html', {'fullname': fullname, 'date': date, 'score': score})


def module_completion(user_id, module_id):
    # get all module
    module_taken = Module.objects.get(id=module_id)
    tests = TestComplete.objects.filter(user_id=user_id, module_id=module_id)
    if CourseCompletion.objects.filter(owner_id=user_id).exists():
        # get the completed tests
        if len(tests) == 2:
            cs = CourseCompletion.objects.get(owner_id=user_id)
            cs.modules.add(module_taken)
            print('the leght of len tests is:', len(tests))

    else:
        CourseCompletion.objects.create(owner_id=user_id)
        if len(tests) == 2:
            cs = CourseCompletion.objects.get(owner_id=user_id)
            cs.modules.add(module_taken)
        print('the leght of len tests is:', len(tests))

    return 'updates run...'
    # after both pre and post test are done, module is added to couser completion


def check_modules(user_id):
    try:
        completion = CourseCompletion.objects.get(owner_id=user_id)
        num_completed = completion.modules.count()
        if num_completed >= 2:
            return_val = 'complete'
            return return_val
        else:
            return_val = 'False'
            return return_val
    except CourseCompletion.DoesNotExist:
        pass



