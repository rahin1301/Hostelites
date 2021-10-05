from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
##from blissedmaths.utils import unique_otp_generator
# Create your models here


class PhoneOTP(models.Model):
    ##phone_regex = RegexValidator( regex   =r'^\+?1?\d{9,14}$', message ="Phone number must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    username       = models.CharField(max_length=17, unique=True,default="")
    otp         = models.CharField(max_length = 9, blank = True, null= True)
    count       = models.IntegerField(default = 0, help_text = 'Number of otp sent')
    logged      = models.BooleanField(default = False, help_text = 'If otp verification got successful')
    forgot      = models.BooleanField(default = False, help_text = 'only true for forgot password')
    forgot_logged = models.BooleanField(default = False, help_text = 'Only true if validdate otp forgot get successful')




class Customer(models.Model):
    user1=models.OneToOneField(User,on_delete=models.CASCADE)
    loggedin_with=models.CharField(max_length=10)
    Name=models.CharField(max_length=100)
    email=models.EmailField(blank=True,null=True)
    phone=models.CharField(max_length=17,blank=True,null=True)
    address=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.user1.username
  

class Shopkeeper(models.Model):
    user1= models.OneToOneField(User,on_delete=models.CASCADE)
    loggedin_with=models.CharField(max_length=10)
    Restaurant_name=models.CharField(max_length=100)
    Owner_name=models.CharField(max_length=100,blank=True,null=True)
    email=models.EmailField(blank=True,null=True)
    phone=models.CharField(max_length=17,blank=True,null=True)
    address=models.TextField(blank=True,null=True)
    Category=models.CharField(max_length=25,blank=True,null=True)
    favourite_restaurants=models.ManyToManyField(Customer,blank=True)


    def __str__(self):
        return self.user1.username


class Items(models.Model):
    user1=models.ForeignKey(Shopkeeper,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    Description=models.TextField()
    Price=models.IntegerField()
    Category=models.CharField(max_length=25,blank=True,null=True)
    favourite_items=models.ManyToManyField(Customer,blank=True)


class OrderItem(models.Model) :
    user = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True, blank=True)
    ##ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Items, on_delete=models.CASCADE,blank=True, null=True)
    quantity = models.IntegerField(default=1)


    # def __str__(self):
    #     return f"{self.quantity} of {self.item.name}"

class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE,null=True, blank=True)
    items = models.ManyToManyField(OrderItem,blank=True, null=True)
    # start_date = models.DateTimeField(auto_now_add=True)
    # ordered_date = models.DateTimeField()
    # ordered = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.user.email


class Shopkeeper_Order_History(models.Model):
        user=models.ForeignKey(Shopkeeper,on_delete=models.CASCADE,null=True,blank=True)
        ##order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
        customer=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
        items=models.ManyToManyField(OrderItem,blank=True,null=True)
        status=models.BooleanField(default=False)

class Customer_Order_History(models.Model):
        user=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
        ##order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True,blank=True)
        shopkeeper=models.ForeignKey(Shopkeeper,on_delete=models.CASCADE,null=True,blank=True)
        items=models.ManyToManyField(OrderItem,blank=True,null=True)
        status=models.BooleanField(default=False)




    

