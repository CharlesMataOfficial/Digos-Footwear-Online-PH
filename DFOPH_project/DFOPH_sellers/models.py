from django.db import models
from DFOPH_accounts.models import User  # import User from accounts app


class SellersProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sellers_profile')
    store_name = models.CharField(max_length=255)
    store_description = models.TextField()

    def __str__(self):
        return self.store_name

    class Meta:
        db_table = 'sellerProfile'

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    seller = models.ForeignKey(SellersProfile, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product'

class Sellers_Inbox(models.Model):
    sender = models.ForeignKey(User, related_name="sellers_sent_inbox", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="sellers_received_inbox", on_delete=models.CASCADE)
    order = models.ForeignKey('DFOPH_buyers.Order', on_delete=models.CASCADE, related_name="sellers_inbox_notifications")
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inbox: {self.sender.username} → {self.receiver.username}"

    class Meta:
        db_table = 'sellers_inbox'
