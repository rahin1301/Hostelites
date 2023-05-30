from django.shortcuts import render
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from hostelites.serializers import RegisterSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes,authentication_classes
import io
from django.contrib.auth import login
from hostelites.models import User,PhoneOTP,Shopkeeper,Customer,Items,OrderItem,Order,Shopkeeper_Order_History,Customer_Order_History
from hostelites.serializers import CreateUserSerializer,LoginUserSerializer,ShopkeeperSerializer,CustomerSerializer,ItemSerializer,soh_serializer,coh_serializer
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.shortcuts import get_object_or_404

import math,random

@csrf_exempt
@authentication_classes([])
@api_view(["POST"])
def register(request):

    serializer=RegisterSerializer(data=request.data)
    if serializer.is_valid():

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)
def otp_generator():
    digits = "0123456789"
    OTP = "" 
    for i in range(4) : 
        OTP += digits[math.floor(random.random() * 10)] 
  
    return OTP 

def send_otp(phone):
    """
    This is an helper function to send otp to session stored phones or 
    passed phone number as argument.
    """
    
    if phone:
        
        key = otp_generator()
        phone = str(phone)
        otp_key = str(key)

        #link = f'https://2factor.in/API/R1/?module=TRANS_SMS&apikey=fc9e5177-b3e7-11e8-a895-0200cd936042&to={phone}&from=wisfrg&templatename=wisfrags&var1={otp_key}'
   
        #result = requests.get(link, verify=False)

        return otp_key
    else:
        return False

def sendotp_email(email):

    if email:
            key = otp_generator()
            email = str(email)
            otp_key = str(key)
            return otp_key
    else:
        return False


@api_view(["POST"])
@authentication_classes([])
@csrf_exempt
def ValidatePhoneSendOTP(request):
    '''
    This class view takes phone number and if it doesn't exists already then it sends otp for
    first coming phone numbers'''

    
    phone_number = request.data.get('phone')
    print(phone_number)
    val=1
    if phone_number:
        username=phone_number
        val=0
    else:
        username=request.data.get('email')
    if username:
            username = str(username)
            user = User.objects.filter(username = username)
            if user.exists():
                return Response({'status': False, 'detail': 'User already exists'})
            else:
                if val==0:
                    otp = send_otp(username)
                else:
                    otp=sendotp_email(username)
               
                if otp:
                    otp = str(otp)
                    count = 0
                    old = PhoneOTP.objects.filter(username = username)
                    if old.exists():
                        count = old.first().count
                        old.first().count = count + 1
                        old.first().save()
                    
                    else:
                        count = count + 1
               
                        PhoneOTP.objects.create(
                             username =  username, 
                             otp =   otp,
                             count = count
        
                             )
                    if count > 7:
                        return Response({
                            'status' : False, 
                             'detail' : 'Maximum otp limits reached. Kindly support our customer care or try with different number'
                        })
                    
                    
                else:
                    return Response({
                                'status': 'False', 'detail' : "OTP sending error. Please try after some time."
                            })

                return Response({
                    'status': True, 'detail': 'Otp has been sent successfully.'
                })
    else:
            return Response({
                'status': 'False', 'detail' : "I haven't received any phone number/e-mail. Please do a POST request."
            })

@api_view(["POST"])
@authentication_classes([])
@csrf_exempt
def ValidateOTP(request):
    '''
    If you have received otp, post a request with phone and that otp and you will be redirected to set the password
    
    '''

    
    phone = request.data.get('phone', False)
    if phone:
        username=phone
    else:
        username=request.data.get('email',False)
    otp_sent   = request.data.get('otp_sent', False)
    print(username,otp_sent)
    if username and otp_sent:
            old = PhoneOTP.objects.filter(username = username)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp) == str(otp_sent):
                    old.logged = True
                    old.save()

                    return Response({
                        'status' : True, 
                        'detail' : 'OTP matched, kindly proceed to save password'
                    })
                else:
                    return Response({
                        'status' : False, 
                        'detail' : 'OTP incorrect, please try again'
                    })
            else:
                return Response({
                    'status' : False,
                    'detail' : 'Phone/E-mail not recognised. Kindly request a new otp with this number/e-mail'
                })


    else:
            return Response({
                'status' : 'False',
                'detail' : 'Either phone/emaail or otp was not recieved in Post request'
            })

@api_view(["POST"])
@authentication_classes([])

