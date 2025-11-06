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
            print("Connected to database")

    def close(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()
            print("Database connection closed")



#student create read update delete
    def create_student(self, fName, lName, gender, dob, year, form, house, sEmail, sPhone, consent, contactID, medicalID):
        query = "INSERT INTO student (fName, lName, gender, dob, year, form, house, sEmail, sPhone, consent, contactID, medicalID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"