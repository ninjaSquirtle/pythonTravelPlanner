from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import *
import random, string, hashlib

# Create your views here.
def index(request):
    if 'session_id' in request.session:
        result=User.objects.UserSessionValidator(request.session['session_id'])
        if result:
            return redirect(reverse('travels:index'))
        else:
            request.session.clear()
    return render(request, 'loginAndRegistration/index.html')

def success(request):
    if 'session_id' not in request.session:
        return redirect(reverse('login:index'))
    elif not User.objects.filter(session=request.session['session_id']):
        request.session.clear()
        return redirect(reverse('login:index'))
    else:
        context = {
            'first_name': User.objects.filter(session=request.session['session_id'])[0].first_name
        }
        return render(request, 'loginAndRegistration/success.html', context)

def register(request):
    salt = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    session = hashlib.md5((salt).encode()).hexdigest()
    errors = User.objects.UserRegisterValidator(request.POST, session)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('login:index'))
    else:
        request.session['session_id'] = session
        messages.success(request, "User has been successfully created.", extra_tags='success')
        return redirect(reverse('travels:index'))

def login(request):
    salt = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    session = hashlib.md5((salt).encode()).hexdigest()
    errors = User.objects.UserLoginValidator(request.POST, session)
    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect(reverse('login:index'))
    else:
        request.session['session_id'] = session
        messages.success(request, "User has successfully logged in.", extra_tags='success')
        return redirect(reverse('travels:index'))

def logout(request):
    if 'session_id' in request.session:
        User.objects.UserLogout(request.session['session_id'])
        request.session.clear()
    return redirect(reverse('login:index'))

