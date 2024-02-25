# Setup Guide
## Requirements

- **Operating System:** Windows 10/11
- **Python:** 3.11.0 or latest versions
- **Python Packages:**
    - Flask 3.0.0 (if not installed, use command: `pip install flask`)
    - mysql-connector-python 8.2.0 (if not installed, use command: `pip install mysql-connector-python`)
    - requests `pip install requests`
 
## Steps to run server locally

1. Open MySQL command line client or any other MySQL tool and create a database named `mydb`.
2. Modify the credentials for flask server in file 'identify.py' on lines 11-14.
3. Run `server.py`: `python server.py`.
4. The default port of the server is set to 5999. If this port is unavailable, change the port in both 'post.py' and 'identify.py' files
5. Inorder to send POST data, change values of variable on lines 8 and 9 in 'post.py' file.
6. Run `post.py`: `python post.py`.
7. JSON response will be displayed on terminal.
