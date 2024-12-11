def main():
    oper = 20
    try:
        print("please enter the first number : ")
        x = get_int()
        print("please enter the second number : ")
        y = get_int()
    except ValueError:
        print("please enter the  numbers as an integer" )
    while oper > 4:
        z = 0
        oper = int(input("please Choose an operation\n1. Add\n2. Subtract\n3. Multiply\n4. Divide\nchoose (1,2,3,4) : "))
        if oper == 1: print(f"the sum is {x} + {y} = {x + y}")
        elif oper == 2 : print(f"the diffrance is {x} - {y} = {x - y}")
        elif oper == 3 : print(f"the multiplication is {x} * {y} = {x * y}")
        elif oper == 4 :
                print(f"the divition is {x} / {y} = {divide(x, y)}")
        else : 
            print ("you must choose a number between 1 and 4 incloseve")

def get_int():
    while True:
        try:
            x = int(input())
            return x
        except ValueError:
            print("please enter the  numbers as an integer :",end=None )
def divide( x, y):
    try:
         return(x / y)
    except ZeroDivisionError:
        return("error the second number can't be 0 ")
if __name__ =="__main__":
        main()