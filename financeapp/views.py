from django.shortcuts import render, redirect, get_object_or_404
from plaid import ApiClient,Configuration
from plaid.api import plaid_api
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from decouple import config
from datetime import datetime, timedelta, date
from .models import Account, Transaction
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomAuthenticationForm
import csv
from collections import defaultdict
from decimal import Decimal

import json


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


@login_required
def dashboard(request):
    # Fetch all accounts for the logged-in user
    accounts = Account.objects.filter(user=request.user)

    # Calculate the total balance across all accounts
    total_balance = sum(account.balance for account in accounts)

    # Fetch recent transactions (last 30 days)
    today = timezone.now()
    last_30_days = today - timedelta(days=30)
    recent_transactions = Transaction.objects.filter(
        account__user=request.user, date__gte=last_30_days
    ).order_by('-date')[:5]  # Show the 5 most recent transactions

    # Placeholder growth calculation
    growth = "6.18%"

    context = {
        'total_balance': total_balance,
        'growth': growth,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'financeapp/dashboard.html', context)

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



@login_required
def accounts_page(request):
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        amount = float(request.POST.get('amount'))
        account = Account.objects.get(id=account_id, user=request.user)

        if 'deposit' in request.path:
            account.balance += Decimal(amount)
            description = "Deposit"
        elif 'withdraw' in request.path:
            account.balance -= Decimal(amount)
            description = "Withdrawal"
        
        account.save()

        # Create the transaction
        Transaction.objects.create(
            account=account,
            date=timezone.now(),
            description=description,
            amount=Decimal(amount)
        )
        
        # Redirect back to the accounts page after successful transaction
        return redirect('accounts')

    # Modify query to order accounts by 'id'
    user_accounts = Account.objects.filter(user=request.user).order_by('id')
    accounts = []
    no_accounts = not user_accounts.exists()

    for account in user_accounts:
        transactions = Transaction.objects.filter(account=account).order_by('date')

        # Group transactions by date to only keep the last transaction per day
        grouped_transactions = defaultdict(list)
        for transaction in transactions:
            transaction_date = transaction.date.date()
            grouped_transactions[transaction_date].append(transaction)

        filtered_transactions = [transactions[-1] for date, transactions in grouped_transactions.items()]

        # Start with the current balance (use actual balance for consistency)
        current_balance = float(account.balance)

        # Prepare data for chart (balance over time)
        dates = []
        balances = []

        for transaction in filtered_transactions[::-1]:
            dates.insert(0, transaction.date.strftime("%Y-%m-%d"))
            balances.insert(0, float(current_balance))
            current_balance -= float(transaction.amount)

        today = timezone.now().strftime("%Y-%m-%d")
        if transactions and dates[-1] != today:
            dates.append(today)
            balances.append(float(account.balance))

        accounts.append({
            'id': account.id,
            'name': account.name,
            'balance': account.balance,
            'account_type': account.account_type,
            'available_balance': account.balance,
            'transactions': transactions[::-1],
            'chart_dates': json.dumps(dates),
            'chart_balances': json.dumps(balances),
        })

    return render(request, 'financeapp/accounts.html', {
        'accounts': accounts,
        'no_accounts': no_accounts  
    })














def account_transactions(request, account_id):
    account = Account.objects.get(id=account_id)
    start_date = request.GET.get('start_date', (timezone.now() - timedelta(days=30)).date())
    end_date = request.GET.get('end_date', timezone.now().date())
    transactions = Transaction.objects.filter(account=account, date__range=[start_date, end_date])
    
    # You can also generate balance history for the chart here
    balance_history = []  # Placeholder for balance vs date data

    return render(request, 'financeapp/account_details.html', {
        'account': account,
        'transactions': transactions,
        'balance_history': balance_history
    })
    
def download_csv(request, account_id):
    account = Account.objects.get(id=account_id)
    transactions = Transaction.objects.filter(account=account)
    
    # Set up the response with content type 'text/csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{account.name}_transactions.csv"'

    writer = csv.writer(response)
    # Write the CSV headers
    writer.writerow(['Date', 'Description', 'Amount', 'Category'])
    
    # Write each transaction's data
    for transaction in transactions:
        writer.writerow([transaction.date, transaction.description, transaction.amount, transaction.category])

    return response

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'financeapp/register.html', {'form': form})


