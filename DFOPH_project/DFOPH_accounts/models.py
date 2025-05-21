from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not password:
            raise ValueError("Superusers must have a password.")
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="users")
    address = models.TextField()
    status = models.CharField(max_length=20)
    last_login = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    
    objects = UserManager()

    USERNAME_FIELD = 'email'  # This is the unique identifier for login
    REQUIRED_FIELDS = ['username', 'role', 'address']  # Required when using createsuperuser

    def __str__(self):
        return self.email

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

