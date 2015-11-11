__author__ = 'hieutran'

import hashlib
from datetime import datetime

from django.core.validators import validate_email
from rest_framework import status
from rest_framework.views import APIView

from base.base.base_views import BaseResponse, BaseRefiner
from base.common import error_code, error_message
from blog.account.account_serializers import AccountRegSerializer, AccountVerifySerializer, AccountDetailSerializer
from blog.models import Account, AccountToken
from blog.token.token_services import TokenManager


##### account registration #####
class AccountRegView(APIView):
    def __init__(self):
        object.__init__(self)
        self.data_response = {}

    def post(self, request):
        serializer = AccountRegSerializer(data=request.DATA)
        if not serializer.is_valid():
            return BaseResponse.send_response(False, error_code.MISSING_REQUIRED_FIELD,
                                              error_message.MISSING_REQUIRED_FIELD, self.data_response,
                                              status.HTTP_200_OK)
        data = BaseRefiner.clean_data(serializer.data)
        accounts = Account.objects.filter(email=data['email'])
        if accounts:
            return BaseResponse.send_response(False, error_code.EMAIL_EXISTED, error_message.EMAIL_EXISTED,
                                              self.data_response, status.HTTP_200_OK)
        if not len(data['password']) == 32:
            return BaseResponse.send_response(False, error_code.PASSWORD_INVALID, error_message.PASSWORD_INVALID,
                                              self.data_response, status.HTTP_200_OK)
        if any(i.isdigit() for i in data['first_name']) or any(i.isdigit() for i in data['last_name']):
            return BaseResponse.send_response(False, error_code.NAME_FORMAT, error_message.NAME_FORMAT,
                                              self.data_response, status.HTTP_200_OK)
        try:
            validate_email(data['email'])
        except:
            return BaseResponse.send_response(False, error_code.EMAIL_INVALID, error_message.EMAIL_INVALID,
                                              self.data_response, status.HTTP_200_OK)
        account = Account.objects.create(email=data['email'])
        account.password = hashlib.md5(data['password']).hexdigest()
        account.first_name = data['first_name']
        account.last_name = data['last_name']
        account.created_date = datetime.now()
        account.updated_date = datetime.now()
        account.verified_flg = False
        account.active_flg = 0
        account.save()
        token_verify = TokenManager.generate_token(account, AccountToken.VERIFY)
        # TODO: implement send verification mail
        print token_verify
        # end TODO
        self.data_response = {
            'id': account.id,
            'email': account.email,
            'name': account.first_name + ' ' + account.last_name
        }
        return BaseResponse.send_response(True, error_code.SUCCESSFUL, error_message.SUCCESSFUL, self.data_response,
                                          status.HTTP_200_OK)

    def get(self, request):
        return BaseResponse.send_response(False, error_code.METHOD_NOT_SUPPORT, error_message.METHOD_NOT_SUPPORT,
                                          self.data_response, status.HTTP_200_OK)

    def put(self, request):
        return BaseResponse.send_response(False, error_code.METHOD_NOT_SUPPORT, error_message.METHOD_NOT_SUPPORT,
                                          self.data_response, status.HTTP_200_OK)

    def delete(self, request):
        return BaseResponse.send_response(False, error_code.METHOD_NOT_SUPPORT, error_message.METHOD_NOT_SUPPORT,
                                          self.data_response, status.HTTP_200_OK)


##### account verification #####
class AccountVerifyView(APIView):
    def __init__(self):
        object.__init__(self)
        self.data_response = {}

    def post(self, request):
        serializer = AccountVerifySerializer(data=request.DATA)
        if not serializer.is_valid():
            return BaseResponse.send_response(False, error_code.MISSING_REQUIRED_FIELD,
                                              error_message.MISSING_REQUIRED_FIELD, self.data_response,
                                              status.HTTP_200_OK)
        data = BaseRefiner.clean_data(serializer.data)
        token_all = AccountToken.objects.filter(valid_flg=True, type__exact=AccountToken.VERIFY)
        if token_all:
            for token in token_all:
                if token.token == data['token']:
                    try:
                        account = Account.objects.get(pk=token.account_id)
                        account.active_flg = 1
                        account.verified_flg = True
                        account.updated_date = datetime.now()
                        access_token = TokenManager.generate_token(account, AccountToken.ACCESS)
                        account.save()
                        token.delete()
                        self.data_response = AccountDetailSerializer(account).data
                        self.data_response['id'] = account.id
                        self.data_response['token'] = access_token
                        self.data_response['expired'] = access_token.expired_date
                        return BaseResponse.send_response(True, error_code.SUCCESSFUL, error_message.SUCCESSFUL,
                                                          self.data_response,
                                                          status.HTTP_200_OK)
                    except:
                        return BaseResponse.send_response(False, error_code.SERVER_ERROR, error_message.SERVER_ERROR,
                                                          self.data_response, status.HTTP_200_OK)
                else:
                    pass
        else:
            return BaseResponse.send_response(False, error_code.TOKEN_EMPTY_OR_INVALID,
                                              error_message.TOKEN_EMPTY_OR_INVALID, self.data_response,
                                              status.HTTP_200_OK)

    def get(self, request):
        return BaseResponse.send_response(False, error_code.METHOD_NOT_SUPPORT, error_message.METHOD_NOT_SUPPORT,
                                          self.data_response, status.HTTP_200_OK)

    def put(self, request):
        return BaseResponse.send_response(False, error_code.METHOD_NOT_SUPPORT, error_message.METHOD_NOT_SUPPORT,
                                          self.data_response, status.HTTP_200_OK)

    def delete(self, request):
        return BaseResponse.send_response(False, error_code.METHOD_NOT_SUPPORT, error_message.METHOD_NOT_SUPPORT,
                                          self.data_response, status.HTTP_200_OK)
