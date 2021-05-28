from django.shortcuts import render
from .models import *
# Create your views here.
import datetime


def index(request):
    slides = HomeSlides.objects.all()
    # also create new user in userinfo table

    return render(request, 'index.html', {'slides': slides})


def module(request):
    if request.method == 'GET':
        value = request.GET.get('module')
        required_test = Tests.objects.filter(module_id=value)
        return render(request, 'modules.html', {'tests': required_test})


def test(request):
    # get the tests
    user_id = request.user.id
    tests = Tests.objects.all()
    completed_tests = TestComplete.objects.filter(user_id=user_id, test_completion=True)
    completed_pk_list = []
    for completed_test in completed_tests:
        completed_pk_list.append(completed_test.test.id)
    # get the questions
    # get the test id that the user selected

    if request.method == 'GET':
        required_test = request.GET.get('pk')
        print('Required test: ', required_test)
        if required_test is not None:
            req_test = Tests.objects.get(id=required_test)
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
        value = Tests.objects.get(pk=test_id).module.id
        # check if test is pre/post test
        if Tests.objects.get(pk=test_id).name == 'Pre-test':
            required_test = Tests.objects.filter(module_id=value)
            required_video = TrainingVideos.objects.filter(module_id=value)
            required_ppt = TrainingPpt.objects.filter(module_id=value)
            pretest_done = True
            return render(request, 'modules.html', {'videos': required_video, 'powerpoints': required_ppt, 'tests': required_test, 'pretest_done': pretest_done})

        else:
            questions = Question.objects.all().filter(test_id=test_id)
            module = Module.objects.get(id=value)
            user_answers = []
            # get the module_id
            module_id = Tests.objects.get(pk=test_id).module.id
            score = 0
            print('checking answers...')
            n = 1
            for question in questions:
                user_answers.append(request.POST[f"question{n}"])
                if request.POST[f"question{n}"] == question.correct_answer:
                    score += 1
                n += 1
            print('The score is: ', score)
            results = calculate_percentage(score, n-1, test_id)

            # start working to update
            user_id = request.user.id
            update = update_db(results, test_id, user_id, module_id, user_answers)

            # if the user has passed post test print certificate
            print(update)

            # Check if course if completed
            completed = check_modules(user_id)
            return render(request, 'Tests.html', {'score': results, 'completed': completed, 'module': module})

            # TODO refine the code
    print('outershell')
    return render(request, 'Tests.html', {'tests': tests, 'completed_pk_list': completed_pk_list})


def training(request):
    modules = Module.objects.all()
    videos = TrainingVideos.objects.all()
    user_id = request.user.id
    if request.method == 'GET':
        try:
            completed = round(((TestComplete.objects.filter(user_id=user_id, test_completion=True).count()) / 7) * 100,0)
            print(' the percentage is ', completed)
            return render(request, 'Training.html', {'modules': modules, 'completed': completed})
        except user_id.DoesNotExist:
            completed = False

    return render(request, 'Training.html', {'modules': modules, 'completed': completed})

        # see how many tests of 16 are complete


def calculate_percentage(score, num_questions, test_id):
    percentage = round((score/num_questions)*100, 0)

    if percentage > 79:
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


def update_db(score, test_id, user_id, module_id, user_answers):  # this function will update the db
    percentage = score['percentage']
    if TestComplete.objects.filter(user_id=user_id, test_id=test_id).exists():
        TestComplete.objects.filter(user_id=user_id, test_id=test_id).update(test_grade=percentage, module_id=module_id, user_answers=user_answers)
        # check if user has passed
        if score['grade'] == 'pass':
            TestComplete.objects.filter(user_id=user_id, test_id=test_id).update(test_completion=True)
            # update module if passed
            update = module_completion(user_id, module_id)

    else:
        TestComplete.objects.create(user_id=user_id, test_id=test_id, test_grade=percentage, module_id=module_id, user_answers=user_answers)
        if score['grade'] == 'pass':
            TestComplete.objects.filter(user_id=user_id, test_id=test_id, test_grade=percentage).update(test_completion=True)
            # update module if passed
            update = module_completion(user_id, module_id)

    return 'test'


