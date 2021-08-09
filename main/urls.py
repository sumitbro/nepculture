from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('all_product', views.all_product, name='all_product'),
    path('singleproduct/<int:id>', views.singleproduct, name='singleproduct'),
    path('add_item', views.create_blog, name='create_blog'),
    path('cart', views.cart, name='cart'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>', views.remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_cart/<int:id>', views.remove_single_item_cart, name='remove_single_item_cart'),
    path('shipping', views.shipping, name='shipping'),
    path('search_item', views.search_item, name='search_item'),
    # path('shipping', views.ShippingView.as_view(), name='shipping')

    
]