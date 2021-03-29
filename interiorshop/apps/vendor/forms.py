from django.forms import ModelForm
from django import forms
from apps.product.models import Product
# from .models import Profile

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price','from_date','to_date'] 




# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['image']


    