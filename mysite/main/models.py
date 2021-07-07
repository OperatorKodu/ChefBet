import datetime as dt
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=20, help_text='Enter an event category (e.g. Soccer)')
    duration = models.IntegerField(default=60, help_text='Enter duration of the event')

    def __str__(self):
        return self.name


class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    host = models.CharField(max_length=30, help_text='Enter an event host (e.g. Borussia Dortmund')
    guest = models.CharField(max_length=30, help_text='Enter an event guest (e.g. Bayern Monachium')
    types = models.JSONField(default=dict)
    start_datetime = models.DateTimeField(default=datetime.now)
    end_datetime = models.DateTimeField(default=datetime.now)
    is_settled = models.BooleanField(default=False)

    def __str__(self):
        title = self.host + ' vs ' + self.guest
        return title

    def save(self, *args, **kwargs):
        minutes = self.category.duration
        self.end_datetime = self.start_datetime + dt.timedelta(minutes=minutes)
        super(Event, self).save(*args, **kwargs)

class Coupon(models.Model):
    id = models.AutoField(primary_key=True)
    types = models.JSONField(default=dict)
    odds = models.FloatField(default=1)
    contribution = models.FloatField()
    prize = models.FloatField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", null=True)
    is_active = models.BooleanField(default=True)
    is_winning = models.BooleanField(default=False)


class Wallet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    money = models.FloatField(default=0)

    def __str__(self):
        name = self.owner.username + "'s wallet"
        return name
