import json
from functools import wraps

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .helpers import enc_password, get_hexdigest, get_saved_data, login_required, openFile, get_file
from .models import *
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from rest_framework import viewsets

from .serializer import UserSerializer,WeatherSerializer
from . import configs
import requests



class sign_up(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def list(self,request, *args, **kwargs):
        context_dict={}
        return render(request, 'sign_up.html', context_dict)

    def create(self,request, *args, **kwargs):
        request.data._mutable = True
        request.data['password'] = enc_password(request.data['password'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return HttpResponseRedirect("/login")
class dashboard(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    @get_saved_data()
    def list(self, request, *args, **kwargs):
        # cities = openFile('city.list.json')
        cities= get_file("city.list.json")
        self.context_dict['cities'] = [[city['id'],city['name']] for city in cities  if city['country']=='IN']

        return render(request, 'dashboard.html', self.context_dict)
    def create(self, request, *args, **kwargs):
        context_dict = {}
        url=configs.WeatherURL%(request.POST.get('city'),configs.Weather_API_Key)
        result=requests.get(url)
        # cities = openFile('city.list.json')
        cities = get_file("city.list.json")
        context_dict['cities'] = [[city['id'],city['name']] for city in cities if city['country'] == 'IN']
        context_dict['city_selected']=request.POST.get('city')
        context_dict['weather'] = str(json.loads(result.content)['main']['temp'] )+ ' C'
        return render(request, 'dashboard.html', context_dict)


class login(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        context_dict = {}
        return render(request, 'login.html', context_dict)

    def create(self, request, *args, **kwargs):
        request.data._mutable = True
        context_dict={}
        encrypted_password= enc_password(request.data['password'])
        user= User.objects.filter(username=request.data['username'])
        if user:
            a = user[0].password.split('$')
            hashdb = str(a[2])
            salt = str(a[1])
            usrhash = get_hexdigest(a[0], a[1], request.data['password'])

        if not user or usrhash!= hashdb:
            context_dict['error'] = True
            return render(request, 'login.html', context_dict)
        request.session['user']=user[0].id
        return HttpResponseRedirect("/dashboard")

@csrf_exempt
def logout(request):
    del request.session['user']
    return HttpResponse(json.dumps({'isSuccess':True}, indent=4))
@login_required()
def save_weather(request):
    try:
        obj=Weather.objects.create(city=request.POST.get('city'),weather=request.POST.get('weather'),user=User.objects.get(id=request.session['user']))
        return HttpResponse(json.dumps({'isSuccess':True}, indent=4))
    except Exception as e:
        return HttpResponse(json.dumps({'isSuccess': False}, indent=4))