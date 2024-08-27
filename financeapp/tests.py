from django.test import TestCase  # Import TestCase
from django.contrib.auth.models import User  # Import the User model
from .models import Account, Transaction  # Import the models you want to test

class AccountModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create an account associated with the user
        self.account = Account.objects.create(
            user=self.user,  # Associate the account with the user
            name="Test Account",
            balance=1000.00,
            account_type="Checking"
        )

    def test_account_creation(self):
        self.assertEqual(self.account.name, "Test Account")
        self.assertEqual(self.account.balance, 1000.00)
        self.assertEqual(self.account.account_type, "Checking")

class TransactionModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')

        # Create an account associated with the user
        self.account = Account.objects.create(
            user=self.user,  # Associate the account with the user
            name="Test Account",
            balance=1000.00,
            account_type="Checking"
        )

        # Create a transaction associated with the account
        self.transaction = Transaction.objects.create(
            account=self.account,
            amount=-100.00,
            description="Test Transaction",
            date="2024-08-30 00:00:00",
            category="Groceries"
        )

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.amount, -100.00)
        self.assertEqual(self.transaction.description, "Test Transaction")
        self.assertEqual(self.transaction.category, "Groceries")
