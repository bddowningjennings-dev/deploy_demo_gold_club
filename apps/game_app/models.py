# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login_app.models import *


class ActivityManager(models.Manager):
  def add(self, user_id, delta_gold, description):
    activity = Activity()
    activity.gold_delta = delta_gold
    activity.description = description
    user = User.objects.get(id=user_id)
    user.gold += delta_gold
    activity.user = user
    activity.save()
    if user.gold <= 0:
      Activity.objects.filter(user=user).delete()
      user.delete()
      return False
    user.save()
    return True

class Activity(models.Model):
  gold_delta = models.IntegerField()
  description = models.CharField(max_length=255)
  user = models.ForeignKey(User, related_name='activities')
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)
  objects = ActivityManager()
  def __str__(self):
    return '\n\nActivity:\nuser: {}\ngold_delta: {}\ngold: {}'.format(self.user.name, self.gold_delta, self.user.gold)