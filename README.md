# AI-Group-project

### How to start frontend

1.  Open two **NEW** terminals and go to the project folder
2.  In both terminals go to the frontend folder using `cd frontend`
3.  In one terminal use the following commands:
       *    `set FLASK_APP=huw.py`
       *    `python -m flask run`
4.  In the other terminal use the following commands:
       *    `set FLASK_APP=huw_recommend.py`
       *    `python -m flask run --port 5001`

if this all works it works it wil give you a link to the webpage in the terminal where u started huw.py (http://127.0.0.1:5000/)

if it doesn't work try following the readme at [gitlab](https://gitlab.com/hu-hbo-ict/ai/v1gp)

### How to create a connection

1. Go to the folder 'backend'
2. Go to the file 'create_connection'
3. Edit the connection values so that it can connect to your database

### How to create recommendations

1. To get the CSV files and the in the database run the file 'MongoDB products to CSV.py' in 'backend/csv' and wait till it finishes
2. To get the recommendations run the file 'FetchCode.py' in 'backend' and wait till it finishes
