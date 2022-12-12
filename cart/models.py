from django.db import models
from store.models import Product, Variation
from accounts.models import Account


# Create your models here.
class Cart(models.Model):
    cart_id= models.CharField(max_length=100)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    
    
class CartItem(models.Model):
    user= models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
   
    quantity=models.IntegerField()
    variations=models.ManyToManyField(Variation, blank=True)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __unicode__(self):
        return self.product



