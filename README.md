# personal-finance-dashboard
Welcome to the Personal Finance Dashboard, a finance management web application that allows users to track, manage, and visualize their financial data through Plaid's sandbox API. This project is designed to demonstrate full stack development using Python, Flask, PostgreSQL, AWS Elastic Beanstalk, and Plaid API integration. It showcases key features like account generation, transaction tracking, and live charting of account balances, making it an excellent portfolio piece for backend, frontend, and full stack development.

## 🚀 Live Demo
The project is hosted on AWS Elastic Beanstalk, making it accessible to users in real-time. Simply visit the hosted URL, register for an account, and get started with demo financial accounts.

## 📋 Table of Contents
Overview
Features
Technologies Used
How to Navigate the App
Planned Features
Installation & Setup
Screenshots
Contributing
License
## 💡 Overview
The Personal Finance Dashboard is a comprehensive tool for managing finances, allowing users to:

- Register and log in to a secure account.
- Automatically generate demo bank accounts and transactions using Plaid’s sandbox API.
- Track balances, deposits, and withdrawals across different accounts.
- Visualise account balances over time using Chart.js.
- Export transaction histories as CSV files for easy financial analysis.

This project demonstrates my ability to build a full stack web application and integrate various third-party APIs while ensuring that the project is scalable through cloud hosting on AWS Elastic Beanstalk.

## ✨ Features
### Current Features:
- **User Authentication**: Secure login and registration with Django’s built-in authentication system.
- **Plaid API Integration**: Generate demo financial accounts and transactions directly from Plaid’s sandbox environment.
- **Transaction Management**: Users can:
  - Deposit and withdraw amounts from demo accounts.
  - Transfer money between accounts.
  - View recent transactions, filtered by date and time.
- **Balance Over Time Visualisation**: Account balances are displayed over time in easy-to-read charts using Chart.js.
- **CSV Export**: Export your account's transaction history as a CSV file with one click.
- **Hosted on AWS**: The app is fully deployed and live on AWS Elastic Beanstalk, ensuring reliability and scalability.

### Planned Features:
- **Two-Factor Authentication (2FA)**: Secure user accounts further by implementing 2FA via email verification during login.
- **Custom Transaction Categorisation**: Allow users to add custom categories to transactions for detailed financial analysis.
- **Budgeting Page**: Let users set budgets for each category to manage their finances more effectively.
- **Date Range Filtering**: Provide more granular filtering of transactions by a customisable date range.
- **User Settings Page**: Create a user settings page to manage preferences and notification settings.
- **Asynchronous Content Loading**: Implement AJAX for a smoother, faster user experience with asynchronous data loading.

## 🛠 Technologies Used
This project is built using a robust stack of modern technologies:

- **Python**: Backend logic and API handling.
- **Flask**: Web framework for building the application.
- **PostgreSQL**: Relational database management for storing users, accounts, and transactions.
- **Django**: For authentication and managing user sessions.
- **Plaid API**: To generate demo financial accounts and transactions.
- **Chart.js**: For rendering dynamic charts that visualise account balances over time.
- **AWS Elastic Beanstalk**: For hosting and scaling the web application.
- **HTML5/CSS3/Bootstrap 5**: For the front-end layout, ensuring responsive design and ease of use.
- **JavaScript (ES6)**: For client-side interactivity.
- **Git/GitHub**: Version control and collaboration.

## 🧭 How to Navigate the App
1. **Register**: Create a new user account via the registration page.
2. **Login**: Use your credentials to log in and access the finance dashboard.
3. **Accounts Page**: If no accounts exist, a "Generate Demo Accounts" button will appear. Click this to automatically generate demo accounts and transactions using the Plaid API.
4. **Transactions**: You can now:
   - View your account balance and recent transactions.
   - Deposit or withdraw funds from an account.
   - Transfer money between accounts.
   - Export transactions to CSV for personal record-keeping.
5. **Visualisations**: See your account balance history in dynamic, responsive charts, with daily balance updates.

## 🛣 Planned Features for Future Releases
These are some features that are currently planned for future releases:

- 2FA Login and Email Verification for enhanced security.
- Custom Categories for transaction classification, allowing for more detailed personal finance management.
- Budgeting Page to help users set and track spending limits in different categories.
- User Preferences and Settings Page for more personalised control of the app's features.
- AJAX and Asynchronous Loading to make the app faster and more responsive without full page reloads.

## 💻 Installation & Setup
If you want to run this project locally, follow these steps:

Clone the repository:
git clone https://github.com/your-username/personal-finance-dashboard.git

Navigate to the project directory:
cd personal-finance-dashboard

Create and activate a virtual environment:
python3 -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

Install the required packages:
pip install -r requirements.txt

Set up PostgreSQL and update your settings.py file with the correct database credentials.
Run migrations:
python manage.py migrate

Add your Plaid API keys in a .env file or set them as environment variables:
PLAID_CLIENT_ID=your_client_id
PLAID_SECRET=your_secret
PLAID_ACCESS_TOKEN=your_access_token

Run the app locally:
python manage.py runserver
Open your browser and go to http://127.0.0.1:8000 to view the app.

## 📸 Screenshots
![Alt text](https://i.imgur.com/f5iVjav.png "Homepage")
![Alt text](https://i.imgur.com/wCFVBqD.png "Accounts Page")


## 🤝 Contributions
Contributions are welcome! Feel free to submit a Pull Request or open an Issue to suggest improvements or report bugs.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
