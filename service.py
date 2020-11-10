import pymysql 
import pymysql.cursors 
import json 
from flask import Flask

app = Flask(__name__)

db_host = 'localhost'
db_user = 'lanadmin'
db_pass = 'acorn77tog'
db_name = 'raffle'

conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)

@app.route('/users')
def fetch_users():
    cur = conn.cursor()
    cur.execute("select * from users;")
    for row in cur:
        # print(row)
        row = json.dumps(row, indent=4, sort_keys=True, default=str)
        return(row)

    # jsonitems = json.dump(cur.description)

    cur.close()
    conn.close()

@app.route('/items')
def fetch_items():
    cur = conn.cursor()
    cur.execute("select * from items;")
    for row in cur:
        # print(row)
        row = json.dumps(row, indent=4, sort_keys=True, default=str)
        return(row)

    # jsonitems = json.dump(cur.description)

    cur.close()
    conn.close()

@app.route('/orders')
def fetch_orders():
    cur = conn.cursor()
    cur.execute("select * from ticket_orders;")
    for row in cur:
        # print(row)
        row = json.dumps(row, indent=4, sort_keys=True, default=str)
        return(row)

    # jsonitems = json.dump(cur.description)

    cur.close()
    conn.close()

if __name__ == '__main__':
    app.run()