def certificate(request):
    user_id = request.user.id
    try:
        course_completion = CourseCompletion.objects.get(owner_id=user_id)
    except CourseCompletion.DoesNotExist:
        course_completion = None
    if request.method == 'POST':
        post = request.POST['certificate']
        # convert from str back to dict
        score = eval(post)
        fullname = request.user.get_full_name
        date = datetime.date.today()
        return render(request, 'certificate.html', {'fullname': fullname, 'date': date, 'score': score, 'course_completion': course_completion})

    return render(request, 'certificate.html', {'course_completion': course_completion})


def module_completion(user_id, module_id):
    # get all module
    module_taken = Module.objects.get(id=module_id)
    tests = TestComplete.objects.filter(user_id=user_id, module_id=module_id, test_completion=True)
    if CourseCompletion.objects.filter(owner_id=user_id).exists():
        # get the completed tests
        if len(tests) == 1:
            cs = CourseCompletion.objects.get(owner_id=user_id)
            cs.modules.add(module_taken)
            print('the leght of len tests is:', len(tests))

    else:
        CourseCompletion.objects.create(owner_id=user_id, )
        if len(tests) == 1:
            cs = CourseCompletion.objects.get(owner_id=user_id)
            cs.modules.add(module_taken)
        print('the leght of len tests is:', len(tests))

    return 'updates run...'
    # after both pre and post test are done, module is added to couser completion


def check_modules(user_id):
    try:
        completion = CourseCompletion.objects.get(owner_id=user_id)
        num_completed = completion.modules.count()
        if num_completed == 7:          # remember to change this to 8
            completion.complete = True
            completion.save()
            return_val = 'complete'
            return return_val
        else:
            return_val = 'False'
            return return_val
    except CourseCompletion.DoesNotExist:
        pass


def portal(request):
    # GET ALL USERS WHO HAVE COMPLETED COURSE
    completed_users = CourseCompletion.objects.filter(complete=True)
    # GET ALL USERS WHO ARE IN PROGRESS
    in_progress_users = CourseCompletion.objects.filter(complete=False)
    if request.method == 'GET':
        val = request.GET.get('needed_val')
        if val == 'completed_users':
            return render(request, 'administrator.html', {'completed_users': completed_users})

        elif val == 'in_progress_users':
            return render(request, 'administrator.html', {'in_progress_users': in_progress_users})

        else:
            questions = Question.objects.all()
            tests = Tests.objects.all()
            tests_complete = TestComplete.objects.filter(user_id=val)
            test_answers = render_answer_template(tests_complete)
            if CourseCompletion.objects.filter(owner_id=val).exists():
                if CourseCompletion.objects.get(owner_id=val).complete:
                    course_completion = CourseCompletion.objects.get(owner_id=val)
                    completed = round(((TestComplete.objects.filter(user_id=val, test_completion=True).count()) / 7) * 100, 0)
                    return render(request, 'administrator.html', {'Tests': tests, 'Test_complete': tests_complete, 'completed': completed, 'test_answers': test_answers, 'questions': questions, 'course_completion': course_completion})
                else:
                    in_progress = round(((TestComplete.objects.filter(user_id=val, test_completion=True).count()) / 7) * 100, 0)
                    return render(request, 'administrator.html', {'Tests': tests, 'in_progress': in_progress})

    return render(request, 'administrator.html')


def render_answer_template(tests):
    test_answers = {}
    for test in tests:
        print(test.user_answers)
        answers_list = create_answers_list(test.user_answers)
        test_answers.update({test.test.pk: answers_list})
    print(test_answers)
    return test_answers


def create_answers_list(val):
    answers_list = []
    t = val.strip("[]")
    g = t.split(',')
    for n in g:
        v = n.strip("''")
        answers_list.append(v)

    return answers_list



'''
        1. get all users and put them in 3 groups completed, in-progress, not-started
        2. for the completed it should contain all their exams and certificates downloadable
        3. for in pogress it should just show their progress as percentage
        4. not started just shows a list of name
    '''
