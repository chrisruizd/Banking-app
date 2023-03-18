# Banking-app
To put all installed packeges in a file use: pip freeze > filename.txt

Github:
"git add ."
"git commit -m "Added new feature X"
"git pull"

Database Schema:
User(ssn, Fname, Lname, DOB, email, psw, country, city) ->pk:ssn
Account(acc_num, ussn, balance, spending, transfers) ->pk: acc_num   ussn is unique 
Transactions(t_id, acc_num, tamount) ->pk: t_id  
Transfers(transf_id, sender_acc, receip_acc, amount) ->pk:transf_id

maybe
Location(ussn, country, city)