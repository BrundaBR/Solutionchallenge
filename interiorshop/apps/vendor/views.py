from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Vendor,User_location
from apps.product.models import Product
from apps.order.models import OrderItem

from .forms import *
def user_location(request):
    
    if request.method=='GET':
        print('in')
        longitude = request.GET["long"]
        print(longitude)
        # loc=User_location(long=long,lat=lat)
        # loc.save()
    else:
        print("no location")
        
    return render(request,'core/base.html')
def awarness(request):
    return render(request,'vendor/awarness.html')
def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)
            # user_location(request)

            return redirect('awarnesspage')
    else:
        form = UserCreationForm()

    return render(request, 'vendor/become_vendor.html', {'form': form})

@login_required
def vendor_admin(request):
    
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders})

@login_required
def add_product(request):
    print("in")
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)


        if form.is_valid():
            print("valid")
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()
            form.save()

            return redirect('vendor_admin')
    else:
        print("no")
        form = ProductForm()
    
    return render(request, 'vendor/add_product.html', {'form': form})

@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        paypal = request.POST.get('paypal', '')
        

        if name:
            vendor.created_by.email = email
            
            vendor.created_by.save()
            
            vendor.name = name
            vendor.save()

            return redirect('vendor_admin')
    
    return render(request, 'vendor/edit_vendor.html', {'vendor':vendor})

def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendor/vendors.html', {'vendors': vendors})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, 'vendor/vendor.html', {'vendor': vendor})

