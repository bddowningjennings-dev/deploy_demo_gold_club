# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_app.models import *
from .models import *
import random
from django.shortcuts import render, redirect

def game(request):
  try:
    request.session['user_id']
  except:
    return redirect('/')
  if request.session['user_id'] == None:
    return redirect('/')
  user = User.objects.get(id=request.session['user_id'])
  context = {
    'user': user,
    'activities': Activity.objects.filter(user=user).order_by('-id')[:10],
  }
  return render(request, 'game_app/game.html', context)

def game_over(request):
  # try:
  #   request.session['user_id']
  # except:
  #   return redirect('/')
  # if request.session['user_id'] == None:
  #   return redirect('/')
  request.session.flush()
  return render(request, 'login_app/gameover.html')

def tire_factory(request):
  try:
    request.session['user_id']
  except:
    return redirect('/')
  if request.session['user_id'] == None:
    return redirect('/')
  delta = random.randrange(-100,20)
  if not Activity.objects.add(request.session['user_id'],delta,'Tire Factory'):
    return redirect('/game/game_over')    
  return redirect('/game')

def dance_off(request):
  try:
    request.session['user_id']
  except:
    return redirect('/')
  if request.session['user_id'] == None:
    return redirect('/')
  delta = random.randrange(-50,50)
  if not Activity.objects.add(request.session['user_id'],delta,'Dance off'): 
    return redirect('/game/game_over')    
  return redirect('/game')

def gmas_house(request):
  try:
    request.session['user_id']
  except:
    return redirect('/')
  if request.session['user_id'] == None:
    return redirect('/')
  delta = random.randrange(-10,200)
  if not Activity.objects.add(request.session['user_id'],delta,'Visit Grandma'):
    return redirect('/game/game_over')    
  return redirect('/game')