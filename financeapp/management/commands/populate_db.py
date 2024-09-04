from django.core.management.base import BaseCommand
from plaid.api import plaid_api
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.api_client import ApiClient
from decouple import config
from financeapp.models import Account
from django.contrib.auth.models import User
import plaid

class Command(BaseCommand):
    help = 'Populate the database with account and transaction data from Plaid'

    def handle(self, *args, **kwargs):
        # Fetch Plaid credentials from environment variables
        client_id = config('PLAID_CLIENT_ID')
        secret = config('PLAID_SECRET')
        access_token = config('PLAID_ACCESS_TOKEN')
        
        print(f"Client ID: {client_id}, Secret: {secret}, Access Token: {access_token}")
        
        # Plaid client setup
        configuration = plaid.Configuration(
            host=plaid.Environment.Sandbox,
            api_key={
                'clientId': client_id,
                'secret': secret
            }
        )
        api_client = ApiClient(configuration)
        client = plaid_api.PlaidApi(api_client)

        try:
            # Create the request to fetch account data
            request = AccountsGetRequest(access_token=access_token)
            response = client.accounts_get(request)
            accounts = response.to_dict().get('accounts', [])
            
            # Print fetched accounts for debugging
            print(f"Fetched accounts: {accounts}")

            # Save fetched accounts to the database
            user = User.objects.first()  # Assuming you have a default user to link accounts
            if not user:
                print("Error: No user found to link accounts. Create a user first.")
                return

            for account in accounts:
                Account.objects.update_or_create(
                    plaid_account_id=account['account_id'],
                    defaults={
                        'user': user,
                        'name': account['name'],
                        'account_type': account['subtype'],
                        'balance': account['balances']['current'],
                    }
                )
            print("Accounts saved to the database successfully.")

        except plaid.ApiException as e:
            print(f"Error populating database: {e}")
