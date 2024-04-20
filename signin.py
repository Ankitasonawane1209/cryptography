from tkinter import *
from tkinter import messagebox

from PIL import ImageTk
import pymysql
from main_app import MainApp
import os


def forget_pass():
    def change_password():
        if user_entry.get()=='' or newpass_entry.get()=='' or confirmpass_entry.get()=='':
            messagebox.showerror('Error','All Fileds Are Requird',parent=window)
        elif newpass_entry.get()!=confirmpass_entry.get():
            messagebox.showerror('Error', 'password and confirm password are not matching', parent=window)
        else:
            con = pymysql.connect(host='localhost', user='root', password='Swapnil@123',database='userdata')
            mycursor = con.cursor()
            query = 'select * from data where username=%s'
            mycursor.execute(query, (user_entry.get()))
            row = mycursor.fetchone()
            if row==None:
                messagebox.showerror('Error','Incorrect Username',parent=window)
            else:
                query='update data set password =%s where username=%s'
                mycursor.execute(query,(newpass_entry.get(),user_entry.get()))
                con.commit()
                con.close()
                messagebox.showinfo('Success', 'password is reset, please login with new password', parent=window)
                window.destroy()

    window = Toplevel()
    window.title('change Password')


    bgPic = ImageTk.PhotoImage(file='background.jpg')
    bglabel= Label(window, image=bgPic)

    bglabel.grid()

    heading_label=Label(window,text='RESET PASSWORD',font=('arial','18','bold'),
                         bg='white',fg='magenta2')
    heading_label.place(x=480,y=60)

    userLabel =Label(window,text='username',font=('arial',12,'bold'),bg='white',fg='pink')
    userLabel.place(x=470,y=130)

    user_entry =Entry(window,width=25,fg='magenta2',font=('arial',11,'bold'),bd=0)
    user_entry.place(x=470,y=160)
    Frame(window,width=250,height=2,bg='pink').place(x=470,y=180)

    passwordLabel = Label(window, text='New Password', font=('arial', 12, 'bold'), bg='white', fg='pink')
    passwordLabel.place(x=470, y=210)

    newpass_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    newpass_entry.place(x=470, y=240)
    Frame(window, width=250, height=2, bg='pink').place(x=470, y=260)

    confirmpassLabel = Label(window, text='confirm password', font=('arial', 12, 'bold'), bg='white', fg='pink')
    confirmpassLabel.place(x=470, y=290)

    confirmpass_entry = Entry(window, width=25, fg='magenta2', font=('arial', 11, 'bold'), bd=0)
    confirmpass_entry.place(x=470, y=320)
    Frame(window, width=250, height=2, bg='pink').place(x=470, y=340)

    submitButton = Button(window, text='SUBMIT', font=('Open Sans', '16', 'bold '),
                        width=19, bg='magenta2', fg='WHITE', bd=0, cursor='hand2', activebackground='magenta2', activeforeground='WHITE',
                          command=change_password)
    submitButton.place(x=470, y=390)

    window.mainloop()


def login_user():
    if usernameEntry.get()==''or passwordEntry.get()=='':
        messagebox.showerror('Error','All Fields Are Required')

    else:
        try:
           con=pymysql.connect(host='localhost',user='root',password='Swapnil@123')
           mycursor= con.cursor()

        except:
            messagebox.showerror('Error','connection is not establish try again')
            return
        query = 'use userdata'
        mycursor.execute(query)
        query='select * from data where username=%s and password=%s'
        mycursor.execute(query,(usernameEntry.get(),passwordEntry.get()))
        row=mycursor.fetchone()
        if row==None:

           messagebox.showerror('Error', 'Invalid username or password')
        else:
            # If login is successful, create a subfolder in the encrypted folder
            username = usernameEntry.get()

            # Specify the path to the encrypted and decrypted folders
            encrypted_folder = os.path.join('C:/Users/91772/Desktop/march15', 'encrypted', username)
            decrypted_folder = os.path.join('C:/Users/91772/Desktop/march15', 'decrypted', username)

            os.makedirs(encrypted_folder, exist_ok=True)
            os.makedirs(decrypted_folder, exist_ok=True)

            messagebox.showinfo('Welcome', 'Login successful')

            login_window.destroy()
            root = Tk()

            obj = MainApp(root)
            obj.username = username
            obj.show_file_manager()


