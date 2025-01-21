from django.contrib import admin
from django.contrib.auth.models import User
from .models import Category,Customers,Orders,Products,Profile

# Register your models here.
admin.site.register(Category)
admin.site.register(Customers)
admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(Profile)

#Mix profile info & User Info
class ProfileInline(admin.StackedInline):
    model = Profile

#Extend User model
class UserAdmin(admin.ModelAdmin):
    model= User
    fields=["username","first_name","last_name","email"]
    inlines=[ProfileInline]

#Unregister The old way of User Model :
admin.site.unregister(User)

#Reregister User model  in new way :
admin.site.register(User,UserAdmin)