__author__ = 'hieutran'

from rest_framework import serializers
from blog.models import Account, AccountToken


class AccountRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password', 'first_name', 'last_name')


class AccountVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountToken
        fields = ('token',)


class AccountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'email', 'username', 'first_name', 'last_name', 'phone', 'created_date', 'updated_date', 'active_flg')
