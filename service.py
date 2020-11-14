import pymysql 
import pymysql.cursors 
import os
from flask import request
from flask import render_template
from flask import Flask

app = Flask(__name__)

db_host = os.getenv('db_host')
db_user = os.getenv('db_user')
db_pass = os.getenv('db_pass')
db_name = os.getenv('db_name')

# Fetch and Manage Users

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

@app.route('/manage/iteusersms', methods=["POST"])
def manage_users():
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)
    cur = conn.cursor()
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email_address = request.form['email_address']
    phone_num = request.form['phone_num']
    active  = request.form['active']
    comments  = request.form['comments']
    password  = request.form['password']
    pass_salt  = request.form['pass_salt']
    cur.execute(f'insert into users (first_name, last_name, email_address, phone_num, active, comments, password, pass_salt) values ("{first_name}", "{last_name}", "{email_address}", "{phone_num}", "{active}", "{comments}", "{password}", "{pass_salt}");')
    res = conn.commit()

    print(res)
    
    cur.close()
    conn.close()

    return '', 204
 
@app.route('/manage/users', methods=["GET"])
def get_manage_users():
    return render_template("manage-users.html")



# Fetch and Manage Items

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
    available = request.form['available']
    created_by = request.form['created_by']
    cur.execute(f'insert into items (item_name, item_desc, item_price, available, created_by) values ("{item_name}", "{item_desc}", "{item_price}", "{available}", "{created_by}");')
    res = conn.commit()

    print(res)
    
    cur.close()
    conn.close()

    return '', 204
 
@app.route('/manage/items', methods=["GET"])
def get_manage_items():
    return render_template("manage-items.html")


# Fetch and Manage Orders

@app.route('/orders')
def fetch_orders():
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)
    dataset = []
    cur = conn.cursor()
    cur.execute("select * from orders;")
    results = cur.fetchall()
    for row in results:
        print(row)
        dataset.append(row)

    cur.close()
    conn.close()
    return render_template("orders.html", rows=dataset)

@app.route('/manage/orders', methods=["POST"])
def manage_orders():
    conn = pymysql.connect(host=db_host, port=3306, user=db_user, passwd=db_pass, db=db_name)
    cur = conn.cursor()
    
    user_id = request.form['user_id']
    ticket_ids = request.form['ticket_ids']
    square_id = request.form['square_id']
    paid = request.form['paid']
    order_total = request.form['order_total']
    order_complete = request.form['order_complete']
    payment_status = request.form['payment_status']
    cur.execute(f'insert into orders (user_id, ticket_ids, square_id, paid, order_total, order_complete, payment_status) values ("{user_id}, {ticket_ids}, {square_id}, {paid}, {order_total}, {order_complete}, {payment_status});')
    res = conn.commit()

    print(res)
    
    cur.close()
    conn.close()

    return '', 204

@app.route('/manage/orders', methods=["GET"])
def get_manage_orders():
    return render_template("manage-orders.html")


#Initialize Flask    

if __name__ == '__main__':
    app.run(host='0.0.0.0')