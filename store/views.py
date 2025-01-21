from django.shortcuts import render,redirect
from .models import Products,Category,Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
from .forms import signup_form, user_update_form, user_password_update_form,user_info_form
import json
from cart.cart import Cart
#Payments App
from payments.forms import shipping_address_form
from payments.models import ShippingAddress
# Create your views here.

def home(request):
    products =Products.objects.all()
    return render(request,'home.html',{'products':products})


def about(request):
    return render(request,'about.html')

def login_user(request):
    if request.method =="POST":
        username =request.POST['username']
        password =request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            #Shopping cart items getting
            current_user = Profile.objects.get(user__id =request.user.id)
            #Get the user saved cart from DB
            saved_cart =current_user.old_cart
            #Convert old_cart string data to py Dict
            if saved_cart:
                try:
                    converted_cart =json.loads(saved_cart)
                    #adding cart dicts to session
                    cart =Cart(request)
                    #looping trough the cart and adding items to sessions
                    for key,value in converted_cart.items():
                        cart.db_add(product=key,quantity=value)
                except json.JSONDecodeError: 
                    # Handle the error, e.g., log it or return an error response 
                    converted_cart = {}


            messages.success(request,("User Login Successful!!"))
            return redirect('home')
        else:
            messages.error(request,("Something went wrong!!"))
            return redirect('login')
            
    
    else:
        return render(request,'login.html')
    
def logout_user(request):
    logout(request)
    messages.success(request,("User Logout Successful!!"))
    return redirect('login')

def signup_user(request):
    form = signup_form()
    if request.method =="POST":
        form =signup_form(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("User Registered Successfully"))
            return redirect('update_info')
        else:
            messages.error(request,("User Registration Failed Please Try Again"))
            return redirect('signup')
    else:
        messages.success(request,"Moonji")
        return render(request,'signup.html',{'form':form})
    
def product_page(request,pk):
    product =Products.objects.get(id=pk)
    return render(request,'product.html',{'product':product})

def category(request,foo):
    #foo = foo.replace('-',' ')
    foo = foo
    try:
        cat =Category.objects.get(name=foo)
        products=Products.objects.filter(category=cat)
        return render(request,'category.html',{'cat':cat,'products':products})
    except:
        messages.success(request,("The Category doesn't exist!!!"))
        return redirect('category_summary')
    
def category_summary(request):
    category=Category.objects.all()
    return render(request,'categorysummary.html',{'category':category})

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form =user_update_form(request.POST or None, instance= current_user)

        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,'user updated')
            return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form})
    else:
        messages.success(request,"you must need to be logged")
        return redirect('home')
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form =user_password_update_form(current_user,request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Your Password Has Been Updated!!!")
                login(request,current_user)
                return redirect('update_user')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
                    return redirect('update_password')
        else:
            form =user_password_update_form(current_user)
            return render(request,'update_password.html',{'form':form})
    else:
        messages.success(request,"You must be Logged in to update password")
        return redirect('home')

def update_info(request):
    if request.user.is_authenticated:
        # Get user 
        current_user =Profile.objects.get(user__id =request.user.id)
        # Get user Shipping Address info
        shipping_info = ShippingAddress.objects.get(user__id =request.user.id)
        #Get user billing address form
        form =user_info_form(request.POST or None, instance= current_user)
        #Get user Shipping Address Form
        ship_form =shipping_address_form(request.POST or None, instance=shipping_info)
        if form.is_valid() or ship_form.is_valid():
            #saving billing address form
            form.save()
            #saving Shipping address form
            ship_form.save()
            messages.success(request,"User info updated succesfully!!!!!")
            return redirect('home')
        return render(request,"update_info.html",{'form':form,'ship_form':ship_form})
    else:
        messages.success(request,"You Must be Logged In to Access this!!!!!")
        return redirect('home')
    
def search_products(request):
    if request.method == "POST":
        searched =request.POST["searched"]
        #Query the Products DB Model
        search =Products.objects.filter(Q(name__icontains =searched) | Q(description__icontains = searched))
        if not search:
            messages.success(request,"The Product does not exist. Please try again!!!")
            return render(request,'search.html',{})
        else:
            return render(request,'search.html',{'search':search})
    else:
        return render(request,'search.html',{})
