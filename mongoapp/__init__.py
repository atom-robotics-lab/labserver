from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify
from pymongo import MongoClient
import datetime
from statistics import mean, mode

app = Flask(__name__)
app.config['SECRET_KEY'] = '8424276c875d016a'
client = MongoClient(
    "mongodb+srv://admin:admin@cluster0.cvhcbeg.mongodb.net/?retryWrites=true&w=majority")
db = client['attendence']

time = datetime.date.today()
tname = ''
sname = ''
d = []


@app.route('/', methods=['POST', 'GET'])
def login_in():
    if request.method == 'POST':
        data = db.login
        find = data.find_one({'username': request.form['username']})
        if find:
            authu = find['username']
            authp = find['password']
            if authu == request.form['username'] and authp == request.form['password']:
                session['username'] = request.form['username']
                return redirect(url_for('index', tname=authu))
            else:
                msg = 'Invalid Credentials'
                return render_template('login.html', msg=msg)
        else:
            msg = 'Invalid Credentials'
            return render_template('login.html', msg=msg)
    return render_template('login.html')


@app.route('/<tname>/', methods=['POST', 'GET'])
def index(tname):
    if session['username']:
        user = db[tname]
        search = user.find()
        return render_template('index.html', search=search, tname=tname)
    return redirect(url_for('login'))


@app.route('/<tname>/search/', methods=['POST', 'GET'])
def search(tname):
    if request.method == 'POST':
        data = db[tname]
        find = data.find({'Name': request.form['search'].upper()})
        find_time = data.find({'Name': request.form['search'].upper()})
        count = data.count_documents({'Name': request.form['search'].upper()})
        msg = ''
        time = [int((x['Time']).replace(':','')) for x in find_time]
        avg_time = str(int(mean(time)))
        avg_time = avg_time[:2]+":"+avg_time[2:4]+":"+avg_time[4:]
        print(f"Average time: {avg_time}")
        return render_template('search_2.html', search=find, tname=tname, msg=msg,count=count, avg_time=avg_time)
    print(tname)
    return render_template('search.html')


@app.route('/logout/')
def logout():
    session['username'] = None
    return redirect(url_for('login_in'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
