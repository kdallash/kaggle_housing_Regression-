students = {}
while True:
    x = int(input("please enter a number 1 o 2 \n 1 if you want to add a student \n 2 if you want to exit\n input : " ))
    if x == 1:
        name = input("please enter your name : ")
        students[name] = {}
        students[name]["age"] = input("Enter student age: ")
        students[name]["grade"] = input("Enter student grade: ")
        students[name]["subjects"] = input("Enter student subjects (comma-separated): ").split(",")
    else : break 
for name in students.keys():
    print(f"The student name is {name}")
    print("Student Information:")
    for key , value in students[name].items():
        print(f"{key} : {value}")