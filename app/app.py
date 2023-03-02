import multiprocessing
from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
from datetime import date, datetime
import pytz
from gui import GUI
try:
    client = MongoClient(
        "mongodb+srv://admin:root@cluster0.rsbrxww.mongodb.net/?retryWrites=true&w=majority", connect=False)
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")
db = client.test
collection2 = db.cardinfo
collection = db.test
Request = None
MyFile = None


class RequestHandler_httpd(BaseHTTPRequestHandler):
    def do_GET(self):
        global Request, MyFile
        Request = self.requestline
        Request = Request[5: int(len(Request)-9)]
        print('Your card number is:')
        print(Request)
        query = {"Card ID": Request}
        result = collection2.find_one(query)
        if result:
            messagetosend = bytes('Marked', "utf")
            print("Atom Member")
            now = datetime.now(pytz.timezone('Asia/Kolkata'))
            d1 = now.strftime("%d/%m/%Y")
            current_time = now.strftime("%H:%M:%S")
            rec1 = {"Card ID": Request,
                    "Name": result["Name"], "Time": current_time, "Date": d1}
            collection.insert_one(rec1)
        else:
            messagetosend = bytes('NotMarked', "utf")
            print("Not an Atom Member")
        self.wfile.write(messagetosend)
        return


def function2():
    print('Starting server ...')
    server_address_httpd = ('', 8080)
    httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
    httpd.serve_forever()


def function1():
    GUI()


if __name__ == "__main__":
    process1 = multiprocessing.Process(target=function1)
    process2 = multiprocessing.Process(target=function2)

    process1.start()
    process2.start()
