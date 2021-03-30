import stripe 
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *

from .forms import CheckoutForm
from apps.order.models import Order,OrderItem
from apps.cart.cart import *
from apps.order.utilities import checkout, notify_customer, notify_vendor
def mapplot(request):
    return render(request,'core/map.html')


def placeorder(request):
    cart=Cart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                phone = request.POST['phone']
                address = request.POST['address']
                zipcode = request.POST['zipcode']
                place = request.POST['place']
                amount=12
                order=Order(first_name=first_name,last_name=last_name, email=email, address=address, zipcode=zipcode, place=place, phone=phone, paid_amount=amount)
                order.save()
                for item in Cart(request):
                    ordr=OrderItem.objects.create( order=order,product=item['product'], vendor=item['product'].vendor, price=item['product'].price, quantity=item['quantity'])
                    order.vendors.add(item['product'].vendor)
                notify_customer(order)
                notify_vendor(order)
                cart.clear()
                return redirect('success')
                
            except Exception:
                messages.error(request, 'There was something wrong with the payment')
    else:
        form = CheckoutForm()
    return render(request,'cart/placeorder.html',{'form': form})

def success(request):
    return render(request, 'cart/success.html')

def user_experience(request):
    if request.method=="POST":
        exp=request.POST["exp"]
        username=request.POST["user-name"]
        usr_exp=UserExperience(user=username,feedback=exp)
        usr_exp.save()
        redirect('/')
        
    return render(request,'cart/user-exp.html') 

def display_user_exp(request):
    exp_content=UserExperience.objects.all()
    return exp_content


def cart_detail(request):
    # cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            # stripe.api_key = settings.STRIPE_SECRET_KEY

            # stripe_token = form.cleaned_data['stripe_token']

            try:
                # charge = stripe.Charge.create(
                #     amount=int(cart.get_total_cost() * 100),
                #     currency='USD',
                #     description='Charge from Interiorshop',
                #     source=stripe_token
                # )

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']

                order = checkout(request, first_name, last_name, email, address, zipcode, place, phone, cart.get_total_cost())
                cart.clear()
                return redirect('success')
                #notify_customer(order)
                # notify_vendor(order)
            except Exception:
                messages.error(request, 'There was something wrong with the payment')
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart/cart.html', {'form': form})
