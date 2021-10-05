from rest_framework import serializers

from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django import forms
from django.contrib.auth import authenticate
from .models import Customer,Shopkeeper,Items,Shopkeeper_Order_History,Customer_Order_History

class RegisterSerializer(serializers.Serializer):

        shopkeeper=serializers.BooleanField(required=True)
        Name=serializers.CharField(required=True,max_length=100)
        email=serializers.EmailField(required=False)
        phone=serializers.CharField(max_length=12,required=False)
        password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
        password2 = serializers.CharField(write_only=True, required=True)
      
        

        def validate(self, attrs):
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})
            return attrs

        def validate(self,data):
            if data.get('shopkeeper')==True:
                if data.get('phone')==None:
                    raise serializers.ValidationError({'Phone value should be supplied'})
            else:
                if data.get('phone')==None and data.get('email')==None:
                    raise serializers.ValidationError({'Either phone or email value should be supplied'})
            
            return data
        
        

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            if User.objects.filter(username=username).exists():
                user = authenticate(request=self.context.get('request'),
                                    username=username, password=password)
                
            else:
                msg = {'detail': 'Phone number/E-mail is not registered.',
                       'register': False}
                raise serializers.ValidationError(msg)

            if not user:
                msg = {
                    'detail': 'Unable to log in with provided credentials.', 'register': True}
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class CustomerSerializer(serializers.ModelSerializer):
        
        class Meta:
            model=Customer
            fields=['Name','email','phone','address','loggedin_with']
      
        def validate(self,data):
            
            username=self.context['request'].user
            obj=Customer.objects.get(user1__username=username)
            obj=CustomerSerializer(obj)
           
            log_value=obj['loggedin_with'].value
           
            val=data.get(log_value)
           
            
            if val:
                print(val,obj[log_value].value)
                
                if val!=obj[log_value].value:
                    raise serializers.ValidationError({"Can't update the value which was used for logging in!!"})
        
            return data

class ShopkeeperSerializer(serializers.ModelSerializer):

        loggedin_with=serializers.CharField(required=False)
        class Meta:
            model=Shopkeeper
            fields=['id','Restaurant_name','Owner_name','email','phone','address','loggedin_with','Category']
        
        def validate(self,data):
            username=self.context['request'].user
           
            obj=Shopkeeper.objects.get(user1__username=username)
            obj=ShopkeeperSerializer(obj)
          
            log_value=obj['loggedin_with'].value
           
            val=data.get(log_value)
            
            if val:
                print(val,obj[log_value].value)
                
                if val!=obj[log_value].value:
                    raise serializers.ValidationError({"Can't update the value which was used for logging in!!"})
        
            return data


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model=Items
        fields=['Name','Description','Price','Category','id']
    
    def validate(self,data):
        username=self.context['request'].user
        li=Shopkeeper.objects.filter(user1__username=username)
        if len(li)==0:
            return Serializers.ValidationError({"Customer can not add items"})
        return data


class soh_serializer(serializers.ModelSerializer):

    class Meta:
        model=Shopkeeper_Order_History
        fields=['id','status','user','items']


class coh_serializer(serializers.ModelSerializer):
    class Meta:
        model=Customer_Order_History
        fields=['id','status','user','items']