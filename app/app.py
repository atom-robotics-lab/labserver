from http.server import BaseHTTPRequestHandler, HTTPServer
from pymongo import MongoClient
from datetime import date,datetime
import pytz


try:
    client = MongoClient(
        "mongodb+srv://admin:root@cluster0.rsbrxww.mongodb.net/?retryWrites=true&w=majority")
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")
db = client.test

collection = db.test
Request = None
MyFile = None


class RequestHandler_httpd(BaseHTTPRequestHandler):
    def do_GET(self):
        global Request, MyFile
        messagetosend = bytes('Welcome!', "utf")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        Request = self.requestline
        Request = Request[5: int(len(Request)-9)]
        print('Your request is:')
        print(Request)
        now = datetime.now(pytz.timezone('Asia/Kolkata'))
        d1 = now.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M:%S")
        rec1 = { "Name": Request,"Time":current_time,"Date":d1}
        collection.insert_one(rec1)
        return


print('Starting server ...')
server_address_httpd = ('', 8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
httpd.serve_forever()
