import datetime

from django.db import models


class User(models.Model):
    password = models.CharField(max_length=256, null=False, blank=False)
    username = models.CharField(max_length=45, null=False, blank=False)
    createdon= models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return str(self.id)

class Weather(models.Model):
    city=models.CharField(max_length=45,null=False,blank=False)
    weather = models.CharField(max_length=45,null=False,blank=False)
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    createdon = models.DateTimeField(default=datetime.datetime.now())