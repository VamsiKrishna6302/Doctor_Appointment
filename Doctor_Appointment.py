import base64
import random
import smtplib


from threading import Thread
from flask import *
from flask_mysqldb import MySQL
from datetime import datetime
from flask_mail import Mail, Message
import os
app = Flask(__name__, static_url_path='/static')


 
app.secret_key = 'vamsi'

otp=random.randint(1000,9999)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pallalavamsikrishna@gmail.com'
app.config['MAIL_PASSWORD'] = 'wtyuyntloojgqncv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '6302369469'
app.config['MYSQL_DB'] = 'DOCTOR'
 
 
mysql = MySQL(app)
mail=Mail(app)
@app.route("/")
def index():
    return render_template("landingpage.html")

@app.route("/home")
def home():
    return render_template("landingpage.html")

@app.route("/About")
def about():
    return render_template("about.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/userlogin")
def userlogin():
    return render_template("userlogin.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/userlogin")
def login_user_login():
    return render_template("userlogin.html")

@app.route("/userregister")
def login_user_register():
    return render_template("userregister.html")

@app.route("/adminlogin")
def login_admin_login():
    return render_template("admin.html")

# @app.route("/user_home")
# def changed_login():
#     return render_template("patienthomepage.html")


# @app.route("/user_validate",methods=['POST','GET'])
# def validate_user():
#     if(request.method=='POST'):
#         email=request.form['email']
#         passwd=request.form['password']
#         cur=mysql.connection.cursor()
#         users=cur.execute("select * from user_register")
#         if(users>0):
#             u=cur.fetchall()
#             return render_template("")
        



@app.route('/user_validate', methods=['POST'])
def login():
    global email
    email = request.form['email']
    password = request.form['password']
    cur=mysql.connection.cursor()
    cur.execute("select * from user_register where email=%s and password=%s",(email,password))
    user = cur.fetchone()
    session['email'] = email
    
    if user:
        return render_template("patienthomepage.html")
    else:
        return render_template("invalid_credentials.html")
    
@app.route('/admin_validate', methods=['POST'])
def admin_login():
    email = request.form['email']
    password = request.form['pswrd']
    cur=mysql.connection.cursor()
    cur.execute("select * from admin_register where email=%s and password=%s",(email,password))
    admin = cur.fetchone()
    if admin:
        cur = mysql.connection.cursor()
        cur.execute("SELECT  * FROM booking")
        data = cur.fetchall()
        cur.close()
        return render_template('index2.html', users=data )
    else:
        return render_template("invalid_credentials.html")
    

@app.route("/feedback",methods=['POST','GET'])
def feedback():
    if request.method=='POST':
        username=request.form['name']
        email=request.form['email']
        feedback=request.form['feedback']
        cur=mysql.connection.cursor()
        cur.execute("insert into feedback values(%s,%s,%s)",(username,email,feedback))
        mysql.connection.commit()
        cur.close()
        return render_template("success.html")
    return "success"

@app.route('/adminSuccess')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM booking")
    data = cur.fetchall()
    cur.close()
    return render_template('index2.html', users=data )



@app.route('/insert', methods = ['POST']) # type: ignore
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        id=request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time=request.form['time']
        message = request.form['Message']
        datetime=date+" "+time
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO booking VALUES (%s,%s, %s, %s,%s,%s)", (id,name, email, phone,datetime,message))
        msg=Message(subject='BOOKED APPOINTMENT SUCCESSFULLY',sender='pallalavamsikrishna@gmail.com',recipients=[email])
        msg.html=render_template('Bookingemail.html',name=name,data=date,data1=time)
        mail.send(msg) 
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("select name,email from booking where id=%s",(id_data,))
    results = cur.fetchall()
    name=results[0][0]
    email=results[0][1]
    cur.execute("DELETE FROM booking WHERE id=%s", (id_data,))
    msg=Message(subject='CANCELLED APPOINTMENT',sender='pallalavamsikrishna@gmail.com',recipients=[email])
    msg.html=render_template('cancelemail1.html',name=name,email=email)
    mail.send(msg)
    mysql.connection.commit()

    return redirect(url_for('Index'))

