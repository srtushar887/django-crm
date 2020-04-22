from django.urls import path

from . import views

urlpatterns =[
    path('',views.home,name='home'),
    path('login',views.loginPage,name='loginPage'),
    path('register',views.register,name='register'),
    path('logout',views.logoutUser,name='logoutUser'),

    path('products/',views.products,name='products'),
    path('customer/<str:pk_test>/',views.customer,name='customer'),

    path('create-order/<str:pk>/',views.createOrder,name='createOrder'),
    path('update-order/<str:pk>/',views.updateOrder,name='updateOrder'),
    path('delete-order/<str:pk>/',views.deleteOrder,name='deleteOrder'),
]