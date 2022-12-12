from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.
def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request, product_id):
    current_user=request.user
    product=Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation=[]
        if request.method == 'POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                # print(key, value)
                try:
                    variation=Variation.objects.get(product=product, variation_cartegory__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except: 
                    pass 
        # try:
        #     cart=Cart.objects.get(cart_id=_cart_id(request))
        # except Cart.DoesNotExist:
        #     cart=Cart.objects.create(
        #         cart_id=_cart_id(request)
        #     )
        # cart.save()
        is_cart_item_exist=CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exist:
            cart_items=CartItem.objects.filter(user=current_user, product=product)
            #exixting variations database
            #current variations product_variation
            #item_id database
            existing_variation_list=[]
            id=[]
            for item in cart_items:
                existing_variation=item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            # print(existing_variation_list)
            # increase the cart_items quantity
            if product_variation in existing_variation_list:
                index=existing_variation_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product, id=item_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(product=product, user=current_user,quantity=1)
                if len(product_variation) > 0:
                    item.variations.clear()
                    # for item in product_variation:
                    item.variations.add(*product_variation)
                # cart_items.quantity+=1
                item.save()
        else:
            cart_items=CartItem.objects.create(
                user=current_user, 
                product=product, 
                quantity=1
            )
            if len(product_variation) > 0:
                cart_items.variations.clear()
                # for item in product_variation:
                cart_items.variations.add(*product_variation)
            cart_items.save()
        return redirect('cart')
    #if user is not authenticated
    else:
        product_variation=[]
        if request.method == 'POST':
            for item in request.POST:
                key=item
                value=request.POST[key]
                # print(key, value)
                try:
                    variation=Variation.objects.get(product=product, variation_cartegory__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                except: 
                    pass 
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(
                cart_id=_cart_id(request)
            )
        cart.save()
        is_cart_item_exist=CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exist:
            cart_items=CartItem.objects.filter(cart=cart, product=product)
            #exixting variations database
            #current variations product_variation
            #item_id database
            existing_variation_list=[]
            id=[]
            for item in cart_items:
                existing_variation=item.variations.all()
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            # print(existing_variation_list)
            # increase the cart_items quantity
            if product_variation in existing_variation_list:
                index=existing_variation_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(product=product, id=item_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(product=product, cart=cart,quantity=1)
                if len(product_variation) > 0:
                    item.variations.clear()
                    # for item in product_variation:
                    item.variations.add(*product_variation)
                # cart_items.quantity+=1
                item.save()
        else:
            cart_items=CartItem.objects.create(
                cart=cart, 
                product=product, 
                quantity=1
            )
            if len(product_variation) > 0:
                cart_items.variations.clear()
                # for item in product_variation:
                cart_items.variations.add(*product_variation)
            cart_items.save()
        return redirect('cart')
    


def cart(request, total=0, quantity=0, cart_items=None):
    
    try:
        tax=0
        grand_total=0
        
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user, is_active=True)
        
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax=(total * 2)/100
            grand_total=(total + tax)
    except ObjectDoesNotExist:
        pass
    
    context={'total': total, 'quantity': quantity, 'cart_items': cart_items, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'store/cart.html', context)


def minusCart(request, product_id, cart_item_id):
    product=get_object_or_404(Product, id=product_id)
    
        
   
    try:
        if request.user.is_authenticated:
            cart_items= CartItem.objects.get(user=request.user, product=product, id=cart_item_id)
        else:
            cart= Cart.objects.get(cart_id=_cart_id(request))
            cart_items= CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
        if cart_items.quantity > 1:
            cart_items.quantity -= 1
            cart_items.save()
        else:
            cart_items.delete()
    except:
        pass
    return redirect('cart')

def removeCart(request, product_id, cart_item_id):
    product=get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_items= CartItem.objects.filter(user=request.user, product=product, id=cart_item_id)
    else:    
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items= CartItem.objects.filter(cart=cart, product=product, id=cart_item_id)
    cart_items.delete()
    return redirect('cart')



@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax=0
        grand_total=0
      
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
            tax=(total * 2)/100
            grand_total=(total + tax)
    except ObjectDoesNotExist:
        pass
    
    context={'total': total, 'quantity': quantity, 'cart_items': cart_items, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'store/checkout.html', context)