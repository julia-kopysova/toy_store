import logging
import sys

from django.shortcuts import render, redirect, get_object_or_404
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
    # receipts = Receipt.objects.filter(user=user)
    receipts = Receipt.objects.raw("SELECT * FROM receipt_receipt WHERE user_id = %s", [user.id])
    list_receipts = []
    for receipt in receipts:
        one_id = receipt.id
        # one_receipt = get_object_or_404(Receipt, id=one_id)
        one_receipt = Receipt.objects.raw("SELECT * FROM receipt_receipt WHERE id = %s", [one_id])[0]
        receipt_toy = ReceiptHasToy.objects.filter(receipt=one_receipt)
        receipt_toy = ReceiptHasToy.objects.raw("SELECT * FROM receipt_receipthastoy WHERE receipt_id = %s",
                                                [one_receipt.id])
        for position in receipt_toy:
            list_receipts.append(position)
    return render(request, 'account.html', {'receipts': receipts, 'list_receipts': list_receipts, 'user': user})
    # return render(request, 'account.html', {'user': user})

# def edit_account(response):
#     if response.method == "POST":
#         form = EditAccountForm(response.POST, instance=response.user)
#         if form.is_valid():
#             form.save()
#             return redirect('/accounts/account')
#     else:
#         form = EditAccountForm(instance=response.user)
#     return render(response, 'edit_account.html',{"form": form})
