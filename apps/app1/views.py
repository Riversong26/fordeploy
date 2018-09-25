from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import *
import bcrypt
from datetime import datetime



def index(request):
    return render(request, 'app1/index.html')

def registration_process(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value, extra_tags='reg')
        print(errors)
        return redirect('/')
    new_user = User(
        name=request.POST['name'],
        alias=request.POST['alias'],
        email=request.POST['email'],
        password=bcrypt.hashpw(request.POST['password'].encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        #Password.objects.create(pwd = password.decode('utf-8') 
        #user = User.objects.get(id = new_user.id)
    )
    new_user.save()
    request.session['id'] = new_user.id 
    request.session['name']= new_user.name
    return redirect('/')

def login_process(request):
    login_errors = User.objects.login_validator(request.POST)
    if len(login_errors):
        for key, value in login_errors.items():
            messages.error(request, value, extra_tags='login')
        return redirect('/')
    #request.POST['password'].encode('utf-8')
    
    request.session['id'] = User.objects.filter(email=request.POST['email'])[0].id
    request.session['name']= User.objects.get(email=request.POST['email']).name 
    return redirect('/pokes')

def logout(request):
    request.session.flush()
    return redirect('/')

def pokes(request):
    try: 
        request.session['id']
    except KeyError:
        return redirect('/')
    else:
        users = User.objects.all()
        pokes = Poke.objects.all()
        context = {
            'users':users,
            'pokes':pokes
        }
        return render(request, 'app1/pokes.html', context)

def more(request, user_id):
    poker = User.objects.get(id=request.session['id'])
    print(poker.name)
    pokie = User.objects.get(id=user_id)
    print(pokie.name)
    poke = Poke()
    poke.poker = poker
    poke.pokie = pokie
    poke.created_at = datetime.now()
    poke.counter+=1
    poke.save()
    return redirect('/pokes')