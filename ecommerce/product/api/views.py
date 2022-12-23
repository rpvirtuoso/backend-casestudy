from datetime import datetime

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProductSerializer, CartItemSerializer, \
    OrderItemTrueSerializer,CategorySerializer,SubCategorySerializer
from ..models import Category, Product, Customer, Cart, CartItem, Order, OrderItemTrue, SubCategory


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_product(request):
    print('add product is being called')
    if request.user.is_admin:
        if request.method == 'POST':
            print(request.data)
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        context = {"ERROR": "You dont have required permission to add any product(s)"}
        return Response(context, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_product(request):
    if request.user.is_admin:
            print(request.data)
            pk = request.data["id"]
            try:
                product = Product.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ProductSerializer(product, data=request.data)
            print(f'serializer is :{serializer}')
            if serializer.is_valid():
                print('serializer is valid')
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer._errors)
    else:
        context = {"ERROR": "You dont have required permission to update any product(s)"}
        return Response(context, status=status.HTTP_403_FORBIDDEN)


@api_view(["GET"])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def product_list(request):
    print("function called")
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def category_list(request):
        print("function called")
        categories=Category.objects.all()
        serializer=CategorySerializer(categories,many=True)
        print(serializer.data)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sub_category_list(request):
        print(request.data)
        id=Category.objects.get(name=request.data['category'])

        sub_categories=SubCategory.objects.filter(category=id)
        serializer=SubCategorySerializer(sub_categories,many=True)
        context={}
        return Response(serializer.data)

@api_view(["GET"])
def filter_by_category(request, category):
    print('filter_by_category is being called')
    try:
        product = Product.objects.filter(category=category)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def filtered_products(request, category):
    try:
        product = Product.objects.filter(category=category)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        p = request.data["MinPrice"]
        product_by_price = product.filter(price__gte=p)
    #     try:
    #         s = request.data["subcategory"]
    #     except KeyError:
    #         print("Key Error , 'subcategory' key doesnt exist")

    except KeyError:
        print("Key Error , 'price' Key doesn't exist")

    # final = product_by_price.filter(subcategory=s)
    serializer = ProductSerializer(product_by_price, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def search_product(request, searchstring):
    try:
        product = Product.objects.filter(name=searchstring)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request, userid):
    # try:
    #     customer = Customer.objects.get(user_id=userid)
    # except Customer.DoesNotExist:
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    # # Current active cart of given user
    # cart = Cart.objects.filter(customer_id=customer.id).get(complete=False)
    # print(cart)
    # serializer = CartSerializer(cart)
    # print(serializer.data)
    # return Response(serializer.data)
    try:
        customer = Customer.objects.get(user_id=userid)
        print(customer.id)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        cart = Cart.objects.filter(customer_id=customer.id).get(complete=False)
    except Cart.DoesNotExist:
        cart = Cart(customer=customer, date_modified=datetime.now())
        cart.save()
        info = "Your Cart was empty.Please add products to the cart"
        context = {"info": info}
        return Response(context)
    cart_id = cart.id
    cart_items = CartItem.objects.filter(cart_id=cart_id)
    context = {"cartId": cart_id}
    cart_item_list = []
    for cart_item in cart_items:
        print(cart_item.id)
        serializer = CartItemSerializer(cart_item)
        cart_item_list.append(serializer.data)
    context["products"] = cart_item_list
    return Response(context, status=status.HTTP_200_OK)

    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart_item(request, userid, cartitemId):
    try:
        customer = Customer.objects.get(user_id=userid)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        cart = Cart.objects.filter(customer_id=customer.id).get(complete=False)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    cart_id = cart.id
    cart_items = CartItem.objects.filter(cart_id=cart_id)
    try:
        cart_item = cart_items.get(id=cartitemId)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(type(cart_item))
    serializer = CartItemSerializer(instance=cart_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, userid, product_id):
    try:
        customer = Customer.objects.get(user_id=userid)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        cart = Cart.objects.filter(customer_id=customer.id).get(complete=False)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    cart_id = cart.id
    try:
        cart_item = CartItem.objects.filter(cart_id=cart_id).get(product_id=product_id)
        cart_item.delete()
        p = Product.objects.get(id=product_id)
        value = p.name + " has been removed"
        context = {"Result": value}
        return Response(context, status=status.HTTP_200_OK)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # serializer = CartItemSerializer(cart_item)
    # return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def add_item_to_cart(request, userid, product_id):
    try:
        customer = Customer.objects.get(user_id=userid)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    try:
        cart = Cart.objects.filter(customer_id=customer.id).get(complete=False)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    cart_id = cart.id
    try:
        cart_item = CartItem.objects.filter(cart_id=cart_id).get(product_id=product_id)
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem(product_id=product_id, quantity=1, cart_id=cart_id)
        cart_item.save()
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_quantity(request, userid, product_id):
    if request.data['quantity']==0:
        context={"Info":"No product added"}
        return Response(context,status=status.HTTP_200_OK)
    try:
        customer = Customer.objects.get(user_id=userid)
    except Customer.DoesNotExist:
        context = {"Result": "Customer ID not found"}
        return Response(context,status=status.HTTP_404_NOT_FOUND)
    try:
        cart = Cart.objects.filter(customer_id=customer.id).get(complete=False)
    except Cart.DoesNotExist:
        cart = Cart(customer=customer, date_modified=datetime.now())
        cart.save()
    cart_id = cart.id
    try:
        # cart_item = CartItem.objects.filter(cart_id=cart_id).get(id=cartItemId)
        cart_item = CartItem.objects.filter(cart_id=cart_id).get(product_id=product_id)
        cart_item.quantity = request.data["quantity"]
        print(request.data)
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem(product_id=product_id, quantity=request.data["quantity"], cart_id=cart_id)
        cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def create_order(requests, userid):
    try:
        customer = Customer.objects.get(user_id=userid)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        cart = Cart.objects.filter(customer_id=customer.id).get(complete=False)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    cart_id = cart.id
    order = Order(status=True, cart=cart, date_ordered=datetime.now())
    order.save()
    cart.complete = True
    cart.save()
    order_id = order.id
    cart_items = CartItem.objects.filter(cart_id=cart_id)
    for x in cart_items:
        p = Product.objects.get(id=x.product_id)
        order_item_true = OrderItemTrue(order=order, product=p, quantity=x.quantity)
        order_item_true.save()
    order_item_list = []
    order_items = OrderItemTrue.objects.filter(order_id=order_id)
    context = {"orderId": order_id}
    for order_item in order_items:
        # print(order_item.id)
        serializer = OrderItemTrueSerializer(order_item)
        print(serializer.data)
        order_item_list.append(serializer.data)
    context["products"] = order_item_list

    return Response(context, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def order_history(requests, userid):
    try:
        customer = Customer.objects.get(user_id=userid)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        cart = Cart.objects.filter(customer_id=customer.id).filter(complete=True)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    cart_id = []
    cart_id = [cart_item.id for cart_item in cart]

    orders_set = Order.objects.filter(cart__id__in=cart_id).filter(status=True)
    order_list = []
    for order in orders_set:
        order_item_list = []
        context = {"orderId": order.id,"date":order.date_ordered,"status":order.status}
        # context={"date":order.date_ordered}
        order_items = OrderItemTrue.objects.filter(order_id=order.id)
        for order_item in order_items:
            # print(order_item.id)
            serializer = OrderItemTrueSerializer(order_item)
            order_item_list.append(serializer.data)
        context["products"] = order_item_list
        order_list.append(context)
    return Response(order_list)

