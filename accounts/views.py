from django.shortcuts import render, redirect
from django.views.generic import View, ListView, DetailView, TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django import forms
import json

from items.models import Table, Category, Item, Menu, Option1, Option2, AddOn
from order.models import Order, OrderItem, Feedback
from .forms import OrderItemForm
from django.forms.models import modelform_factory

# Create your views here.
class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)

class Index(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'accounts/index.html'

@login_required
def update_cart(request):
    if request.is_ajax and request.method == "GET":
        myOrderDict = {}
        for key in request.GET:
            quantity = request.GET[key]
            key = key.split('[')[1].split(']')[0]
            order_item = OrderItem.objects.get(pk=int(key))
            order_item.quantity = quantity
            if int(quantity) == 0:
                order_item.delete()
            else:
                order_item.save()
    return HttpResponse("Success")

@login_required
def create_orderitem(request, tableNumber):
    context = {}
    context['form'] = OrderItemForm()
    context['tableNumber'] = tableNumber
    if request.POST:
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.cleaned_data.get("item")
            menu = form.cleaned_data.get('menu')
            if item and menu:
                messages.warning(request, "Please select only one, either item or menu. You can't select both")
                return render(request, 'accounts/update_item.html', context)
            if not item and not menu:
                messages.warning(request, "Both item and menu can't be empty. You must select one")
                return render(request, 'accounts/update_item.html', context)
            if item:
                option1 = form.cleaned_data.get('option1')
                option2 = form.cleaned_data.get('option2')
                addOn = form.cleaned_data.get('addOn')
                quantity = form.cleaned_data.get('quantity')
                table = Table.objects.get(tableNumber=tableNumber)
                order_item = OrderItem.objects.create(table=table, item=item, option1=option1, option2=option2, addOn=addOn, quantity=quantity, ordered=True, paid=False)
                order = Order.objects.get(table = table, ordered=False)
                order_item.save()
                order.item.add(order_item)
                order.save()
                return redirect("accounts:view_table", pk=tableNumber)
            if menu:
                option1 = form.cleaned_data.get('option1')
                person = form.cleaned_data.get('person')
                if not person:
                    messages.warning(request, "Please select number of person for menu.")
                    return render(request, 'accounts/update_item.html', context)
                quantity = form.cleaned_data.get('quantity')
                table = Table.objects.get(tableNumber=tableNumber)
                order_item = OrderItem.objects.create(table=table, menu=menu, option1=option1, person=person, quantity=quantity, ordered=True, paid=False)
                order = Order.objects.get(table = table, ordered=False)
                order_item.save()
                order.item.add(order_item)
                order.save()
                return redirect("accounts:view_table", pk=tableNumber)
    return render(request, 'accounts/update_item.html', context)

@login_required
def items_list(request):
    context = { 'menu_list' : Menu.objects.all(), 'category_list' : Category.objects.all() }
    return render(request, 'accounts/items_list.html', context)

@login_required
def options_list(request):
    context = { 'option1' :  Option1.objects.all(), 'option2' : Option2.objects.all(), 'addOn' : AddOn.objects.all() }
    return render(request, 'accounts/options_list.html', context)

@login_required
def feedback_list(request):
    context = { 'feedback' :  Feedback.objects.all().order_by("-time") }
    return render(request, 'accounts/feedback_list.html', context)

@login_required
def item_availaible(request, pk):
    item = Item.objects.get(pk=pk)
    if item.availaible:
        item.availaible = False
    else:
        item.availaible = True
    item.save()
    return redirect("accounts:items_list")

@login_required
def menu_availaible(request, pk):
    item = Menu.objects.get(pk=pk)
    if item.availaible:
        item.availaible = False
    else:
        item.availaible = True
    item.save()
    return redirect("accounts:items_list")

class ItemsUpdateView(LoginRequiredMixin, ModelFormWidgetMixin, UpdateView):
    model = Item
    widgets = {
        'options': forms.CheckboxSelectMultiple,
        'suggestions' : forms.CheckboxSelectMultiple,
    }
    template_name = 'accounts/update_item.html'
    fields = [
              "category",
              "article_number",
              "name",
              "price",
              "description",
              "veg",
              "vegan",
              "option1",
              "addOn",
              "options",
              "suggestions",
              "image",
    ]
    success_url = reverse_lazy("accounts:items_list")

class CategoryUpdateView(LoginRequiredMixin, ModelFormWidgetMixin, UpdateView):
    model = Category
    widgets = {
        'options': forms.CheckboxSelectMultiple,
        'extras' : forms.CheckboxSelectMultiple,
    }
    template_name = 'accounts/update_item.html'
    fields = [
              "name",
              "veg",
              "vegan",
              "options",
              "extras",
              "addOnPrice",
              "images",
    ]
    success_url = reverse_lazy("accounts:items_list")

class MenuUpdateView(LoginRequiredMixin, ModelFormWidgetMixin, UpdateView):
    model = Menu
    widgets = {
        'options': forms.CheckboxSelectMultiple,
    }
    template_name = 'accounts/update_menu.html'
    fields = [
              "name",
              "veg",
              "vegan",
              "body",
              "price2",
              "price3",
              "price4",
              "options",
              "image",
    ]
    labels = {
        'price2' : "Price for 2 persons",
        'price3' : "Price for 3 persons",
        'price4' : "Price for 4 persons",
    }
    success_url = reverse_lazy("accounts:items_list")

class ItemsCreateView(LoginRequiredMixin, ModelFormWidgetMixin, CreateView):
    model = Item
    widgets = {
        'options': forms.CheckboxSelectMultiple,
        'suggestions' : forms.CheckboxSelectMultiple,
    }
    template_name = 'accounts/update_item.html'
    fields = [
              "category",
              "article_number",
              "name",
              "price",
              "description",
              "veg",
              "vegan",
              "option1",
              "addOn",
              "options",
              "suggestions",
              "image",
    ]
    success_url = reverse_lazy("accounts:items_list")

class CategoryCreateView(LoginRequiredMixin, ModelFormWidgetMixin, CreateView):
    model = Category
    widgets = {
        'options': forms.CheckboxSelectMultiple,
        'extras' : forms.CheckboxSelectMultiple,
    }
    template_name = 'accounts/update_item.html'
    fields = [
              "name",
              "veg",
              "vegan",
              "options",
              "extras",
              "addOnPrice",
              "images",
    ]
    success_url = reverse_lazy("accounts:items_list")

class MenuCreateView(LoginRequiredMixin, ModelFormWidgetMixin, CreateView):
    model = Menu
    widgets = {
        'options': forms.CheckboxSelectMultiple,
    }
    template_name = 'accounts/update_menu.html'
    fields = [
              "name",
              "veg",
              "vegan",
              "body",
              "price2",
              "price3",
              "price4",
              "options",
              "image",
    ]
    labels = {
        'price2' : "Price for 2 persons",
        'price3' : "Price for 3 persons",
        'price4' : "Price for 4 persons",
    }
    success_url = reverse_lazy("accounts:items_list")

class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    template_name = 'accounts/update_item.html'
    fields = ["tableNumber"]
    success_url = reverse_lazy("accounts:index")

class Option1UpdateView(LoginRequiredMixin, UpdateView):
    model = Option1
    template_name = "accounts/update_item.html"
    fields = ["name"]
    success_url = reverse_lazy("accounts:options_list")

class Option1CreateView(LoginRequiredMixin, CreateView):
    model = Option1
    template_name = "accounts/update_item.html"
    fields = ["name"]
    success_url = reverse_lazy("accounts:options_list")

class Option1DeleteView(LoginRequiredMixin, DeleteView):
    model = Option1
    template_name = "accounts/delete_item.html"
    fields = ["name"]
    success_url = reverse_lazy("accounts:options_list")

class Option2UpdateView(LoginRequiredMixin, UpdateView):
    model = Option2
    template_name = "accounts/update_item.html"
    fields = ["name"]
    success_url = reverse_lazy("accounts:options_list")

class Option2CreateView(LoginRequiredMixin, CreateView):
    model = Option2
    template_name = "accounts/update_item.html"
    fields = ["name"]
    success_url = reverse_lazy("accounts:options_list")

class Option2DeleteView(LoginRequiredMixin, DeleteView):
    model = Option2
    template_name = "accounts/delete_item.html"
    fields = ["name"]
    success_url = reverse_lazy("accounts:options_list")

class ExtrasUpdateView(LoginRequiredMixin, UpdateView):
    model = AddOn
    template_name = "accounts/update_item.html"
    fields = ["item"]
    success_url = reverse_lazy("accounts:options_list")

class ExtrasCreateView(LoginRequiredMixin, CreateView):
    model = AddOn
    template_name = "accounts/update_item.html"
    fields = ["item"]
    success_url = reverse_lazy("accounts:options_list")

class ExtrasDeleteView(LoginRequiredMixin, DeleteView):
    model = AddOn
    template_name = "accounts/delete_item.html"
    success_url = reverse_lazy("accounts:options_list")

class FeedbackDeleteView(LoginRequiredMixin, DeleteView):
    model = Feedback
    template_name = "accounts/delete_item.html"
    success_url = reverse_lazy("accounts:feedback_list")

def view_table(request, pk):
    table = Table.objects.get(tableNumber=pk)
    context = {'table' : table}
    context['tableNumber'] = table.tableNumber
    order = Order.objects.filter(table=table, ordered=False)
    if order:
        context['current_order'] = order[0].item.filter(ordered=True, paid=False)
        context['get_total_ordered'] = order[0].get_total_ordered()
    context['previous_order']  = Order.objects.filter(table=table, ordered=True)
    return render(request, 'accounts/view_table.html', context)

def view_order(request, pk):
    order = Order.objects.get(pk=pk)
    return render(request, 'accounts/view_order.html', {'order': order})

def table_availaible(request, tableNumber):
    table = Table.objects.get(tableNumber = tableNumber)
    order = Order.objects.filter(ordered = False)
    if order:
        order = order[0]
        for item in order.item.filter(ordered = True):
            item.paid = True
            item.save()
        for item in order.item.filter(ordered = False):
            item.delete()
        order.ordered = True
        order.save()
    table.availaible = True
    table.unique_number = None
    table.save()
    channel_layer = get_channel_layer()
    text = { 'tableNumber':tableNumber, 'type':'move_to_inactive' }
    async_to_sync(channel_layer.group_send)('broadcast', { 'type': 'websocket.message', 'text': json.dumps(text) })
    return redirect("accounts:view_table", pk=tableNumber)

def table_unavailaible(request, tableNumber):
    table = Table.objects.get(tableNumber = tableNumber)
    table.availaible = False
    table.unique_number = None
    table.save()
    channel_layer = get_channel_layer()
    text = { 'tableNumber':tableNumber, 'type':'move_to_active' }
    async_to_sync(channel_layer.group_send)('broadcast', { 'type': 'websocket.message', 'text': json.dumps(text) })
    return redirect("accounts:view_table", pk=tableNumber)
