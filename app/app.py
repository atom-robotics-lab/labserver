import multiprocessing
from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
from datetime import date, datetime
import pytz
import csv
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import secrets
import matplotlib

try:
    client = MongoClient(
        "mongodb+srv://admin:admin@cluster0.cvhcbeg.mongodb.net/?retryWrites=true&w=majority")
    print("Connected successfully to MongoDB")
except:
    print("Could not connect to MongoDB")

matplotlib.use('Agg')
db = client.attendence
collection2 = db.cardinfo
collection = db.admin
Request = None
MyFile = None
teal = "#2b6969"
dark_teal = "#28393a"
light_teal = "#badee2"
img_file = "atom.png"
plus_img = "add.png"
delete_img = "delete.png"
filename = "records.csv"
username = "admin"
passwd = "Atom281121"
multiplier = .4
secure_random = secrets.SystemRandom()

class GUI:
    
    def __init__(self):
        #new
        record=["NULL"]
        self.add_records(record)

        self.screen1 = tk.Tk()

        self.screen_x = 1000
        self.screen_y = 650

        self.x = self.screen1.winfo_screenwidth() // 2 - self.screen_x//2
        self.y = int(self.screen1.winfo_screenheight() * 0.15)

        # Initialize
        self.screen1.title("A.T.O.M Card Auth")
        self.screen1.geometry(
            f"{self.screen_x}x{self.screen_y}+{str(self.x)}+{str(self.y)}")
        self.screen1.config(bg=teal)

        # screen1.eval("tk::PlaceWindow . center")

        # Frame 1 creation
        self.frame1 = tk.Frame(
            self.screen1,
            width=1000,
            height=650,
            bg=teal)

        self.frame1.pack(
            pady=50,
            padx=40,
            fill=tk.BOTH)
        # expand=True)

        # Frame 2 creation
        self.frame2 = tk.Frame(
            self.screen1,
            width=str(400*multiplier),
            height=str(650*multiplier),
            bg=teal)

        self.frame2.pack(
            pady=50,
            padx=50,
            fill=tk.BOTH)
        # expand=True)

        self.login_screen()
        # self.card_screen()

        self.screen1.mainloop()

    def login_screen(self):
        # Display Frame1
        self.frame1.tkraise()
        self.frame1.pack_propagate(False)

        # Login frame
        self.login_frame = tk.Frame(
            self.frame1,
            width=str(400*multiplier),
            height=str(650*multiplier),
            bg=teal)
        self.login_frame.pack(side=tk.RIGHT, padx=10)

        # Logo
        self.logo_img = Image.open(img_file)
        self.logo_img = self.logo_img.resize((400, 400))

        self.logo = ImageTk.PhotoImage(self.logo_img)
        self.logo_widget = tk.Label(
            self.frame1, image=self.logo, bd=0, bg=teal)
        self.logo_widget.image = self.logo
        self.logo_widget.pack(side=tk.LEFT)

        # Incorrect pass label
        self.incor = tk.Label(
            self.login_frame,
            text='Incorrect username or password, try again',
            bg=teal,
            fg=teal,
            font=("TkHeadingFont", 10))

        self.incor.grid(row=0, pady=10, padx=25)

        # Frame for input fields
        self.text_frame = tk.Frame(self.login_frame, bg=teal)
        self.text_frame.grid(row=1, pady=5, padx=25)

        tk.Label(
            self.text_frame,
            text='Username:',
            bg=teal,
            fg="white",
            font=("TkMenuFont", 12)).grid(row=0, padx=5)

        tk.Label(
            self.text_frame,
            text='Password:',
            bg=teal,
            fg="white",
            font=("TkMenuFont", 12)).grid(row=1, padx=5)

        # Entry fields
        self.user = tk.Entry(self.text_frame)
        self.user.grid(row=0, column=1, padx=5, pady=10)

        self.pwd = tk.Entry(self.text_frame, show="*")
        self.pwd.grid(row=1, column=1, padx=5, pady=10)

        # Visibility Button
        self.check_var = tk.IntVar()
        self.check = tk.Checkbutton(
            self.text_frame,
            bg=teal,
            variable=self.check_var,
            command=lambda: self.pass_visi())

        self.check.grid(row=1, column=2)

        # Login button
        tk.Button(
            self.login_frame,
            text="Login",
            font=("TkHeadingFont", 11),
            bg=dark_teal,
            fg="white",
            cursor="hand2",
            activebackground=light_teal,
            activeforeground="black",
            command=lambda: self.pwd_chk()).grid(row=2, pady=10, padx=25)

    def card_screen(self):
        # remove Frame 1
        self.frame1.pack_forget()
        self.frame2.tkraise()
        self.add_grid_visible = False
        self.del_grid_visible = False

        # Add button

        # Open image
        self.add_img = Image.open(plus_img)
        self.add_img = self.add_img.resize((150, 150))
        self.add_but = ImageTk.PhotoImage(self.add_img)

        # Button
        self.add_button = tk.Button(
            self.frame2,
            # text="Add an entry",
            # font=("TkHeadingFont",11),
            bg=teal,
            # fg="white",
            image=self.add_but,
            cursor="hand2",
            activebackground=light_teal,
            relief="flat",
            # activeforeground="black",
            command=lambda: self.add_func())

        self.add_button.grid(row=0, column=0, pady=10, padx=150)
        #self.add_button.config(state="disabled")

        tk.Label(
            self.frame2,
            text='Add an entry',
            bg=teal,
            fg="white",
            font=("TkMenuFont", 16)).grid(row=1, column=0, padx=5)

        # Delete button

        # Open image
        self.dlt_img = Image.open(delete_img)
        self.dlt_img = self.dlt_img.resize((150, 150))
        self.dlt_but = ImageTk.PhotoImage(self.dlt_img)

        # Button
        self.delete_button = tk.Button(
            self.frame2,
            # text="Delete an entry",
            # font=("TkHeadingFont",11),
            bg=teal,
            # fg="white",
            image=self.dlt_but,
            cursor="hand2",
            activebackground=light_teal,
            relief="flat",
            # activeforeground="black",
            command=lambda: self.del_func())

        self.delete_button.grid(row=0, column=1, pady=10, padx=150)
        #self.delete_button.config(state="disabled")

        tk.Label(
            self.frame2,
            text='Delete an entry',
            bg=teal,
            fg="white",
            font=("TkMenuFont", 16)).grid(row=1, column=1, padx=5)

    def add_func(self):
        global card_no
        # Check and remove delete grid
        if self.del_grid_visible:
            self.card_frame2.grid_forget()
            self.del_grid_visible = False

        # Check if add grid visible
        if self.add_grid_visible == False:
            self.add_grid()

        else:
            if (self.name.get() == "" and self.num.get() == "" and self.mail.get() == ""):

                self.text_frame2.grid_forget()
                self.add_grid_visible = False
            else:
                # with open(filename,"a+",newline="") as f:
                #     reader=csv.reader(f)
                #     ids=[row[0] for row in reader]
                query = {"Name": self.name.get().upper()}
                result = collection2.find_one(query)
                if result:
                    card_no = result["Card ID"]
                else:
                    card_no = "ATM"+str(secure_random.randint(100, 999))
                    # while card_no in ids:
                    query2 = {"Card ID": card_no}
                    result2 = collection2.find_one(query2)
                    while result2:
                        card_no = "ATM"+str(secure_random.randint(100, 999))
                        result2 = collection2.find_one(query2)
                    rec = {"Card ID": card_no, "Name": self.name.get(
                    ).upper(), "Number": self.num.get(), "Mail": self.mail.get()}
                    collection2.insert_one(rec)
                record=[card_no]
                self.add_records(record)
                print(
                    f"Name: {self.name.get()} \nPhone number: {self.num.get()} \nMail: {self.mail.get()} \nCard num: {card_no}")
                messagebox.showinfo("Success",f"Your Card id is: {card_no}")

    def add_grid(self):
        self.add_grid_visible = True
        # Label fields

        self.text_frame2 = tk.Frame(
            self.frame2,
            # width =100,
            # height = 100,
            bg=teal)

        self.text_frame2.grid(row=2, column=0, pady=20, padx=35)

        tk.Label(
            self.text_frame2,
            text='Name:',
            bg=teal, fg="white",
            font=("TkMenuFont", 14)).grid(row=0, padx=5)

        tk.Label(
            self.text_frame2,
            text='Phone num:',
            bg=teal, fg="white",
            font=("TkMenuFont", 14)).grid(row=1, padx=5)

        tk.Label(
            self.text_frame2,
            text='Email:',
            bg=teal, fg="white",
            font=("TkMenuFont", 14)).grid(row=2, padx=5)

        # Text fields
        self.name = tk.Entry(self.text_frame2)
        self.name.grid(row=0,
                       column=1,
                       padx=5,
                       pady=5)

        self.num = tk.Entry(self.text_frame2)
        self.num.grid(row=1,
                      column=1,
                      padx=5,
                      pady=5)

        self.mail = tk.Entry(self.text_frame2)
        self.mail.grid(row=2,
                       column=1,
                       padx=5,
                       pady=5)

    def del_func(self):
        # Check and remove add grid
        if self.add_grid_visible:
            self.text_frame2.grid_forget()
            self.add_grid_visible = False

        # Check if delete grid visible
        if self.del_grid_visible == False:
            self.del_grid()

        else:
            if (self.name.get() == ""):

                self.card_frame2.grid_forget()
                self.del_grid_visible = False
            else:
                card_no="delete"
                record=[card_no]
                self.add_records(record)
                print(f"Name: {self.name.get()}")
                #rec= {"Card ID": None, "Name": None, "Number": None, "Mail": None}
                collection2.delete_one({"Name":self.name.get().upper()})

    def del_grid(self):
        self.del_grid_visible = True

        self.card_frame2 = tk.Frame(
            self.frame2,
            # width =100,
            # height = 100,
            bg=teal)

        self.card_frame2.grid(row=2, column=1, pady=20, padx=35)

        # Label
        tk.Label(
            self.card_frame2,
            text='Name:',
            bg=teal, fg="white",
            font=("TkMenuFont", 14)).grid(row=0, column=0, padx=5)

        # Text fields
        self.name = tk.Entry(self.card_frame2)
        self.name.grid(row=0,
                        column=1,
                        padx=5,
                        pady=5)

    def pass_visi(self):
        if self.check_var.get() == 1:
            self.pwd.config(show="")
        else:
            self.pwd.config(show="*")

    def pwd_chk(self):
        if self.pwd.get() == passwd and self.user.get() == username:
            self.incor.config(fg=teal)
            self.card_screen()
        else:
            print("Wrong username or password entered, try again")
            self.incor.config(fg="red")

    def clear(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def add_records(self,record):
        with open(filename,"w",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(record)

class RequestHandler_httpd(BaseHTTPRequestHandler):
    def do_GET(self):
        with open(filename,"r",newline="") as f:
            reader=csv.reader(f)
            for lines in reader:
                card_no=lines
            if card_no[0]!="NULL":
                messagetosend = bytes(card_no[0], "utf-8")            
                self.wfile.write(messagetosend)
                with open(filename,"w",newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["NULL"])
        return
    
class RequestHandler_httpd2(BaseHTTPRequestHandler):
    def do_GET(self):
        global Request, MyFile
        Request = self.requestline
        Request = Request[5: int(len(Request)-9)]
        print('Your card number is:',Request)
        query = {"Card ID": Request}
        result = collection2.find_one(query)
        if result:
            messagetosend = bytes('Marked', "utf-8")
            print("Atom Member")
            now = datetime.now(pytz.timezone('Asia/Kolkata'))
            d1 = now.strftime("%d/%m/%Y")
            current_time = now.strftime("%H:%M:%S")
            rec1 = {"Card ID": Request,
                    "Name": result["Name"], "Time": current_time, "Date": d1}
            collection.insert_one(rec1)
        else:
            messagetosend = bytes('NotMarked', "utf-8")
            print("Not an Atom Member")
        self.wfile.write(messagetosend)
        return


def function2():
    print('Starting server for Creating/Deleting cards')
    server_address_httpd = ('', 8080)
    httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
    httpd.allow_reuse_address = True
    httpd.serve_forever()


def function3():
    print('Starting server for Attendance')
    server_address_httpd = ('', 8000)
    httpd = HTTPServer(server_address_httpd, RequestHandler_httpd2)
    httpd.allow_reuse_address = True
    httpd.serve_forever()


def function1():
    GUI()


if __name__ == "__main__":
    process1 = multiprocessing.Process(target=function1)
    process2 = multiprocessing.Process(target=function2)
    process3 = multiprocessing.Process(target=function3)

    process1.start()
    process2.start()
    process3.start()