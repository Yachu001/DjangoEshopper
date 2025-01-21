from django.shortcuts import render,redirect
from django.contrib import messages
from cart.cart import Cart
from .forms import shipping_address_form, PaymentForm
from .models import ShippingAddress,Order,OrderItem
from store.models import Products,Profile
from cart import cart
import datetime

# Create your views here.
def process_order(request):
    if request.POST:
        #Get The Cart
        cart =Cart(request)
        cart_products =cart.get_products
        quantities =cart.get_quantity
        total =cart.cart_total()

        #get billing info from last page
        payment_form=PaymentForm(request.POST or None)
        #Get shipping session datas
        my_shipping =request.session.get('my_shipping')
        #Gather Info for order
        full_name =my_shipping['shipping_full_name']
        email=my_shipping['shipping_email']
        shipping_address=f"{my_shipping['shipping_full_name']}\n{my_shipping['shipping_email']}\n{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_country']}"
        amount_paid=total
        #Order Creation for logged users
        if request.user.is_authenticated:
            user=request.user
            order_creation=Order(user=user,full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            order_creation.save()
            #add order items
            #Get the order id
            order_id =order_creation.pk
            #Get products info
            for product in cart_products():
                #Get product ID
                product_id = product.id
                #Get product price
                if product.on_sale:
                    price =product.sale_price
                else:
                    price =product.price
                    #Get Quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #Create Order item
                        Create_order_item =OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price)
                        Create_order_item.save()
            #Delete our Cart after order confirm
            for key in list(request.session.keys()):
                if key == "session_key":
                    #Delete the keys
                    del request.session[key]
            #Delete old cart after order proccessed from DB {Profile.Old_cart }
            current_user=Profile.objects.filter(user__id =request.user.id)
            current_user.update(old_cart="")
            messages.success(request,"Order Placed Successfully!!!")
            return redirect('home')
        else:
            user=request.user
            order_creation=Order(full_name=full_name,email=email,shipping_address=shipping_address,amount_paid=amount_paid)
            order_creation.save()
            #add order items
            #Get the order id
            order_id =order_creation.pk
            #Get products info
            for product in cart_products():
                #Get product ID
                product_id = product.id
                #Get product price
                if product.on_sale:
                    price =product.sale_price
                else:
                    price =product.price
                    #Get Quantity
                for key,value in quantities().items():
                    if int(key) == product.id:
                        #Create Order item
                        Create_order_item =OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price)
                        Create_order_item.save()
            #Delete our Cart after order confirm
            for key in list(request.session.keys()):
                if key == "session_key":
                    #Delete the keys
                    del request.session[key]
                            
            messages.success(request,"Order Placed Successfully!!!")
            return redirect('home')

    else:
        messages.success(request,"Access denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        #Get The Cart
        cart =Cart(request)
        cart_products =cart.get_products
        quantities =cart.get_quantity
        total =cart.cart_total

        #create a session with shipping info
        my_shipping=request.POST
        request.session['my_shipping']=my_shipping
        #Checking The User Is Logged In
        if request.user.is_authenticated:
            #Get The billing form
            billing_form =PaymentForm()
            return render(request,'billing_info.html',{"cart_products":cart_products,"quantities":quantities,"total":total,'ship_info':request.POST,'billing_form':billing_form})
        else:
            #if user is not logged 
            #Get The billing form
            billing_form =PaymentForm()
            return render(request,'billing_info.html',{"cart_products":cart_products,"quantities":quantities,"total":total,'ship_info':request.POST,'billing_form':billing_form})
        

        
        shipping_form = request.POST
        return render(request,'billing_info.html',{"cart_products":cart_products,"quantities":quantities,"total":total,'ship_form':shipping_form})
    else:
        messages.success(request,"Access denied")
        return redirect('home')

def payment_success(request):
    return render(request,'payment_success.html',{})

def checkout(request):
    cart =Cart(request)
    cart_products =cart.get_products
    quantities =cart.get_quantity
    total =cart.cart_total
    #For Logged Users
    if request.user.is_authenticated:
        #Getting User
        ship_user =ShippingAddress.objects.get(user__id =request.user.id)
        ship_form =shipping_address_form(request.POST or None,instance=ship_user)
        return render(request,'checkout.html',{"cart_products":cart_products,"quantities":quantities,"total":total,'ship_form':ship_form})
    #For guest users
    else:
        ship_form =shipping_address_form(request.POST or None)
        return render(request,'checkout.html',{"cart_products":cart_products,"quantities":quantities,"total":total,'ship_form':ship_form})
    
def shipped_dash(request):
    #Checking the user is logged & is admin
    if request.user.is_authenticated and request.user.is_superuser:
        #Getting the shipped orders list
        orders =Order.objects.filter(shipped=True)
        if request.POST:
            status =request.POST['shipping_status']
            num =request.POST['num']
            order =Order.objects.filter(id=num)
            now =datetime.datetime.now()
            order.update(shipped=False)
            messages.success(request,"Order Unshipped Successfully!!")


        return render(request,'shipped_dash.html',{"orders":orders})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')
    
def not_shipped_dash(request):
    #Checking the user is logged & is admin
    if request.user.is_authenticated and request.user.is_superuser:
        #Getting the non-shipped orders list
        orders =Order.objects.filter(shipped=False)
        if request.POST:
            status =request.POST['shipping_status']
            num =request.POST['num']
            order =Order.objects.filter(id=num)
            now =datetime.datetime.now()
            order.update(shipped=True,date_shipped=now)
            messages.success(request,"Order shipped Successfully!!")
        return render(request,'not_shipped_dash.html',{"orders":orders})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')
    
def orders(request,pk):
    #Checking the user is logged & is admin
    if request.user.is_authenticated and request.user.is_superuser:
        #Get the order
        order =Order.objects.get(id=pk)
        #Get the order items
        items =OrderItem.objects.filter(order=pk)
        if request.POST:
            status =request.POST['shipping_status']
            #Check Shipping status true or false
            if status == "true":
                order=Order.objects.filter(id=pk)
                now =datetime.datetime.now()
                order.update(shipped = True,date_shipped=now)
            else:
                order =Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request,"Order Shipping Status Updated")
            return redirect('home')

        return render(request,'orders.html',{'order':order,'items':items})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')