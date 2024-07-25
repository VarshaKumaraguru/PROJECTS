from tkinter import *
import tkinter as tk
import mysql.connector
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
from email.message import EmailMessage
import ssl
import smtplib
import sqlite3

#Method to design Home page

root=Tk()
root.title("Home Page")

bg=PhotoImage(file="D:/VARSHA/Presentation2.png")

my_label=Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

root.iconbitmap("D:/VARSHA/PICS")
canvas=Canvas(root, width=600, height=400)
canvas.pack()

my_img=(Image.open("D:/VARSHA/PICS/logopics.jpeg"))
resized_img=my_img.resize((600,400), Image.ANTIALIAS)
new_img=ImageTk.PhotoImage(resized_img)
canvas.create_image(10,10, anchor=NW, image=new_img)

my_text=Label(root, text="Welcome to Book Town- The Best Place to Buy & Sell Books", fg="black", font=("Broadway 24 italic bold underline"))
my_text.pack(padx=5, pady=25)

p1=PhotoImage(file="C:/Users/DELL/Downloads/logopics.gif")
root.iconphoto(False, p1)

nameVar=StringVar()
emailVar=StringVar()
passVar=StringVar()

#method to add user register data in database    
def addNew():

    name=nameVar.get()
    email=emailVar.get()
    password=passVar.get()
    
    conn = sqlite3.connect('StudentDatabase.db')
    with conn:
        cursor=conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS StudentTable (Name TEXT,Email TEXT,Password Text)')
    count=cursor.execute('INSERT INTO StudentTable (Name,Email,Password) VALUES(?,?,?)',(name,email,password))
    
    if(cursor.rowcount>0):
        messagebox.showinfo("Success","Sign up Done")
        nextcmd()
    else:
        messagebox.showerror("Error","Signup Error")
    conn.commit()
    

#method to perform login    

def loginNow():

    email=emailVar.get()
    password=passVar.get()
    
    conn = sqlite3.connect('StudentDatabase.db')
    with conn:
        cursor=conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS StudentTable (Name TEXT,Email TEXT,Password Text)')
    cursor.execute('Select * from StudentTable Where Email=? AND Password=?',(email,password))
    
    if cursor.fetchone() is not None:
        messagebox.showinfo("Success","Login successful!")
        nextcmd()
    else:
        messagebox.showerror("Error","Login failed")

    conn.commit()
   

#method to design register window
def registerWindow():

    registerScreen=Toplevel(root)
    registerScreen.title("Register Here")
    registerScreen.geometry('500x500')
    registerScreen["background"]="light sky blue"

    p1=PhotoImage(file="C:/Users/DELL/Downloads/logopics.gif")
    registerScreen.iconphoto(False, p1)

    label = Label(registerScreen, text="Registration Here",width=20,fg="blue",font=("bold", 20))
    label.place(x=90,y=53)

    nameLabel = Label(registerScreen, text="FullName",width=20,font=("bold", 10))
    nameLabel.place(x=80,y=130)

    nameEntery = Entry(registerScreen,textvar=nameVar)
    nameEntery.place(x=250,y=130)

    emailLabel = Label(registerScreen, text="Email",width=20,font=("bold", 10))
    emailLabel.place(x=68,y=180)

    emailEntry = Entry(registerScreen,textvar=emailVar)
    emailEntry.place(x=250,y=180)

    passLabel = Label(registerScreen, text="Password",width=20,font=("bold", 10))
    passLabel.place(x=78,y=230)

    passEntry = Entry(registerScreen,textvar=passVar,show='*')
    passEntry.place(x=250,y=230)

    Button(registerScreen, text='Submit',width=20,bg='blue',fg='white',pady=5,command=addNew).place(x=180,y=380)

#Method to design login Screen   

def login():

    loginScreen=Toplevel(root)
    loginScreen.title("Login Here")
    loginScreen.geometry('500x500')
    p1=PhotoImage(file="C:/Users/DELL/Downloads/logopics.gif")
    loginScreen.iconphoto(False, p1)
    loginScreen["background"]="light sky blue"

    label = Label(loginScreen, text="Login Here",width=20,fg="blue", font=("bold", 20))
    label.place(x=90,y=53)

    emailLabel = Label(loginScreen, text="Email",width=20,font=("bold", 10))
    emailLabel.place(x=68,y=130)

    emailEntry = Entry(loginScreen,textvar=emailVar)
    emailEntry.place(x=240,y=130)

    passwordLabel = Label(loginScreen, text="Password",width=20,font=("bold", 10))
    passwordLabel.place(x=68,y=180)

    passwordEntry = Entry(loginScreen,textvar=passVar,show='*')
    passwordEntry.place(x=240,y=180)

    Button(loginScreen, text='Login Now',width=20,bg='blue',fg='white',pady=5,command=loginNow).place(x=180,y=230)

