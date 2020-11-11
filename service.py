import pymysql 
import pymysql.cursors 
import json 
import jsonify
import random
from flask import request
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
    dataset = []
    cur = conn.cursor()
    cur.execute("select * from users;")
    results = cur.fetchall()
    for row in results:
        print(row)
        dataset.append(row)

    cur.close()
    conn.close()
    return render_template("users.html", rows=dataset)

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
    return render_template("items.html", rows=dataset)

@app.route('/manage/items', methods=["POST"])
def manage_items():
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)
    cur = conn.cursor()
    
    item_name = request.form['item_name']
    item_desc = request.form['item_desc']
    item_price = request.form['item_price']
    sold = request.form['sold']
    creator = request.form['creator']
    cur.execute(f'insert into items (item_name, item_desc, item_price, sold, creator) values ("{item_name}", "{item_desc}", "{item_price}", "{sold}", "{creator}");')
    res = conn.commit()

    print(res)
    
    cur.close()
    conn.close()

    return '', 204
 
@app.route('/manage/items', methods=["GET"])
def get_manage_items():
    return render_template("manage-items.html")


@app.route('/orders')
def fetch_orders():
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)
    dataset = []
    cur = conn.cursor()
    cur.execute("select * from ticket_orders;")
    results = cur.fetchall()
    for row in results:
        print(row)
        dataset.append(row)

    cur.close()
    conn.close()
    return render_template("items.html", rows=dataset)

if __name__ == '__main__':
    app.run(host='0.0.0.0')