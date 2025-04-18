from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")
    address = models.TextField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class Seller(models.Model):
    seller_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
    store_name = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name

    class Meta:
        db_table = 'seller'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")  # Buyer
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.order_id}"

    class Meta:
        db_table = 'order'


class Inbox(models.Model):
    sender = models.ForeignKey(User, related_name="sent_inbox", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_inbox", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="inbox_notifications")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inbox: {self.sender.username} → {self.receiver.username}"

    class Meta:
        db_table = 'inbox'


class AccountBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_balances")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="account_balances")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Balance for {self.user.username}"

    class Meta:
        db_table = 'account_balance'


class PurchaseRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchase_requests")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchase_requests")
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Request: {self.user.username} → {self.product.name}"

    class Meta:
        db_table = 'purchase_request'
