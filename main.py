import os
import psycopg2
import psycopg2.extras
from flask import Flask, request, render_template, g, current_app
from flask.cli import with_appcontext
import click

# initialize Flask
app = Flask(__name__)

####################################################
# Routes

@app.route("/dump")
def dump_entries():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rows = cursor.fetchall()
    output = ""
    for r in rows:
        output += str(dict(r))
        output += "\n"
    return "<pre>" + output + "</pre>"

@app.route("/browse")
def browse():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('select id, date, title, content from entries order by date')
    rowlist = cursor.fetchall()
    return render_template('browse.html', entries=rowlist)


def dump_entries():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("select * from Peoples")
    rows = cur.fetchall()
    print("Here are the Peoples:")
    print(rows)
    

#####################################################
# Database handling 
  
def connect_db():
    """Connects to the database."""
    conn = psycopg2.connect(
     host="localhost",
     database="MashaSalaeva",
     user="postgres",
     password="w221267")
    return conn
    
def get_db():
    """Retrieve the database connection or initialize it. The connection
    is unique for each request and will be reused if this is called again.
    """
    if "db" not in g:
        g.db = connect_db()

    return g.db

@app.cli.command("initdb")
def init_db():
    """Clear existing data and create new tables."""
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("schema.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Initialized the database.")

@app.cli.command('populate')
def populate_db():
    conn = get_db()
    cur = conn.cursor()
    with current_app.open_resource("populate.sql") as file: # open the file
        alltext = file.read() # read all the text
        cur.execute(alltext) # execute all the SQL in the file
    conn.commit()
    print("Populated DB with sample data.")
    dump_entries()

# Create the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
