from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from product.api.views import get_cart, get_cart_item, add_item_to_cart, remove_cart_item, change_quantity

app_name = 'product'

urlpatterns = [
    path('<int:userid>/getCart/', get_cart, name="get-cart"),
    path('<int:userid>/getCartItem/<int:cartitemId>', get_cart_item, name="get-cart-item"),
    path('<int:userid>/add/<int:product_id>', add_item_to_cart, name="add-cart-item"),
    path('<int:userid>/remove/<int:product_id>', remove_cart_item, name="remove-cart-item"),
    path('<int:userid>/changeQuantity/<int:product_id>', change_quantity, name="change-quantity"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
