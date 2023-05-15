from django.shortcuts import render, redirect, get_object_or_404

import orders
# import requests

from orders.models import Address, Order, OrderProduct
from .forms import AddressForm, CustomUserForm, UserForm, UserProfileForm
from .models import CustomUser, UserProfile
from orders.models import Order
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import smtplib
# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from datetime import timedelta
from datetime import date


def register(request):
    if request.method == 'POST':

        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        phone = request.POST['phone']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        user = CustomUser.objects.create_user(
            first_name=first_name, last_name=last_name, phone=phone, email=email, password=password1)
        messages.success(request, 'Registeratiion successfull')
        current_site = get_current_site(request)
        mail_subject = 'please activate your account'
        messsage = render_to_string('accounts/account_verification_email.html', {
            'user': user,
            'domin': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        to_email = email
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login('anaghaponnore2000@gmail.com', 'ijrwxatoqswbbywd')
        smtp_server.sendmail('anaghaponnore2000@gmail.com', to_email, messsage)
        user.save()
        # messages.success(request, 'Thank you for registering with us. we have sent you a verifiation email to your email address.please verify it.')
        return redirect('/accounts/login/?command=verification&email='+email)

    return render(request, 'accounts/register.html')


def login(request):
    if 'email' in request.session:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(
                        cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)

                        # getting the product variations by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        # get the cart items from the user to access his product variations
                        cart_item = CartItem.objects.filter(user=user)

                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                        # product_variation=[1,2,3,4,6]
                        # ex_var_list=[4,6,3,5]

                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()

                except:
                    pass
                request.session['email'] = email

                auth.login(request, user)
                # messages.success(request, 'Successfully logged in!')
                return redirect('home')
                url = request.META.get('HTTP_REFERER')
                
                try:
                    query = requests.utils.urlparse(url).query

                    # next=/cart/checkout/
                    params = dict(x.split('=')for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)

                except:
                    return redirect('home')
            else:

                messages.error(request, 'You are Blocked !!')
                return redirect('login')
        else:
            messages.error(request, 'Invalid login')
            return redirect('login')
    else:

        return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'congratulation!Your accountis activated. ')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.order_by(
        '-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    context = {
        'orders_count': orders_count,
    }
    return render(request, 'accounts/dashboard.html', context)


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact=email)
            send_forgotpassword_mail(request, user, email)
            return redirect('login')

        else:
            messages.error(request, 'Account does not exist')
            return render(request, 'accounts/forgotpassword.html')

    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password")
        return render(request, 'accounts/resetPassword.html')
    else:
        messages.error(request, "This link has been expired")
        return redirect('login')


@login_required(login_url='login')
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = CustomUser.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfull")
            return redirect('login')

        else:
            messages.error(request, "Passwords do not match")
            return redirect('resetPassword')
    else:

        return render(request, 'accounts/resetPassword.html')


def send_forgotpassword_mail(request, user, email):
    current_site = get_current_site(request)
    mail_subject = 'reset your password'
    messsage = render_to_string('accounts/reset_password_email.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = email
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login('anaghaponnore2000@gmail.com', 'ijrwxatoqswbbywd')
    smtp_server.sendmail('anaghaponnore2000@gmail.com', to_email, messsage)
    messages.success(
        request, 'password reset email has been sent to your email address.')


@login_required(login_url='login')
def edit_profile(request):
    context = {}
    userprofile = UserProfile.objects.filter(id=request.user.id)

    # userprofile = get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('edit_profile')
        else:
            user_form = UserForm(instance=request.user)
            profile_form = UserProfileForm(instance=userprofile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }

    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = CustomUser.objects.get(username=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')

        else:
            messages.error(request, 'Password doeds not match!')
            return redirect('change_password')

    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user, is_ordered=True).order_by('-created_at')
    orders_count = orders.count()
    context = {
        'orders': orders,
    }

    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,

    }
    return render(request, 'accounts/order_detail.html',context)




@login_required(login_url='login')
def myAddress(request):
  current_user = request.user
  address = Address.objects.filter(user=current_user)
  paginator = Paginator(address,3)
  page= request.GET.get('page')
  paged_address = paginator.get_page(page)
  
  context = {
    'address':paged_address,
  }
  return render(request, 'accounts/myAddress.html', context)


@login_required(login_url='login')
def addAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name = form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone = form.cleaned_data['phone']
            detail.email = form.cleaned_data['email']
            detail.address_line_1 = form.cleaned_data['address_line_1']
            detail.address_line_2 = form.cleaned_data['address_line_2']
            detail.state = form.cleaned_data['state']
            detail.country = form.cleaned_data['country']
            detail.city = form.cleaned_data['city']
            detail.save()
            messages.success(request, 'Address added Successfully')
            return redirect('myAddress')
        else:
            messages.success(request, 'Form is Not valid')
            return redirect('myAddress')
    else:
        form = AddressForm()
        context = {
            'form': form
        }
    return render(request, 'accounts/addAddress.html', context)


@login_required(login_url='login')
def deleteAddress(request, id):
    address = Address.objects.get(id=id)
    messages.success(request, "Address Deleted")
    address.delete()
    return redirect('myAddress')


@login_required(login_url='login')
def editAddress(request, id):
    address = Address.objects.get(id=id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address Updated Successfully')
            return redirect('myAddress')
        else:
            messages.error(request, 'Invalid Inputs!!!')
            return redirect('myAddress')
    else:
        form = AddressForm(instance=address)

    context = {
        'form': form,
    }
    return render(request, 'accounts/editAddress.html', context)


# checkout
def deleteCheckoutAddress(request, id):
    address = Address.objects.get(id=id)
    messages.success(request, "Address Deleted")
    address.delete()
    return redirect('checkout')


def AddCheckoutAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name = form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone = form.cleaned_data['phone']
            detail.email = form.cleaned_data['email']
            detail.address_line_1 = form.cleaned_data['address_line_1']
            detail.address_line_2 = form.cleaned_data['address_line_2']
            detail.state = form.cleaned_data['state']
            detail.country = form.cleaned_data['country']
            detail.city = form.cleaned_data['city']
            detail.save()
            messages.success(request, 'Address added Successfully')
            return redirect('checkout')
        else:
            messages.success(request, 'Form is Not valid')
            return redirect('checkout')