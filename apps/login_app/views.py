# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from ..game_app.models import *
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages

def index(request):
    try:
        request.session['user_id']
    except:
        request.session['user_id'] = None
    if request.session['user_id'] != None:
        return redirect('/home')
    context = {
        'users': User.objects.all(),
    }
    return render(request, 'login_app/index.html', context)

def register(request):
    if request.method != 'POST':
        return redirect('/')
    results = User.objects.validation_register(request.POST)
    if len(results['errors']) > 0:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/')
    user = User.objects.create(request.POST)
    request.session['user_id'] = user.id
    return redirect('/home')

def login(request):
    if request.method != 'POST':
        return redirect('/')
    try:
        request.session['user_id']
    except:
        return redirect('/')
    results = User.objects.validation_login(request.POST)
    if len(results['errors']) > 0:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = results['user_id']
    return redirect('/home')

def logout(request):
    try:
        request.session['user_id']
    except:
        return redirect('/')
    request.session.flush()
    return redirect('/')

def home(request):
    try:
        request.session['user_id']
    except:
        return redirect('/')
    if request.session['user_id'] == None:
        return redirect('/')
    context = {
        'users': User.objects.all(),
        'user': User.objects.get(id=request.session['user_id']),
        'top_5': User.objects.all().order_by('-gold')[:5],
    }
    return render(request, 'login_app/home.html', context)

def all(request):
    context = {
        'users': User.objects.all().order_by('-gold'),
    }
    return render(request, 'login_app/all.html', context)

def user(request, user_id):
    try:
        request.session['user_id']
    except:
        return redirect('/')
    user = User.objects.get(id=user_id)
    context = {
        'activities': Activity.objects.filter(user=user),
        'user': user,
    }
    return render(request, 'login_app/user.html', context)
