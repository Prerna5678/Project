class Bank:

    def __init__(self,Acc_no,Acc_name,Acc_bal):
        self.Acc_no=Acc_no
        self.Acc_name=Acc_name
        self.Acc_bal=Acc_bal

    def deposit(self,amount):
        self.Acc_bal+= amount
        print(f"{self.Acc_bal} balance,your new balance {amount} ")

    def withdraw(self,amount):
        self.Acc_bal-=amount
        print(f"{self.Acc_bal} Your total Bank Balance is{amount}")

    def display(self):
        print(self.Acc_bal)

Acc_name=input("Enter the Account Name")
Acc_no=int(input("Enter the Account No."))
Acc_bal=int(input("Enter the Account balance"))
bank1=Bank( Acc_name,Acc_no,Acc_bal)
Acc_bal=int(input("Enter the dposit amount"))
bank1.deposit(Acc_bal)
Acc_bal=int(input("Enter the withdraw amount"))
bank1.withdraw(Acc_bal)
bank1.display()

        