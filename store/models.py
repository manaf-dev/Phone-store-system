from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    name = models.CharField('Name', max_length=225)
    address = models.CharField('Address', max_length=255)
    phone = models.CharField('Phone Number', max_length=20)
    gender = models.CharField('Gender', max_length=10)


    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
    

class PaymentMode(models.Model):
    mode = models.CharField("Payment Method", max_length=30)

    def __str__(self):
        return self.mode
    

class Invoice(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    pay_mode = models.ForeignKey(PaymentMode, on_delete=models.PROTECT, related_name='paymode')
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    comment = models.CharField(max_length=255, default='No exceptions.')

    def __str__(self):
        return self.comment



class Order(models.Model):
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customers')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True, related_name='invoices')

    @classmethod
    def create_order(cls, invoice_id, customer):
        order = cls(date=timezone.now(), customer=customer, invoice_id=invoice_id)
        order.save()
        
    
    def __str__(self):
        return 'Order placed'


class Product(models.Model):
    productid = models.IntegerField(primary_key=True)
    name = models.CharField('Product name', max_length=255)
    price = models.DecimalField('Price of the item', max_digits=10, decimal_places=2)
    type = models.CharField('Product type', max_length=50)
    brand = models.CharField('Brand', max_length=50)
    quantityInStock = models.IntegerField()

    @classmethod
    def update_stock(cls, quantity):
        cls.quantityInStock = cls.quantityInStock - quantity
        
    
    def __str__(self):
        return f'{self.name} added to stock'


class OrderDetail(models.Model):
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    productID = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['orderID', 'productID'], name='unique_order')
        ]