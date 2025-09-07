from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import   Product,ContactUs,Customer,Cart,OrderPlaced,Payment
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from base_app.forms import CustomerRegistrationForm,CustomerProfileForm
from django.db.models import Q
import razorpay
from django.conf import settings


# Create your views here.


def home(request):
    return render(request,'home.html')

def About(request):
    return render(request,'about.html')



def Contact(request):
    return render(request,'contact.html')

def ContactSave(request):
    n=''
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        ap=ContactUs(name=name,email=email,message=message)
        ap.save()
        n='THANKU FOR YOUR FEEDBACK'
        return render(request,"contact.html",{'n':n})



class CategoryView(View):
    def get(self,request,val):
        product=Product.objects.filter(category=val)
        return render(request,"category.html",locals())
    
class ProductDetail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,"productdetail.html",locals())
    
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'registration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm( request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"congratulations! User Registration Succcesfully")
        else:
            messages.error(request,"Invalid Input Data")
        return render(request,"registration.html",locals())

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,"profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,city=city,locality=locality,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulation! Profile saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")

        return render(request,"profile.html",locals())

    
# def address(request):
#     add=Customer.objects.filter(user = request.user)
#     return render(request,"address.html",locals())

# class UpdateAddress(View):
#     def get(self,request,pk):
#         add= Customer.objects.get(pk=pk)
#         form=CustomerProfileForm(instance=add)
#         return render(request,"Updateaddress.html",locals())
#     def post(self,request,pk):
#         form=CustomerProfileForm(request.POST)
#         if form.is_valid():
#             add = Customer.objects.get(pk=pk)
#             add.name = form.cleaned_data['name']
#             add.locality = form.cleaned_data['locality']
#             add.city = form.cleaned_data['city']
#             add.mobile = form.cleaned_data['mobile']
#             add.state = form.cleaned_data['state']
#             add.zipcode = form.cleaned_data['zipcode']
#             add.save()
#             messages.success(request,"Congratulations! Profile Update successfully")
#         else:
#             messages.warning(request,"Invalid Input Data")
#         return redirect("address")

class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,"profile.html",locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user,name=name,city=city,locality=locality,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulation! Profile saved Successfully")
        else:
            messages.warning(request,"Invalid Input Data")

        return render(request,"profile.html",locals())
    
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request,"address.html",locals())

class UpdateAddress(View):
    def get(self,request,pk):
        add= Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request,"Updateaddress.html",locals())
    def post(self,request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Update successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("/address/")
    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 550
    return render(request,'addtocart.html',locals())

def plus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 50
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 50
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == "GET":
        prod_id=request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 50
        data = {
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
class Checkout(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_OCH2eMzzCjjQcm', 'entity': 'order', 'amount': 504000, 'amount_paid': 0, 'amount_due': 504000, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1716104576}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request,'checkout.html',locals())

    def post(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 40
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency":"INR","receipt":"order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request,'checkout.html',locals())

def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    # print("payment_done":oil = ",order_id," pid = ",payment_id," cid = ",cust_id")
    user = request.user
    # return redirect("orders")
    customer = Customer.objects.get(id=cust_id)
     # To update payment status and payment id
    payment = Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    # To save order details
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()    