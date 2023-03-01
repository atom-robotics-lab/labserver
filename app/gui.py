# import os
# import csv
# import threading
# import time
from pymongo import MongoClient
import serial
from serial.tools import list_ports
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import secrets
import matplotlib
matplotlib.use('Agg')
try:
    client = MongoClient(
        "mongodb+srv://admin:root@cluster0.rsbrxww.mongodb.net/?retryWrites=true&w=majority")
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")
dba = client.test
collection2a = dba.cardinfo
collectiona = dba.cardinfo
secure_random = secrets.SystemRandom()

teal = "#2b6969"
dark_teal = "#28393a"
light_teal = "#badee2"

img_file = "atom logo 2k.png"
plus_img = "add plus.png"
delete_img = "delete cross.png"
filename = "records.csv"

username = "admin"
passwd = "Atom281121"
multiplier = .4


class GUI:

    def __init__(self):

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

        # Add COM functionality

        # Create frame
        self.com_frame = tk.Frame(
            self.frame2,
            bg="pink")
        self.com_frame.grid(row=0, column=0, pady=60)

        # Search button
        self.search_button = tk.Button(
            self.frame2,
            text="Search for devices",
            command=self.search,
            bg=teal,
            fg="white",
            # relief="flat",
            activebackground=light_teal)
        self.search_button.grid(row=0, column=0, padx=40)

        # COM ports
        self.options = ["No COM Ports available"]
        self.clicked = tk.StringVar()
        self.clicked.set("Choose COM Port")

        self.drop = tk.OptionMenu(self.frame2, self.clicked, ())
        self.drop.grid(row=0, column=1, padx=100)
        self.drop.config(bg=teal, fg="white",
                         highlightthickness=0, state="disabled", width=20)

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

        self.add_button.grid(row=1, column=0, pady=10, padx=150)
        self.add_button.config(state="disabled")

        tk.Label(
            self.frame2,
            text='Add an entry',
            bg=teal,
            fg="white",
            font=("TkMenuFont", 16)).grid(row=2, column=0, padx=5)

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

        self.delete_button.grid(row=1, column=1, pady=10, padx=150)
        self.delete_button.config(state="disabled")

        tk.Label(
            self.frame2,
            text='Delete an entry',
            bg=teal,
            fg="white",
            font=("TkMenuFont", 16)).grid(row=2, column=1, padx=5)

    def add_func(self):
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
                query = {"Name": self.name.get()}
                result = collection2a.find_one(query)
                if result:
                    card_no = result["Card ID"]
                else:
                    card_no = "ATM"+str(secure_random.randint(100, 999))
                    # while card_no in ids:
                    query2 = {"Card ID": card_no}
                    result2 = collection2a.find_one(query2)
                    while result2:
                        card_no = "ATM"+str(secure_random.randint(100, 999))
                        result2 = collection2a.find_one(query2)
                    rec = {"Card ID": card_no, "Name": self.name.get(
                    ), "Number": self.num.get(), "Mail": self.mail.get()}
                    collectiona.insert_one(rec)
                    # self.add_records(rec)
                self.send(card_no)
                print(
                    f"Name: {self.name.get()} \nPhone number: {self.num.get()} \nMail: {self.mail.get()} \nCard num: {card_no}")

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
            if (self.card_num.get() == ""):

                self.card_frame2.grid_forget()
                self.del_grid_visible = False
            else:
                print(f"Card number: {self.card_num.get()}")

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
            text='Card num:',
            bg=teal, fg="white",
            font=("TkMenuFont", 14)).grid(row=0, column=0, padx=5)

        # Text fields
        self.card_num = tk.Entry(self.card_frame2)
        self.card_num.grid(row=0,
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

    # def add_records(self,record):
    #     header=["Card num","Name","Number","Mail"]
    #     file_exists = os.path.isfile(filename)

    #     with open(filename,"a",newline="") as f:
    #         writer = csv.writer(f)
    #         if not file_exists:
    #             writer.writerow(header)

    #         writer.writerow(record)

    def search(self):
        self.options = list_ports.comports()
        if len(self.options) == 0:
            messagebox.showerror(
                'Error', 'No Devices found. Please check that your device is plugged in properly.')
            return
        self.drop["menu"].delete(0, 'end')
        for i in self.options:
            self.drop["menu"].add_command(
                label=i, command=lambda port=str(i): self.open(port))
        self.drop.configure(state="normal")

    def open(self, port):
        try:
            global arduino
            arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
            self.clicked.set(port)
            print("Port opened successfully!")
            self.add_button.config(state="normal")
            self.delete_button.config(state="normal")
        except:
            messagebox.showerror(
                'Error', 'Unable to Open the Port. Please check that your device is plugged in and you have selected the correct COM port.')

    def send(self, data):
        arduino.write(bytes(str(data), "utf-8"))