# Functionality part
def signup_page():
    login_window.destroy()
    import signup


def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)

def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)

def user_enter(event):
    if usernameEntry.get() == 'Username':
        usernameEntry.delete(0, END)

def password_enter(event):
    if passwordEntry.get() == 'Password':
        passwordEntry.delete(0, END)

# GUI part
# GUI part
login_window = Tk()

login_window.title('Login Page')

# Maximize the window
login_window.attributes('-fullscreen', True)

bgImage = ImageTk.PhotoImage(file='bg.jpg')
bgLabel = Label(login_window, image=bgImage)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

heading = Label(login_window, text='USER LOGIN', font=('microsoft Yahei UI Light', 23, 'bold'),
                bg='white', fg='firebrick1')
heading.place(x=870, y=210)

usernameEntry = Entry(login_window, width=25, font=('microsoft Yahei UI Light', 11, 'bold'),
                      bg='white',bd=0 ,fg='firebrick1')
usernameEntry.place(x=860, y=290)
usernameEntry.insert(0, 'Username')
usernameEntry.bind('<FocusIn>', user_enter)

frame1 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame1.place(x=860, y=320)

passwordEntry = Entry(login_window, width=25, font=('microsoft Yahei UI Light', 11, 'bold'),
                      bg='white',bd=0, fg='firebrick1')
passwordEntry.place(x=860, y=350)
passwordEntry.insert(0, 'Password')
passwordEntry.bind('<FocusIn>', password_enter)

frame2 = Frame(login_window, width=250, height=2, bg='firebrick1')
frame2.place(x=860, y=380)

openeye = PhotoImage(file='openeye.png')
eyeButton = Button(login_window, image=openeye, bd=0, bg='white', activebackground='white',
                   cursor='hand2', command=hide)
eyeButton.place(x=1080, y=350)

forgotButton = Button(login_window, text='Forgot Password', bd=0, bg='white', activebackground='white',
                      cursor='hand2', font=('microsoft Yahei UI Light', 9, 'bold'),
                      fg='firebrick1', activeforeground='firebrick1',command=forget_pass)
forgotButton.place(x=990, y=390)

loginButton = Button(login_window, text='login', font=('Open Sans', 16, 'bold'),
                     fg='white', bg='firebrick1', activeforeground='white', activebackground='firebrick1',
                     cursor='hand2', bd=0, width=19,command=login_user)
loginButton.place(x=850, y=430)

orLabel = Label(login_window, text='----------------OR---------------', font=('Open Sans', 16), fg='firebrick1', bg='white')
orLabel.place(x=850, y=490)

google_logo = PhotoImage(file='google.png')
googleLabel = Label(login_window, image=google_logo, bg='white')
googleLabel.place(x=880, y=530)

facebook_logo = PhotoImage(file='facebook.png')
fbLabel = Label(login_window, image=facebook_logo, bg='white')
fbLabel.place(x=950, y=530)

twitter_logo = PhotoImage(file='twitter.png')
twitterLabel = Label(login_window, image=twitter_logo, bg='white')
twitterLabel.place(x=1025, y=530)

signupLabel = Label(login_window, text='Dont have an account?', font=('Open Sans', 9), fg='firebrick1', bg='white')
signupLabel.place(x=860, y=590)

newaccountButton = Button(login_window, text='Create New One', font=('Open Sans', 9, 'bold underline'),
                          fg='blue', bg='white', activeforeground='blue',
                          activebackground='white',
                          cursor='hand2', bd=0,command=signup_page)
newaccountButton.place(x=990, y=590)




login_window.mainloop()