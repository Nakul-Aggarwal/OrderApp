from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Table(models.Model):
    tableNumber = models.IntegerField(unique = True, verbose_name=('Table Number'))
    availaible = models.BooleanField(default = True)
    unique_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Table Number {}".format(self.tableNumber)

class AddOn(models.Model):
    item = models.CharField(max_length = 256)

    def __str__(self):
        return self.item

class Option1(models.Model):
    name = models.CharField(max_length = 256)

    def __str__(self):
        return self.name

class Option2(models.Model):
    name = models.CharField(max_length = 256)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length = 512, unique = True)
    veg = models.BooleanField(default = False)
    vegan = models.BooleanField(default=False)
    images = models.ImageField(upload_to = 'items/Category', default='items/Category/default.jpg')
    addOnPrice = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name=('Extra Option Price'))
    extras = models.ManyToManyField(AddOn, blank = True, related_name = 'category')
    options = models.ManyToManyField(Option1, blank = True, related_name = 'category')

    def __str__(self):
        return self.name

    def set_image_to_default(self):
        self.avatar.delete(save=False)  # delete old image file
        self.avatar = DEFAULT
        self.save()

class Menu(models.Model):
    name = models.CharField(max_length = 512)
    veg = models.BooleanField(default = False)
    vegan = models.BooleanField(default=False)
    availaible = models.BooleanField(default = True)
    price2 = models.DecimalField( max_digits=8, decimal_places=2, verbose_name=('Price for 2 person'))
    price3 = models.DecimalField( max_digits=8, decimal_places=2, verbose_name=('Price for 3 person'))
    price4 = models.DecimalField( max_digits=8, decimal_places=2, verbose_name=('Price for 4 person'))
    options = models.ManyToManyField(Option1, blank = True, related_name = 'menu')
    body = RichTextField(blank = True, null = True)
    image = models.ImageField(blank = True, null = True, upload_to = 'items/menu')

    def __str__(self):
        return "{} with pk {}".format(self.name,self.pk)

class Item(models.Model):
    category = models.ForeignKey(Category, related_name = 'products', on_delete = models.CASCADE)
    article_number = models.IntegerField(unique = True, blank=True, null=True)
    name = models.CharField(max_length=512)
    price = models.DecimalField( max_digits=8, decimal_places=2)
    availaible = models.BooleanField(default = True)
    option1 = models.BooleanField(default = False, verbose_name=('Show Category Options'))
    addOn = models.BooleanField(default=False, verbose_name=('Extras'))
    veg = models.BooleanField(default = False)
    vegan = models.BooleanField(default = False)
    description = models.TextField(max_length = 2000, blank = True, null = True)
    suggestions = models.ManyToManyField("Item", blank = True, symmetrical=False, related_name = 'related_to')
    options = models.ManyToManyField(Option2, blank = True, related_name = 'Items', verbose_name=('Show Following options'))
    image = models.ImageField(blank = True, null = True, upload_to = 'items/items')

    def __str__(self):
        if self.article_number:
            return "{}. {}".format(self.article_number, self.name)
        else :
            return self.name
