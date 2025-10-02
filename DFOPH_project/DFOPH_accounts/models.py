from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# ==============================
# Role model
# ==============================
class Role(models.Model):
    # Stores the name of the role (e.g., "admin", "buyer", "seller").
    # unique=True ensures that no two roles can have the same name.
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # When we print a Role instance, it shows its name (for readability).
        return self.name

    class Meta:
        db_table = 'role'  # Forces the database table to be named "role".


# ==============================
# Custom User Manager
# ==============================
class UserManager(BaseUserManager):
    # This method is the foundation for creating normal users.
    def create_user(self, email, username, password=None, **extra_fields):
        # Validate required fields
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")

        # Normalize email (converts domain part to lowercase)
        email = self.normalize_email(email)

        # Handle "role" assignment if provided
        role_val = extra_fields.pop("role", None)  # Remove role from extra_fields if present
        if role_val is not None:
            # CASE 1: role is already a Role instance (just use it)
            if isinstance(role_val, Role):
                extra_fields["role"] = role_val
            # CASE 2: role is given as an ID (e.g., 1 or "2"), fetch it from DB
            elif isinstance(role_val, int) or (isinstance(role_val, str) and role_val.isdigit()):
                extra_fields["role"] = Role.objects.get(pk=int(role_val))
            # CASE 3: role is given as a string name (e.g., "admin"), fetch it by name
            elif isinstance(role_val, str):
                extra_fields["role"] = Role.objects.get(name=role_val)

        # Create the user object with given fields
        user = self.model(email=email, username=username, **extra_fields)
        # Use Django’s secure hashing for the password
        user.set_password(password)
        # Save the user to the database
        user.save(using=self._db)
        return user

    # This method is specifically for creating superusers (admins).
    def create_superuser(self, email, username, password=None, **extra_fields):
        # Forcefully set flags needed for a superuser
        extra_fields.setdefault("is_staff", True)      # Can log into admin site
        extra_fields.setdefault("is_superuser", True)  # Has all permissions
        extra_fields.setdefault("is_active", True)     # Account is active

        # Ensure every superuser always has the "admin" role
        admin_role, _ = Role.objects.get_or_create(name="admin")
        extra_fields["role"] = admin_role

        # Superusers must have a password for security reasons
        if not password:
            raise ValueError("Superusers must have a password.")

        # Reuse the create_user logic so we don’t duplicate code
        return self.create_user(email, username, password, **extra_fields)


# ==============================
# Custom User Model
# ==============================
class User(AbstractBaseUser, PermissionsMixin):  
    # Core identity fields
    email = models.EmailField(max_length=255, unique=True)      # Used for login
    username = models.CharField(max_length=150, unique=True)    # Display/username
    first_name = models.CharField(max_length=30, blank=True)    # Optional
    last_name = models.CharField(max_length=30, blank=True)     # Optional
    created_at = models.DateTimeField(auto_now_add=True)        # Timestamp of creation

    # Role is linked with a foreign key (one-to-many: many users can share one role)
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,   # If role is deleted, delete related users
        related_name="users",       # Allows Role.users.all() to fetch users of that role
        null=True, blank=True,      # Role is optional
        default=None
    )

    # Extra profile details
    address = models.TextField(blank=True, null=True, default="")  
    status = models.CharField(max_length=20, default="active")   # e.g., active/inactive
    last_login = models.DateTimeField(null=True, blank=True)     # Tracks last login time

    # Authentication-related fields
    is_active = models.BooleanField(default=True)   # Controls if user can log in
    is_staff = models.BooleanField(default=False)   # Controls access to admin site

    # Connect to custom user manager
    objects = UserManager()

    # Define what field is used to log in (we use email instead of username)
    USERNAME_FIELD = "email"
    # Django will also ask for "username" when creating a user via CLI (createsuperuser)
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        # Represent the user by their email (for readability in admin, shell, etc.)
        return self.email

    class Meta:
        db_table = 'user'  # Explicitly set database table name


# ==============================
# Account Balance model
# ==============================
class AccountBalance(models.Model):
    # Link to User (one user can have multiple balances for different roles)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_balances")
    # Link to Role (balance depends on the role, e.g., seller’s earnings vs buyer’s wallet)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="account_balances")
    # Numeric balance value (money), with precision up to 10 digits and 2 decimals
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Auto-updated timestamp every time the record is modified
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Example: "Balance for johndoe"
        return f"Balance for {self.user.username}"

    class Meta:
        db_table = 'account_balance'  # Explicitly set database table name
