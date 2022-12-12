from django.shortcuts import render, redirect
from .forms import RegistrationForms
from .models import Account
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from cart.models import Cart, CartItem
from cart.views import _cart_id
# Create your views here.
import requests

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage




def register(request):
    if request.method == 'POST':
        forms = RegistrationForms(request.POST)
        if forms.is_valid():
            first_name= forms.cleaned_data['first_name']
            last_name= forms.cleaned_data['last_name']
            email= forms.cleaned_data['email']
            phone_number= forms.cleaned_data['phone_number']
            password= forms.cleaned_data['password']
            username=email.split('@')[0]
            
            user=Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number=phone_number
            user.save()
            # current_site
            current_site=get_current_site(request)
            mail_subject='Please acivate your account'
            message=render_to_string('accounts/account_verification_email.html',{
                'user': user,
                'domain': current_site, 
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email=email
            send_email= EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for signing up, please proceed to you email to comfirm the link by clicking. Thank')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        forms= RegistrationForms()
    context={'forms': forms}
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email= request.POST['email']
        password= request.POST['password']
        user=auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist=CartItem.objects.filter(cart=cart)
                if is_cart_item_exist:
                    cart_items=CartItem.objects.filter(cart=cart)
                    product_variation=[]
                    for item in cart_items:
                        variation=item.variations.all()
                        product_variation.append(list(variation))
                    cart_items=CartItem.objects.filter(user=user)
                    existing_variation_list=[]
                    id=[]
                    for item in cart_items:
                        existing_variation=item.variations.all()
                        existing_variation_list.append(list(existing_variation))
                        id.append(item.id)
                    for product in product_variation:
                        if product in existing_variation_list:
                            index=existing_variation_list.index(product)
                            item_id=id[index]
                            item=CartItem.objects.get(id=item_id) 
                            item.quantity+=1
                            item.user=user
                            item.save()
                        
                        else:
                            cart_items=CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user=user
                                item.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'Login Successful')
            url= request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                print('query =>', query)
                params=dict(x.split('=')for x in query.split('&'))
                if 'next' in params:
                    nextpage=params['next']
                    return redirect(nextpage)
                print('params =>', params)
                print('-------')  
            except:
                return redirect('dashboard')  
            # url=request.META.get('HTTP_RERERER')
            # try:
            #     query=requests.utils.urlparse(url).query
            #     print('query =>',query)
            #     print('------')
            #     params=dict(x.split('=')for x in query.split('&'))
            #     if 'next' in params:
            #         nextpage=params['next']
            #         return redirect(nextpage)
                
            # except:
            #     return redirect('dashboard') 
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
           
    return render(request, 'accounts/login.html')

login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('login')


def activate(request, uidb64, token):
    
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError, Account.DoesNotExist):
        user=None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(request, 'Congratulations! You have successfully activated your account')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
    
def forgotpassword(request):
    if request.method == 'POST':
        email= request.POST['email']
        if Account.objects.filter(email=email).exists():
            user= Account.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject='Reset your password'
            message=render_to_string('accounts/reset_password_email.html',{
                'user': user,
                'domain': current_site, 
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email=email
            send_email= EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Reset Password email sent successfully')
            return redirect('login') 
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError, Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid']=uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'Expired link credentials')
        return redirect('login')
        
  
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid=request.session.get('uid')
            user= Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        
        else:
            messages.error(request, 'Password does not match')
            return redirect('resetpassword')
    else:
        
        return render(request, 'accounts/resetpassword.html')