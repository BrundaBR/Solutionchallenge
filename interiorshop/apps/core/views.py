from django.shortcuts import render

from apps.product.models import Product
from apps.cart.views import display_user_exp
from apps.vendor.views import user_location

def frontpage(request):
    newest_products = Product.objects.all()[0:8]
    exp=display_user_exp(request)
    

    return render(request, 'core/frontpage.html', {'newest_products': newest_products,'exp':exp})

def contact(request):
    return render(request, 'core/contact.html')