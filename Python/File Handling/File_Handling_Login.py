from File_Handling_Registration import *
''' This is login page from customer side '''
# Login form for Customer
username = input("Enter your name: ")
email = input("Enter your email: ")
Cust_login = {'username': username, 'email': email}
if Cust_login == new_user:
    print(Customer)
    print("You login successfully", Cust_login)
    f = open(username, "w")
    f.write(username + "\n" + email)
    f.close()  
else:
    print("invalid login! pls do first registration")
  
