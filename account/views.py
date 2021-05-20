from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm, EditAccountForm
# from django.urls import reverse_lazy
# from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# from chechout.models import Order, OrderHasProduct


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
    # orders = Order.objects.filter(user=user)
    # array = []
    # for order in orders:
    #     one_id = order.id
    #     one_order = get_object_or_404(Order, id=one_id)
    #     orderhasproduct = OrderHasProduct.objects.filter(order = one_order)
    #     for o in orderhasproduct:
    #         array.append(o)
    # return render(request,'account.html', {'orders':orders, 'array':array})
    return render(request, 'account.html', {'user': user})


# def edit_account(response):
#     if response.method == "POST":
#         form = EditAccountForm(response.POST, instance=response.user)
#         if form.is_valid():
#             form.save()
#             return redirect('/accounts/account')
#     else:
#         form = EditAccountForm(instance=response.user)
#     return render(response, 'edit_account.html',{"form": form})
