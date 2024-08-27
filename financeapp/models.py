from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    """
    Represents a financial account associated with a user.

    Attributes:
        user (ForeignKey): Reference to the Django User model.
        name (CharField): The name of the account (e.g., Checking, Savings).
        account_type (CharField): Type of the account (e.g., Checking, Savings).
        balance (DecimalField): Current balance of the account.
        created_at (DateTimeField): Timestamp when the account was created.
    """
    
    user: User = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name: str = models.CharField(max_length=100)
    account_type: str = models.CharField(max_length=50)  # e.g., 'Checking', 'Savings'
    balance: float = models.DecimalField(max_digits=10, decimal_places=2)
    created_at: str = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        String representation of the Account object.

        Returns:
            str: The name of the account.
        """
        return self.name


class Transaction(models.Model):
    """
    Represents a transaction that occurs within an account.

    Attributes:
        account (ForeignKey): Reference to the associated account.
        date (DateTimeField): The date and time of the transaction.
        description (CharField): Brief description of the transaction.
        amount (DecimalField): Amount of money involved in the transaction.
        category (CharField): Category of the transaction (e.g., Groceries, Utilities).
        created_at (DateTimeField): Timestamp when the transaction was created.
    """
    
    account: Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date: str = models.DateTimeField()
    description: str = models.CharField(max_length=255)
    amount: float = models.DecimalField(max_digits=10, decimal_places=2)
    category: str = models.CharField(max_length=100)  # e.g., 'Groceries', 'Utilities'
    created_at: str = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        String representation of the Transaction object.

        Returns:
            str: A brief summary of the transaction.
        """
        return f"{self.description} - {self.amount}"


class Subscription(models.Model):
    """
    Represents a recurring subscription linked to an account.

    Attributes:
        account (ForeignKey): Reference to the associated account.
        name (CharField): The name of the subscription (e.g., Netflix, Spotify).
        amount (DecimalField): Amount charged for the subscription.
        start_date (DateTimeField): The start date of the subscription.
        renewal_period (CharField): The renewal period of the subscription (e.g., Monthly, Yearly).
    """
    
    account: Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name: str = models.CharField(max_length=100)
    amount: float = models.DecimalField(max_digits=10, decimal_places=2)
    start_date: str = models.DateTimeField()
    renewal_period: str = models.CharField(max_length=50)  # e.g., 'Monthly', 'Yearly'
    
    def __str__(self) -> str:
        """
        String representation of the Subscription object.

        Returns:
            str: The name of the subscription.
        """
        return self.name