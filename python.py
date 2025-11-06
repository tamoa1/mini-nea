import streamlit as st
import pandas as pd
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



def assign_trip_group(tripChoice, arrgroups):
    tripFile = find_trip_file(tripChoice)

    if tripFile is None:
        print("Trip not found.")
        return
    
    with open("studentInformation.json", "r") as f:
        studentsData = json.load(f)

    with open(tripFile, "r") as f:
        tripData = json.load(f)

    for student in studentsData["students"]:
        if any(group in arrgroups for group in student["groups"]["classes"]) or student["groups"]["form"] in arrgroups:
            tripData["students"].append({"firstName": student["firstName"], "lastName": student["lastName"], "present": False})

    with open(tripFile, 'w') as f:
        json.dump(tripData, f, indent=4)
    print("groups assigned successfully!")


def assign_trip_teachers(tripChoice, arrrteachers):
    tripFile = find_trip_file(tripChoice)

    if tripFile is None:
        print("Trip not found.")
        return

    with open(tripFile, "r") as f:
        tripData = json.load(f)

    with open("authorisedUsers.json", "r") as f:
        teacherFile = json.load(f)
        for teacher in teacherFile:
            if teacher["isAdmin"] == True and (teacher["firstName"] in arrrteachers or teacher["lastName"] in arrrteachers or teacher["userName"] in arrrteachers):
                tripData["teachers"].append({"firstName": teacher["firstName"], "lastName": teacher["lastName"], "userName": teacher["userName"]})
    with open(tripFile, 'w') as f:
        json.dump(tripData, f, indent=4)
    print("Teachers assigned successfully!")


def assign_trip_students(tripChoice, arrstudents):
    tripFile = find_trip_file(tripChoice)

    if tripFile is None:
        print("Trip not found.")
        return
    
    with open("studentInformation.json", "r") as f:
        studentsData = json.load(f)

    with open(tripFile, "r") as f:
        tripData = json.load(f)

    for student in studentsData["students"]:
        if student["firstName"] in arrstudents or student["lastName"] in arrstudents:
            tripData["students"].append({"firstName": student["firstName"], "lastName": student["lastName"], "present": False})

    with open(tripFile, 'w') as f:
        json.dump(tripData, f, indent=4)
    print("Students assigned successfully!")



arrgroups = ["LE1", "MfOW"]
arrrteachers = ["Linda", "tamoa"]
arrstudents = ["Toma", "Emily"]

assign_student_to_trip("London", arrstudents) #need to fix and make all assign functions to check if already assigned


def register_user(file):
    with open(file + ".json", "r") as f:
        data = json.load(f)
    for student in data["students"]:
        if input(f"is {student['firstName']} {student['lastName']} present? (1/0): ") == "1":
            student["present"] = True
        else:
            student["present"] = False
    with open(file + ".json", 'w') as f:
        json.dump(data, f, indent=4)



    
