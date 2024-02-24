import requests
import json

#Port being used for flask server
PORT=5999

#Data to be sent through POST
email=""
phone=""

post_data={"email":email,"phoneNumber":phone}
json_data = json.dumps(post_data)

# URL for the flask server 
URL="http://localhost:"+str(PORT)+"/identify"

# Header of the request
headers={'Content-Type':'application/json'}

#Response
response=requests.post(URL,data=json_data,headers=headers)