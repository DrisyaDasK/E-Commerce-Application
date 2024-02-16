from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    Category_name = models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return self.Category_name
class Products(models.Model):
    product_name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    images=models.ImageField(upload_to='image',null=True)
    description=models.CharField(max_length=100)
    def  __str__(self):
        return self.product_name
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    product=models.ForeignKey(Products,on_delete=models.CASCADE) 
    # User import from auth .model
    quantity=models.PositiveIntegerField(default=1)
    # quantity no.of set to defaultly 1
    options=(
                ('in-cart','in cart'),
                ( 'cancelled' , 'cancelled'),
                ( 'oredr-placed' , 'oredr-placed'),

    )
    # options set ina  dictionary(key value format)  1st value here key and 2nd its value
    status=models.CharField(max_length=100,choices=options,default='in-cart')
    # here status means charfield and  choices means the option which we given above and choice defualtly in-cart


class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart= models.ForeignKey(Cart,on_delete=models.CASCADE)
    order_date= models.DateTimeField(auto_now_add=True)
    address=models.TextField(max_length=255)
    email=models.EmailField()
    options=(
            ('oredr-placed' , 'oredr-placed'),
            ( 'cancelled' , 'cancelled'),
            ('dispatch','dispatch'),
            ( 'delivered' , 'delivered')


    )
    status=models.CharField(max_length=100,choices=options,default='order-placed')