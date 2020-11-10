import collections
import json
import pymysql
from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello_world():
    cur = pymysql.connect(host='localhost', port=3306, user='lanadmin', passwd='acorn77tog', db='raffle')

    cur.connect('select * from items')
    row_headers=[x[0] for x in cur.description] 
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

if __name__ == '__main__':
   app.run(debug=True)

