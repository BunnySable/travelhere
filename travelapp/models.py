from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Travel(models.Model):
    location = models.CharField(max_length=50)
    catagory = models.CharField(max_length=40)
    price = models.FloatField()
    transpotation = models.CharField(max_length=50)
    guide = models.CharField(max_length=50)
    details = models.CharField(max_length=100)
    imagepath = models.ImageField(upload_to='image',default='')

class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid')
    travelid = models.ForeignKey(Travel, on_delete=models.CASCADE,db_column='traveltid')
    quantity = models.IntegerField(default=1)

class Profile(models.Model):
    id=models.ForeignKey(User,on_delete=models.CASCADE,db_column='id',primary_key=True)
    mobile=models.CharField(max_length=10)
    address=models.TextField(max_length=100)

class Order(models.Model):
    orderid= models.CharField(max_length=50)
    userid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    travelid=models.ForeignKey(Travel,on_delete=models.CASCADE,db_column='travelid')
    quantity=models.IntegerField()

