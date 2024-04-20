from tkinter import *
from tkinter import messagebox
import pymysql
from PIL import ImageTk

def clear():
    emailEntry.delete(0, END)
    usernameEntry.delete(0, END)
    passwordEntry.delete(0, END)
    confirmEntry.delete(0, END)
    check.set(0)


def connect_database():
    global obj
    if emailEntry.get() == '' or usernameEntry.get() == '' or passwordEntry.get() == '' or confirmEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif passwordEntry.get() != confirmEntry.get():
        messagebox.showerror('Error', 'Password Mismatch')
    elif check.get() == 0:
        messagebox.showerror('Error', 'Please Accept Term & Condition')
    else:
        try:
            con = pymysql.connect(host='localhost', user='root', password='Swapnil@123')
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Database connectivity Issue,Please Try Again')
            return

        try:
            query = 'CREATE DATABASE IF NOT EXISTS userdata'
            mycursor.execute(query)
            query = 'use userdata'
            mycursor.execute(query)

            query = 'CREATE TABLE data (id INT AUTO_INCREMENT PRIMARY KEY NOT NULL, email VARCHAR(50), username VARCHAR(100), password VARCHAR(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')
            query='select * from data where username=%s'
            mycursor.execute(query,(usernameEntry.get()))
            row=mycursor.fetchone()
            if row !=None:
                messagebox.showerror('Error','username Already exists')
            else:
                query ='insert into data(email,username,password) values(%s,%s,%s)'
                mycursor.execute(query,(emailEntry.get(),usernameEntry.get(),passwordEntry.get()))
                con.commit()
                con.close()
                # obj.username = usernameEntry.get()
                messagebox.showinfo('success','Registration is successful')
                clear()
                signup_window.destroy()
                import signin

def login_page():
    signup_window.destroy()
    import signin

signup_window = Tk()
signup_window.title('Signup Page')
signup_window.attributes('-fullscreen', True)
background = ImageTk.PhotoImage(file='bg.jpg')

bgLabel = Label(signup_window, image=background)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

frame = Frame(signup_window, bg='WHITE', bd=0)
frame.place(relx=0.63, rely=0.48, anchor=CENTER)

heading = Label(frame, text='CREATE AN ACCOUNT', font=('Microsoft Yahei UI Light', 18, 'bold'), bg='WHITE', fg='firebrick1')
heading.grid(row=0, column=0, pady=10)

emailLabel = Label(frame, text='Email', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='WHITE', fg='firebrick1')
emailLabel.grid(row=1, column=0, sticky='w', padx=20, pady=(10, 0))

emailEntry = Entry(frame, width=20, font=('Microsoft Yahei UI Light', 18, 'bold'), fg='WHITE', bg='firebrick1')
emailEntry.grid(row=2, column=0, sticky='w', padx=20)

usernameLabel = Label(frame, text='Username', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='WHITE', fg='firebrick1')
usernameLabel.grid(row=3, column=0, sticky='w', padx=20, pady=(10, 0))

usernameEntry = Entry(frame, width=20, font=('Microsoft Yahei UI Light', 18, 'bold'), fg='WHITE', bg='firebrick1')
usernameEntry.grid(row=4, column=0, sticky='w', padx=20)

passwordLabel = Label(frame, text='Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='WHITE', fg='firebrick1')
passwordLabel.grid(row=5, column=0, sticky='w', padx=20, pady=(10, 0))

passwordEntry = Entry(frame, width=20, font=('Microsoft Yahei UI Light', 18, 'bold'), fg='WHITE', bg='firebrick1')
passwordEntry.grid(row=6, column=0, sticky='w', padx=20)

confirmLabel = Label(frame, text='Confirm Password', font=('Microsoft Yahei UI Light', 10, 'bold'), bg='WHITE', fg='firebrick1')
confirmLabel.grid(row=7, column=0, sticky='w', padx=20, pady=(10, 0))

confirmEntry = Entry(frame, width=20, font=('Microsoft Yahei UI Light', 18, 'bold'), fg='WHITE', bg='firebrick1')
confirmEntry.grid(row=8, column=0, sticky='w', padx=20)
check = IntVar()

termsandconditions = Checkbutton(frame, text='I agree to the Terms & Conditions', font=('Microsoft Yahei UI Light', 9, 'bold'), fg='firebrick1', bg='WHITE', activebackground='WHITE', activeforeground='firebrick1', cursor='hand2', variable=check)
termsandconditions.grid(row=9, column=0, pady=10, padx=15)

signupbutton = Button(frame, text='Signup', font=('Open Sans', 16, 'bold'), bd=0, bg='firebrick1', fg='WHITE', activebackground='firebrick1', activeforeground='WHITE', width=17, command=connect_database)
signupbutton.grid(row=10, column=0, pady=10)

alreadyaccount = Label(frame, text="Already have an account?", font=('Open Sans', '9', 'bold'), bg='WHITE', fg='firebrick1')
alreadyaccount.grid(row=11, column=0, sticky='w', padx=20, pady=10)

loginButton = Button(frame, text='Log in', font=('Open Sans', '9', 'bold underline'), bg='WHITE', fg='blue', bd=0, cursor='hand2', activebackground='WHITE', activeforeground='blue', command=login_page)
loginButton.place(x=170, y=450)

signup_window.mainloop()


