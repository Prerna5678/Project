# Registration Form
''' This is Registration from customer side '''
Customer = []
print("\n Registration Form")
reg_username = input("Enter your name: ")
reg_email = input("Enter your email: ")
new_user = {'username': reg_username, 'email': reg_email}


if new_user in Customer:
    print("User already registered.")
else:
    Customer.append(new_user)
    print("Your registration was successful.")
    print(Customer)

if new_user not in Customer:
    Customer.append(new_user)
else:
    print("user already registered")
    