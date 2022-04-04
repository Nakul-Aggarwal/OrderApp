from django.views.generic import TemplateView
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
import json, datetime, random
from django.core import serializers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from items.models import Table, Category, Item, Menu
from order.models import Order, OrderItem, Feedback
from order.forms import CartForm

def get_time():
    currentTime = datetime.datetime.now()
    time = ('{}:{}'.format(currentTime.hour, currentTime.minute))
    d = datetime.datetime.strptime(time, "%H:%M")
    return d.strftime("%I:%M %p")

def index(request):

    if request.method == 'POST':
        tableNumber = request.POST['tableNumber']
        table = Table.objects.filter(tableNumber = tableNumber)
        if table:
            table = table[0]
            if table.availaible:
                channel_layer = get_channel_layer()
                message = "Table Number {} is now active".format(tableNumber)
                text = { 'tableNumber':tableNumber, 'message':message, 'type':'Active', 'time':get_time() }
                async_to_sync(channel_layer.group_send)('broadcast', { 'type': 'websocket.message', 'text': json.dumps(text) })
                messages.warning(request, "This device is the primary device for table no. {}. Please use this device to place order".format(tableNumber))
                return redirect("order:menu", tableNumber = tableNumber)
            else:
                unique_number = int(request.COOKIES.get('unique_number', 404))
                if table.unique_number == unique_number:
                    messages.warning(
                        request, "This device is the primary device for table no. {}. Please use this device to place order".format(tableNumber))
                    return redirect("order:menu", tableNumber=tableNumber)

                else:
                    context = { 'tableNumber':tableNumber }
                    context['category_list'] = Category.objects.all()
                    context['menu_list'] = Menu.objects.all()
                    messages.warning(request, "Please check the menu and use the primary device on your table to place the order")
                    return render(request, 'order/staticmenu.html', context)
        else:
            messages.warning(request, "Please enter correct table number")
            return render(request, 'order/index.html')

    return render(request, 'order/index.html')

def menu_from_thanks(request, tableNumber):
    try:
        table = Table.objects.get(tableNumber = tableNumber)
        if not table.availaible:
            unique_number = int(request.COOKIES.get('unique_number', 404))
            if table.unique_number == unique_number:
                channel_layer = get_channel_layer()
                message = "Table Number {} is now active".format(tableNumber)
                text = { 'tableNumber':tableNumber, 'message':message, 'type':'Active', 'time':get_time() }
                async_to_sync(channel_layer.group_send)('broadcast', { 'type': 'websocket.message', 'text': json.dumps(text) })
                return redirect("order:menu", tableNumber = tableNumber)
            else:
                messages.warning(request, "Please enter correct table number")
                return render(request, 'order/index.html')
        else:
            channel_layer = get_channel_layer()
            message = "Table Number {} is now active".format(tableNumber)
            text = { 'tableNumber':tableNumber, 'message':message, 'type':'Active', 'time':get_time() }
            async_to_sync(channel_layer.group_send)('broadcast', { 'type': 'websocket.message', 'text': json.dumps(text) })
            return redirect("order:menu", tableNumber = tableNumber)
    except:
        messages.warning(request, "Please enter correct table number")
        return render(request, 'order/index.html')

def menu(request, tableNumber):

    try:
        table = Table.objects.get(tableNumber = tableNumber)
        context = { 'tableNumber':tableNumber }
        if table.availaible:
            table.unique_number = random.randint(100000,999999)
            table.availaible = False
            table.save()
            context['category_list'] = Category.objects.all()
            context['menu_list'] = Menu.objects.all()
            response = render(request, 'order/ordermenu.html', context)
            response.set_cookie('unique_number', table.unique_number, 3600*24*3)
            return response

        else:
            unique_number = int(request.COOKIES.get('unique_number', 404))
            if table.unique_number == unique_number:
                context['category_list'] = Category.objects.all()
                context['menu_list'] = Menu.objects.all()
                return render(request, 'order/ordermenu.html', context)
            else:
                messages.warning(request, "Sorry this table is already equipped")
                return redirect("order:index")

    except ObjectDoesNotExist:
        messages.warning(request, "No such table exist")
        return redirect("order:index")

