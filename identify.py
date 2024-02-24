from flask import Flask,request
import mysql.connector
from datetime import datetime


PORT=5999
app = Flask(__name__)

# Connection parameters of MySQL database
hostname="localhost"
username="root"
password="root"
database="mydb"

def prepareResponse():
	pass

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


				# Check if any record already exists with given email and phone
				sql="""
				SELECT * from Contact where email=%s and phoneNumber=%s
				"""
				mycursor.execute(sql,(email,phone,))
				# Fetch rows if exist
				rows = mycursor.fetchall()

				if rows:
					pass

				# Check if any record already exists with given email or phone
				sql="""
				SELECT * from Contact where email=%s or phoneNumber=%s
				"""
				mycursor.execute(sql,(email,phone,))

				# Fetch rows if exist
				rows = mycursor.fetchall()			

				if rows:
					pass
				else:
					#Create a datetime object representing the current date and time
					current_datetime = datetime.now()

					# Convert the datetime object to a string formatted as MySQL DATETIME
					mysql_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

					sql="""
					INSERT into Contact(phoneNumber,email,linkPrecedence,createdAt,updatedAt ) values(%s,%s,%s,%s,%s)
					"""
					mycursor.execute(sql,(phone,email,"primary",mysql_datetime,mysql_datetime))
					mydb.commit()

		app.run(debug=True,port=PORT)

	except mysql.connector.Error as err:
		 print(f"Error: {err}")