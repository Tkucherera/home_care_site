
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User, auth
from .models import *
# Create your views here.
# Create your views here.
# register view


def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        username = request.POST['username']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)

            return redirect('index')

        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


def register(request):
    # get data from register form
    if request.method == 'POST':
        first_name = request.POST['name']
        last_name = request.POST['last-name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # check to see if the email is taken
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('register')

        else:
            user = User.objects.create_user(password=password, email=email, first_name=first_name, last_name=last_name, username=username)
            user.save()

            return redirect('login')
    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('login')







