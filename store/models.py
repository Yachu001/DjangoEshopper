from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import datetime

# Create your models here.
class Category(models.Model):
    name =models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    date_modified =models.DateTimeField(User,auto_now=True)
    phone =models.CharField(max_length=20,blank=True)
    adress1 =models.CharField(max_length=200,blank=True)
    adress2 =models.CharField(max_length=200,blank=True)
    city =models.CharField(max_length=200,blank=True)
    zipcode =models.CharField(max_length=10,blank=True)
    state =models.CharField(max_length=200,blank=True)
    country =models.CharField(max_length=200,blank=True)
    old_cart =models.CharField(max_length=200,blank=True,null=True)

    def __str__(self):
        return self.user.username
    
    #Create a user profile by default while user signup#
def create_profile(sender,instance,created,**kwargs):
    if created:
        user_profile =Profile(user=instance)
        user_profile.save()

    #Automate the Profile 
post_save.connect(create_profile,sender=User)
    
class Customers(models.Model):
    first_name =models.CharField(max_length=50)
    last_name =models.CharField(max_length=50)
    phone =models.CharField(max_length=20)
    email =models.EmailField()
    password =models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Products(models.Model):
    name =models.CharField(max_length=50)
    price =models.DecimalField(default=0, decimal_places=2,max_digits=6)
    category =models.ForeignKey(Category,on_delete=models.CASCADE, default=1)
    description =models.CharField(max_length=250,null=True,blank=True)
    image =models.ImageField(upload_to='products/',)

    on_sale =models.BooleanField(default=False)
    sale_price =models.DecimalField(default=0,decimal_places=2,max_digits=6)

    def __str__(self):
        return self.name
    
class Orders(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    customer =models.ForeignKey(Customers,on_delete=models.CASCADE)
    quantity =models.IntegerField(default=1)
    address =models.CharField(max_length=250, null=True,blank=True)
    phone =models.CharField(max_length=20,null=True,blank=True)
    date =models.DateField(default=datetime.datetime.today)
    status =models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product}"