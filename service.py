import pymysql 
import pymysql.cursors 
import json 
import jsonify
import random
from flask import render_template
from flask import Flask

app = Flask(__name__)

db_host = '10.100.10.66'
db_user = 'lanadmin'
db_pass = 'acorn77tog'
db_name = 'raffle'

@app.route('/users')
def fetch_users():
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)
    cur = conn.cursor()
    cur.execute("select * from users;")
    data = cur.fetchall()
    for row in data:
        print(row)
        row = json.dumps(row, indent=4, sort_keys=True, default=str)
        #print(json.dumps({'id': 0, 'first_name': 1}, sort_keys=True, indent=4, default=str))
        return(row)

    cur.close()
    conn.close()

@app.route('/items')
def fetch_items():
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)
    dataset = []
    cur = conn.cursor()
    cur.execute("select * from items;")
    results = cur.fetchall()
    for row in results:
        print(row)
        dataset.append(row)

    cur.close()
    conn.close()
    return render_template("index.html", rows=dataset)

@app.route('/orders')
def fetch_orders():
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)
    cur = conn.cursor()
    cur.execute("select * from ticket_orders;")
    for row in cur:
        print(row)
        row = json.dumps(row, indent=4, sort_keys=True, default=str)
        return(row)

    cur.close()
    conn.close()

if __name__ == '__main__':
    app.run()