def cart(request, tableNumber):

    try:

        table = Table.objects.get(tableNumber = tableNumber)
        context = { 'tableNumber':tableNumber }
        if not table.availaible:
            unique_number = int(request.COOKIES.get('unique_number', 404))
            if table.unique_number == unique_number:
                order = Order.objects.filter(table = table, ordered = False)
                if order:
                    context['order'] = order[0]
                    context['order_items'] = order[0].item.filter(paid=False, ordered=False)
                    if not context['order_items']:
                        messages.warning(request, "Your cart is currently empty.")
                    return render(request, 'order/cart.html', context)
                else:
                    messages.warning(request, "Sorry, you do not have any active order")
                    return redirect("order:menu", tableNumber=tableNumber)
            else:
                messages.warning(request, "Sorry this table is already equipped")
                return redirect("order:index")

        else:
            return redirect("order:index")

    except ObjectDoesNotExist:
        messages.warning(request, "OOPs! Something went wrong")
        return redirect("order:index")

def orderCart(request, tableNumber):

    try:
        table = Table.objects.get(tableNumber = tableNumber)
        context = { 'tableNumber':tableNumber }
        if not table.availaible:
            unique_number = int(request.COOKIES.get('unique_number', 404))
            if table.unique_number == unique_number:
                order = Order.objects.filter(table = table, ordered = False)
                if order:
                    context['order_items'] = order[0].item.filter(ordered=True, paid=False)
                    if not context['order_items']:
                        messages.warning(request, "You have not placed any order yet")
                    context['order'] = order[0]
                    return render(request, 'order/orderCart.html', context)
                else:
                    messages.warning(request, "Sorry, you do not have any active order")
                    return redirect("order:menu", tableNumber=tableNumber)
            else:
                messages.warning(request, "Sorry, this table is already equipped")
                return redirect("order:index")

        else:
            return redirect("order:index")

    except ObjectDoesNotExist:
        messages.warning(request, "OOPs! something went wrong")
        return redirect("order:index")

