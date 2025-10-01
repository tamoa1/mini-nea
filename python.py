import os
import json


def assign_student_to_trip(file, fName, lName):
    #register = open(file + ".json", "a")
    found = False
    with open(file + ".json", "r") as f:
        data = json.load(f)
        for student in data["students"]:
            if student["firstName"].lower() == fName.lower() and student["lastName"].lower() == lName.lower():
                print(f"Student {fName} {lName} is already registered.")
                found = True
                break
        if found == False:
            data["students"].append({"firstName": fName, "lastName": lName, "present": False})
            with open(file + ".json", 'w') as f:
                json.dump(data, f, indent=4) 
            print(f"Student {fName} {lName} has been registered successfully.")
                      

    #register.write(f"{fName.lower()},{lName.lower()},{0} \n")
   # register.close()
    #print("Registration successful!")

#assign_student_to_trip("trip1", "Toma", "Croome")




def authentication():
    global userName, password, switchAdmin
    userName = input("Enter your username: ")
    password = input("Enter your password: ")
    with open("authorisedUsers.json", "r") as f:
        users = json.load(f)
    for user in users:
        if userName == user["userName"] and password == user["password"]:
            print("Login successful!")
            if user["isAdmin"] == True:
                switchAdmin = True
            else:
                switchAdmin = False
            return True
    print("Login failed!")
    return False





def signUp():
    userName = input("Enter your desired username: ")
    password = input("Enter your desired password: ")
    fName = input("Enter your first name: ")
    lName = input("Enter your last name: ")
    with open("authorisedUsers.json", "r") as f:
        users = json.load(f)
        users.append({"userName": userName, "password": password, "firstName": fName, "lastName": lName, "isAdmin": False})
        with open("authorisedUsers.json", 'w') as f:
            json.dump(users, f, indent=4)
    print("Sign-up successful!")




def create_trip():
    files = [f for f in os.listdir() if os.path.isfile(f)]
    usedFileNum = []
    for file in files:
        if file.startswith("trip") and file.endswith(".json"):
            usedFileNum += file[4:-5]
    n = 1
    while str(n) in usedFileNum:
        n += 1
    filenum = n - 1
    trip = open("trip" + str(filenum + 1) + ".json", "w")
    tripName = input("Enter the name of the trip: ")
    format = {"tripDetails": {"destination": tripName, "departureDate": "", "returnDate": "", "cost": "", "maxStudents":""}, "teachers": [{"firstName": "", "lastName": "", "userName":""}], "students": [{"firstName": "", "lastName": "", "present": False}]}
    trip.write(json.dumps(format, indent=4))
    trip.close()
    print("Trip created successfully!")



def find_trip_file(tripChoice):
    for filename in os.listdir():
        if filename.endswith('.json') and filename.startswith('trip'):
            f = open(filename, 'r')
            data = json.load(f)
            destination = data["tripDetails"]["destination"].lower()
            if destination == tripChoice.lower():
                return filename
    return None



def assign_trip(arrgroups, arrrteachers):
    groups = ""
    teachers = ""

    for group in arrgroups:
        groups += group + ","
       # groups = groups[:-1]

    for teacher in arrrteachers:
        teachers += teacher + ","
      #  teachers = teachers[:-1]

    tripChoice = input("Enter the trip name: ").lower()
    found_file = find_trip_file(tripChoice)
    if found_file != None:
        print(f"Trip '{tripChoice}' found in file: {found_file}")
        f = open(found_file, 'r')
        lines = f.readlines()
        lines.insert(1, str(groups) + '\n')
        lines.insert(2, str(teachers) + '\n')
        with open(found_file, 'w') as f:
            f.writelines(lines)
    else:
        print(f"Trip '{tripChoice}' not found in any file.")





#arrgroups = ["group1", "group2"]
#arrrteachers = ["teacher1", "teacher2"]
#assign_trip(arrgroups, arrrteachers)


def register_user(file):
    f = open(file + ".txt", "w")
    for row in f:
        line = f.readline()
        present = input(f"is {line[0]}{line[1]} present? (1/0): ")
        if present == "1":
            line = f.writelines(line[0], line[1], 1)


register_user("trip1") #ts pmo does not work yet
