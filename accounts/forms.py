from django.forms import ModelForm

from order.models import OrderItem

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['item', 'menu', 'option1', 'option2', 'addOn', 'person', 'quantity']
