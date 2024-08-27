from django.contrib import admin
from django.urls import path
from financeapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('transactions/', views.fetch_transactions, name='fetch_transactions'),
    path('accounts/', views.plaid_data_view, name='plaid_data_view'),
    path('balances/', views.fetch_account_balances, name='plaid_balance_view'),
]

