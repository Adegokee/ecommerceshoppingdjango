from django.contrib import admin
from .models import Cartegory

# Register your models here.
class CartegoryAdmin(admin.ModelAdmin):
    list_display=('cartegory_name', 'slug')
    prepopulated_fields={'slug': ['cartegory_name'],}
    
admin.site.register(Cartegory, CartegoryAdmin)


