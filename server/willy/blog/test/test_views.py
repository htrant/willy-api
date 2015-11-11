__author__ = 'hieutran'

from rest_framework import status
from rest_framework.views import APIView
from base.base.base_views import BaseRefiner, BaseResponse
from base.common import error_message, error_code
from blog.test.test_serializers import TestSerializer
from blog.models import AccountToken


##### test api view #####
class TestView(APIView):
    def __init__(self):
        object.__init__(self)
        self.data_response = {}

    def post(self, request):
        serializer = TestSerializer(data=request.DATA)
        if not serializer.is_valid():
            return BaseResponse.send_response(False, error_code.MISSING_REQUIRED_FIELD,
                                              error_message.MISSING_REQUIRED_FIELD, self.data_response,
                                              status.HTTP_200_OK)
        data = BaseRefiner.clean_data(serializer.data)
        token_all = AccountToken.objects.filter(valid_flg=True, type__exact=AccountToken.VERIFY)
        return BaseResponse.send_response(False, error_code.TOKEN_EMPTY_OR_INVALID,
                                              error_message.TOKEN_EMPTY_OR_INVALID, self.data_response,
                                              status.HTTP_200_OK)

    def get(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
