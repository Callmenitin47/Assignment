import requests
import json

email="nitink121196@gmail.com"
phone="9910612882"

post_data={"email":email,"phoneNumber":phone}
json_data = json.dumps(post_data)

# URL for the flask server 
URL="https://callmenitin.pythonanywhere.com/identify"

# Header of the request
headers={'Content-Type':'application/json'}

# Response
response=requests.post(URL,data=json_data,headers=headers)

print(response)
print(response.text)