import re
import json
import sqlite3
from flask import g
from flask import Flask,request,url_for
from flask_mail import Mail,Message
from flask.templating import render_template
def readData():
    with open('test/data.json','r') as file:
        return json.load(file)

app = Flask(__name__)
app.secret_key='e952c00c229a124132265734b385c88c'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'se.abdullah.h@gmail.com'
app.config['MAIL_PASSWORD'] = 'uaasndhhcmyatchi'



mail = Mail(app)
 #send email to user and company
@app.route('/email', methods=['POST'])
def send_email():
    fname = request.form['fname']
    lname = request.form['lname']
    user_email = request.form['user_email']
    phone = request.form['phone']
    role = request.form['role']
    company = request.form['company']

    #send user message to company email

    #usr_msg = Message('Customer - Contact Us', sender= f'{user_email}' , recipients= ['khaledmaddah1995@gmail.com'])
    #usr_msg.body = f'''{user_message} \n - {user_email}'''
    #mail.send(usr_msg)

    #reply confirmation to user
    msg = Message('Job application response', sender = "noreply@interviewr.com", recipients = [user_email])
    msg.body = f''' Hello {fname } {lname} , we have recieved your application, we will get back to you in the next 2 weeks'''
    mail.send(msg)
    return email()

@app.route('/index')
@app.route('/')
def index():
    return render_template('jobs.html')


@app.route('/about')
def aboutus_():
    return render_template('aboutus.html')

@app.route('/login')
def login():
    return render_template('registration.html')

@app.route('/email')
def email():
    return render_template('email_conf.html')

# route will contain a parameter of type string named job.
# the data will be entered in the browser by the user.
# the job parameter will be processed by the function jobs. 
# the jobs function accepts one parameter named job which will be passed by the route function.
# the variable f uses the function readData() to read the data.json file.
# we then use the job parameter as the key to retrieve the requested data from the json by the user.
@app.route('/<string:job>')
def jobs(job):
    g.cur.execute(f"select * from Jobs where ID = '{job}' ")
    js= g.cur.fetchall()
    g.cur.execute(f"select * from interviewers where sid = '{job}' ")
    ints= g.cur.fetchall()
    
    return render_template('job1.html',js=js[0], ints=ints[0])







@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/m',methods=['POST'])
def reg():

    email= request.form['email']
    un= request.form['un']
    pw= request.form['pw']

    print(email,un,pw)
    g.cur.execute(f"INSERT INTO users (email , username , password) VALUES ('{email}' ,'{un}' ,'{pw}')") 
    g.db.commit()
    return render_template('jobs.html')

    

@app.before_request
def before_request():
    g.db = sqlite3.connect(r"C:\Users\zarak\OneDrive\Desktop\interview\interviewer.db")
    g.cur = g.db.cursor()


if __name__ == '__main__':
    app.run(debug=True, port='3000')
