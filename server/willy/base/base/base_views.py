__author__ = 'hieutran'

import datetime, calendar, traceback, sys

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from base_serializers import BaseSerializer
from base.common import error_code, error_message
from blog.models import AccountToken


##### Request helper class #####
class BaseRequest(APIView):
    def post(self, request):
        serializer = BaseSerializer(data=request.data)
        return BaseRequest.generate_response(serializer)

    def get(self, request):
        serializer = BaseSerializer(data=request.query_params)
        return BaseRequest.generate_response(serializer)

    def put(self, request):
        serializer = BaseSerializer(data=request.data)
        return BaseRequest.generate_response(serializer)

    def delete(self, request):
        serializer = BaseSerializer(data=request.query_params)
        return BaseRequest.generate_response(serializer)

    @staticmethod
    def generate_response(serializer):
        if not serializer.is_valid():
            return error_code.SYS_TOKEN_REQUIRED
        data = serializer.data
        token_all = AccountToken.objects.filter(valid_flg=True)
        for token in token_all:
            if token.token == data['token'] and token.type == AccountToken.ACCESS_TOKEN:
                timestamp = calendar.timegm(token.expired_date.timetuple())
                timestamp_now = calendar.timegm(datetime.datetime.now().timetuple())
                if timestamp_now > timestamp:   # expired token
                    token.delete()
                    return error_code.SYS_TOKEN_EXPIRED
                elif token.account.active_flg is not True:   # inactive account
                    token.delete()
                    return error_code.SYS_ACCOUNT_BLOCKED
                else:
                    return token.account_id
        return error_code.SYS_TOKEN_EMPTY_OR_INVALID


##### Response helper class #####
class BaseResponse:
    @staticmethod
    def send_response(is_success, code, message, data, status):
        if data:
            response_data = {
                'success': is_success,
                'code': code,
                'message': message,
                'data': data
            }
        else:
            response_data = {
                'success': is_success,
                'code': code,
                'message': message
            }
        return Response(response_data, status=status)

    @staticmethod
    def send_error_response(code):
        data_response = {}
        if code == error_code.SYS_TOKEN_EMPTY_OR_INVALID:
            return_code = error_code.TOKEN_EMPTY_OR_INVALID
            return_message = error_message.TOKEN_EMPTY_OR_INVALID
        elif code == error_code.SYS_TOKEN_EXPIRED:
            return_code = error_code.TOKEN_EXPIRED
            return_message = error_message.TOKEN_EXPIRED
        elif code == error_code.SYS_ACCOUNT_BLOCKED:
            return_code = error_code.ACCOUNT_BLOCKED
            return_message = error_message.ACCOUNT_BLOCKED
        else:
            return_code = error_code.TOKEN_REQUIRED
            return_message = error_message.TOKEN_REQUIRED
        return BaseResponse.send_response(False, return_code, return_message, data_response, status.HTTP_200_OK)


##### Sanitizer class #####
class BaseRefiner:
    @staticmethod
    def clean_data(data):
        for key in data:
            data[key] = data[key].strip()
        return data
