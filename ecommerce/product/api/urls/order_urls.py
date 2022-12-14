from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from product.api.views import create_order, order_history

app_name = 'product'

urlpatterns = [
    path('<int:userid>/createOrder', create_order, name="create-order"),
    path('<int:userid>/getOrders', order_history, name='order-history'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
