from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [

    path('index', views.index, name="index"),
    path('menu/<int:tableNumber>/', views.menu, name="menu"),
    path('placeOrder', views.placeOrder, name="placeOrder"),
    path('cart/<int:tableNumber>/', views.cart, name="cart"),
    path('order_list/<int:tableNumber>', views.orderCart, name="order_list"),
    path('confirmOrder/<int:tableNumber>', views.confirmOrder, name="confirmOrder"),
    path('thanks/<int:tableNumber>', views.thanks, name='thanks'),
    path('add_to_cart/<int:pk>/<int:tableNumber>', views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:pk>/<int:tableNumber>', views.remove_from_cart, name="remove_from_cart"),
    path('remove_addOn/<int:pk>/<int:tableNumber>', views.remove_addOn, name="remove_addOn"),
    path('updateCart', views.updateCart, name="updateCart"),
    path('waiter/', views.CallWaiter, name='waiter'),
    path('menuThanks/<int:tableNumber>', views.menu_from_thanks, name='menuThanks'),
]