def placeOrder(request):

    if request.is_ajax and request.method == "GET":

        myOrderDict = {}
        for key in request.GET:
            if (key.startswith('order')):

                value = json.loads(request.GET[key])
                key = key.split('[')[1].split(']')[0]
                myOrderDict[key] = value

        tableNumber = request.GET['tableNumber']
        print(myOrderDict)

        table = Table.objects.get(tableNumber = tableNumber)
        order_qs = Order.objects.filter(table = table, ordered = False)
        order = Order.objects
        if order_qs:                                                            #Order already exist
            order = order_qs[0]
        else:
            order = Order.objects.create(table = table, ordered=False, orderDate = timezone.now())
        for key in myOrderDict:
            pk = int(key[4:])
            myOrder = myOrderDict[key]
            if( key[:4] == 'item' ):                                        #Update items quantity
                item = Item.objects.get(pk = pk)
                if (item.option1 and item.options.count()):
                    for option1 in myOrder:
                        for option2 in myOrder[option1]:
                            if isinstance(myOrder[option1][option2], dict):
                                for addOn in myOrder[option1][option2]:
                                    if addOn == "None":
                                        order_item_qs = OrderItem.objects.filter(
                                            table=table, ordered=False, item=item, option1=option1, option2=option2, addOn=None)
                                        if order_item_qs:
                                            order_item = order_item_qs[0]
                                            order_item.quantity = myOrder[option1][option2][addOn]
                                            order_item.save()
                                            order.save()
                                        else:
                                            order_item = OrderItem.objects.create(
                                                table=table, ordered=False, paid=False, item=item, addOn=None, option2=option2, option1=option1, quantity=myOrder[option1][option2][addOn])
                                            order_item.save()
                                            order.item.add(order_item)
                                            order.save()
                                    else:
                                        order_item_qs = OrderItem.objects.filter(table = table, ordered = False, item = item, addOn=addOn, option1=option1, option2=option2)
                                        if order_item_qs:
                                            order_item = order_item_qs[0]
                                            order_item.quantity = myOrder[option1][option2][addOn]
                                            order_item.save()
                                            order.save()
                                        else:
                                            order_item = OrderItem.objects.create(table = table, ordered=False, paid=False, item=item, option2=option2, option1=option1, addOn=addOn, quantity=myOrder[option1][option2][addOn])
                                            order_item.save()
                                            order.item.add(order_item)
                                            order.save()
                            else:
                                order_item_qs = OrderItem.objects.filter(table = table, ordered = False, item = item, option1=option1, option2=option2)
                                if order_item_qs:
                                    order_item = order_item_qs[0]
                                    order_item.quantity = myOrder[option1][option2]
                                    order_item.save()
                                    order.save()
                                else:
                                    order_item = OrderItem.objects.create(table = table, ordered=False, paid=False, item=item, option2=option2, option1=option1, quantity=myOrder[option1][option2])
                                    order_item.save()
                                    order.item.add(order_item)
                                    order.save()

                elif (item.option1):
                    for option1 in myOrder:
                        if isinstance(myOrder[option1], dict):
                            for addOn in myOrder[option1]:
                                if addOn == "None":
                                    order_item_qs = OrderItem.objects.filter(
                                        table=table, ordered=False, item=item, option1=option1, addOn=None)
                                    if order_item_qs:
                                        order_item = order_item_qs[0]
                                        order_item.quantity = myOrder[option1][addOn]
                                        order_item.save()
                                        order.save()
                                    else:
                                        order_item = OrderItem.objects.create(
                                            table=table, ordered=False, paid=False, item=item, option1=option1, addOn=None, quantity=myOrder[option1][addOn])
                                        order_item.save()
                                        order.item.add(order_item)
                                        order.save()
                                else:
                                    order_item_qs = OrderItem.objects.filter(table = table, ordered = False, item=item, option1 = option1, addOn=addOn)
                                    if order_item_qs:
                                        order_item = order_item_qs[0]
                                        order_item.quantity = myOrder[option1][addOn]
                                        order_item.save()
                                        order.save()
                                    else:
                                        order_item = OrderItem.objects.create(table=table, ordered=False, paid=False, item=item, option1=option1, addOn=addOn, quantity=myOrder[option1][addOn])
                                        order_item.save()
                                        order.item.add(order_item)
                                        order.save()
                        else:
                            order_item_qs = OrderItem.objects.filter(table = table, ordered = False, item=item, option1 = option1)
                            if order_item_qs:
                                order_item = order_item_qs[0]
                                order_item.quantity = myOrder[option1]
                                order_item.save()
                                order.save()
                            else:
                                order_item = OrderItem.objects.create(table=table, ordered=False, paid=False, item=item, option1=option1, quantity=myOrder[option1])
                                order_item.save()
                                order.item.add(order_item)
                                order.save()

                elif (item.options.count()):
                    for option2 in myOrder:
                        if isinstance(myOrder[option2], dict):
                            for addOn in myOrder[option2]:
                                if addOn == "None":
                                    order_item_qs = OrderItem.objects.filter(
                                        table=table, ordered=False, item=item, addOn=None, option2=option2)
                                    if order_item_qs:
                                        order_item = order_item_qs[0]
                                        order_item.quantity = myOrder[option2][addOn]
                                        order_item.save()
                                        order.save()
                                    else:
                                        order_item = OrderItem.objects.create(
                                            table=table, ordered=False, paid=False, addOn=None, item=item, option2=option2, quantity=myOrder[option2][addOn])
                                        order_item.save()
                                        order.item.add(order_item)
                                        order.save()
                                else:
                                    order_item_qs = OrderItem.objects.filter(table = table, ordered = False, item=item, option2 = option2, addOn=addOn)
                                    if order_item_qs:
                                        order_item = order_item_qs[0]
                                        order_item.quantity = myOrder[option2][addOn]
                                        order_item.save()
                                        order.save()
                                    else:
                                        order_item = OrderItem.objects.create(table=table, ordered=False, paid=False, item=item, option2=option2, addOn=addOn, quantity=myOrder[option2][addOn])
                                        order_item.save()
                                        order.item.add(order_item)
                                        order.save()
                        else:
                            order_item_qs = OrderItem.objects.filter(table = table, ordered = False, item=item, option2 = option2)
                            if order_item_qs:
                                order_item = order_item_qs[0]
                                order_item.quantity = myOrder[option2]
                                order_item.save()
                                order.save()
                            else:
                                order_item = OrderItem.objects.create(table=table, ordered=False, paid=False, item=item, option2=option2, quantity=myOrder[option2])
                                order_item.save()
                                order.item.add(order_item)
                                order.save()

                else:

                    if isinstance(myOrder, dict):
                        for addOn in myOrder:
                            if addOn == "None":
                                order_item_qs = OrderItem.objects.filter(table = table, addOn=None, ordered = False, item=item)
                                if order_item_qs:
                                    order_item = order_item_qs[0]
                                    order_item.quantity = myOrder[addOn]
                                    order_item.save()
                                    order.save()
                                else:
                                    order_item = OrderItem.objects.create(table=table, addOn=None, ordered=False, paid=False, item=item, quantity=myOrder[addOn])
                                    order_item.save()
                                    order.item.add(order_item)
                                    order.save()
                            else:
                                order_item_qs = OrderItem.objects.filter(table = table, ordered = False, item=item, addOn=addOn)
                                if order_item_qs:
                                    order_item = order_item_qs[0]
                                    order_item.quantity = myOrder[addOn]
                                    order_item.save()
                                    order.save()
                                else:
                                    order_item = OrderItem.objects.create(table=table, ordered=False, paid=False, item=item, addOn=addOn, quantity=myOrder[addOn])
                                    order_item.save()
                                    order.item.add(order_item)
                                    order.save()
                    else:
                        order_item_qs = OrderItem.objects.filter(table = table, ordered = False, item=item)
                        if order_item_qs:
                            order_item = order_item_qs[0]
                            order_item.quantity = myOrder
                            order_item.save()
                            order.save()
                        else:
                            order_item = OrderItem.objects.create(table=table, ordered=False, paid=False, item=item, quantity=myOrder)
                            order_item.save()
                            order.item.add(order_item)
                            order.save()

            else:                                                           #Update menu quantity
                menu = Menu.objects.get(pk = pk)
                for option1 in myOrder:
                    person_list = myOrder[option1]
                    for person in person_list:
                        quantity = person_list[person]
                        if OrderItem.objects.filter(menu = menu, table = table, ordered = False, option1 = option1, person = person).exists():
                            order_item = OrderItem.objects.get(menu = menu, table=table, ordered=False, option1=option1, person = person)
                            order_item.quantity = quantity
                            order_item.save()
                            order.save()
                        else:
                            order_item = OrderItem.objects.create(menu = menu, table = table, option1=option1, ordered=False, person = person, quantity=quantity)
                            order_item.save()
                            order.item.add(order_item)
                            order.save()

        return HttpResponse('Order Submitted')

    else:
        redirect("order:index")

