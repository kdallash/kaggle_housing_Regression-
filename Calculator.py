z = 1
try:
    x = int(input("please enter the first number : "))
    y = int(input("please enter the second number : "))
except ValueError:
    print("please enter the  numbers as an integer" )
while z:
    z = 0
    oper = int(input("please Choose an operation\n1. Add\n2. Subtract\n3. Multiply\n4. Divide\nchoose (1,2,3,4) : "))
    if oper == 1: print(f"the sum is {x} + {y} = {x + y}")
    elif oper == 2 : print(f"the diffrance is {x} - {y} = {x - y}")
    elif oper == 3 : print(f"the multiplication is {x} * {y} = {x * y}")
    elif oper == 4 :
        try:
            print(f"the divition is {x} / {y} = {x / y}")
        except ZeroDivisionError:
            print("the second number can't be 0 if you are tring to devide ")
    else : 
        print ("you must choose a number between 1 and 4 incloseve")
        z = 1