@csrf_exempt
def Register(request):

    '''Takes phone and a password and creates a new user only if otp was verified and phone is new'''

    
    serializer1=RegisterSerializer(data=request.data)
    if serializer1.is_valid():
            phone=request.data.get('phone',False)
            val=0
            if phone:
                username=phone
            else:
                val=1
                username=request.data.get('email',False)
            password=request.data.get('password',False)
           
         
                
            if username and password:
                    username = str(username)
                    user = User.objects.filter(username = username)
                    if user.exists():
                        return Response({'status': False, 'detail': 'Phone Number/E-mail  already have hostelites associated. Kindly try forgot password'})
                    else:
                        old = PhoneOTP.objects.filter(username = username)
                        
                        if old.exists():
                            old = old.first()
                            if old.logged:
                                Temp_data = {'username': username, 'password': password }

                                serializer = CreateUserSerializer(data=Temp_data)
                                serializer.is_valid(raise_exception=True)
                                user = serializer.save()
                                user.save()
                        
                                if val==0:
                                    log_value='phone'
                                else:
                                    log_value='email'
                                name=request.data.get('Name',None)
                                email=request.data.get('email',None)
                                phone=request.data.get('phone',None)
                              
                                serializer1.is_valid()
                                if serializer1.validated_data['shopkeeper']:
                                    print(type(serializer1.validated_data['shopkeeper']))
                                    Token.objects.create(user=user)
                                    Shopkeeper.objects.create(user1=user,loggedin_with=log_value,Owner_name=name,email=email,phone=phone)
                                else:
                                   
                                    Customer.objects.create(user1=user,loggedin_with=log_value,Name=name,email=email,phone=phone)
                                    Token.objects.create(user=user)
                                old.delete()
                                return Response({
                                    'status' : True, 
                                    'detail' : 'Congrts, user has been created successfully.'
                                })

                            else:
                                return Response({
                                    'status': False,
                                    'detail': 'Your otp was not verified earlier. Please go back and verify otp'

                                })
                        else:
                            return Response({
                            'status' : False,
                            'detail' : 'Phone number/E-mail not recognised. Kindly request a new otp with this number/e-mail'
                        })
                            




            else:
                    return Response({
                        'status' : 'False',
                        'detail' : 'Either phone/e-mail or password was not recieved in Post request'
                    })
    else:
        return Response(serializer1.errors)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_exempt
def Login(request):
    
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
        
            user = serializer.validated_data['user']
            
            login(request, user)
    

            token = Token.objects.get(user=user)
            return Response(token.key)    
                
        else:
                return Response({
                    'status' : 'False',
                                'detail' : 'Incorrect credentials'

                })

@api_view(["POST","PUT"])

@csrf_exempt

def update_profile(request):

    if request.method=='PUT':
        username=request.user.username
        
        obj=Customer.objects.filter(user1__username=username)
       
        if len(obj)==1:
            obj1=Customer.objects.get(user1__username=username)
            serializer=CustomerSerializer(obj1,data=request.data,partial=True,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"Profile updated successfuly"})
        
            return Response(serializer.errors)
        else:
            obj1=Shopkeeper.objects.get(user1__username=username)
            serializer=ShopkeeperSerializer(obj1,data=request.data,partial=True,context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({"Profile updated successfuly"})
        
           
        
        return Response(serializer.errors)


@api_view(['GET'])
def get_restaurants(request,pk=False,name=False):
   
    if not pk:
        if name:
            restaurants=Shopkeeper.objects.filter(Restaurant_name=name)
        else:   
            restaurants=Shopkeeper.objects.all()
        
    else:
        restaurants=Shopkeeper.objects.filter(Category=pk)
    serializer=ShopkeeperSerializer(restaurants,many=True)
    return Response(serializer.data)


@api_view(["POST","PUT"])

@csrf_exempt

def add_items(request):
 
    if request.method=='POST':
        serializer=ItemSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            user1=Shopkeeper.objects.get(user1=request.user)
            Items.objects.create(user1=user1,Name=serializer.validated_data['Name'],
                Description=serializer.validated_data['Description'],Price=serializer.validated_data['Price'],Category=serializer.validated_data['Price'])
            return Response({"Item added successfully"})
        return Response(serializer.errors)

@api_view(['POST'])

def remove_item(request,pk):
    obj=Items.objects.get(id=pk)
    obj.delete()

@api_view(['GET'])

def get_items(request,pk=False,name=False,category=False):
   
        if pk and not name and not category:
            restaurant=Shopkeeper.objects.get(id=pk)

            li=Items.objects.filter(user1=restaurant)
    
        if pk and name and not category:
            restaurant=Shopkeeper.objects.get(id=pk)
         
            li=Items.objects.filter(Name=name).filter(user1=restaurant)
        if pk and not name and category:
            restaurant=Shopkeeper.objects.get(id=pk)
        
            li=Items.objects.filter(Category=category).filter(user1=restaurant)
        serializer=ItemSerializer(li,many=True)
        return Response(serializer.data)


@api_view(["POST","PUT"])

@csrf_exempt

def add_remove_favourite_restaurant(request,pk):
    restaurant=Shopkeeper.objects.get(id=pk)
    customer=Customer.objects.get(user1=request.user)
    if customer in restaurant.favourite_restaurants.all():
        restaurant.favourite_restaurants.remove(customer)
    else:
        restaurant.favourite_restaurants.add(customer)
    return Response({"Updated Successfully"})
    
    

@api_view(["POST","PUT"])

@csrf_exempt

def add_remove_favourite_item(request,pk):
    item=Items.objects.get(id=pk)
    customer=Customer.objects.get(user1=request.user)
    print(item,customer)
    if customer in item.favourite_items.all():
        item.favourite_items.remove(customer)
    else:
        item.favourite_items.add(customer)
    return Response({"Updated Successfully"})


@api_view(['GET'])

def user_favourite_restaurants(request):
    customer=Customer.objects.get(user1=request.user)
    user_favourites = Shopkeeper.objects.filter(favourite_restaurants=customer)
    serializer=ShopkeeperSerializer(user_favourites,many=True)
    return Response(serializer.data)


    
@api_view(['GET'])

def user_favourite_items(request):
    customer=Customer.objects.get(user1=request.user)
    user_favourites=Items.objects.filter(favourite_items=customer)
    serializer=ItemSerializer(user_favourites,many=True)
    return Response(serializer.data)


@api_view(['POST'])

def add_to_cart(request, pk):
    item = get_object_or_404(Items, pk=pk)
    customer=Customer.objects.get(user1=request.user)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=customer
    )
    order_qs = Order.objects.filter(user=customer)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity += 1
            order_item.save()
            return Response({"message": "Added quantity Item", },
                           
                            )
        else:
            order_item.quantity=1
            order_item.save()
            order.items.add(order_item)
            return Response({"message": " Item added to your cart", },
                        
                            )
    else:
        order = Order.objects.create(user=customer)
        order_item.quantity=1
        order_item.save()
        order.items.add(order_item)
       
        return Response({"message": "Item added to your cart", },
                      
                        )