@login_required
def deposit_amount(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        account_id = request.POST.get('account_id')

        if not account_id:
            return redirect('accounts')  # Redirect on error

        try:
            account = Account.objects.get(id=account_id, user=request.user)
        except Account.DoesNotExist:
            return redirect('accounts')  # Redirect on invalid account

        try:
            amount = Decimal(amount)  # Convert to Decimal
        except:
            return redirect('accounts')  # Redirect on invalid amount

        if amount > 0 and amount <= Decimal('25000'):
            # Update account balance and save the transaction
            account.balance += amount
            account.save()

            # Create a new transaction
            Transaction.objects.create(
                account=account,
                date=timezone.now(),
                description="Deposit",
                amount=amount
            )

    return redirect('accounts')  # Always redirect after processing


@login_required
def withdraw_amount(request):
    if request.method == "POST":
        amount = request.POST.get('amount')
        account_id = request.POST.get('account_id')

        if not account_id:
            return redirect('accounts')  # Redirect on error

        try:
            account = Account.objects.get(id=account_id, user=request.user)
        except Account.DoesNotExist:
            return redirect('accounts')  # Redirect on invalid account

        try:
            amount = Decimal(amount)  # Convert to Decimal
        except:
            return redirect('accounts')  # Redirect on invalid amount

        # Max withdrawal amount logic
        if amount > 0 and amount <= Decimal('5000'):
            if account.balance >= amount:
                # Update account balance and save the transaction
                account.balance -= amount
                account.save()

                # Create a new transaction
                Transaction.objects.create(
                    account=account,
                    date=timezone.now(),
                    description="Withdrawal",
                    amount=-amount  # Negative for withdrawal
                )

            else:
                return redirect('accounts')  # Redirect on insufficient funds

    return redirect('accounts')  # Always redirect after processing

@login_required
def generate_demo_accounts(request):
    try:
        # Plaid API to simulate accounts and transactions in the sandbox
        access_token = config('PLAID_ACCESS_TOKEN')
        accounts_request = AccountsGetRequest(access_token=access_token)
        response = client.accounts_get(accounts_request)

        # Loop over the accounts and save them to the database
        for account_data in response['accounts']:
            account = Account.objects.create(
                user=request.user,
                name=account_data['name'],
                balance=account_data['balances']['current'],
                account_type=account_data['subtype']
            )

            # Use actual datetime.date objects for the start and end dates
            start_date = datetime(2023, 1, 1).date()  # Example start date
            end_date = datetime(2024, 1, 1).date()    # Example end date

            # Generate some fake transactions for the account
            transactions_request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date
                # Remove 'account_ids' as it's not valid in the sandbox
            )
            transactions_response = client.transactions_get(transactions_request)

            for txn in transactions_response['transactions']:
                Transaction.objects.create(
                    account=account,
                    date=txn['date'],
                    description=txn['name'],
                    amount=txn['amount']
                )

        return redirect('accounts')  # After generating, redirect to the accounts page

    except Exception as e:
        print(f"Error generating demo accounts: {e}")
        return JsonResponse({'error': str(e)}, status=400)
    

def transfer_money(request):
    if request.method == 'POST':
        try:
            from_account_id = request.POST.get('from_account_id')
            to_account_id = request.POST.get('to_account_id')
            amount = Decimal(request.POST.get('amount'))

            # Fetch the accounts
            from_account = get_object_or_404(Account, id=from_account_id, user=request.user)
            to_account = get_object_or_404(Account, id=to_account_id, user=request.user)

            # Ensure enough balance in the from account for the transfer
            if from_account.balance >= amount:
                # Withdraw from the 'from' account
                from_account.balance -= amount
                from_account.save()

                # Deposit into the 'to' account
                to_account.balance += amount
                to_account.save()

                # Create transaction entries for both accounts
                Transaction.objects.create(
                    account=from_account, 
                    amount=-amount, 
                    description=f"Transfer to {to_account.name}"
                    # created_at will automatically be filled
                )
                Transaction.objects.create(
                    account=to_account, 
                    amount=amount, 
                    description=f"Transfer from {from_account.name}"
                    # created_at will automatically be filled
                )

                # Redirect or return a success response
                return redirect('accounts')

            else:
                return JsonResponse({'error': 'Insufficient funds in the selected account'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

