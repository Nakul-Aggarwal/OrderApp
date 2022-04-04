from django.db import models
from items.models import Item, Menu, Table
# Create your models here.

class OrderItem(models.Model):
    table = models.ForeignKey(Table, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE, null = True, blank = True, related_name = 'items')
    menu = models.ForeignKey(Menu, on_delete = models.CASCADE, null = True, blank = True, related_name = 'menus')
    person = models.IntegerField(blank = True, null = True)
    quantity = models.IntegerField()
    addOn = models.CharField(max_length = 256, blank = True, null = True)
    option1 = models.CharField(max_length = 256, blank = True, null = True)
    option2 = models.CharField(max_length = 256, blank = True, null = True)
    ordered = models.BooleanField(default = False)
    description = models.TextField(blank = True, null = True)
    paid = models.BooleanField(default = False)

    def __str__(self):
        try:
            return "{} of {} with {} persons".format(self.quantity, self.item.name, self.person)

        except:
            return "{} of {}".format(self.quantity, self.menu.name)

    def get_name(self):
        if self.item:
            return self.item.name
        else:
            return self.menu.name

    def getPrice(self):
        price = 0
        if self.item:
            price =  self.item.price * self.quantity

        else:
            if self.person == 2:
                return self.menu.price2*self.quantity

            elif self.person == 3:
                return self.menu.price3*self.quantity

            else:
                return self.menu.price4*self.quantity

        if self.addOn:
            price += (self.item.category.addOnPrice*self.quantity)

        return price


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete = models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default = False)
    orderDate = models.DateTimeField(blank = True, null = True)
    starters = models.BooleanField(default = False)
    orderID = models.IntegerField(blank = True, null = True)

    def __str__(self):
        return "Order for Table {}".format(self.table.tableNumber)

    def get_total_ordered(self):
        total = 0
        for order_items in self.item.all():
            if order_items.ordered:
                total += order_items.getPrice()
        return total

    def get_total_unordered(self):
        total = 0
        for order_items in self.item.all():
            if not order_items.ordered:
                total += order_items.getPrice()
        return total

class Feedback(models.Model):
    message = models.TextField(max_length=2000, blank=True, null=True)
    time = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.message
