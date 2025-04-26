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



class AccountBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_balances")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="account_balances")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Balance for {self.user.username}"

    class Meta:
        db_table = 'account_balance'

