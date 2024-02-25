# Setup Guide
## Requirements

- **Operating System:** Windows 10/11
- **Python:** 3.11.0 or latest versions
- **Python Packages:**
    - Flask 3.0.0 (if not installed, use command: `pip install flask`)
    - mysql-connector-python 8.2.0 (if not installed, use command: `pip install mysql-connector-python`)
    - requests `pip install requests`

### Database Table: Contact

| Field          | Type     | Null | Key | Default | Extra          |
|----------------|----------|------|-----|---------|----------------|
| id             | int      | NO   | PRI | NULL    | auto_increment |
| phoneNumber    | text     | YES  |     | NULL    |                |
| email          | text     | YES  |     | NULL    |                |
| linkedId       | int      | YES  |     | NULL    |                |
| linkPrecedence | text     | YES  |     | NULL    |                |
| createdAt      | datetime | YES  |     | NULL    |                |
| updatedAt      | datetime | YES  |     | NULL    |                |
| deletedAt      | datetime | YES  |     | NULL    |                |

## Steps to run server locally

1. Open MySQL command line client or any other MySQL tool and create a database named `mydb`.
2. Modify the credentials for flask server in file 'identify.py' on lines 11-14.
3. Run `server.py`: `python server.py`.
4. The default port of the server is set to 5999. If this port is unavailable, change the port in both `post.py` and `identify.py` files
5. Inorder to send POST data, change values of variable on lines 8 and 9 in `post.py` file.
6. Run `post.py`: `python post.py`.
7. JSON response will be displayed on terminal.

## Steps to send POST requests to server hosted remotely

1. Inorder to send POST data to remote server, change values of variable on lines 4 and 5 in `post_remote.py` file.
2. Run `post_remote.py`: `python post_remote.py`.
3. JSON response will be displayed on terminal.
4. You can also create your own code to send POST requests to hosted app.
5. URL for hosted app is: `https://callmenitin.pythonanywhere.com/identify`



