import os



def register_user(file):
    register = open(file + ".txt", "a")
    fName, lName = input("Enter your  name: ").split()
    register.write(f"{fName.lower()},{lName.lower()},{0} \n")
    register.close()
    print("Registration successful!")

#register_user("trip1")




def authentication():
    global userName, password
    userName = input("Enter your username: ")
    password = input("Enter your password: ")
    for line in open("authorisedUsers.txt", "r").readlines():
        storedName, storedPass = line.strip().split(",")
        if userName == storedName and password == storedPass:
            print("Login successful!")
            return True
    print("Login failed!")
    return False





def signUp():
    userName = input("Enter your desired username: ")
    password = input("Enter your desired password: ")
    with open("authorisedUsers.txt", "a") as file:
        file.write(f"{userName},{password}\n")
    print("Sign-up successful!")

#signUp()
#authentication()

#print(userName + password)


def create_trip(filenum):
    trip = open("trip" + str(filenum + 1) + ".txt", "w")
    tripName = input("Enter the name of the trip: ")
    trip.write(tripName + "\n")
    trip.close()
    print("Trip created successfully!")


def find_trip_file(tripChoice):
    for filename in os.listdir():
        if filename.endswith('.txt'):
            f = open(filename, 'r')
            first_line = f.readline().strip().lower()
            if first_line == tripChoice.lower():
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


#num_of_concurrent_trips = 0
#create_trip(num_of_concurrent_trips)


#arrgroups = ["group1", "group2"]
#arrrteachers = ["teacher1", "teacher2"]
#assign_trip(arrgroups, arrrteachers)