import hashlib
import json
from functools import wraps
import random

import boto3
from django.shortcuts import render
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from rest_framework import viewsets

from .serializer import UserSerializer,WeatherSerializer
from . import configs
import requests



def enc_password(password):
    algo = 'sha1'
    salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
    hsh = get_hexdigest(algo, salt, password)
    password = '%s$%s$%s' % (algo, salt, hsh)
    return password

def get_hexdigest(algorithm, salt, raw_password):

    raw_password, salt = smart_str(raw_password), smart_str(salt)
    return hashlib.sha1((salt + raw_password).encode('utf-8')).hexdigest()


def login_required():
    def _login_required(view_func):
        def _decorator(request):
            user = request.session.get('user')
            if not user:
                return HttpResponseBadRequest()

            else:

                response = view_func(request)
                # maybe do something after the view_func call
                return response
        return wraps(view_func)(_decorator)
    return _login_required

def get_saved_data():
    def _get_saved_data(view_func):
        def _decorator(clss, request, *args, **kwargs):
            userid = request.session.get('user')
            clss.context_dict = {}
            if userid:
                latest_data = Weather.objects.filter(user__id=userid).order_by('-id')
                if latest_data:
                    latest_data=latest_data[0]
                    clss.context_dict['city_selected'] =latest_data.city
                    clss.context_dict['weather'] =latest_data.weather

            response = view_func(clss, request, *args, **kwargs)
            return response
        return wraps(view_func)(_decorator)
    return _get_saved_data

def openFile(filename):
    file = open(filename, encoding='utf8')
    cities = json.loads(file.read())
    return cities

def get_file(filename):




    client =  boto3.client('s3',
                      aws_access_key_id=configs.AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=configs.AWS_SECRET_ACCESS_KEY,
                      region_name='us-east-1',
                      )
    file= client.get_object(Bucket=configs.BUCKET_NAME, Key=filename)
    body = file['Body']
    data=body.read().decode('utf-8')
    return json.loads(data)