def CallWaiter(request):
    if request.is_ajax() and request.method == "GET":
        tableNumber = json.loads(request.GET['tableNumber'])
        channel_layer = get_channel_layer()
        message = "Table Number {} has requested for waiter".format(tableNumber)

        text = { 'tableNumber':tableNumber, 'message':message, 'type':'Waiter', 'time': get_time() }
        async_to_sync(channel_layer.group_send)('broadcast', { 'type': 'websocket.message', 'text': json.dumps(text) })
    return HttpResponse("Waiter Has been called")


def updateCart(request):
    if request.is_ajax and request.method == "GET":

        myOrderDict = {}
        for key in request.GET:
            if (key.startswith('order')):

                value = json.loads(request.GET[key])
                key = key.split('[')[1].split(']')[0]
                myOrderDict[key] = value

        print(myOrderDict)
        starters = json.loads(request.GET['starters'])
        tableNumber = json.loads(request.GET['tableNumber'])
        for order in myOrderDict:
            id = int(order[10:])
            item = OrderItem.objects.get(pk=id)
            if myOrderDict[order][0]>0:
                item.quantity = myOrderDict[order][0]
                if myOrderDict[order][1]:
                    item.description = myOrderDict[order][1]
                item.save()
            else :
                item.delete()
        if starters:
            table = Table.objects.get(tableNumber = tableNumber)
            myOrder = Order.objects.get( table = table, ordered = False)
            myOrder.starters = True
            myOrder.save()

        return HttpResponse("Updated Cart")

