__author__ = 'hieutran'

from rest_framework import serializers
from blog.models import AccountToken


class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountToken
        fields = ('token',)
