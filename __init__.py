from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import random

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'pallalavamsikrishna@gmail.com'
app.config['MAIL_PASSWORD'] = 'wtyuyntloojgqncv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

app.secret_key = 'many random bytes' # type: ignore
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '6302369469'
app.config['MYSQL_DB'] = 'DOCTOR'

mysql = MySQL(app)
mail=Mail(app)

@app.route("/")
def user_bookings():
    email = 'pvamsikrishnaece2022@gmail.com'
    cur=mysql.connection.cursor()
    cur.execute("select * from booking where email=%s ",(email,))
    data=cur.fetchall()
    cur.close()
    return render_template("bookedappointments.html",data=data)

# @app.route('/')
# def get_users_by_name(name):
#     # Create a cursor
#     email = 'pvamsikrishnaece2022@gmail.com'
#     cursor = mysql.connection.cursor()

#     # Execute the SELECT statement with the condition
#     query = "SELECT * FROM booking WHERE email = %s"
#     cursor.execute(query, (email,))

#     # Fetch the results
#     data = cursor.fetchall()

#     # Close the cursor
#     cursor.close()

#     # Render the results template with the results
#     return render_template("bookedappointments.html",data=data)
# @app.route("/")
# def index():
#     return render_template("cancellation.html")

# @app.route("/canceluser",methods=['POST','GET'])
# def user_cancel():
#     id=request.form['id']
#     id1=int(id)
#     name=request.form['name']
#     email=request.form['email']
#     cur=mysql.connection.cursor()
#     cur.execute("delete from dummy where id=%s and email=%s and name=%s",(id1,email,name))
#     mysql.connection.commit()
#     return "success"
       
    return "fail"

# otp=random.randint(1000,9999)
# @app.route('/')
# def index():
#     return render_template("forgotpassword.html")

# @app.route('/verify',methods=["POST"])
# def verify():
#     email=request.form['email']
#     msg=Message(subject='RESET PASSWORD',sender='pallalavamsikrishna@gmail.com',recipients=[email])
#     msg.body=str(otp)
#     mail.send(msg)
#     return render_template('verify.html')
# @app.route('/validate',methods=['POST'])
# def validate():
#     user_otp=request.form['otp']
#     if otp==int(user_otp):
#         return "<h3>Email varification succesfull</h3>"
#     return "<h3>Please Try Again</h3>"

# @app.route("/",methods=['POST','GET']) # type: ignore
# def forgot_password():
#     if(request.method=='POST'):
#         email=request.form['email']
#         ran=random.randint(1000,9999)
#         otp(email,ran)
#         return render_template("forgotpassword.html")


# def otp(email,ran):
#     msg = Message('Thank You for Registering!!!', 
#                   sender='pallalavamsikrishna@gmail.com',
#                   recipients=[email])
#     msg.html = render_template('otp_email.html', name=ran)
#     mail.send(msg)

# @app.route("/reset_form",methods=['POST','GET'])
# def reset_form():
#     return render_template("otp_and_reset.html")





        




    



# @app.route('/')
# def Index():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT  * FROM booking")
#     data = cur.fetchall()
#     cur.close()
#     return render_template('index2.html', users=data )



# @app.route('/insert', methods = ['POST'])
# def insert():

#     if request.method == "POST":
#         flash("Data Inserted Successfully")
#         id=request.form['id']
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         datetime = request.form['datetime']
#         message = request.form['Message']
#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO booking VALUES (%s,%s, %s, %s,%s,%s)", (id,name, email, phone,datetime,message))
#         mysql.connection.commit()
#         return redirect(url_for('Index'))

# @app.route('/delete/<string:id_data>', methods = ['GET'])
# def delete(id_data):
#     flash("Record Has Been Deleted Successfully")
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM booking WHERE id=%s", (id_data,))
#     mysql.connection.commit()
#     return redirect(url_for('Index'))

# @app.route('/update',methods=['POST','GET'])
# def update():

#     if request.method == 'POST':
#         id=request.form['id']
#         name = request.form['name']
#         email = request.form['email']
#         phone = request.form['phone']
#         datetime = request.form['datetime']
#         message = request.form['Message']
#         cur = mysql.connection.cursor()
#         cur.execute("""
#                UPDATE booking
#                SET name=%s, email=%s, phone=%s, appointmentdatetime=%s,message=%s
#                WHERE id=%s
#             """, (name , email, phone, datetime , message ,id))
#         flash("Data Updated Successfully")
#         mysql.connection.commit()
#         return redirect(url_for('Index'))
    



if __name__ == "__main__":
    app.run(debug=True)
