from django.db import models
from DFOPH_accounts.models import User  # import User from accounts app
from DFOPH_sellers.models import Product


class BuyersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyers_profile')
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f"Username:  {self.user.username}"

    class Meta:
        db_table = 'buyers_profile'
    
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey('DFOPH_sellers.Product', on_delete=models.CASCADE, related_name="orders")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")  # Buyer
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.order_id}"

    class Meta:
        db_table = 'order'

class Buyers_Inbox(models.Model):
    sender = models.ForeignKey(User, related_name="buyers_sent_inbox", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="buyers_received_inbox", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="buyers_inbox_notifications")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inbox: {self.sender.username} → {self.receiver.username}"

    class Meta:
        db_table = 'buyers_inbox'

class PurchaseRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchase_requests")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="purchase_requests")
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"Request: {self.user.username} → {self.product.name}"

    class Meta:
        db_table = 'purchase_request'
