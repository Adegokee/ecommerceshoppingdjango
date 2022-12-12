from django.db import models
from cartegory.models import Cartegory
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name= models.CharField(max_length=200)
    slug= models.CharField(max_length=100)
    price= models.IntegerField()
    stock=models.IntegerField()
    description= models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    modify_date=models.DateTimeField(auto_now=True)
    is_available=models.BooleanField(default=True)
    images=models.ImageField(upload_to='photos/products')
    cartegory=models.ForeignKey(Cartegory, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('product_details', args=[self.cartegory.slug, self.slug])
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_cartegory='color', is_active=True)
    
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_cartegory='size', is_active=True)
    
variation_cartegory_choice=(
    ('color', 'color'),
    ('size', 'size'),
)
    

class Variation(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_cartegory=models.CharField(max_length=100, choices=variation_cartegory_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now_add=True)
    
    objects=VariationManager()
    
    def __str__(self):
        return self.variation_value
    
    
    