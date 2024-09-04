from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from financeapp import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', views.accounts_page, name='accounts'), 
    path('account/<int:account_id>/transactions/', views.account_transactions, name='account_transactions'),
    path('account/<int:account_id>/download_csv/', views.download_csv, name='download_csv'),
    path('balances/', views.fetch_account_balances, name='plaid_balance_view'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='financeapp/login.html'), name='login'),
]

