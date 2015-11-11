__author__ = 'hieutran'

from django.db import models


class Account(models.Model):
    email = models.EmailField(null=False, default="")
    password = models.CharField(max_length=128, default="")
    first_name = models.CharField(max_length=30, null=False, default="")
    last_name = models.CharField(max_length=30, null=False, default="")
    username = models.CharField(max_length=30, default="")
    phone = models.CharField(max_length=30, default="")
    facebook_id = models.CharField(max_length=30, default="")
    facebook_flg = models.BooleanField(default=False)
    verified_flg = models.BooleanField(default=False)
    created_date = models.DateTimeField(null=False, auto_now_add=True)
    updated_date = models.DateTimeField(null=False, auto_now_add=True)
    active_flg = models.SmallIntegerField(default=0)


class AccountToken(models.Model):
    ACCESS = 'ac'
    VERIFY = 've'
    TOKEN_TYPE_CHOICES = (
        (ACCESS, 'accessed token'),
        (VERIFY, 'verified token'),
    )
    account = models.ForeignKey(Account)
    token = models.CharField(max_length=128, default="")
    type = models.CharField(max_length=2, choices=TOKEN_TYPE_CHOICES, default=ACCESS)
    created_date = models.DateTimeField(null=False, auto_now_add=True)
    expired_date = models.DateTimeField(null=False, auto_now_add=True)
    valid_flg = models.BooleanField(null=False, default=False)
