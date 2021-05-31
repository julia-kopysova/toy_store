import logging
import sys

from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from receipt.models import Receipt, ReceiptHasToy

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}
logging.config.dictConfig(LOGGING)


def signup(response):
    if response.method == "POST":
        form = SignUpForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(response, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(response, 'signup.html', {"form": form})


def change_password(response):
    if response.method == "POST":
        form = PasswordChangeForm(data=response.POST, user=response.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(response, form.user)
            return redirect('/accounts/account')
        else:
            return redirect('/accounts/account/change_password')
    else:
        form = PasswordChangeForm(user=response.user)
    return render(response, 'change_password.html', {"form": form})


def own_account(request):
    user = request.user
    receipts = Receipt.objects.raw("SELECT * FROM receipt_receipt WHERE user_id = %s", [user.id])
    dict_receipts = {}
    for receipt in receipts:
        one_id = receipt.id
        one_receipt = Receipt.objects.raw("SELECT * FROM receipt_receipt WHERE id = %s", [one_id])[0]
        dict_receipts[one_receipt] = []
        receipt_toy = ReceiptHasToy.objects.raw("SELECT *  FROM receipt_receipthastoy JOIN product_toy ON "
                                                "receipt_receipthastoy.toy_id = product_toy.id "
                                                "WHERE receipt_receipthastoy.receipt_id = %s", [one_receipt.id])
        for position in receipt_toy:
            dict_receipts[one_receipt].append(position)
    return render(request, 'account.html', {'receipts': receipts, 'dict_receipts': dict_receipts, 'user': user})
