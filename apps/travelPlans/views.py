from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from ..loginAndRegistration.models import *
from django.contrib import messages
# Create your views here.
def index(request):
    if 'session_id' in request.session:
        result=User.objects.UserSessionValidator(request.session['session_id'])
        if result:
            this_user = User.objects.filter(session=request.session['session_id'])[0]
            context = {
                'first_name': this_user.first_name,
                'trips': (travels.objects.filter(traveler=this_user) | this_user.joined_trips.all()).distinct,
                'others': travels.objects.exclude(traveler=this_user).exclude(id__in=[i.id for i in this_user.joined_trips.all()]).select_related('traveler')
            }
            return render(request, 'travelPlans/index.html', context)
        else:
            request.session.clear()
    return redirect(reverse('login:index'))

def showtrip(request,number):
    if 'session_id' in request.session:
        result=User.objects.UserSessionValidator(request.session['session_id'])
        if result:
            context = {
                'trip': travels.objects.filter(id=number).select_related('traveler')[0],
                'others': travels.objects.get(id=number).joiners.all()

            }
            return render(request, 'travelPlans/showtrip.html', context)
        else:
            request.session.clear()
    return redirect(reverse('login:index'))

def newtrip(request):
    if 'session_id' in request.session:
        result=User.objects.UserSessionValidator(request.session['session_id'])
        if result:
            return render(request, 'travelPlans/newtrip.html')
        else:
            request.session.clear()
    return redirect(reverse('login:index'))

def createtrip(request):
    if 'session_id' in request.session:
        result=User.objects.UserSessionValidator(request.session['session_id'])
        if result:
            user_id = User.objects.filter(session=request.session['session_id'])[0].id
            errors = travels.objects.travelsValidator(request.POST, user_id)
            if errors:
                for key, value in errors.items():
                    messages.error(request, value, extra_tags=key)
                return redirect(reverse('travels:newtrip'))
            else:
                messages.success(request, "Your trip has been successfully created.", extra_tags='success')
                return redirect(reverse('travels:index'))
        else:
            request.session.clear()
    return redirect(reverse('login:index'))

def jointrip(request, number):
    if 'session_id' in request.session:
        result=User.objects.UserSessionValidator(request.session['session_id'])
        if result:
            this_trip = travels.objects.get(id=number)
            this_user = User.objects.get(session=request.session['session_id'])
            this_user.joined_trips.add(this_trip)
            return redirect(reverse('travels:index'))
        else:
            request.session.clear()
    return redirect(reverse('login:index'))