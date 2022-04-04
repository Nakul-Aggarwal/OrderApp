from django.contrib import admin
from order.models import OrderItem, Order, Feedback
# Register your models here.

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Feedback)
