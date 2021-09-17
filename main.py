from flask import Flask
import requests
import psycopg2
from sqlalchemy import create_engine
import os
from dataclasses import dataclass

app = Flask(__name__)

@app.get("/")
def hello_world():
    return '<p>Hello from @BFC_APP_DOMAIN@! Try using <a href="/fetch_and_process">/fetch_and_process</a></p>'

@dataclass
class Todo:
    id: int
    title: str
    completed: bool

# fetch_and_process fetches from a web api and processes the results
# with some python code
@app.get("/fetch_and_process")
def fetch_and_process():
    resp = requests.get("https://jsonplaceholder.typicode.com/todos")

    todos = []
    for object in resp.json():
        todos.append(Todo(id=object["id"], title=object["title"], completed=object["completed"]))

    num_completed = len([todo for todo in todos if todo.completed])
    return "num_completed: " + str(num_completed)

# db is a connection to the postgres database
db = create_engine(os.environ["PG_DSN"].replace('postgres://', 'postgresql://'))

# create a table to hold data from the api
db.execute("CREATE TABLE IF NOT EXISTS todos (id int, title text, completed bool)")  

# fetch_and_store fetches from a web api and stores the results
# in the postgres database
@app.get("/fetch_and_store")
def fetch_and_store():
    resp = requests.get("https://jsonplaceholder.typicode.com/todos")
    db.execute("DELETE FROM todos")
    for object in resp.json():
        db.execute("INSERT INTO todos (id, title, completed) VALUES (%s, %s, %s)", (
            object["id"],
            object["title"],
            object["completed"],
        ))
    return "success"

# query processes data in the postgres database
@app.get("/query")
def query():
    row = db.execute("SELECT COUNT(*) FROM todos WHERE completed=true").one()
    count = row[0]
    return "num_completed: " + str(count)