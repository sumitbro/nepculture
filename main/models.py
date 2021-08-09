from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField


CATEGORY_CHOICES=(
    ('canvas','Canvas Art'),
    ('sculpture', 'Sculpture'),
    ('wood_craft', 'Wood craft'),
    ('musical', 'Musical instrument'),
    ('handicraft', 'Handicraft'),
    ('antique', 'Antique'),
    ('statue', 'Statue'),
    ('painting', 'Painting'),
    ('mithila_art', 'Mithila Art'),
    

)



# Create your models here.
class Category(models.Model):
    # name=models.CharField(max_length=200, null=True)
    name= models.CharField(choices=CATEGORY_CHOICES, max_length=200, null=True)
    def __str__(self):
        return self.name



class Item(models.Model):
    category= models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title= models.CharField(max_length=50, null= True)
    # artist_name=models.CharField(max_length=50, null=True)
    
    price= models.FloatField(null=True)
    img= models.ImageField(upload_to='pics', null=True)
    description= models.TextField(null= True)
    
    def __str__(self):
        return self.title

    def get_item_by_category_id(category_id):
        if category_id:
            return Item.objects.filter(category=category_id)
        else:
            return Item.objects.all()


    # def get_add_to_cart_url(self):
    #     return reverse("lib:add_to_cart", kwargs={
    #         'id':self.id
    #     })





class Orderitem(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    ordered= models.BooleanField(default=False, null=True)
    item= models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    # order= models.ForeignKey(Order, on_delete=models.CASCADE, null= True)
    quantity= models.IntegerField(default=1, null=True, blank=True)
    

    def __str__(self):
        return self.item.title

    def get_total_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_price()




class Order(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    items_order=models.ManyToManyField(Orderitem) 
    date_added= models.DateTimeField(auto_now_add=True, null=True)
    date_ordered= models.DateTimeField(auto_now_add=True, null=True)
    ordered= models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return self.user.username

    def get_total(self):
        total=0
        for odr in self.items_order.all():
            total+= odr.get_final_price()
        return total

    




Payment_choice=(
    ('E', 'eSewa'),
    ('K', 'Khalti')
)
class Shipping(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    item= models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    order= models.ForeignKey(Order, on_delete=models.CASCADE, null= True)
    address1= models.CharField(max_length=50, null= True)
    address2= models.CharField(max_length=50, null= True, blank=True)
    country= CountryField(multiple=False, null=True)
    zipcode= models.CharField(max_length=50, null= True)
    payment= models.CharField(max_length=200, choices= Payment_choice, null=True)
    date_added= models.DateTimeField(auto_now_add=True, null=True)

    # def __str__(self):
    #     return self.user.username



# class Cart(models.Model):
#     item= models.ManyToManyField(Item, null=True, blank=True)
#     total= models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
#     timestamp= models.DateTimeField(auto_now_add=True, auto_now=False)
#     updated= models.DateTimeField(auto_now_add=False, auto_now=True)
#     active= models.BooleanField(default=True)


#     def __inicode(self):
#         return "Card id: %s" %(self.id)


