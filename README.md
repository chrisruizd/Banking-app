# Banking-app

For this app, our team had the idea of replicating a banking application called ‘USF Online Banking’. Our aim for this application is to demonstrate the functionalities of a bank app, but in a unique way that would not only be convenient to students but also would be available to other members outside of the USF community. 

The application is a basic replica of the USF FCU website, however, we hope to mimic the functionalities in a more user-friendly way, especially through our email alerts feature.
![ER diagrams](New%20ER%20diagram.png)

Banking-app\New ER diagram.png
<pre>

Database Schema:
User(username, password)    ->pk:username
Profile(username, Fname, Lname, DOB, email, country, city) ->fk:username
Account(acc_num, balance, a_username) ->pk: acc_num    
Transactions(t_id, tacc_num, tamount, tr_type, date_time) ->pk: t_id  
Transfers(transf_id, sender_acc, rece_acc, amount) ->pk:transf_id





Corey Schafer YouTube channel (Django Tutorials) as a resource



