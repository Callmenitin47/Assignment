from flask import Flask,request,jsonify
import mysql.connector
from datetime import datetime

PORT=5999
app=Flask(__name__)
mydb= None
mycursor= None

# Connection parameters of MySQL database
hostname="localhost"
username="root"
password="root"
database="mydb"

def prepareResponse(cursor,db,primary_id):
	emails=set()
	phone_numbers=set()
	secondaryContactIds=[]

	query1="""
	SELECT * from Contact where id=%s
	"""
	query2="""
	SELECT * from Contact where linkedId=%s order by id ASC
	"""
	cursor.execute(query1,(primary_id,))
	row=cursor.fetchone();
	cursor.execute(query2,(primary_id,))
	rows=cursor.fetchall();
	emails.add(row[2])
	phone_numbers.add(row[1])

	for r in rows:
		emails.add(r[2])
		phone_numbers.add(r[1])
		secondaryContactIds.append(r[0])
	emails=list(emails)
	phone_numbers=list(phone_numbers)

	response_contact={
	"primaryContactId": primary_id,
	"emails":emails,
	"phoneNumbers":phone_numbers,
	"secondaryContactIds":secondaryContactIds
	}
	response=jsonify({"contact":response_contact})
	response.status_code=200
	return response	

def insertRecord(cursor,db,result,phone,email,precedence):

	linkedId=result[3]
	if(linkedId is None):
		linkedId=result[0]
	query="""
		INSERT into Contact(phoneNumber,email,linkedId,linkPrecedence,createdAt,updatedAt) values(%s,%s,%s,%s,%s,%s)
		"""
	current_datetime = datetime.now()
	mysql_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')	

	cursor.execute(query,(phone,email,linkedId,precedence,mysql_datetime,mysql_datetime,))
	db.commit()

	return linkedId

def updateRecord(cursor,db,result1,result2,phone,email):

	precedence1=result1[4]
	precedence2=result2[4]
	Id1=result1[0]
	Id2=result2[0]
	linkedId1=result1[3]
	linkedId2=result2[3]

	# Checking if phone and email are already linked
	if(linkedId1==Id2): 
		return Id2
	if(linkedId2==Id1):
		return Id1

	current_datetime = datetime.now()
	mysql_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

	if precedence1=="primary" and precedence2=="secondary":
		query="""
		UPDATE Contact set updatedAt=%s,linkedId=%s,linkPrecedence=%s where id=%s
		"""
		if(linkedId2<Id1):
			cursor.execute(query,(mysql_datetime,linkedId2,"secondary",Id1))
			db.commit()
			return linkedId2
		else:
			cursor.execute(query,(mysql_datetime,Id1,"secondary",linkedId2))
			cursor.execute(query,(mysql_datetime,Id1,"secondary",Id2))
			db.commit()
			return Id1
	elif precedence2=="primary" and precedence1=="secondary":
		query="""
		UPDATE Contact set updatedAt=%s,linkedId=%s,linkPrecedence=%s where id=%s
		"""
		if(linkedId1<Id2):
			cursor.execute(query,(mysql_datetime,linkedId1,"secondary",Id2))
			db.commit()
			return linkedId1
		else:
			cursor.execute(query,(mysql_datetime,Id2,"secondary",linkedId1))
			cursor.execute(query,(mysql_datetime,Id2,"secondary",Id1))
			db.commit()
			return Id2
	elif precedence1=="secondary" and precedence2=="secondary":
		query="""
		UPDATE Contact set updatedAt=%s,linkedId=%s,linkPrecedence=%s where id=%s
		"""
		if(linkedId1<linkedId2):
			cursor.execute(query,(mysql_datetime,linkedId1,"secondary",linkedId2))
			cursor.execute(query,(mysql_datetime,linkedId1,"secondary",Id2))
			db.commit()
			return linkedId1
		else:
			cursor.execute(query,(mysql_datetime,linkedId2,"secondary",linkedId1))
			cursor.execute(query,(mysql_datetime,linkedId2,"secondary",Id1))
			db.commit()
			return linkedId2
	else:
		query="""
		UPDATE Contact set updatedAt=%s,linkedId=%s,linkPrecedence=%s where id=%s
		"""
		if Id1<Id2:
			cursor.execute(query,(mysql_datetime,Id1,"secondary",Id2))
			db.commit()
			return Id1
		else:
			cursor.execute(query,(mysql_datetime,Id2,"secondary",Id1))
			db.commit()
			return Id2


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
			global mydb
			global mycursor
			if request.method=="GET":
				return "Invalid request"
			elif request.method=="POST":

				# Checking if connection to MySQL exists
				if not mydb.is_connected() or mydb is None:
					mydb = mysql.connector.connect(
					host=hostname,
					user=username,
					password=password,
					database=database
					 )
					mycursor=mydb.cursor()

				json_data=request.json
				email=json_data["email"]
				phone=json_data["phoneNumber"]

				# To be used as primary contact Id
				responseId=-1

				# Check if any record already exists with given email and phone

				sql="""
				SELECT * from Contact where email=%s and phoneNumber=%s
				"""
				mycursor.execute(sql,(email,phone,))

				# Fetch rows if exist
				rows = mycursor.fetchone()

				#If yes return the response
				if rows:
					return prepareResponse(mycursor,mydb,rows[0])

				query1="""
				SELECT * from Contact where email=%s
				"""
				query2="""
				SELECT * from Contact where phoneNumber=%s
				"""
				mycursor.execute(query1,(email,))
				result1=mycursor.fetchall();

				mycursor.execute(query2,(phone,))
				result2=mycursor.fetchall();

				if result2 and not result1:
					responseId=insertRecord(mycursor,mydb,result2[0],phone,email,"secondary")
				elif result1 and not result2:
					responseId=insertRecord(mycursor,mydb,result1[0],phone,email,"secondary")
				elif result1 and result2:
					responseId=updateRecord(mycursor,mydb,result1[0],result2[0],phone,email)
				else:
					#Create record if if no record with given email or phone exists

					current_datetime = datetime.now()
					mysql_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

					sql="""
					INSERT into Contact(phoneNumber,email,linkedId,linkPrecedence,createdAt,updatedAt ) values(%s,%s,%s,%s,%s,%s)
					"""
					mycursor.execute(sql,(phone,email,None,"primary",mysql_datetime,mysql_datetime))

					query="""
					SELECT id from Contact where email=%s and phoneNumber=%s
					"""
					mycursor.execute(query,(email,phone,))
					row=mycursor.fetchone()
					responseId=row[0]
					mydb.commit()

				return prepareResponse(mycursor,mydb,responseId)

		app.run(debug=True,port=PORT)

	except mysql.connector.Error as err:
		 print(f"Error: {err}")