@api_view(['POST'])
def remove_from_cart(request,pk):
    item = get_object_or_404(Items, pk=pk)
    customer=Customer.objects.get(user1=request.user)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=customer
    )
    order_qs = Order.objects.filter(user=customer)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            order_item.quantity -= 1
            order_item.save()
            if order_item.quantity==0:
                order.items.erase(order_item)
            return Response({"message": "Removed quantity Item", },
                            
                            )
        else:
            return Response({"message": " Item already removed!!", },
                          
                            )

@api_view(['POST'])

def request_order(request,pk):
    shopkeeper=Shopkeeper.objects.get(id=pk)
    customer=Customer.objects.get(user1=request.user)
    order=Order.objects.get(user=customer)
    
    instance=Shopkeeper_Order_History.objects.create(user=shopkeeper,customer=customer)
    instance.items.set(order.items.all())
    instance1=Customer_Order_History.objects.create(user=customer,shopkeeper=shopkeeper)
    instance1.items.set(order.items.all())
    order.delete()
    return Response({"Order requested!!"})

@api_view(['POST'])
def shopkeeper_accept(request,pk):
    obj=Shopkeeper_Order_History.objects.get(id=pk)
    obj.status=True
    obj.save()
    order=obj.order
    obj1=Customer_Order_History.objects.get(id=pk)
    obj1.status=True
    obj1.save()
    return Response({"Order accepted!!"})



@api_view(['POST'])
def shopkeeper_reject(request,pk):
    obj=Shopkeeper_Order_History.objects.get(id=pk)
    order=obj.order
    obj.delete()
    obj1=Customer_Order_History.objects.get(id=pk)
    obj1.delete()
    return Response({"Order cancelled!!"})



@api_view(['POST'])
def customer_reject(request,pk):
    obj=Customer_Order_History.objects.get(id=pk)
    order=obj.order
    obj.delete()
    obj1=Shopkeeper_Order_History.objects.get(id=pk)
    obj1.delete()
    return Response({"Order cancelled!!"})


@api_view(['GET'])
def shopkeeper_order_history(request):
    shopkeeper=Shopkeeper.objects.get(user1=request.user)
    obj=Shopkeeper_Order_History.objects.filter(user=shopkeeper)
    serializer=soh_serializer(obj,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def customer_order_history(request):
    customer=Customer.objects.get(user1=request.user)
    obj=Customer_Order_History.objects.filter(user=customer)
    serializer=coh_serializer(obj,many=True)
    return Response(serializer.data)