#Navigates to main page

def nextcmd():

    top1=Toplevel(root)
    top1.title("MainPage")
    top1.geometry("450x300")
    top1["background"]="light sky blue"

    p1=PhotoImage(file="C:/Users/DELL/Downloads/logopics.gif")
    top1.iconphoto(False, p1)

    buyer=Button(top1, text="Here to Buy?", font=("Times 24 italic"), command=buyerpop)
    buyer.pack(padx=5, pady=5)
    
    text=Label(top1, text="or", fg="black", font=("Times 24 italic"))
    text.pack(padx=5, pady=25)

    seller=Button(top1, text="Here to Sell?", font=("Times 24 italic"), command=sellerpop)
    seller.pack(padx=5, pady=35)

#Message to be displayed after buying
    
def select_record():

    reply = messagebox.askyesno('confirmation', 'Are you sure you want to place the order?')
    if reply == True:
        messagebox.showinfo('successful','Thank you for shopping with Book Town! WE ACCEPT ONLY CASH ON DELIVERY')

    email=emailVar.get()
    password=passVar.get()

    email_sender="shopatbooktown@gmail.com"
    email_password=password
    email_receiver=email

    subject="BOOK TOWN"
    body="Your order has been placed! Thank you for shopping with Book Town. For any queries contact us at shopatbooktown@gmail.com"

    em=EmailMessage()
    em["From"]=email_sender
    em["To"]=email_receiver
    em["subject"]=subject
    em.set_content(body)
    context=ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
    

#Design for buyer page
    
def buyerpop():
    r=Toplevel()
    r.title("Books Available")
    r.geometry("450x300")
    r["background"]="light sky blue"
    
    p1=PhotoImage(file="C:/Users/DELL/Downloads/logopics.gif")
    r.iconphoto(False, p1)

    my_connect = mysql.connector.connect(
    host="localhost",
    user="root", 
    passwd="1234",
    database="bookdata")

    my_conn = my_connect.cursor()

    def display():
        my_conn.execute("SELECT * FROM bookinformation")
        global i
        i=0
        for book in my_conn:
            for j in range(len(book)):
                e =Label(r,width=25,fg="black", text=book[j],relief="ridge", anchor="w")
                e.grid(row=i, column=j)
            e=tk.Button(r,width=12,text="Buy", relief="ridge",anchor="w",command=select_record)
            e.grid(row=i, column=7)
            i+=1
    display()

    r.mainloop()

#Design for Seller page

