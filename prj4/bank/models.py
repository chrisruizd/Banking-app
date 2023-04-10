from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import uuid

# Create your models here.
from django.db import models


#notice it is using Django pre-built User model, it contains the attributes username and password

#user can only have one profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Fname = models.CharField(max_length=50)
    Lname = models.CharField(max_length=50)
    DOB = models.DateField()
    email = models.EmailField()
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    
    

    #this returns how you want the user to be printed
    def __str__(self):
        return f"{self.Fname}"
    
    def save(self, *args, **kawargs):
        super().save(*args, **kawargs)


# a profile can have multiple accounts, but an account can only have a single profile
class Account(models.Model):
    acc_num = models.CharField(max_length=20, primary_key=True)
    a_username = models.ForeignKey(Profile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.acc_num}"
    
    def save(self, *args, **kawargs):
        super().save(*args, **kawargs)


    
# an account can have multiple transactions, but a transaction can only have a single account related
class Transactions(models.Model):
    t_id = models.CharField(max_length=20, primary_key=True)
    acc_num = models.ForeignKey(Account, on_delete=models.CASCADE)
    tamount = models.DecimalField(max_digits=12, decimal_places=2)
    tr_type = models.CharField(max_length=1)    #transaction type
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.t_id}"
    
    def save(self, *args, **kawargs):
        if not self.t_id:
            #assing random unique value to t_id
            self.t_id = str(uuid.uuid4().int)[:10]
        super().save(*args, **kawargs)


# an account can have multiple transfers, a transfer requires receiver and sender accounts
class Transfers(models.Model):
    transf_id = models.CharField(max_length=20, primary_key=True)
    sender_acc = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender_account')
    receip_acc = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='recipient_account')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.transf_id}"
    
    def save(self, *args, **kawargs):
        if not self.transf_id:
            #assing random unique value to transf_id
            self.transf_id = str(uuid.uuid4().int)[:10]
        super().save(*args, **kawargs)




#python manage.py makemigrations
#python manage.py sqlmigrate blog ####
#python manage.py migrate

#user.account_set.all() will give every account from that user