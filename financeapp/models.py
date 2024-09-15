from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    """
    Represents a financial account associated with a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plaid_account_id = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50)  # e.g., 'Checking', 'Savings'
    balance = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.account_type}"


class Transaction(models.Model):
    """
    Represents a transaction that occurs within an account.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    plaid_transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)  # Plaid's Transaction ID
    date = models.DateTimeField()
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=100, null=True, blank=True)  # e.g., 'Groceries', 'Utilities'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"


class Subscription(models.Model):
    """
    Represents a recurring subscription linked to an account.
    """
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateTimeField()
    renewal_period = models.CharField(max_length=50)  # e.g., 'Monthly', 'Yearly'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents a user-defined tag for categorizing transactions.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Budget(models.Model):
    """
    Represents a budget for a specific category or tag.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Budget for {self.tag.name} - {self.amount}"


class UserProfile(models.Model):
    """
    Represents an extended profile for the user.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_currency = models.CharField(max_length=10, default='USD')
    two_factor_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class UserSettings(models.Model):
    """
    Represents user-specific settings like display preferences.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Settings for {self.user.username}"
