from django.core.management.base import BaseCommand
from plaid.model.item_webhook_update_request import ItemWebhookUpdateRequest
from plaid.api.plaid_api import PlaidApi
from plaid import ApiClient, Configuration, Environment
import os

class Command(BaseCommand):
    help = 'Updates the webhook for the Plaid sandbox item'

    def handle(self, *args, **kwargs):
        # Initialize the Plaid client
        configuration = Configuration(
            host=Environment.Sandbox,
            api_key={
                'clientId': os.getenv('PLAID_CLIENT_ID'),
                'secret': os.getenv('PLAID_SECRET'),
            }
        )
        api_client = ApiClient(configuration)
        client = PlaidApi(api_client)

        # Set the access token
        access_token = os.getenv('PLAID_ACCESS_TOKEN')

        # Update the webhook for the item
        webhook_url = "https://example.com/webhook"  # This is a placeholder URL
        
        request = ItemWebhookUpdateRequest(
            access_token=access_token,
            webhook=webhook_url
        )

        # Call the Plaid API to update the webhook
        try:
            response = client.item_webhook_update(request)
            self.stdout.write(self.style.SUCCESS(f"Webhook updated: {response}"))
        except Exception as e:
            self.stderr.write(f"Error updating webhook: {e}")
