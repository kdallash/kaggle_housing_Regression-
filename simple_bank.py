user_name = input("please enter your user name :")
bank_id =  input("please enter your bank id  :")
print (f"welcome to the bank Mr/Mrs {user_name}")
balance =  int(input ("Your balance is:"))
action = int(input("Choose an action:\n1. Deposit\n2. Withdraw\n3. Check Balance\nEnter choice: "))
if action == 1:
    x = int(input("Enter amount to deposit: "))
    print (f"your balance is {balance + x}")
elif action == 2:
    x = int(input("Enter amount to Withdraw: "))
    if x <= balance:
        print (f"your balance is {balance - x}")
    else: print("no enough fund")
elif action == 3: print (f"your balance is {balance}")
else : print ("you choose a wrong number \n here is your balance : ",balance)