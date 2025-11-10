import mysql.connector
#to connect database


#creating class for the database allows for neater code because all the code related to opening and closing the database is in one place.
#works better than functions beacause for functions i would have to open and close the database connection each time.

class tripDataBase:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="TomaCroomeDB",
            database="mydb"
        )
        if self.db.is_connected():
            self.cursor = self.db.cursor()
            print("connected to database")

    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            print("database connection closed")






#student create read update delete





    def create_student(self, fName, lName, gender, dob, year, form, house, sEmail, sPhone, consent, contactID, medicalID):
        query = "INSERT INTO student (fName, lName, gender, dob, year, form, house, sEmail, sPhone, consent, contactID, medicalID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        #sql query INSERT the values held by the placeholder %s, which means only valid data can be inputted(no sql querys can be enterred)
        values = (fName, lName, gender, dob, year, form, house, sEmail, sPhone, consent, contactID, medicalID)
        try:
            self.cursor().execute(query, values)
            self.db.commit()
            # execute the query and commit the changes to the database
            print("student added")

        except: #if there is any errors:
            self.db.rollback() #reverse any changes to last commit
            print("error")

    def read_all_students(self): #read all students from database
        try:
            query = "SELECT * FROM student"
            self.cursor().execute(query)
            results = self.cursor().fetchall() #fetches the results of the query executed by the cursor
            return results
        except:
            print("error")
            return []


    def read_student_by_id(self, studentID):
        try:
            query = "SELECT * FROM student WHERE studentID = %s"
            values = (studentID)
            self.cursor().execute(query, values)
            result = self.cursor().fetchone() #fetches one result
            return result
        except:
            print("error")
            return None
        

    def update_student(self, studentID, **kwargs): #kwargs means any number of parameters 
        #to use method db.update_student(1, fName="naame", lName="lastname")
        #works like dictionary with key and value pairs
        fields = []
        values = []
        try:
            for key, value in kwargs.items():
                fields.append(f"{key} = %s") #creates a list of the fields to be updated 
                values.append(value) #creates a list of the new values
            
            values.append(studentID) #append studentID to the end of the values list for the WHERE clause
            query = f"UPDATE student SET {', '.join(fields)} WHERE studentID = %s" #{', '.join(fields)} joins the fields list into a string separated by commas
            self.cursor().execute(query, tuple(values))
            self.db.commit()
            print("student updated")
        except:
            self.db.rollback()
            print("error")
    
    def delete_student(self, studentID):
        try:
            query = "DELETE FROM student WHERE studentID = %s"
            values = (studentID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("student deleted")
        except:
            self.db.rollback()
            print("error")

    
    #trip create read update delete

    def create_trip(self, destination, date, returnDate, status, leaderID):
        try:
            query = "INSERT INTO trip(destination, date, returnDate, status, leaderID) VALUES(%s, %s, %s, %s, %s)"
            values = (destination, date, returnDate, status, leaderID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("trip created")
        except:
            self.db.rollback()
            print("error")

    def read_all_trips(self):
        try:
            query = "SELECT * FROM trip"
            self.cursor().execute(query)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []
    
    def read_trip_by_id(self, tripID):
        try:
            query = "SELECT * FROM trip WHERE tripID = %s"
            values = (tripID)
            self.cursor().execute(query, values)
            result = self.cursor().fetchone()
            return result
        except:
            print("error")
            return None
    
    def read_trips_by_leader(self, leaderID):
        try:
            query = "SELECT * FROM trip WHERE leaderID = %s"
            values = (leaderID)
            self.cursor().execute(query, values)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []
        
    def read_trips_by_destination(self, destination):
        try:
            query = "SELECT * FROM trip WHERE destination = %s"
            values = (destination)
            self.cursor().execute(query, values)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []
        
    def update_trip(self, tripID, **kwargs):
        fields = []
        values = []
        try:
            for key, value in kwargs.items():
                fields.append(f"{key} = %s")
                values.append(value)
            values.append(tripID)
            query = f"UPDATE trip SET {', '.join(fields)} WHERE tripID = %s"
            self.cursor().execute(query, tuple(values))
            self.db.commit()
            print("trip updated")
        except:
            self.db.rollback()
            print("error")

    def delete_trip(self, tripID):
        try:
            query = "DELETE FROM trip WHERE tripID = %s"
            values = (tripID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("trip deleted")
        except:
            self.db.rollback()
            print("error")
    


    #trip asssign and removing functions


    def assign_student_to_trip(self, tripID, studentID):
        try:
            query = "INSERT INTO trip_students (tripID, studentID) VALUES (%s, %s)"
            values = (tripID, studentID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("student assigned to trip")
        except:
            self.db.rollback()
            print("error")

    def remove_student_from_trip(self, tripID, studentID):
        try:
            query = "DELETE FROM trip_students WHERE tripID = %s AND studentID = %s"
            values = (tripID, studentID)
            self.cursor().execute(query, values)
            self.db.commit()
            print("student removed from trip")
        except:
            self.db.rollback()
            print("error")
    
    def get_trip_students(self, tripID): #get all students assigned to a trip
        try:
            query = "SELECT studentID FROM trip_students WHERE tripID = %s"
            values = (tripID)
            self.cursor().execute(query, values)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []
    
    def get_student_trips(self, studentID): #get all trips a student is assigned to
        try:
            query = "SELECT tripID FROM trip_students WHERE studentID = %s"
            values = (studentID)
            self.cursor().execute(query, values)
            results = self.cursor().fetchall()
            return results
        except:
            print("error")
            return []


    #USER create read update delete

    def create_user(self, username, password, fname, lname, email, phone, role_id):
        try:
            query = "INSERT INTO user (username, password, fName, lName, email, phone, role_roleID) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (username, password, fname, lname, email, phone, role_id)
            self.cursor.execute(query, values)
            self.db.commit()
            print("user created")
        except:
            print("error")
            self.db.rollback()

    def read_user_by_username(self, username):
        try:
            query = "SELECT * FROM user WHERE username = %s"
            values = (username)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            return result
        except:
            print("error")
            return None
        
    def read_all_users(self):
        try:
            query = "SELECT * FROM user"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except:
            print("error")
            return []
        
    def read_user_by_id(self, userID):
        try:
            query = "SELECT * FROM user WHERE userID = %s"
            values = (userID)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            return result
        except:
            print("error")
            return None
    
    def update_user(self, userID, **kwargs):
        fields = []
        values = []
        try:
            for key, value in kwargs.items():
                fields.append(f"{key} = %s")
                values.append(value)
            values.append(userID)
            query = f"UPDATE user SET {', '.join(fields)} WHERE userID = %s"
            self.cursor.execute(query, tuple(values))
            self.db.commit()
            print("user updated")
        except:
            self.db.rollback()
            print("error")

    def delete_user(self, userID):
        try:
            query = "DELETE FROM user WHERE userID = %s"
            values = (userID)
            self.cursor.execute(query, values)
            self.db.commit()
            print("user deleted")
        except:
            self.db.rollback()
            print("error")

    def verify_user(self, username, password):
        try:
            query = "SELECT * FROM user WHERE username = %s AND password = %s"
            values = (username, password)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result: #if a matching user is found
                return True
            else: #no matching user
                return False
        except:
            print("error")
            return False



    #emergency contact create read update delete

    def create_medical_info(self, dietary_needs, medical, notes, doctors):
        try:
            query = "INSERT INTO medical_information (dietaryneeds, medical, notes, doctors) VALUES (%s, %s, %s, %s)"
            values = (dietary_needs, medical, notes, doctors)
            self.cursor.execute(query, values)
            self.db.commit()
            print("medical information created")
        except:
            print("error")
            self.db.rollback()

    def read_medical_info_by_id(self, medicalID):
        try:
            query = "SELECT * FROM medical_information WHERE medicalID = %s"
            values = (medicalID)
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            return result
        except:
            print("error")
            return None
    
    def read_all_medical_info(self):
        try:
            query = "SELECT * FROM medical_information"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except:
            print("error")
            return []

    def read_medical_info_by_trip(self, tripID):
        try:
            query = """SELECT medical_information.* FROM medical_information
                       JOIN student ON medical_information.medicalID = student.medicalID
                       JOIN trip_students ON student.studentID = trip_students.studentID
                       WHERE trip_students.tripID = %s"""
            values = (tripID)
            self.cursor.execute(query, values)
            results = self.cursor.fetchall()
            return results
        except:
            print("error")
            return []
        
    def update_medical_info(self, medicalID, **kwargs):
        fields = []
        values = []
        try:
            for key, value in kwargs.items():
                fields.append(f"{key} = %s")
                values.append(value)
            values.append(medicalID)
            query = f"UPDATE medical_information SET {', '.join(fields)} WHERE medicalID = %s"
            self.cursor.execute(query, tuple(values))
            self.db.commit()
            print("medical information updated")
        except:
            self.db.rollback()
            print("error")

    def delete_medical_info(self, medicalID):
        try:
            query = "DELETE FROM medical_information WHERE medicalID = %s"
            values = (medicalID)
            self.cursor.execute(query, values)
            self.db.commit()
            print("medical information deleted")
        except:
            self.db.rollback()
            print("error")
