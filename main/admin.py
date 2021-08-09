from django.contrib import admin
from .models import Item, Order, Orderitem, Shipping, Category
# Register your models here.


class AdminItem(admin.ModelAdmin):
    list_display=['title', 'price', 'img', 'description']


admin.site.register(Item, AdminItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Orderitem)
admin.site.register(Shipping)
# admin.site.register(Cart)
