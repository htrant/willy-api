__author__ = 'hieutran'

from rest_framework import serializers
from blog.models import AccountToken


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountToken
        fields = ('token',)
