from django.urls import path
from .views import product_handler, category_handler, order_handler

urlpatterns = [
    
    path('categories/', category_handler, name='category_handler'),  
    path('categories/<int:category_id>/', category_handler, name='category_detail'),  

    
    path('products/', product_handler, name='product_handler'),  
    path('products/<int:product_id>/', product_handler, name='product_detail'),  

    
    path('orders/', order_handler, name='order_handler'),  
    path('orders/<int:order_id>/', order_handler, name='order_detail'),  
]