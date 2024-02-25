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

def insertRecord(cursor,db,result,phone,email,precedence):
	linkedId=result[2]
	if(linkedId is None):
		linkedId=result2[7]
	sql="""
		INSERT into Contact(phoneNumber,email,linkedId,linkPrecedence,createdAt,updatedAt) values(%s,%s,%s,%s,%s,%s)
		"""
	current_datetime = datetime.now()

	# Convert the datetime object to a string formatted as MySQL DATETIME
	mysql_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
					
	cursor.execute(sql,(phone,email,linkedId,precedence,mysql_datetime,mysql_datetime,))
	db.commit()

def updateRecord(cursor,db,result1,result2,phone,email):
	precedence1=result1[3]
	precedence2=result2[3]
	Id1=result1[7]
	Id2=result2[7]
	linkedId1=result1[2]
	linkedId2=result2[2]

	current_datetime = datetime.now()
	mysql_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

	if precedence1=="primary" and precedence2=="secondary":
		query="""
		UPDATE contact set updatedAt=%s,linkedId=%s,linkPrecedence=%s where id=%s
		"""
		if(linkedId2>Id1):
			cursor.execute(query,(mysql_datetime,linkedId2,"secondary",Id1))
			db.commit()
		else:
			cursor.execute(query,(mysql_datetime,Id1,"secondary",linkedId2))
			cursor.execute(query,(mysql_datetime,Id1,"secondary",Id2))
			db.commit()
	elif precedence2=="primary" and precedence1=="secondary":
		query="""
		UPDATE contact set updatedAt=%s,linkedId=%s,linkPrecedence=%s where id=%s
		"""
		if(linkedId1>Id2):
			cursor.execute(query,(mysql_datetime,linkedId1,"secondary",Id2))
			db.commit()
		else:
			cursor.execute(query,(mysql_datetime,Id2,"secondary",linkedId1))
			cursor.execute(query,(mysql_datetime,Id2,"secondary",Id1))
			db.commit()
	elif precedence1=="secondary" and precedence2=="secondary":
		query="""
		UPDATE contact set updatedAt=%s,linkedId=%s,linkPrecedence=%s where id=%s
		"""
		if(linkedId1>linkedId2):
			cursor.execute(query,(mysql_datetime,linkedId1,"secondary",linkedId2))
			cursor.execute(query,(mysql_datetime,linkedId1,"secondary",Id2))
			db.commit()
		else:
			cursor.execute(query,(mysql_datetime,linkedId2,"secondary",linkedId1))
			cursor.execute(query,(mysql_datetime,linkedId2,"secondary",Id1))
			db.commit()
	else:
		query="""
		UPDATE contact set updatedAt=%s,linkedId=%s,linkPrecedence=%s where id=%s
		"""
		if Id1>Id2:
			cursor.execute(query,(mysql_datetime,Id1,"secondary",Id2))
			db.commit()
		else:
			cursor.execute(query,(mysql_datetime,Id2,"secondary",Id1))
			db.commit()




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

				query1="""
				SELECT * from Contact where email=%s
				"""
				query2="""
				SELECT * from Contact where phoneNumber=%s
				"""
				mycursor.execute(query1,(email,))
				result1=mycursor.fetchone();

				mycursor.execute(query2,(phone,))
				result2=mycursor.fetchone();

				if result2 and not result1:
					insertRecord(mycursor,mydb,result2,phone,email,"secondary")
				elif result1 and not result2:
					insertRecord(mycursor,mydb,result1,phone,email,"secondary")
				elif result1 and result2:
					updateRecord(mycursor,mydb,result1,result2,phone,email)
				else:
					#Create record if if no record with given email or phone exists
					#Create a datetime object representing the current date and time
					current_datetime = datetime.now()

					# Convert the datetime object to a string formatted as MySQL DATETIME
					mysql_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

					sql="""
					INSERT into Contact(phoneNumber,email,linkedId,linkPrecedence,createdAt,updatedAt ) values(%s,%s,%s,%s,%s,%s)
					"""
					mycursor.execute(sql,(phone,email,None,"primary",mysql_datetime,mysql_datetime))
					mydb.commit()

		app.run(debug=True,port=PORT)

	except mysql.connector.Error as err:
		 print(f"Error: {err}")