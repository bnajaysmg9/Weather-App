from rest_framework import exceptions, serializers
from .models import Weather,User


class WeatherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Weather
        # exclude = ('ipaddress','registeredon', )
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # exclude = ('ipaddress','registeredon', )
        fields = '__all__'