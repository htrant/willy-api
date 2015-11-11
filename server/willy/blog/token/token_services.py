__author__ = 'hieutran'

import uuid
from datetime import datetime, timedelta
from blog.models import AccountToken


class TokenManager:
    def __init__(self):
        pass

    @staticmethod
    def generate_token(account, token_type):
        token = AccountToken.objects.create(account=account)
        token.token = uuid.uuid4().hex
        token.type = token_type
        token.created_date = datetime.now()
        token.expired_date = datetime.now() + timedelta(days=30)
        token.valid_flg = True
        token.save()
        return token
