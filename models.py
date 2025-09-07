from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY=(
    ('SO','SONATA'),
    ('KE','KENNETH COLE'),
    ('FA','FASTRACK'),
    ('TH','TOMMY HILFIGER'),
    ('PO','POLICE'),
    ('TI','TITAN'),
    ('AN','ANNE KLEIN'),
    ('ZO','ZOOP'),
    ('CA','CAOCH')

)

STATE_CHOICES = (
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhatisgarh','Chattisgarh'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujrat','Gujrat'),
    ('Haryana','Haryana'),
    ('HimachalPradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Punjab',"Punjab"),
    ('Rajasthan',"Rajasthan"),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttrakhand','Uttrakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal')
     )

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price= models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition =models.TextField(default="")
    prodapp= models.TextField(default="")
    category=models.CharField(choices=CATEGORY, max_length=50)
    product_image=models.ImageField(upload_to='products')
    def __str__(self):
        return self.title
    
class ContactUs(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField( max_length=254)
    message=models.TextField(default="")

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField( max_length=100)
    locality = models.CharField( max_length=100)
    city = models.CharField( max_length=50)
    mobile = models.IntegerField()
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    

STATUS_CHOICES = (
    ('Order placed','Order placed'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price