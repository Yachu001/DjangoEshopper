from django.shortcuts import render,get_object_or_404
from store.models import Products
from .cart import Cart
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def CartSummary(request):
    cart =Cart(request)
    cart_products =cart.get_products
    quantities =cart.get_quantity
    total =cart.cart_total
    return render(request,'summary.html',{"cart_products":cart_products,"quantities":quantities,"total":total})

def CartAdd(request):
    #Get the cart
    cart =Cart(request)

    #Test for POST
    if request.POST.get('action')=='post':
        #get stuffs
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        #lookup product in DataBase
        product =get_object_or_404(Products,id=product_id)
        #save to Session
        cart.add(product=product,quantity=product_qty)
        #get cart Quantity
        cart_quantity =cart.__len__()
        #return response
        #response=JsonResponse({'product name':product.name})
        response=JsonResponse({'qty':cart_quantity})
        messages.success(request,("Item added to cart Successfully!!!"))
        return response

def CartUpdate(request,):
    #Get the cart
    cart =Cart(request)

    #Test for POST
    if request.POST.get('action')=='post':
        #get stuffs
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id,quantity=product_qty)
        response =JsonResponse({'qty':product_qty})
        messages.success(request,("Cart Updated Successfully!!!"))
        return response

def CartDelete(request):
    #GET the Cart
    cart=Cart(request)

    #Test For POST
    product_id =int(request.POST.get('product_id'))
    cart.delete(product=product_id)

    response=JsonResponse({'product':product_id})
    messages.success(request,("Item removed from Cart"))
    return response
