# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
from django.db import models
import re

EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

class UserManager(models.Manager):
  def validation_register(self, postData):
    results = {
      'errors': [],
    }
    for val in postData:
      if len(postData[val]) < 1 and str(val) != 'c_password':
        results['errors'].append('{} field cannot be blank'.format(str(val).capitalize()))
      elif len(postData[val]) < 2 and str(val) != 'c_password' and str(val) != 'password':
        results['errors'].append('{} field must have at least one character'.format(str(val).capitalize()))
      elif len(postData[val]) < 8 and str(val) == 'password':
        results['errors'].append('{} field must have at least eight characters'.format(str(val).capitalize()))
    if postData['password'] != postData['c_password']:
      results['errors'].append('Passwords not successfully confirmed, try again')
    if not re.match(EMAIL_REGEX, postData['email']):
      results['errors'].append('Invalide Email')
    if User.objects.filter(email=postData['email']).exists():
      results['errors'].append('Email attached to previously registered user')
    return results
  def create(self, postData):
    user = User()
    user.name = postData['name']
    user.email = postData['email']
    user.password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
    user.gold = 100
    user.save()
    return user

  def validation_login(self, postData):
    results = {
      'errors': [],
    }
    for val in postData:
      if len(postData[val]) < 1:
        results['errors'].append('{} field cannot be blank'.format(str(val).capitalize()))
    if not self.filter(email=postData['email']).exists():
      results['errors'].append('Email not registered to existing account')
    else:
      user = self.filter(email=postData['email'])[0]
      results['user_id'] = user.id
      if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
        results['errors'].append('Wrong password, fool')
    return results

class User(models.Model):
  name = models.CharField(max_length=100)
  email = models.CharField(max_length=100)
  password = models.CharField(max_length=255)
  gold = models.IntegerField()
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  objects = UserManager()
  def __str__(self):
    return '\n\nUser:\nname: {}\nemail: {}\ngold: {}\n'.format(self.name, self.email, self.gold)


