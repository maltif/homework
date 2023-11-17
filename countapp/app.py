from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors
from decouple import config
import os
import re

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['MYSQL_HOST'] = config('DB_HOST')
app.config['MYSQL_PORT'] = int(config('DB_PORT'))
app.config['MYSQL_USER'] = config('DB_USER')
app.config['MYSQL_PASSWORD'] = config('DB_PASSWORD')
app.config['MYSQL_DB'] = config('DB_DATABASE')

db = MySQL(app)

@app.route('/')
def home():
    cursor = db.connection.cursor(MySQLdb.cursors.Cursor)
    cursor.execute("SELECT count FROM counter")
    cr = cursor.fetchone()
    inc = int(cr[0])+1
    cursor.execute("UPDATE counter set count = count + 1")
    cursor.connection.commit()
    cursor.close()
    return render_template('home.html', count=inc)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=6000)
