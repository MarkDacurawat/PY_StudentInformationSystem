import subprocess
from dotenv import load_dotenv, dotenv_values
import customtkinter
from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error

# ---------- FUNCTIONS ------------

config = dotenv_values('.env')

host = config["DB_HOST"]
user = config["DB_USER"]
password = config["DB_PASSWORD"]
database = config["DB_NAME"]

try:
    db = mysql.connector.connect(host=host,user=user,password=password,database=database)

    if db.is_connected():
        print("Connected To Database")

        def authenticate():
            username = usernameEntry.get()
            password = passwordEntry.get()

            sql = "SELECT * FROM admin WHERE username = %s AND password = %s"
            cursor = db.cursor()
            cursor.execute(sql,(username,password))
            user = cursor.fetchone()

            if user:
                messagebox.showinfo(title="Login Successfully",message="Login Successfully!")
                app.withdraw()
                open_another_file()
            else:
                messagebox.showerror(title="Login Failed!",message="Login Failed!")
                
        def open_another_file():
            # Replace 'path/to/your/other/file.py' with the actual path to your Python file
            subprocess.run(["python", "./mainpage.py"])
    else:
        raise Exception("Connection to MySQL database failed")
except Error as error:
    print(f"Database Error: {error}")

# ---------- END OF FUNCTIONS ------------



# ---------- GUI ------------
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.title("Login Form")
app.geometry("400x380")

customtkinter.CTkLabel(app,text="LOGIN FORM",font=("Arial",30,"bold")).place(x=105,y=80)

usernameEntry = customtkinter.CTkEntry(app,placeholder_text="Enter Your Username",width=230)
usernameEntry.place(x=90,y=150)

passwordEntry = customtkinter.CTkEntry(app,placeholder_text="Enter Your Password",show="*",width=230)
passwordEntry.place(x=90,y=200)

loginButton = customtkinter.CTkButton(app,width=230,height=40,text="LOGIN",command=authenticate)
loginButton.place(x=90,y=250)

app.mainloop()
# ---------- END OF GUI ------------