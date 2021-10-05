from django.contrib import admin
from account.models import PhoneOTP,Customer,Shopkeeper,Items,OrderItem,Order,Shopkeeper_Order_History,Customer_Order_History

admin.site.register(PhoneOTP)
admin.site.register(Customer)
##admin.site.register(Shopkeeper)
admin.site.register(Items)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Shopkeeper_Order_History)
admin.site.register(Customer_Order_History)


class ShopkeeperAdmin(admin.ModelAdmin):
    list_display=['id','user1']
admin.site.register(Shopkeeper,ShopkeeperAdmin)
##from account.models import User
# Register your models here.


# class UserAdmin(admin.ModelAdmin):
#     list_display=['Name','username']

# admin.site.register(User,UserAdmin)