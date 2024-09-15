from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from financeapp import views
from financeapp.forms import CustomAuthenticationForm



urlpatterns = [
    path('', views.dashboard, name='home'),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='financeapp/login.html'), name='login'),  # Updated login URL
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Updated logout URL
    path('register/', views.register, name='register'),
    path('accounts/', views.accounts_page, name='accounts'),
    path('accounts/deposit/', views.deposit_amount, name='deposit_amount'),
    path('accounts/withdraw/', views.withdraw_amount, name='withdraw_amount'),
    path('account/<int:account_id>/transactions/', views.account_transactions, name='account_transactions'),
    path('account/<int:account_id>/download_csv/', views.download_csv, name='download_csv'),
    path('balances/', views.fetch_account_balances, name='plaid_balance_view'),
]