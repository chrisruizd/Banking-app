from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login, logout

T_FLAG = 0

# Create your views here.
def home(request):
    return render(request, 'bank/home.html')

def about(request):
    return render(request, 'bank/about.html')
"""
def login_user(request):
    if request.method == "POST":
        username1 = request.POST.get['username']
        password = request.POST.get['password']
        user = authenticate(request, username=username1, psw=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'You have been logged in!')

            return redirect('bank-home')
        else:
            messages.error(request, f'There was an error')
            return redirect('bank-login')
        
    return render(request, 'bank/login.html')
"""
def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid(): #validate form
            user = form.save()  #save user on database
            messages.success(request, f'Your user account has been created successfully!')

            # create a profile for the new user
            profile = Profile.objects.create(user=user, 
                                             Fname=form.cleaned_data.get('Fname'),
                                              Lname=form.cleaned_data.get('Lname'), 
                                              DOB=form.cleaned_data.get('DOB'),
                                              email=form.cleaned_data.get('email'), 
                                              country=form.cleaned_data.get('country'),
                                              city=form.cleaned_data.get('city'))


            login(request, user)    #not sure 
            return redirect('bank-profile')
    else:
        form = UserRegisterForm()
    
    return render(request, 'bank/signup.html', {'form': form})


#def logout_user(request):
    
#when I sign up and the profile page is opened it does not detects the user
#not making the connection btw profile and user
@login_required
def profile(request):
    user = request.user
    accounts = Account.objects.filter(a_username__user=request.user)
    transactions = Transactions.objects.filter(acc_num__a_username=user.profile).order_by('-date_time')
    context = {'user': user, 'accounts': accounts, 'transactions': transactions, 'T_FLAG': T_FLAG}

    return render(request, 'bank/profile.html', context)


@login_required
def createAcc(request):
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.a_username = request.user.profile
            account.save()
            messages.success(request, 'Account created successfully.')
            return redirect('bank-profile')
    else:
        form = CreateAccountForm()
    return render(request, 'bank/createAcc.html', {'form': form})



@login_required
def deposit(request):
    user = request.user
    accounts = Account.objects.filter(a_username=user.profile)

    if request.method == 'POST':
        form = PerformDeposit(request.POST, user=user.profile)
        if form.is_valid():
            transaction = form.save(commit=False)
            account_number = form.cleaned_data['acc_num']
            amount = form.cleaned_data['tamount']
            # Retrieve the account based on the account number entered by the user
            try:
                account = Account.objects.get(acc_num=account_number, a_username=request.user.profile)
            except Account.DoesNotExist:
                form.add_error('acc_num', 'Invalid account number')
                return render(request, 'bank/deposit.html', {'form': form, 'accounts': accounts})


            # Check that the account belongs to the logged-in user
            if account.a_username != user.profile:
                form.add_error('acc_num', 'Invalid account number')
                return render(request, 'bank/deposit.html', {'form': form, 'accounts': accounts})

            # Update the account balance and save the transaction
            account.balance += transaction.tamount
            account.save()

            transaction.tr_type = 'D'
            transaction.acc_num = account
            transaction.save()

            messages.success(request, f'Deposit of {amount} successfully made to account {account_number}.')
            return redirect('bank-profile')
    else:
        form = PerformDeposit(user=user.profile)
    
    return render(request, 'bank/deposit.html', {'form': form, 'accounts': accounts})



@login_required
def withdraw(request):
    user = request.user
    accounts = Account.objects.filter(a_username=user.profile)

    if request.method == 'POST':
        form = PerformDeposit(request.POST, user=user.profile)
        if form.is_valid():
            transaction = form.save(commit=False)
            account_number = form.cleaned_data['acc_num']
            amount = form.cleaned_data['tamount']
            # Retrieve the account based on the account number entered by the user
            try:
                account = Account.objects.get(acc_num=account_number, a_username=request.user.profile)
            except Account.DoesNotExist:
                form.add_error('acc_num', 'Invalid account number')
                return render(request, 'bank/withdraw.html', {'form': form, 'accounts': accounts})


            # Check that the account belongs to the logged-in user
            if account.a_username != user.profile:
                form.add_error('acc_num', 'Invalid account number')
                return render(request, 'bank/withdraw.html', {'form': form, 'accounts': accounts})

            if amount > account.balance:
                messages.warning(request, f'Opss! Trying to withdraw more money than you have.')
                return render(request, 'bank/send.html', {'form': form, 'accounts': accounts})

            # Update the account balance and save the transaction
            account.balance -= transaction.tamount
            account.save()

            transaction.tr_type = 'W'
            transaction.acc_num = account
            transaction.save()

            messages.success(request, f'Withdraw of {amount} successfully made to account {account_number}.')
            return redirect('bank-profile')
    else:
        form = PerformDeposit(user=user.profile)
    
    return render(request, 'bank/withdraw.html', {'form': form, 'accounts': accounts})

#fields = ['sender_acc', 'receip_acc', 'amount']