@app.route('/update',methods=['POST','GET']) # type: ignore
def update():

    if request.method == 'POST':
        id=request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time=request.form['time']
        datetime=date+" "+time
        message = request.form['Message']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE booking
               SET name=%s, email=%s, phone=%s, appointmentdatetime=%s,message=%s
               WHERE id=%s
            """, (name , email, phone, datetime , message ,id))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('Index'))
    
@app.route('/Cancelleddata')
def get_data():

    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM cancelled_appointments")
    data = cur.fetchall()
    cur.close()
    cur.close()
    return render_template('cancelleddisplay.html', data=data)

@app.route('/UserFeedback')
def view_feedback():

    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM user_feedback")
    data = cur.fetchall()
    cur.close()
    cur.close()
    return render_template('FeedBackView.html', data=data)

@app.route("/adminregistration")
def admin_registerform():
    return render_template("adminregister.html")

@app.route("/adminregistered",methods=['POST','GET'])
def admin_register():
    if(request.method=='POST'):
        username=request.form['fullname']
        email=request.form['email']
        password=request.form['password']
        cnfrmpassword=request.form['confirmpassword']
        if(password==cnfrmpassword):
            cur=mysql.connection.cursor()
            cur.execute("insert into admin_register values(%s,%s,%s)",(email,password,username))
            mysql.connection.commit()
            cur.close()
            return render_template("success.html")
    return "success"

@app.route("/adminlogout")
def admin_logout():
    return render_template("logout.html")


# @app.route('/adminprofile')
# def admin_profile():
#     # Replace this with your actual profile data
#     profile_info = {'name': 'John Doe', 'email': 'johndoe@example.com'}
#     return render_template('admin_profile.html', profile_data=profile_info)

@app.route("/contactus",methods=['POST','GET']) # type: ignore
def contact_insert():
    if(request.method=='POST'):
        username=request.form['name']
        email=request.form['email']
        msg=request.form['msg']
        cur=mysql.connection.cursor()
        cur.execute("insert into contact_us(name,email,message) values(%s,%s,%s)",(username,email,msg))
        mysql.connection.commit()
        cur.close()
        return render_template("success.html")
    

@app.route('/Messages')
def contact_us():
    cur=mysql.connection.cursor()
    cur.execute("SELECT id,name,email,message,reply FROM contact_us")
    data = cur.fetchall()
    cur.close()
    return render_template('MessagesShow.html', data=data)

@app.route("/replymsg",methods=['POST','GET'])
def replymsg():
    if(request.method=='POST'):
        id1=request.form['id']
        id=int(id1)
        msg=request.form['reply']
        cur=mysql.connection.cursor()
        cur.execute("update contact_us set reply=%s where id=%s;",(msg,id))
        replymsgmail(id)
        # cur.execute("select * from contact_us where id=%s",(id))
        # data=cur.fetchone()
        # print(data)
        mysql.connection.commit()
        cur.close()
        return "success"
    return "sucess"

@app.route('/email/<int:id>', methods=['GET'])
def replymsgmail(id):
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT email FROM contact_us WHERE id = %s', (id,))
    results = cursor.fetchall()
    email=results[0][0]
    msg = Message('Reply from Admin!!!', 
                  sender='BookYourAppointment@hospital.com',
                  recipients=[email])
    msg.html = render_template('replymsgemail.html')
    mail.send(msg)
    return 'Email sent!'
    



@app.route("/user",methods=['POST','GET']) # type: ignore
def user_register():
    if(request.method=='POST'):
        username=request.form['name']
        email=request.form['email']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute("insert into user_register values(%s,%s,%s)",(username,email,password))
        register_email(username,email)
        mysql.connection.commit()
        cur.close()
        return render_template("patienthomepage.html")

# @app.route('/user_validate')
def register_email(username,email):
    msg = Message('Thank You for Registering!!!', 
                  sender='BookYourAppointment@hospital.com',
                  recipients=[email])
    msg.html = render_template('practicemail.html', name=username)
    mail.send(msg)
    return 'Email sent!'

@app.route('/password')
def password_template():
    return render_template("forgotpassword.html")

@app.route('/verify',methods=["POST"])
def verify():
    email=request.form['email']
    msg=Message(subject='RESET PASSWORD',sender='pallalavamsikrishna@gmail.com',recipients=[email])
    msg.html=render_template('otp_email.html',data=otp)
    mail.send(msg)
    return render_template('verify.html')

@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return render_template("reset_password.html")
    return render_template("invalid_credentials.html")


@app.route('/user_home',methods=['POST','GET']) # type: ignore
def user_changed_password():
    if(request.method=='POST'):
        email=request.form['email']
        password=request.form['password']
        cnfrm_psswd=request.form['confirm-password']
        cur=mysql.connection.cursor()
        if(password==cnfrm_psswd):
            cur.execute("update user_register set password=%s where email=%s",(password,email))
            mysql.connection.commit()
            cur.close()
            return render_template("patienthomepage.html")
        return render_template("invalid_credentials.html")

@app.route("/pickadate")
def pickadate(): # type: ignore
    return render_template("practice.html")

@app.route('/available_appointments',methods=['POST','GET']) # type: ignore
def view_dates():
    if(request.method=='POST'):
        date=request.form['date']
        k=[date+" 3:00pm-4:00pm",date+" 2:00pm-3:00pm",date+" 1:00pm-2:00pm",date+" 11:00am-12:00pm",date+" 12:00pm-1:00pm",date+" 10:00am-11:00am",date+" 9:00am-10:00am"]
        cur=mysql.connection.cursor()
        cur.execute("select Appointmentdatetime  from booking")
        dat=cur.fetchall()
        print(type(dat))
        m=[]
        a=[]
        for i in dat:
            for j in i:
                a.append(j)
        for i in k:
            if i not in a:
                m.append(i)
        return render_template('practice.html',data=m)


@app.route("/user_booking_form")
def user_booking():
    return render_template("Appointment.html")

@app.route("/user_booked",methods=['POST','GET']) # type: ignore
def user_booked():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time=request.form['time']
        datetime=date+" "+time
        message = request.form['Message']
        cur = mysql.connection.cursor()
        if(session.get('email')==email):
            cur.execute("""
               insert into booking(name,email,phone,appointmentdatetime,message) values(%s,%s,%s,%s,%s);
            """, (name , email, phone, datetime , message))
            msg=Message(subject='BOOKED APPOINTMENT SUCCESSFULLY',sender='pallalavamsikrishna@gmail.com',recipients=[email])
            msg.html=render_template('Bookingemail.html',name=name,data=date,data1=time)
            mail.send(msg)    
            mysql.connection.commit()
            return render_template("success.html")
        else:
            return "failure"
    
@app.route("/user_cancellation_form")
def user_cancellation_form():
    return render_template("cancellation.html")
    
@app.route("/canceluser",methods=['POST','GET'])
def user_cancel():
    id=request.form['id']
    id1=int(id)
    name=request.form['name']
    email=request.form['email']
    cur=mysql.connection.cursor()
    if(session.get('email')==email):
        cur.execute("select name,email from booking where id=%s",(id,))
        results = cur.fetchall()
        name=results[0][0]
        email=results[0][1]
        msg=Message(subject='CANCELLED APPOINTMENT',sender='pallalavamsikrishna@gmail.com',recipients=[email])
        msg.html=render_template('cancelemail1.html',name=name,email=email)
        mail.send(msg)

        cur.execute("delete from booking where id=%s and email=%s and name=%s",(id1,email,name))
        mysql.connection.commit()
        return "success"
    else:
        return "failure"


@app.route("/mybookings")
def user_bookings():
    email = session.get('email')
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM booking WHERE email = %s"
    cursor.execute(query, (email,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("bookedappointments.html",data=data)

@app.route("/mycancellations")
def user_cancelation():
    email = session.get('email')
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM cancelled_appointments WHERE email = %s"
    cursor.execute(query, (email,))
    data = cursor.fetchall()
    cursor.close()
    return render_template("cancelleddisplay.html",data=data)


@app.route("/feedback_form")
def user_feedback_form():
    return render_template("feedback.html")

@app.route("/feedbacks",methods=['POST','GET']) # type: ignore
def user_feedbacks():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        msg= request.form['feedback']
        if(session.get('email')==email):
            cur=mysql.connection.cursor()
            cur.execute("insert into user_feedback values(%s,%s,%s)",(name,email,msg))
            mysql.connection.commit()
            cur.close()
            return "done"
        else:
            return "Wrong email address Mentioned "
        
@app.route("/myfeedbacksshow")
def myfeedbacks():
    email=session.get('email')
    cur=mysql.connection.cursor()
    cur.execute("select * from user_feedback where email=%s",(email,))
    mysql.connection.commit()
    data=cur.fetchall()
    return render_template("showfeedbacks.html",data=data)

@app.route("/myadminreplys",methods=['POST','GET'])
def admin_replys():
    email=session.get('email')
    cur=mysql.connection.cursor()
    cur.execute("select * from contact_us where email=%s",(email,))
    mysql.connection.commit()
    data=cur.fetchall()
    return render_template("admin_replys.html",data=data)




if __name__ == "__main__":
    app.run(debug=True)