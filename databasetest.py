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

    def read_student(self):
        try:
            query = "SELECT * FROM student"
            self.cursor().execute(query)
            results = self.cursor().fetchall() #fetches the results of the query executed by the cursor
        except:
            print("error")

    def update_student(self
