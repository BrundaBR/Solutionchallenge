from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('success/', views.success, name='success'),
    path('userexperience/',views.user_experience,name="exp"),
    path('placeorder/',views.placeorder,name="placeorder"),
    path('experience/',views.user_experience,name="disp_exp"),
    path('nearme/',views.mapplot,name="map"),
]