from django.contrib import admin
from .models import Product,ContactUs,Customer,Cart,Payment,OrderPlaced
# Register your models here.


@admin.register(Product)
class   ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'selling_price', 'discounted_price','description','composition','product_image')

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']

@admin.register(ContactUs)
class   ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','message')  


@admin.register(Cart)
class   CartAdmin(admin.ModelAdmin):
    list_display = ('user','product','quantity') 



# admin.site.register(Product,ProductAdmin)
# admin.site.register(ContactUs,ContactAdmin)
# admin.site.register(Customer)
# admin.site.register(Cart,CartAdmin)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']

@admin.register(OrderPlaced)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','product','quantity','customer','ordered_date','status','payment']