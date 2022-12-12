from django.db import models
from django.urls import reverse

# Create your models here.
class Cartegory(models.Model):
    cartegory_name= models.CharField(max_length=100, unique=True)
    slug= models.SlugField(max_length=100, unique=True)
    description= models.TextField()
    cart_image= models.ImageField(upload_to='photos/cartegories')
    
    class Meta:
        verbose_name ='Cartegory'
        verbose_name_plural ='Cartegories'
    def get_url(self):
        return reverse('product_by_cartegory', args=[self.slug])
    
    def __str__(self):
        return self.cartegory_name
    
