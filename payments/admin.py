from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem

# Register your models here.
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#Creating an orderitem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#Extending our order model
class OrderAdmin(admin.ModelAdmin):
    model =Order
    inlines = [OrderItemInline]
    readonly_fields = ["date_ordered"]

#unregistering old order model
admin.site.unregister(Order)

#Re registering order & registering OrderAdmin Models
admin.site.register(Order,OrderAdmin)


