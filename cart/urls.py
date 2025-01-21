from django.urls import path
from . import views

urlpatterns=[
    path('',views.CartSummary , name='cartsummary'),
    path('add/',views.CartAdd , name='cartadd'),
    path('update/',views.CartUpdate , name='cartupdate'),
    path('delete/',views.CartDelete , name='cartdelete'),
    ]