
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.forms import widgets

"""
#not sure if it's saving the input in the db
class UserRegisterForm(forms.Form):
    ssn = forms.CharField(max_length=9)
    Fname = forms.CharField(max_length=50)
    Lname = forms.CharField(max_length=50)
    DOB = forms.DateField()
    email = forms.EmailField()
    psw = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)

    # Define the layout for the form using Crispy Forms
    helper = FormHelper()
    helper.form_method = 'post'
    helper.layout = Layout(
        'Fname',
        'Lname',
        'DOB',
        'country',
        'city',
        'email',
        'psw',
        Submit('submit', 'Submit', css_class='btn-primary')
    )
"""

from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    Fname = forms.CharField(max_length=50, label='First name')
    Lname = forms.CharField(max_length=50, label='Last name')
    DOB = forms.DateField(label='Date of birth')
    email = forms.EmailField(label='Email')
    country = forms.CharField(max_length=50, label='Country')
    city = forms.CharField(max_length=50, label='City')

    class Meta:
        model = User
        fields = ['Fname', 'Lname', 'DOB', 'email', 'country', 'city', 'username', 'password1', 'password2']



class CreateAccountForm(forms.ModelForm):
    acc_num = forms.CharField(max_length=20, label='Account Number')
    
    class Meta:
        model = Account
        fields = ['acc_num', 'balance']

    
    
from django import forms
from .models import Transactions


#used for withdraw and deposit, same implementation
class PerformDeposit(forms.ModelForm):
    acc_num = forms.ModelChoiceField(queryset=Account.objects.none(), label='Account Number')
    tamount = forms.DecimalField(label='Amount', max_digits=12, decimal_places=2)
    #tr_type = forms.CharField(widget=forms.HiddenInput()) #to differentiate withdraw from deposit

    class Meta:
        model = Transactions
        fields = ('acc_num', 'tamount')
        

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PerformDeposit, self).__init__(*args, **kwargs)
        self.fields['acc_num'].queryset = Account.objects.filter(a_username=self.user)
        self.fields['acc_num'].widget.attrs.update({'class': 'form-control'})
        self.fields['tamount'].widget.attrs.update({'class': 'form-control'})



class PerformTransfer(forms.ModelForm):
    sender_acc = forms.ModelChoiceField(queryset=Account.objects.none(), label='Sender Account Number')
    receip_acc = forms.ModelChoiceField(queryset=Account.objects.none(), label='Recipient Account Number')
    amount = forms.DecimalField(label='Amount', max_digits=12, decimal_places=2)
    
    class Meta:
        model = Transfers
        fields = ['sender_acc', 'receip_acc', 'amount']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PerformTransfer, self).__init__(*args, **kwargs)
        self.fields['sender_acc'].queryset = Account.objects.filter(a_username=self.user)
        self.fields['sender_acc'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})

        self.fields['receip_acc'].queryset = Account.objects.filter(a_username=self.user)
        self.fields['receip_acc'].widget.attrs.update({'class': 'form-control'})



class PerformUserSend(forms.ModelForm):
    sender_acc = forms.ModelChoiceField(queryset=Account.objects.none(), label='Sender Account Number')
    receip_acc = forms.CharField(max_length=10, label='Recipient Account Number')
    amount = forms.DecimalField(label='Amount', max_digits=12, decimal_places=2)
    
    class Meta:
        model = Transfers
        fields = ['sender_acc', 'receip_acc', 'amount']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PerformUserSend, self).__init__(*args, **kwargs)
        self.fields['sender_acc'].queryset = Account.objects.filter(a_username=self.user)
        self.fields['sender_acc'].widget.attrs.update({'class': 'form-control'})
        self.fields['amount'].widget.attrs.update({'class': 'form-control'})

        #self.fields['receip_acc'].queryset =  Account.objects.exclude(a_username=self.user)
        self.fields['receip_acc'].widget.attrs.update({'class': 'form-control'})


    def clean(self):
        cleaned_data = super().clean()
        receip_acc_num = cleaned_data.get('receip_acc')

        try:
            receip_acc = Account.objects.get(acc_num=receip_acc_num)
        except Account.DoesNotExist:
            raise forms.ValidationError('Recipient account number does not exist')

        cleaned_data['receip_acc'] = receip_acc

        return cleaned_data



        
"""
    # Enforce unique constraint on SSN field
    def valid_ssn(self):
        ssn = self.cleaned_data.get('username')
        if User.objects.filter(ssn=ssn).exists():
            raise ValidationError('This username already exists. Please enter a unique username.')
        return ssn

    # Add Crispy Form Helper to customize form layout
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Save', css_class='btn-primary'))
"""