from django.shortcuts import render
from plaid import ApiClient,Configuration
from plaid.api import plaid_api
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from decouple import config
from datetime import datetime, timedelta, date

# Set up Plaid client
configuration = Configuration(
    host="https://sandbox.plaid.com",
    api_key={
        "clientId": config('PLAID_CLIENT_ID'),
        "secret": config('PLAID_SECRET'),
    }
)
api_client = ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

def fetch_transactions(request):
    """
    Fetches transactions for a specific date range and renders them in the dashboard.
    """
    # Use the access token from the environment
    access_token = config('PLAID_ACCESS_TOKEN')

    # Set default date range (last 30 days)
    start_date = request.GET.get('start_date', (datetime.now().date() - timedelta(days=30)))
    end_date = request.GET.get('end_date', datetime.now().date())

    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)

    try:
        # Fetch transactions from Plaid
        transactions_request = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        transactions_response = client.transactions_get(transactions_request)
        transactions = transactions_response['transactions']

        # Render the transactions in the dashboard
        return render(request, 'financeapp/dashboard.html', {'transactions': transactions})
    except Exception as e:
        print("Error fetching transactions:", e)
        return render(request, 'financeapp/dashboard.html', {'error': str(e)})

def plaid_data_view(request):
    """
    Fetches account details and renders them in the dashboard.
    """
    client_id = config('PLAID_CLIENT_ID')
    secret = config('PLAID_SECRET')
    access_token = config('PLAID_ACCESS_TOKEN', default='access-sandbox-12345678-1234-1234-1234-1234567890ab')

    print(f"Client ID: {client_id}, Secret: {secret}, Access Token: {access_token}")

    try:
        accounts_request = AccountsGetRequest(
            access_token=access_token
        )
        response = client.accounts_get(accounts_request)
        accounts = response['accounts']

        # Render the accounts in the dashboard
        return render(request, 'financeapp/dashboard.html', {'accounts': accounts})

    except Exception as e:
        print(f"Error fetching account details: {e}")
        return render(request, 'financeapp/dashboard.html', {'error': str(e)})

def fetch_account_balances(request):
    """
    Fetches account balances and renders them in the dashboard.
    """
    client_id = config('PLAID_CLIENT_ID')
    secret = config('PLAID_SECRET')
    access_token = config('PLAID_ACCESS_TOKEN', default='access-sandbox-12345678-1234-1234-1234-1234567890ab')

    print(f"Client ID: {client_id}, Secret: {secret}, Access Token: {access_token}")

    try:
        balances_request = AccountsBalanceGetRequest(
            access_token=access_token
        )
        response = client.accounts_balance_get(balances_request)
        balances = response['accounts']

        # Render the account balances in the dashboard
        return render(request, 'financeapp/dashboard.html', {'balances': balances})

    except Exception as e:
        print(f"Error fetching account balances: {e}")
        return render(request, 'financeapp/dashboard.html', {'error': str(e)})
