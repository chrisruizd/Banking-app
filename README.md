# Banking-app

To put all installed packeges in a file use: pip freeze > filename.txt

<pre>
Corey Schafer YouTube channel (Django Tutorials) as a resource


Github:
"git add ."
"git commit -m "Added new feature X"
"git push"

git checkout "b_name"   switch branch
git branch "b_name"     create new branch named "b_name"
git branch -a           see all branches
git status
git branch -d "b_name"  delete branch  
git merge "b_name"      merge branch "b_name" to the main branch
git log --oneline       get list of commits


Database Schema:
User(username, password)    ->pk:username
Profile(username, Fname, Lname, DOB, email, country, city) ->fk:username
Account(acc_num, balance, a_username) ->pk: acc_num    
Transactions(t_id, tacc_num, tamount, tr_type, date_time) ->pk: t_id  
Transfers(transf_id, sender_acc, rece_acc, amount) ->pk:transf_id




Use sqlite:
py manage.py dbshell

select *
from bank_account;

select *
from bank_profile;
