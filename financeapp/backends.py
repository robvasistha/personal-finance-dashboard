from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
import logging

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Try finding user by email first, then by username
            user = User.objects.get(email=username)
            logging.info(f'User found by email: {user.username}')
        except User.DoesNotExist:
            try:
                user = User.objects.get(username=username)
                logging.info(f'User found by username: {user.username}')
            except User.DoesNotExist:
                logging.error(f'User not found for {username}')
                return None
        
        # Check if the password is correct
        if user.check_password(password):
            return user
        else:
            logging.error(f'Password check failed for {username}')
            return None