def sellerpop():
    r =Toplevel()
    r.title("Book details")
    r.geometry("450x300")
    r["background"]="light sky blue"

    tree = ttk.Treeview(r)

    p1=PhotoImage(file="C:/Users/DELL/Downloads/logopics.gif")
    r.iconphoto(False, p1)
    
    connect = mysql.connector.connect(host="localhost", user="root", passwd="1234", database="bookdata")
    conn = connect.cursor()
    conn.execute("select * from bookinformation")

    tree = ttk.Treeview(r)
    tree["show"] = "headings"

    tree["columns"] = ("Name", "Author", "Edition", "Category", "Cost", "Owner_Address", "Owner_phoneno")

    tree.column("Name", width=200, minwidth=200, anchor=tk.CENTER)
    tree.column("Author", width=150, minwidth=150, anchor=tk.CENTER)
    tree.column("Edition", width=100, minwidth=100, anchor=tk.CENTER)
    tree.column("Category", width=150, minwidth=150, anchor=tk.CENTER)
    tree.column("Cost", width=150, minwidth=150, anchor=tk.CENTER)
    tree.column("Owner_Address", width=150, minwidth=150, anchor=tk.CENTER)
    tree.column("Owner_phoneno", width=150, minwidth=150, anchor=tk.CENTER)

    tree.heading("Name", text="Name", anchor=tk.CENTER)
    tree.heading("Author", text="Author", anchor=tk.CENTER)
    tree.heading("Edition", text="Edition", anchor=tk.CENTER)
    tree.heading("Category", text="Category", anchor=tk.CENTER)
    tree.heading("Cost", text="Cost", anchor=tk.CENTER)
    tree.heading("Owner_Address", text="Owner's Address", anchor=tk.CENTER)
    tree.heading("Owner_phoneno", text="Owner's contact no", anchor=tk.CENTER)

    i = 0
    for ro in conn:
        tree.insert('', i, text="", values=(ro[0], ro[1], ro[2], ro[3], ro[4], ro[5], ro[6]))
    i += 1

    hsb = ttk.Scrollbar(r, orient="horizontal")

    hsb.configure(command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)
    hsb.pack(fill=X, side=BOTTOM)

    vsb = ttk.Scrollbar(r, orient="vertical")
    vsb.configure(command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(fill=Y, side=RIGHT)
    tree.pack()

    name = tk.StringVar()
    author = tk.StringVar()
    edition = tk.IntVar()
    category = tk.StringVar()
    cost = tk.IntVar()
    owner_address = tk.StringVar()
    owner_phoneno = tk.IntVar()

    #Method to add data in seller page

    def add_data(tree):
        f = Frame(r, width=400, height=320, background="grey")
        f.place(x=100, y=250)
        
        l1 = Label(f, text="name", width=8, font=("Times", 11, "bold"))
        e1 = Entry(f, textvariable=name, width=25)
        l1.place(x=50, y=30)
        e1.place(x=170, y=30)

        l2 = Label(f, text="author", width=8, font=("Times", 11, "bold"))
        e2 = Entry(f, textvariable=author, width=25)
        l2.place(x=50, y=70)
        e2.place(x=170, y=70)

        l3 = Label(f, text="edition", width=8, font=("Times", 11, "bold"))
        e3 = Entry(f, textvariable=edition, width=25)
        l3.place(x=50, y=110)
        e3.place(x=170, y=110)
        e3.delete(0, END)

        l4 = Label(f, text="category", width=8, font=("Times", 11, "bold"))
        e4 = Entry(f, textvariable=category, width=25)
        l4.place(x=50, y=150)
        e4.place(x=170, y=150)

        l5 = Label(f, text="cost", width=8, font=("Times", 11, "bold"))
        e5 = Entry(f, textvariable=cost, width=25)
        l5.place(x=50, y=190)
        e5.place(x=170, y=190)
        e5.delete(0, END)

        l6 = Label(f, text="address", width=8, font=("Times", 11, "bold"))
        e6 = Entry(f, textvariable=owner_address, width=25)
        l6.place(x=50, y=230)
        e6.place(x=170, y=230)

        l7 = Label(f, text="phoneno", width=8, font=("Times", 11, "bold"))
        e7 = Entry(f, textvariable=owner_phoneno, width=25)
        l7.place(x=50, y=270)
        e7.place(x=170, y=270)
        e7.delete(0, END)

        def insert_data():
            nonlocal e1, e2, e3, e4, e5, e6, e7
            s = name.get()
            a = author.get()
            e = edition.get()
            cat = category.get()
            cst = cost.get()
            addr = owner_address.get()
            ph = owner_phoneno.get()
            conn.execute(
            "INSERT INTO bookinformation("
            "name,author,edition,category,cost,owner_address,owner_phoneno"
            ") VALUES(%s,%s,%s,%s,%s,%s,%s)",
            (s, a, e, cat, cst, addr, ph))
            connect.commit()
            tree.insert('', "end", text="", values=(s, a, e, cat, cst, addr, ph))
            messagebox.showinfo("Success", "Data updated! Thank you for choosing Book Town")

            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e5.delete(0, END)
            e6.delete(0, END)
            e7.delete(0, END)
            f.destroy()

            email=emailVar.get()
            password=passVar.get()

            email_sender="shopatbooktown@gmail.com"
            email_password=password
            email_receiver=email

            subject="BOOK TOWN"
            body="Your books have been updated successfully! For any queries contact us at shopatbooktown@gmail.com"

            em=EmailMessage()
            em["From"]=email_sender
            em["To"]=email_receiver
            em["subject"]=subject
            em.set_content(body)
            context=ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

        submitbutton = tk.Button(f, text="Submit", command=insert_data)
        submitbutton.configure(font="Times 11 bold", bg="PaleTurquoise3", fg="white")
        submitbutton.place(x=100, y=290)

        cancelbutton = tk.Button(f, text="Cancel", command=f.destroy)
        cancelbutton.configure(font="Times 11 bold", bg="PaleTurquoise3", fg="white")
        cancelbutton.place(x=240, y=290)


    insertbutton = tk.Button(r, text="Insert", command=lambda: add_data(tree))
    insertbutton.configure(font="calibri 14 bold", bg="PaleTurquoise3", fg="white")
    insertbutton.place(x=600, y=260)

    r.mainloop()

#Buttons present in the home screen

button1=Button(root, text="Register here", font=("Times 14 italic"), command=registerWindow)
button1.pack(padx=5, pady=5)
button2=Button(root, text="Already have an account? Login", font=("Times 14 italic"), command=login)
button2.pack()

root.mainloop()


