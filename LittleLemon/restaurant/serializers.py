from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Booking, Menu


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['title', 'price', 'inventory']
        

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