@login_required
def transfer(request):
    user = request.user
    accounts = Account.objects.filter(a_username=user.profile)

    if request.method == 'POST':
        form = PerformTransfer(request.POST, user=user.profile)
        if form.is_valid():
            transfer = form.save(commit=False)
            account_num_send = form.cleaned_data['sender_acc']
            account_num_rec = form.cleaned_data['receip_acc']
            if account_num_send == account_num_rec:
                messages.success(request, f'Invalid Transfer. Please try again')
                form.add_error('receip_acc', 'Select different account')
                return render(request, 'bank/transfer.html', {'form': form, 'accounts': accounts})

            amount = form.cleaned_data['amount']
            # Retrieve the account based on the account number entered by the user
            try:
                account_S = Account.objects.get(acc_num=account_num_send, a_username=request.user.profile)
                account_R = Account.objects.get(acc_num=account_num_rec, a_username=request.user.profile)
            except Account.DoesNotExist:
                form.add_error('sender_acc', 'Invalid account number')
                return render(request, 'bank/transfer.html', {'form': form, 'accounts': accounts})


            # Check that the account belongs to the logged-in user
            if account_S.a_username != user.profile:
                form.add_error('sender_acc', 'Invalid account number')
                return render(request, 'bank/transfer.html', {'form': form, 'accounts': accounts})


            if amount > account_S.balance:
                messages.warning(request, f'Opss! Trying to transfer more money than you have.')
                return render(request, 'bank/send.html', {'form': form, 'accounts': accounts})

            # Update the account balance and save the transaction
            account_S.balance -= transfer.amount
            account_R.balance += transfer.amount
            account_S.save()
            account_R.save()

            transfer.sender_acc = account_S
            transfer.receip_acc = account_R
            transfer.save()

            messages.success(request, f'Transfer of {amount} successfully made to account {account_num_rec}.')
            return redirect('bank-profile')
    else:
        form = PerformTransfer(user=user.profile)
    
    return render(request, 'bank/transfer.html', {'form': form, 'accounts': accounts})



@login_required
def send(request):
    user = request.user
    accounts = Account.objects.filter(a_username=user.profile)

    if request.method == 'POST':
        form = PerformUserSend(request.POST, user=user.profile)
        if form.is_valid():
            transfer = form.save(commit=False)
            account_num_send = form.cleaned_data['sender_acc']
            account_num_rec = form.cleaned_data['receip_acc']

            if account_num_send == account_num_rec:
                messages.success(request, f'Invalid Transfer. Please try again')
                form.add_error('receip_acc', 'Select different account')
                return render(request, 'bank/send.html', {'form': form, 'accounts': accounts})

            amount = form.cleaned_data['amount']
            # Retrieve the account based on the account number entered by the user
            try:
                account_S = Account.objects.get(acc_num=account_num_send, a_username=request.user.profile)
                #account_R = Account.objects.get(acc_num=account_num_rec, a_username=request.user.profile)
            except Account.DoesNotExist:
                form.add_error('sender_acc', 'Invalid account number')
                return render(request, 'bank/send.html', {'form': form, 'accounts': accounts})


            # Check that the account belongs to the logged-in user
            if account_S.a_username != user.profile:
                form.add_error('sender_acc', 'Invalid account number')
                return render(request, 'bank/send.html', {'form': form, 'accounts': accounts})

            try:
                account_R = Account.objects.exclude(a_username=user.profile).get(acc_num=account_num_rec)
            except Account.DoesNotExist:
                form.add_error('receip_acc', 'Invalid account number')
                return render(request, 'bank/send.html', {'form': form, 'accounts': accounts})
            

            #making sure user does not send more money than
            if amount > account_S.balance:
                messages.warning(request, f'Opss! Trying to send more money than you have.')
                return render(request, 'bank/send.html', {'form': form, 'accounts': accounts})

            # Update the account balance and save the transaction
            account_S.balance -= transfer.amount
            account_R.balance += transfer.amount
            account_S.save()
            account_R.save()

            transfer.sender_acc = account_S
            transfer.receip_acc = account_R
            transfer.save()

            messages.success(request, f'Transfer of {amount} successfully made to account {account_num_rec}.')
            return redirect('bank-profile')
    else:
        form = PerformUserSend(user=user.profile)
    
    return render(request, 'bank/send.html', {'form': form, 'accounts': accounts})



"""
#need to modify
@login_required
def profile(request, user_ssn):
    user = User.objects.get(ssn=user_ssn)
    accounts = Account.objects.filter(ussn=user)
    account_info = []
    for account in accounts:
        info = {'acc_num': account.acc_num, 'balance': account.balance, 'spendings': account.spendings}
        account_info.append(info)
    context = {'user_ssn': user_ssn, 'account_info': account_info}
    return render(request, 'profile.html', context)


<h1>Accounts for User {{ user_ssn }}</h1>
<table>
  <tr>
    <th>Account Number</th>
    <th>Balance</th>
    <th>Spendings</th>
  </tr>
  {% for account in account_info %}
  <tr>
    <td>{{ account.acc_num }}</td>
    <td>{{ account.balance }}</td>
    <td>{{ account.spendings }}</td>
  </tr>
  {% endfor %}
</table>


@login_required
def deposit(request):
    account = Account.objects.get(a_username=request.user.profile)
    if request.method == 'POST':
        form = PerformDeposit(request.POST)
        if form.is_valid():
            # Update the account balance
            
            amount = form.cleaned_data['amount']
            account.balance += amount
            account.save()

            # Save the transaction
            Transactions.objects.create(
                acc_num=account,
                tamount=amount
            )
            
            return redirect('bank-profile')
    else:
        form = PerformDeposit()
    return render(request, 'bank/deposit.html', {'form': form})
"""
