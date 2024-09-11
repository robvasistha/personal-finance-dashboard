from django.core.management.base import BaseCommand
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.sandbox_item_fire_webhook_request import SandboxItemFireWebhookRequest
from plaid import ApiClient, Configuration, Environment
from plaid.api import plaid_api
from financeapp.models import Account, Transaction
from datetime import datetime, timedelta, date
import os

class Command(BaseCommand):
    help = 'Simulates transactions in Plaid sandbox and saves them to the database'

    def handle(self, *args, **kwargs):
        # Correct Plaid client initialization with ApiClient and Configuration
        configuration = Configuration(
            host=Environment.Sandbox,  # Sandbox environment
            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SECRET'),
            }
        )
        
        # Initialize the ApiClient using the configuration
        api_client = ApiClient(configuration)

        # Use the initialized client to create a Plaid API client
        client = plaid_api.PlaidApi(api_client)

        access_token = os.getenv('PLAID_ACCESS_TOKEN')  # Use your actual sandbox access token

        try:
            # Simulate transactions for a Plaid Sandbox account by firing a webhook event
            webhook_code = 'DEFAULT_UPDATE'  # webhook that simulates a transactions update
            sandbox_item_fire_webhook_request = SandboxItemFireWebhookRequest(
                access_token=access_token,
                webhook_code=webhook_code
            )
            client.sandbox_item_fire_webhook(sandbox_item_fire_webhook_request)
            self.stdout.write(self.style.SUCCESS(f"Transaction simulation webhook fired: {webhook_code}"))

            # Fetch transactions for the past 30 days
            start_date = datetime.now().date() - timedelta(days=30)  # This will be a `date` object, not a string
            end_date = datetime.now().date()  # This will also be a `date` object

            transactions_request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,  # Pass as a `date` object
                end_date=end_date  # Pass as a `date` object
            )

            transactions_response = client.transactions_get(transactions_request)
            transactions = transactions_response['transactions']

            # Save transactions to the database
            for transaction in transactions:
                account = Account.objects.get(plaid_account_id=transaction['account_id'])
                Transaction.objects.create(
                    account=account,
                    plaid_transaction_id=transaction['transaction_id'],
                    date=transaction['date'],
                    description=transaction['name'],
                    amount=transaction['amount'],
                    category=transaction.get('category', [None])[0]
                )

            self.stdout.write(self.style.SUCCESS('Transactions successfully simulated and saved.'))

        except Exception as e:
            self.stderr.write(f"Error simulating transactions: {e}")