def confirmOrder(request, tableNumber):

        try:
            table = Table.objects.get(tableNumber = tableNumber)
            context = { 'tableNumber':tableNumber }
            if not table.availaible:
                order = Order.objects.get( table = table, ordered=False )
                order_placed = {}
                for items in order.item.filter(ordered = False):
                    order_placed[items.pk] = { 'quantity':items.quantity }
                    order_placed[items.pk]['name'] = items.get_name()
                    if items.option1:
                        order_placed[items.pk]['option1'] = items.option1
                    if items.option2:
                        order_placed[items.pk]['option2'] = items.option2
                    if items.addOn:
                        order_placed[items.pk]['addOn'] = items.addOn
                    if items.person:
                        order_placed[items.pk]['person'] = items.person
                    if items.description:
                        order_placed[items.pk]['description'] = items.description
                    if items.item and items.item.article_number:
                        order_placed[items.pk]['article_number'] = items.item.article_number
                    print(order_placed)

                    item_qs = OrderItem.objects.filter(table = table, item = items.item, menu = items.menu, ordered=True, paid = False, option1 = items.option1, addOn = items.addOn, person=items.person, option2=items.option2)
                    if item_qs:
                        item_qs = item_qs[0]
                        item_qs.quantity += items.quantity
                        item_qs.save()
                        items.delete()
                    else:
                        items.ordered = True
                        items.save()


                channel_layer = get_channel_layer()
                text = { 'tableNumber':tableNumber, 'order_placed':order_placed, 'type': 'Order', 'time': get_time(), 'information': order.starters }
                async_to_sync(channel_layer.group_send)('broadcast', { 'type': 'websocket.message', 'text': json.dumps(text) })
                return redirect("order:order_list", tableNumber = tableNumber)

            else:
                messages.warning(request, "Sorry, this table is currently not availaible")
                return redirect("order:index")

        except ObjectDoesNotExist:
            messages.warning(request, "No such table exist")
            return redirect("order:index")

def thanks(request, tableNumber):
    try:
        print("Inside try block")
        table = Table.objects.get(tableNumber = tableNumber)
        context = { 'tableNumber':tableNumber }
        if request.POST:
            message = request.POST['feedback']
            feedback = Feedback.objects.create(message = message, time=timezone.now())
            feedback.save()
            messages.success(request,"Your feedback has been submitted successfully")
            return render(request, 'order/thanks.html', context)
        if not table.availaible:
            order = Order.objects.filter(table = table, ordered = False)
            if order:
                order = order[0]
                for item in order.item.filter(ordered = True):
                    item.paid = True
                    item.save()
                for item in order.item.filter(ordered = False):
                    item.delete()
                order.ordered = True
                order.save()
                messages.success(request, "Your request for bill has been submitted")
                channel_layer = get_channel_layer()
                message = "Table Number {} has requested for bill".format(tableNumber)
                text = { 'tableNumber':tableNumber, 'message':message, 'type':'Inactive', 'time': get_time() }
                async_to_sync(channel_layer.group_send)('broadcast', { 'type': 'websocket.message', 'text': json.dumps(text) })
            return render(request, 'order/thanks.html', context)

        else:
            messages.warning(request, "Sorry, this table is currently not availaible")
            return redirect("order:index")

    except ObjectDoesNotExist:
        messages.warning(request, "No such table exist")
        return redirect("order:index")

def add_to_cart(request, pk, tableNumber):

    try:
        item = OrderItem.objects.get(pk=pk)
        item.quantity += 1
        item.save()
        return redirect("order:cart", tableNumber=tableNumber)

    except:
        messages.warning(request, "OOPs! Something went wrong")
        return redirect("order:index")

def remove_from_cart(request, pk, tableNumber):

    try:
        item = OrderItem.objects.get(pk=pk)
        item.quantity -= 1
        if item.quantity<1:
            item.delete()
        else:
            item.save()
        return redirect("order:cart", tableNumber=tableNumber)

    except:
        messages.warning(request, "OOPs! Something went wrong")
        return redirect("order:index")

def remove_addOn(request, pk, tableNumber):

    item = OrderItem.objects.get(pk=pk)
    item.addOn = None
    item.save()
    return redirect("order:cart", tableNumber=tableNumber)

    # except:
    #     messages.warning(request, "OOPs! Something went wrong")
    #     return redirect("order:index")
