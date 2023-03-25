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
User(ssn, Fname, Lname, DOB, email, psw, country, city) ->pk:ssn
Account(acc_num, ussn, balance, spendings) ->pk: acc_num   ussn is unique 
Transactions(t_id, acc_num, tamount) ->pk: t_id  
Transfers(transf_id, sender_acc, receip_acc, amount) ->pk:transf_id

maybe
Location(ussn, country, city)


Notes:
need a logged in home page that displays the user and the accounts
and links to get all the info from that user 
links to transfer money to another user
links to pay/withdraw

