from File_Handling_Login import *
while True:
    print("\nYou are welcome in Customer")
    print("\n 1.Login \n 2.Registration \n 0.Exit")
    choice=input("enter the choice")
    for Cust in Customer:
        if Cust_login == Cust:
            print(Cust)
            print("You login successfully", Cust_login)
            flag = True
    '''
    while True:
        print("\n 1.Jeans \n 2.Shirt \n 3.T-Shirt \n 4.Jacket \n 5.Checkout \n 6.View Cart \n 0.Exit")
        prod_choice = int(input("\nEnter your choice: "))
        name=0
        price=0
        total_amt=0
        # Jeans
        if prod_choice==1:
             # Qty user side input
            qty = int(input(f"Enter quantity for {name}:"))
            # Calculation method of product * qty
            subtotal = Product[0]["price"]* qty
            total_amt += subtotal            
            print(name," x ",qty ,"= Rs.",subtotal,"\n")
            print("Total Amount: Rs.",total_amt)
            print("Thank you for shopping!")
        '''