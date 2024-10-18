from django.contrib import admin
from travelapp.models import Travel, Cart, Order


# Register your models here.

class Traveladmin(admin.ModelAdmin):
    list_display=['location', 'catagory', 'price', 'transpotation', 'guide', 'details', 'imagepath']
    list_filter=['location','catagory','price','transpotation']

class CartAdmin(admin.ModelAdmin):
    list_display=['id','travelid','uid','quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display=['id','orderid','userid','travelid','quantity']



admin.site.register(Travel,Traveladmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Order,OrderAdmin)