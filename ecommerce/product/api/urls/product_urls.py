from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from product.api.views import add_product, category_list, update_product, product_detail, filter_by_category, search_product, \
    filtered_products,product_list,sub_category_list

app_name = 'product'

urlpatterns = [
    path('addProduct', add_product, name="add-product"),
    path('update', update_product, name="update"),
    path('getCategories', category_list, name="categories-list"),
    path('getSubCategories', sub_category_list, name="sub_categories-list"),
    path('',product_list,name="product-list"),
    path('getById/<int:pk>', product_detail, name="product-detail"),
    path('<str:category>', filter_by_category, name="filter-by-category"),
    path('<str:category>/getFilteredProducts', filtered_products, name="filtered-products"),
    path('search/<str:searchstring>', search_product, name="search-product"),

]
urlpatterns = format_suffix_patterns(urlpatterns)
