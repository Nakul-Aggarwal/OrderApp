from django.contrib import admin
from items import models

# Register your models here.
admin.site.register(models.Table)
admin.site.register(models.Category)
admin.site.register(models.AddOn)
admin.site.register(models.Menu)
admin.site.register(models.Item)
admin.site.register(models.Option1)
admin.site.register(models.Option2)
