from store.models import Products,Profile
class Cart():
    def __init__(self,request):
        self.session=request.session
        #Get Request (user)
        self.request = request
        #Get the current session key if it exists
        cart =self.session.get('session_key')
        #if user is new create one session key
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}

        self.cart=cart
    
    def db_add(self,product,quantity):
        product_id=str(product.id)
        product_qty =str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=int(product_qty)
        self.session.modified =True

        #Deal with Logged in User
        if self.request.user.is_authenticated:
            current_user =Profile.objects.filter(user__id =self.request.user.id)

        #{'?':?,'?':?} to {"?":?,"?":?}
            carty=str(self.cart)
            carty=carty.replace("\'","\"")
        #Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def add(self,product,quantity):
        product_id=str(product.id)
        product_qty =str(quantity)
        #logic
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id]=int(product_qty)
        self.session.modified =True

        #Deal with Logged in User
        if self.request.user.is_authenticated:
            current_user =Profile.objects.filter(user__id =self.request.user.id)

        #{'?':?,'?':?} to {"?":?,"?":?}
            carty=str(self.cart)
            carty=carty.replace("\'","\"")
        #Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        product_ids =self.cart.keys()
        #use IDs to Lookup Products in DataBase Model
        products =Products.objects.filter(id__in =product_ids)

        return products

    def get_quantity(self):
        quantities =self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id =str(product)
        product_qty =int(quantity)

        #get CART
        ourcart =self.cart

        #update CART
        ourcart[product_id]=product_qty
        self.session.modified =True
        #Deal with Logged in User
        if self.request.user.is_authenticated:
            current_user =Profile.objects.filter(user__id =self.request.user.id)

        #{'?':?,'?':?} to {"?":?,"?":?}
            carty=str(self.cart)
            carty=carty.replace("\'","\"")
        #Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
        thing = self.cart
        return thing
    
    def delete(self,product):
        product_id =str(product)

        #checking product is available
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified=True
        #Deal with Logged in User
        if self.request.user.is_authenticated:
            current_user =Profile.objects.filter(user__id =self.request.user.id)

        #{'?':?,'?':?} to {"?":?,"?":?}
            carty=str(self.cart)
            carty=carty.replace("\'","\"")
        #Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        #Get Products IDS
        product_ids =self.cart.keys()

        #Lookup those products in our DB model
        products =Products.objects.filter(id__in =product_ids)

        #Get Quantites
        quantities =self.cart

        #Declaring total
        total = 0

        for key,value in quantities.items():
            #Converting key into integer 
            key =int(key)
            for product in products:
                if product.id == key:
                    if product.on_sale:
                        total=total+(product.sale_price*value)
                    else:
                        total=total+(product.price*value)
        return total