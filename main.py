import customtkinter
from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
import mysql.connector
from mysql.connector import Error
import re

host = "localhost"
user = "root"
password = ""
database = "student_information_db"

try:
    db = mysql.connector.connect(host=host,user=user,password=password,database=database)

    if db.is_connected():
        print("Connected To Database")

        def authenticate(usernameEntry,passwordEntry):
            username = usernameEntry.get()
            password = passwordEntry.get()

            sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
            cursor = db.cursor()
            cursor.execute(sql,(username,password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo(title="Login Successfully",message="Login Successfully!")
                loginWindow.withdraw()
                mainpageOutput()
            else:
                messagebox.showerror(title="Login Failed!",message="Login Failed!")
                
    else:
        raise Exception("Connection to MySQL database failed")
except Error as error:
    print(f"Database Error: {error}")

# ---------- END OF FUNCTIONS ------------

# ---------- GUI ------------
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

def loginWindowOutput():
    global loginWindow
    loginWindow = customtkinter.CTk()  # create CTk window like you do with the Tk window
    loginWindow.title("Login Form")
    loginWindow.geometry("400x380")

    customtkinter.CTkLabel(loginWindow,text="LOGIN FORM",font=("Arial",30,"bold")).place(x=105,y=80)

    usernameEntry = customtkinter.CTkEntry(loginWindow,placeholder_text="Enter Your Username",width=230)
    usernameEntry.place(x=90,y=150)

    passwordEntry = customtkinter.CTkEntry(loginWindow,placeholder_text="Enter Your Password",show="*",width=230)
    passwordEntry.place(x=90,y=200)

    loginButton = customtkinter.CTkButton(loginWindow,width=230,height=40,text="LOGIN",command=lambda: authenticate(usernameEntry,passwordEntry))
    loginButton.place(x=90,y=250)

    loginWindow.mainloop()

def mainpageOutput():
    global mainWindow
    mainWindow = customtkinter.CTk()
    mainWindow.title("Main Page")
    mainWindow.geometry("1920x680+-5+5")

    # ---------- FUNCTIONS ------------
    lrn_pattern = re.compile(r'^\d{12}$')
    first_name_pattern = re.compile(r'^[A-Za-z]{1,30}(?: [A-Za-z]{1,30})?$')
    middle_name_pattern = re.compile(r'^[A-Za-z]*(?: [A-Za-z]{1,30})*$')
    last_name_pattern = re.compile(r'^[A-Za-z]{1,30}(?: [A-Za-z]{1,30})?$')
    address_pattern = re.compile(r'^[A-Za-z0-9\s\.,#-]{1,100}$')
    phone_number_pattern = re.compile(r'^\d{11}$')

    def validate_input():
        lrn = studentLRNEntry.get()
        first_name = studentFNameEntry.get()
        middle_name = studentMNameEntry.get()
        last_name = studentLNameEntry.get()
        address = studentAddressEntry.get()
        phone_number = studentPhoneNumberEntry.get()
        year_level = studentYearLevelEntry.get()

        if not lrn_pattern.match(lrn):
            messagebox.showwarning("Warning", "Invalid LRN format. Please enter a 12-digit numeric value.")
            return False

        if not first_name_pattern.match(first_name):
            messagebox.showwarning("Warning", "Invalid first name format. Please enter only alphabetical characters (A-Z, a-z) with a maximum length of 30 characters.")
            return False

        if not middle_name_pattern.match(middle_name):
            messagebox.showwarning("Warning", "Invalid middle name format. Please enter alphabetical characters (A-Z, a-z) and optionally separated by spaces, with a maximum length of 30 characters.")
            return False

        if not last_name_pattern.match(last_name):
            messagebox.showwarning("Warning", "Invalid last name format. Please enter alphabetical characters (A-Z, a-z) and optionally hyphenated, with a maximum length of 30 characters.")
            return False

        if not address_pattern.match(address):
            messagebox.showwarning("Warning", "Invalid address format. Please use only letters (A-Z, a-z), numbers (0-9), and the following special characters: space, comma, period, hash, and hyphen, with a maximum length of 100 characters.")
            return False

        if not phone_number_pattern.match(phone_number):
            messagebox.showwarning("Warning", "Invalid phone number format. Please enter a valid 11-digit phone number without spaces or special characters.")
            return False

        return True


    def add_data():
        if not validate_input():
            return
        
        lrn = studentLRNEntry.get()
        first_name = studentFNameEntry.get()
        middle_name = studentMNameEntry.get()
        last_name = studentLNameEntry.get()
        gender = studentGenderEntry.get()
        address = studentAddressEntry.get()
        phone_number = studentPhoneNumberEntry.get()
        year_level = studentYearLevelEntry.get()
        course = studentCourseEntry.get()

        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(host=host,user=user,password=password,database=database)

            # Create a cursor object
            cursor = connection.cursor()

            # Check if LRN already exists
            cursor.execute("SELECT * FROM students WHERE student_lrn=%s", (lrn,))
            existing_student = cursor.fetchone()

            if existing_student:
                messagebox.showwarning("Warning", "Student with the same LRN already exists.")
                return

            # Execute an INSERT query
            cursor.execute("INSERT INTO students (student_lrn, student_firstname, student_middlename, student_lastname, student_gender, student_address, student_phonenumber, student_year_level,student_course) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)",
                        (lrn, first_name, middle_name, last_name, gender, address, phone_number, year_level, course))

            # Commit the changes
            connection.commit()

            # Fetch updated data and refresh the Treeview
            fetch_data()

            # Clear the entry fields
            clearFunction()

        except Error as e:
            messagebox.showerror("Error", f"Error adding data to the database: {e}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def update_data():
        if not validate_input():
            return
        
        # Get the selected item from the Treeview
        selected_item = studentTable.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to update.")
            return
        
        # Ask for confirmation
        confirmed = messagebox.askokcancel("Confirm Deletion", "Are you sure you want to update this record?")

        if not confirmed:
            return


        # Get the values of the selected item
        values = studentTable.item(selected_item, 'values')

        # Extract the ID from the values
        selected_id = values[0]

        # Check if all required entry fields have values
        if not all((studentLRNEntry.get(), studentFNameEntry.get(), studentMNameEntry.get(), studentLNameEntry.get(), studentGenderEntry.get(), studentAddressEntry.get(), studentPhoneNumberEntry.get(), studentYearLevelEntry.get(),studentCourseEntry.get())):
            messagebox.showwarning("Warning", "Please fill in all required fields before updating.")
            return

        lrn = studentLRNEntry.get()
        first_name = studentFNameEntry.get()
        middle_name = studentMNameEntry.get()
        last_name = studentLNameEntry.get()
        gender = studentGenderEntry.get()
        address = studentAddressEntry.get()
        phone_number = studentPhoneNumberEntry.get()
        year_level = studentYearLevelEntry.get()
        course = studentCourseEntry.get()

        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(host=host,user=user,password=password,database=database)

            # Create a cursor object
            cursor = connection.cursor()

            # Execute an UPDATE query
            cursor.execute("UPDATE students SET student_lrn=%s, student_firstname=%s, student_middlename=%s, student_lastname=%s, student_gender=%s, student_address=%s, student_phonenumber=%s, student_year_level=%s, student_course=%s WHERE id=%s",
                        (lrn, first_name, middle_name, last_name, gender, address, phone_number, year_level,course, selected_id))

            # Commit the changes
            connection.commit()

            # Fetch updated data and refresh the Treeview
            fetch_data()

            # Clear the entry fields
            clearFunction()

        except Error as e:
            messagebox.showerror("Error", f"Error updating data in the database: {e}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_data():
        # Get the selected item from the Treeview
        selected_item = studentTable.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row to delete.")
            return

        # Ask for confirmation
        confirmed = messagebox.askokcancel("Confirm Deletion", "Are you sure you want to delete this record?")

        if not confirmed:
            return

        # Get the values of the selected item
        values = studentTable.item(selected_item, 'values')

        # Extract the ID from the values
        selected_id = values[0]

        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(host=host,user=user,password=password,database=database)

            # Create a cursor object
            cursor = connection.cursor()

            # Execute a DELETE query
            cursor.execute("DELETE FROM students WHERE id=%s", (selected_id,))

            # Commit the changes
            connection.commit()

            # Fetch updated data and refresh the Treeview
            fetch_data()

            # Clear the entry fields
            clearFunction()

        except Error as e:
            messagebox.showerror("Error", f"Error deleting data from the database: {e}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def fetch_data():
        # Clear existing data in the Treeview
        for record in studentTable.get_children():
            studentTable.delete(record)

        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(host=host,user=user,password=password,database=database)

            # Create a cursor object
            cursor = connection.cursor()

            # Execute a SELECT query
            cursor.execute("SELECT * FROM students")

            # Fetch all records
            records = cursor.fetchall()

            # Insert records into the Treeview
            for record in records:
                studentTable.insert("", "end", values=record)

        except Error as e:
            messagebox.showerror("Error", f"Error fetching data from the database: {e}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def clearFunction():
        for entry_widget in (studentLRNEntry, studentFNameEntry, studentMNameEntry, studentLNameEntry, studentAddressEntry, studentPhoneNumberEntry,):
            entry_widget.delete(0, 'end')

    def fetch_search_data(search_query=None, year_level=None):
        try:
            connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
            cursor = connection.cursor()

            if search_query:
                if year_level and not year_level == "All":
                    query = "SELECT * FROM students WHERE (student_lrn LIKE %s OR student_firstname LIKE %s OR student_middlename LIKE %s OR student_lastname LIKE %s) AND student_year_level = %s"
                    search_pattern = f"%{search_query}%"
                    cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern, year_level))
                else:
                    query = "SELECT * FROM students WHERE student_lrn LIKE %s OR student_firstname LIKE %s OR student_middlename LIKE %s OR student_lastname LIKE %s"
                    search_pattern = f"%{search_query}%"
                    cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            else:
                if year_level and not year_level == "All":
                    cursor.execute("SELECT * FROM students WHERE student_year_level = %s", (year_level,))
                else:
                    cursor.execute("SELECT * FROM students")

            rows = cursor.fetchall()

            for row in studentTable.get_children():
                studentTable.delete(row)

            for row in rows:
                studentTable.insert("", "end", values=row)

        except Error as e:
            messagebox.showerror("Error", f"Error fetching data from the database: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def fetch_data_option(year_level):
        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(host=host,user=user,password=password,database=database)

            # Create a cursor object
            cursor = connection.cursor()

            # Construct the SELECT query with a WHERE clause for search
            if year_level and not year_level == "All":
                query = "SELECT * FROM students WHERE student_year_level = %s "
                cursor.execute(query, (year_level,))
            else:
                # Execute a SELECT query without search
                cursor.execute("SELECT * FROM students")

            # Fetch all the rows
            rows = cursor.fetchall()

            # Clear existing data in the Treeview
            for row in studentTable.get_children():
                studentTable.delete(row)

            # Insert fetched data into the Treeview
            for row in rows:
                studentTable.insert("", "end", values=row)

        except Error as e:
            messagebox.showerror("Error", f"Error fetching data from the database: {e}")

        finally:
            # Close the cursor and connection
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def search_data():
        search_query = searchEntry.get()
        year_level = yearLevelOption.get()

        fetch_search_data(search_query, year_level)

    def select_data():
        # Get the selected item from the Treeview
        selected_item = studentTable.selection()

        if not selected_item:
            messagebox.showwarning("Warning", "Please select a row.")
            return

        # Fetch data for the selected item and populate the entry fields
        values = studentTable.item(selected_item, 'values')
        studentLRNEntry.delete(0, 'end')
        studentLRNEntry.insert(0, values[1])  # LRN
        studentFNameEntry.delete(0, 'end')
        studentFNameEntry.insert(0, values[2])  # First Name
        studentMNameEntry.delete(0, 'end')
        studentMNameEntry.insert(0, values[3])  # Middle Name
        studentLNameEntry.delete(0, 'end')
        studentLNameEntry.insert(0, values[4])  # Last Name
        studentGenderEntry.set(values[5])  # Gender
        studentAddressEntry.delete(0, 'end')
        studentAddressEntry.insert(0, values[6])  # Address
        studentPhoneNumberEntry.delete(0, 'end')
        studentPhoneNumberEntry.insert(0, values[7])  # Phone Number
        studentYearLevelEntry.set(values[8])   # Year Level
        studentCourseEntry.set(values[9])    # Course

    # ---------- END OF FUNCTIONS ------------

    pageTitle = customtkinter.CTkLabel(mainWindow, text="STUDENT INFORMATION SYSTEM", font=("Arial", 30, "bold"))
    pageTitle.pack(pady=20, anchor="center")

    addAdminButton = customtkinter.CTkButton(mainWindow,text='ADD ADMIN',height=40,width=130)
    addAdminButton.place(x=1200,y=20)

    # ---------- FORM FRAME------------
    formsFrame = customtkinter.CTkFrame(mainWindow, height=220)
    formsFrame.pack(fill=X,padx=30)

    studentLRNFrame = customtkinter.CTkFrame(formsFrame,width=380,height=35,fg_color='transparent')
    studentLRNFrame.place(x=55,y=25)
    studentLRNLabel = customtkinter.CTkLabel(studentLRNFrame,text="STUDENT LRN: ",font=('Arial',13,'bold'))
    studentLRNLabel.place(x=0,y=3)
    studentLRNEntry = customtkinter.CTkEntry(studentLRNFrame,placeholder_text="e.g 107921324321", width=250, height=35)
    studentLRNEntry.place(x=110,y=1)

    studentFNameFrame = customtkinter.CTkFrame(formsFrame,width=380,height=35,fg_color='transparent')
    studentFNameFrame.place(x=55,y=90)
    studentFNameLabel = customtkinter.CTkLabel(studentFNameFrame,text="FIRST NAME: ",font=('Arial',13,'bold'))
    studentFNameLabel.place(x=0,y=3)
    studentFNameEntry = customtkinter.CTkEntry(studentFNameFrame,placeholder_text="e.g Mark", width=250, height=35)
    studentFNameEntry.place(x=110,y=1)

    studentMNameFrame = customtkinter.CTkFrame(formsFrame,width=380,height=35,fg_color='transparent')
    studentMNameFrame.place(x=55,y=155)
    studentMNameLabel = customtkinter.CTkLabel(studentMNameFrame,text="MIDDLE NAME: ",font=('Arial',13,'bold'))
    studentMNameLabel.place(x=0,y=3)
    studentMNameEntry = customtkinter.CTkEntry(studentMNameFrame,placeholder_text="e.g Resma", width=250, height=35)
    studentMNameEntry.place(x=110,y=1)

    studentLNameFrame = customtkinter.CTkFrame(formsFrame,width=380,height=35,fg_color='transparent')
    studentLNameFrame.place(x=475,y=25)
    studentLNameLabel = customtkinter.CTkLabel(studentLNameFrame,text="LAST NAME: ",font=('Arial',13,'bold'))
    studentLNameLabel.place(x=0,y=3)
    studentLNameEntry = customtkinter.CTkEntry(studentLNameFrame,placeholder_text="e.g Dacurawat", width=250, height=35)
    studentLNameEntry.place(x=110,y=1)

    studentGenderFrame = customtkinter.CTkFrame(formsFrame,width=380,height=35,fg_color='transparent')
    studentGenderFrame.place(x=475,y=90)
    studentGenderLabel = customtkinter.CTkLabel(studentGenderFrame,text="GENDER: ",font=('Arial',13,'bold'))
    studentGenderLabel.place(x=0,y=3)
    studentGenderEntry = customtkinter.CTkOptionMenu(studentGenderFrame, width=250, height=35,values=['Male','Female'])
    studentGenderEntry.place(x=110,y=1)

    studentAddressFrame = customtkinter.CTkFrame(formsFrame,width=380,height=35,fg_color='transparent')
    studentAddressFrame.place(x=475,y=155)
    studentAddressLabel = customtkinter.CTkLabel(studentAddressFrame,text="ADDRESS: ",font=('Arial',13,'bold'))
    studentAddressLabel.place(x=0,y=3)
    studentAddressEntry = customtkinter.CTkEntry(studentAddressFrame,placeholder_text="e.g Blk 50 Lot 2 ...", width=250, height=35)
    studentAddressEntry.place(x=110,y=1)

    studentPhoneNumberFrame = customtkinter.CTkFrame(formsFrame,width=380,height=35,fg_color='transparent')
    studentPhoneNumberFrame.place(x=895,y=25)
    studentPhoneNumberLabel = customtkinter.CTkLabel(studentPhoneNumberFrame,text="MOBILE NUM: ",font=('Arial',13,'bold'))
    studentPhoneNumberLabel.place(x=0,y=3)
    studentPhoneNumberEntry = customtkinter.CTkEntry(studentPhoneNumberFrame,placeholder_text="e.g 09212121212", width=250, height=35)
    studentPhoneNumberEntry.place(x=110,y=1)

    studentYearLevelFrame = customtkinter.CTkFrame(formsFrame,width=380,height=35,fg_color='transparent')
    studentYearLevelFrame.place(x=895,y=90)
    studentYearLevelLabel = customtkinter.CTkLabel(studentYearLevelFrame,text="YEAR LEVEL: ",font=('Arial',13,'bold'))
    studentYearLevelLabel.place(x=0,y=3)
    studentYearLevelEntry = customtkinter.CTkOptionMenu(studentYearLevelFrame,width=250, height=35,values=['1st Year','2nd Year','3rd Year','4th Year'])
    studentYearLevelEntry.place(x=110,y=1)

    # Create a frame for the course dropdown
    studentCourseFrame = customtkinter.CTkFrame(formsFrame, width=380, height=35, fg_color='transparent')
    studentCourseFrame.place(x=895, y=155)
    studentCourseLabel = customtkinter.CTkLabel(studentCourseFrame, text="COURSE: ", font=('Arial', 13, 'bold'))
    studentCourseLabel.place(x=0, y=3)
    studentCourseEntry = customtkinter.CTkOptionMenu(studentCourseFrame, width=250, height=35, values=['B.S Computer Science', 'B.S Tourism Mngt.', 'B.S Hospitality Mngt.', 'B.S Bus. Administration', 'BTVTed Education'])
    studentCourseEntry.place(x=110, y=1)
    # ---------- END OF FORM FRAME------------

    # ---------- BUTTONS FRAME------------
    buttonsFrame = customtkinter.CTkFrame(mainWindow, height=70)
    buttonsFrame.pack(fill=X,padx=30,pady=10)

    selectButton = customtkinter.CTkButton(buttonsFrame,text='SELECT',height=40,width=130,command=select_data)
    selectButton.place(x=20,y=15)

    addButton = customtkinter.CTkButton(buttonsFrame,text='ADD STUDENT',height=40,width=130,command=add_data)
    addButton.place(x=160,y=15)

    updateButton = customtkinter.CTkButton(buttonsFrame,text='UPDATE',height=40,width=130,command=update_data)
    updateButton.place(x=300,y=15)

    deleteButton = customtkinter.CTkButton(buttonsFrame,text='DELETE',height=40,width=130,fg_color='red',hover_color="darkred",command=delete_data)
    deleteButton.place(x=440,y=15)

    clearButton = customtkinter.CTkButton(buttonsFrame,text='CLEAR',height=40,width=100,fg_color='red',hover_color="darkred",command=clearFunction)
    clearButton.place(x=580,y=15)

    yearLevelOption = customtkinter.CTkOptionMenu(buttonsFrame,width=150, height=35,values=['All','1st Year','2nd Year','3rd Year','4th Year'],command=fetch_data_option)
    yearLevelOption.place(x=710, y=18)
    yearLevelOption.set("All")

    searchFrame = customtkinter.CTkFrame(buttonsFrame,width=380,height=35,fg_color='transparent')
    searchFrame.place(x=890,y=18)
    searchLabel = customtkinter.CTkLabel(searchFrame,text="Search: ",font=('Arial',13,'bold'))
    searchLabel.place(x=0,y=3)
    searchEntry = customtkinter.CTkEntry(searchFrame,placeholder_text="Search", width=200, height=35)
    searchEntry.place(x=80,y=1)

    searchButton = customtkinter.CTkButton(buttonsFrame,text='SEARCH',height=40,width= 100,command=search_data)
    searchButton.place(x=1185,y=15)

    # ---------- END OF BUTTONS FRAME------------

    # ---------- TABLE FRAME------------
    tableFrame = customtkinter.CTkFrame(mainWindow, height=275)
    tableFrame.pack(fill=X,padx=30)

    columns = ("id", "lrn", "first_name", "middle_name", "last_name", "gender", "address", "phone_number", "year_level","course")

    studentTable = ttk.Treeview(tableFrame, columns=columns,show="headings")

    # Set the width of the "id" column
    studentTable.column("id", width=50)
    studentTable.column("lrn",width=100)
    studentTable.column("gender",width=100)
    studentTable.column("phone_number", width=100)   

    # Add columns
    for col in columns:
        studentTable.heading(col, text=col.upper(),anchor=CENTER)
        studentTable.column(col, anchor=CENTER)

    fetch_data()

    # Create vertical scrollbar
    vsb = customtkinter.CTkScrollbar(tableFrame,orientation="vertical",command=studentTable.yview)
    studentTable.configure(yscrollcommand=vsb.set)


    # Create horizontal scrollbar
    hsb = customtkinter.CTkScrollbar(tableFrame,orientation="horizontal",command=studentTable.xview)
    studentTable.configure(xscrollcommand=hsb.set)


    # Place the Treeview and scrollbars in the frame
    studentTable.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    # Configure row and column weights to make the Treeview expand
    tableFrame.rowconfigure(0, weight=1)
    tableFrame.columnconfigure(0, weight=1)

    # ---------- END OF TABLE FRAME------------
    mainWindow.mainloop()

loginWindowOutput()