from django.urls import path

from . import views


urlpatterns=[
    path('',views.index),
    path('home/',views.index),
    path('Food/',views.Food),
    path('contact/',views.contact),
    path('about/',views.about),
    path('login/',views.login),
    path('faqs/',views.faqs),
    path('register/',views.register),
    path('booktable/',views.booktable),
    path('logout/',views.logout),
    path('cart/',views.cart),
    path('myprofile/',views.myprofile),
    path('orderhistory/',views.orderhistory),
    path('showcart/',views.showcart),
    path('productcart/',views.cartforproduct),
    path('order/',views.order),


]