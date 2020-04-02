from flask import Flask,render_template,request
import sqlite3 as sq

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        uname = request.form['uname']
        psw = request.form['psw']
        print(uname,psw)
        conn = sq.connect('userdeets')
        cursor = conn.cursor()
        cursor.execute('''
        create table if not exists users(username varchar,password varchar)
        ''')
        conn.commit()
        cursor.execute('''
        insert into users(username,password)
        values (?,?)
        ''',(uname,psw))
        conn.commit()
        return render_template('success.html')
    return render_template('success.html')

@app.route('/dashboard')
def dashboard():
    conn = sq.connect('userdeets')
    cursor = conn.cursor()
    cursor.execute('''
    select * from users
    ''')
    check = cursor.fetchall()

    if check:
        lis = []
        for i in check:
            par = {
                'username':i[0],
                'password':i[1]
            }
            lis.append(par)
        return render_template('dashboard.html',data=lis)
if '__main__' == __name__:
    app.run(debug="true")