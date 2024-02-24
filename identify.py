from flask import Flask,request
import mysql.connector


PORT=5999
app = Flask(__name__)

# Connection parameters of MySQL database
hostname="localhost"
username="root"
password="root"
database="mydb"

if __name__=="__main__":
	try:
	    # Establish a connection to the MySQL database
	   mydb = mysql.connector.connect(
	    host=hostname,
	    user=username,
	    password=password,
	    database=database
	    )

	   if mydb.is_connected():
	      print("Connected to MySQL!")

	   mycursor=mydb.cursor()

	   @app.route('/identify',methods = ["GET","POST"])
	   def getIdentity():
	       if request.method=="GET":
	         return "Invalid request"
	       elif request.method=="POST":
	       	json_data=request.json
	       	email=json_data["email"]
	       	phone=json_data["phoneNumber"]

	   app.run(debug=True,port=PORT)
	except mysql.connector.Error as err:
	    print(f"Error: {err}")