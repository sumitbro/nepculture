from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import View
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from .forms import ShippingForm
from django.db.models import Q


# Create your views here.


def home(request):
    # item= Item.objects.all()
    item= Item.objects.filter(category__name="painting")[:6]
    print(item)
    item1= Item.objects.filter(category__name="statue")[:6]
    print(item1)
    item2= Item.objects.filter(category__name="canvas")[:6]
    item3= Item.objects.filter(category__name="mithila_art")[:6]
    
    context={
        
        'item':item,
        'item1':item1,
        'item2':item2,
        'item3':item3
    }

    return render(request, 'index.html', context)


def all_product(request):
    item= Item.objects.filter(category__name="painting")[:6]
    print(item)
    item1= Item.objects.filter(category__name="statue")[:6]
    print(item1)
    item2= Item.objects.filter(category__name="canvas")[:6]
    item3= Item.objects.filter(category__name="mithila_art")[:6]
    # item= Item.objects.all()
    # item1= Item.objects.filter(category_id=1)
    # item2= Item.objects.filter(category_id=2)
    # item3= Item.objects.filter(category_id=3)
    
    context={
        
        'item':item,
        'item1':item1,
        'item2':item2,
        'item3':item3
    }
    return render(request, 'all_product.html', context)


def singleproduct(request,id):
    pro= Item.objects.get(id=id)
    context={'pro':pro}

    return render(request, 'product-details.html',context)

def create_blog(request):
    
    if request.method=='POST':
        # category=request.POST['category']
        title=request.POST['title']
        price=request.POST['price']
        img=request.FILES['img']
        description= request.POST['description']
        data=Item(title=title,price=price, img=img, description=description)

        
        data.save()

        print("data saved")
        messages.info(request, "Your item was added")
        return redirect('/')

    else:
        
      
        return render(request, 'add_item.html')
      

@login_required
def add_to_cart(request, id):
    item= get_object_or_404(Item, id=id)
    order_item, created= Orderitem.objects.get_or_create(item=item,
    user=request.user,
    ordered=False
    )
    order_qs= Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order= order_qs[0]
        if order.items_order.filter(item__id=item.id).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "This item was updated")
        else:
            order.items_order.add(order_item)
            messages.info(request, "Your book was added to your cart")
            return redirect("cart")
    else:
        order= Order.objects.create(user=request.user)
        order.items_order.add(order_item)
        messages.info(request, "Your book was added to your cart")
        
    return HttpResponseRedirect(reverse("cart"))   

        
@login_required
def remove_from_cart(request,id):
    item= get_object_or_404(Item, id=id)
    order_qs= Order.objects.filter(
        user=request.user,
        ordered=False
        )
    if order_qs.exists():
        order=order_qs[0]
        if order.items_order.filter(item__id=item.id).exists():
            order_item= Orderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items_order.remove(order_item)
            messages.info(request, "Your book was removed from your cart")
            return redirect("cart")
        else:
            messages.info(request, "Your book was not in your cart")
            return redirect("singleproduct", id=id)
    else:
        messages.info(request, "You donot have an active order")
        return redirect("singleproduct", id=id)
        
@login_required
def remove_single_item_cart(request,id):
    item= get_object_or_404(Item, id=id)
    order_qs= Order.objects.filter(
        user=request.user,
        ordered=False
        )
    if order_qs.exists():
        order=order_qs[0]
        if order.items_order.filter(item__id=item.id).exists():
            order_item= Orderitem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity>1:
                order_item.quantity -=1
                order_item.save()
            else:
                order.items_order.remove(order_item)

            messages.info(request, "Your book was updated")
            return redirect("cart")
        else:
            messages.info(request, "Your book was not in your cart")
            return redirect("cart")
    else:
        messages.info(request, "You donot have an active order")
        return redirect("cart")
        

@login_required
def cart(request):
    try:
        crt_order= Order.objects.get(user=request.user, ordered=False)
        context= {'crt_order':crt_order}
        return render(request, 'cart.html', context)

    except ObjectDoesNotExist:
        messages.error(request,"You do not have an active order")
        return redirect("/")


def shipping(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form= ShippingForm(request.POST)
        # order= Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                form.save()
                print("data saved")
                messages.info(request, "Order successfull")
                return redirect('/shipping')
        form= ShippingForm()
        context={'form': form}
    return render(request, 'checkout.html', context)
    



def search_item(request):
    if request.method=="POST":
        search=request.POST['search_item']
        if search:
                  data= Item.objects.filter(Q(title__icontains=search))
                  if data:
                    return render(request, 'search.html', {'sr':data})
                  else:
                      messages.info(request, "No result Found")
                    #   messages.error(request, 'No result found')
                      return redirect('/')

        else:
            return HttpResponseRedirect("/search_item")


    else:
        return render(request, 'search.html')
