import pymysql 
import pymysql.cursors 
import json 
 
db_host = 'localhost'
db_user = 'lanadmin'
db_pass = 'acorn77tog'
db_name = 'raffle'

item_list = ''

conn = pymysql.connect(host='localhost', port=3306, user='lanadmin', passwd='acorn77tog', db='raffle')
cur = conn.cursor()
cur.execute("select * from items;")
print(cur.description)
print()

for row in cur:
    print(row)

jsonitems = json.dump(cur.description)

cur.close()
conn.close()

#        json.dump(rows, write_file)
