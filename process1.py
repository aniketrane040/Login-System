import mysql.connector
from flask import Flask,render_template,url_for,request,session,redirect,flash,Response
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.secret_key = 'aniket'

mail=Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mail-id'
app.config['MAIL_PASSWORD'] = 'mail-password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route("/process",methods = ['POST', 'GET'])
def process():
	
    if request.method == 'POST':
      user = request.form['txtuname']
    else:
      user = request.args.get('txtuname')

    myresult = exists(user)

    for x in myresult:
        upass = x[5]
        if upass == request.form['txtupass']:
            session['username'] = user
            return render_template("home.html")
        else:
            flash("Inalid Password ...")
            return render_template("login.html")
     
    flash("Inalid Username ...")
    return render_template("login.html")

@app.route("/forgot",methods = ['POST', 'GET'])
def forgot():
    return render_template("forgotpassword.html")

@app.route("/send_otp",methods = ['POST', 'GET'])
def send_otp():
    uname = request.form['txtuname']
    session['forgot_user'] = uname
    email = ""
    myresult = exists(uname)
    for x in myresult:
        email = x[3]
        
    m = random.randint(10000, 99999)
    otp = str(m)
    session['otp'] = otp
    
    msg = Message(otp, sender = 'mail-id', recipients = [email])
    msg.body = "OTP Verification Password Recovery"
    mail.send(msg)
    return render_template("otpverify.html")

@app.route("/verify",methods = ['POST', 'GET'])
def verify():
    tmpotp = request.form['txtotp']
    if tmpotp == session['otp']:
        return render_template("change_password.html")
    
    return render_template("forgotpassword.html")

@app.route("/change",methods = ['POST', 'GET'])
def change():
    upwd = request.form['txtpass']
    uname = session['forgot_user']
    sql = "update students set password='"+upwd+"' where username='"+uname+"'"
    mydb = connect()
    mycursor = mydb.cursor(prepared=True)
    mycursor.execute(sql)
    mydb.commit()
    return render_template("Login.html")
    

@app.route("/register",methods = ['POST', 'GET'])
def register():
    name = request.form['txtname']
    rollno = request.form['txtrn']
    mail = request.form['txtmail']
    uname = request.form['txtuname']
    password = request.form['txtpass']
    f = request.files['file']
    img = f.filename
    mydb = connect()
    mycursor = mydb.cursor(prepared=True)
    sql="insert into students values('"+name+"','"+img+"','"+rollno+"','"+mail+"','"+uname+"','"+password+"')"
    mycursor.execute(sql)
    mydb.commit()
    return render_template("Login.html")
    
@app.route("/profile")
def profile():
    if 'username' in session:
        user = session['username']
        myresult = exists(user)

        for x in myresult:
            return render_template("student.html",result = x)
        
    return render_template("login.html")
        
def connect():
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="College"
            )
    return mydb

def exists(user):
        mydb = connect()
        mycursor = mydb.cursor(prepared=True)
        sql = "select * from students where username='"+ user +"'"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        return myresult
    
@app.route("/logout")
def logout():
    session.pop('username',None)
    return render_template("login.html")
    
    
if __name__ == '__main__':
   app.run()