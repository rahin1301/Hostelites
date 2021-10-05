"""food_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account import views
from rest_framework.authtoken.views import obtain_auth_token 
urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api-tokn-auth'),
    path('admin/', admin.site.urls),
    #3rd
    path('register',views.Register),
    ##1st 
    path('validatephonesendotp',views.ValidatePhoneSendOTP),
    #2nd
    path('validateotp',views.ValidateOTP),
    path('login',views.Login),
    ##to get restaurant by cousines
    path('get_restaurants/<slug:pk>/',views.get_restaurants),
    ## to get restaurant by name
    path('get_restaurant_byname/<slug:name>/',views.get_restaurants),
    ##to get all restaurants
    path('get_restaurants',views.get_restaurants),
    path('update_profile',views.update_profile),


    path('add_items',views.add_items),
    path('remove_item/<int:pk>',views.remove_item),
    ## gets items in a restaurant
    path('get_items/<int:pk>/',views.get_items),
    #restaurant/category
    path('get_items_bycategory/<int:pk>/<slug:category>/',views.get_items),
    ##restaurant/name
    path('get_items_byname/<int:pk>/<slug:name>/',views.get_items),
    ##add remove fav 
    path('favourite_restaurant/<int:pk>',views.add_remove_favourite_restaurant),
    path('favourite_items/<int:pk>',views.add_remove_favourite_item),
    ##get fav
    path('get_fav_restaurant',views.user_favourite_restaurants),
    path('get_fav_items',views.user_favourite_items),
    path('add_to_cart/<int:pk>',views.add_to_cart),
    path('request_order/<int:pk>',views.request_order),
    path('shopkeeper_accept/<int:pk>',views.shopkeeper_accept),
     path('shopkeeper_reject/<int:pk>',views.shopkeeper_reject),
      path('customer_reject/<int:pk>',views.customer_reject),
    path('shopkeeper_order_history',views.shopkeeper_order_history),
    path('customer_order_history',views.customer_order_history)
]

###http POST http://localhost:8000/api-token-auth/ username='969' password="abcd1234@"