from django.db import models
# from accounts.models import Account


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField("accounts.Account", null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.user


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    class Meta:
        verbose_name_plural = "Sub-Categories"

    name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, blank=True)
    price = models.FloatField(null=True)
    image = models.ImageField(upload_to='products', default='default.jpg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, to_field='name')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True, to_field='name')
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    # image

    def __str__(self):
        return self.name


class Cart(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_modified = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status_types = [
        ('SHI', 'Shipped'),
        ('DEL', 'Out for Delivery'),
        ('NOT', 'No Info'),
    ]
    status = models.CharField(max_length=3, choices=status_types, default='SHI')

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class OrderItemTrue(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=False, null=True)
    status_types = [
        ('SHI', 'Shipped'),
        ('DEL', 'Out for Delivery'),
        ('NOT', 'No Info'),
    ]
    status = models.CharField(max_length=3, choices=status_types, default='SHI')

    def __str__(self):
        return str(self.id)


class ShippingAddress(models.Model):
    class Meta:
        verbose_name_plural = "Addresses"

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    Order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
