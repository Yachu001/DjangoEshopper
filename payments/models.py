from django.db import models
from django.contrib.auth.models import User
from store.models import Products
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import datetime

# Create your models here.
class ShippingAddress(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    shipping_full_name =models.CharField(max_length=200)
    shipping_email =models.CharField(max_length=200)
    shipping_address1 =models.CharField(max_length=200)
    shipping_address2 =models.CharField(max_length=200)
    shipping_city =models.CharField(max_length=200)
    shipping_zipcode =models.CharField(max_length=10)
    shipping_state =models.CharField(max_length=200)
    shipping_country =models.CharField(max_length=200)

    #Prevent Name Pluralizing
    class Meta:
        verbose_name_plural ="ShippingAddress"
    
    def __str__(self):
        return f'ShippingAddress -{str(self.id)}'

#Create A Shipping Address by default when a user signup    
def ShipAddressCreate(sender,instance,created,**kwargs):
    if created:
        ship_address=ShippingAddress(user=instance)
        ship_address.save()
#Automate the Shipping Address Creation
post_save.connect(ShipAddressCreate,sender=User)
    
class Order(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    full_name =models.CharField(max_length=200)
    email =models.EmailField(max_length=200)
    shipping_address =models.TextField()
    amount_paid =models.DecimalField(max_digits=10,decimal_places=2)
    date_ordered =models.DateField(auto_now_add=True)
    shipped =models.BooleanField(default=False)
    date_shipped = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f'Order - {str(self.id)}'
#Auto Add Shipping Date & Time    
@receiver(pre_save,sender=Order)
def set_shipping_date_on_update(sender,instance,**kwargs):
    if instance.pk:
        now =datetime.datetime.now()
        obj =sender._default_manager.get(pk=instance.pk)
        if instance.shipped and not obj.shipped:
            instance.date_shipped =now


class OrderItem(models.Model):
    order =models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    product =models.ForeignKey(Products,on_delete=models.CASCADE,null=True)
    user =models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    quantity =models.PositiveBigIntegerField(default=1)
    price =models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'
    
