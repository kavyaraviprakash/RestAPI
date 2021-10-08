from rest_framework import serializers
from .models import *
from orders.models import Order


class cSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class uSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email')


class pSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('category', 'name', 'price')
        # fields = '__all__'


class oSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'phone')
