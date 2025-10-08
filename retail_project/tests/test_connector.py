import traceback

import mysql.connector

server="localhost"
port=3306
database="k23416_retail"
username="root"
password="@Obama123"
try:
    conn = mysql.connector.connect(
                    host=server,
                    port=port,
                    database=database,
                    user=username,
                    password=password)
except:
    traceback.print_exc()
print("---Tiếp tục phần mềm---")
print("--CRUD----")
#Câu 1: Đăng nhập cho Customer
def login_customer(email,pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM customer " \
          "where Email='"+email +"' and Password ='"+pwd+"'"
    print(sql)
    cursor.execute(sql)
    dataset = cursor.fetchone()
    if dataset != None:
        print(dataset)
    else:
        print("Login failed!")
    cursor.close()
login_customer("daodao@gmail.com","123")
def login_employee(email,pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM employee " \
          "where Email=%s and Password=%s"
    val=(email,pwd)
    cursor.execute(sql, val)
    dataset = cursor.fetchone()
    if dataset != None:
        print(dataset)
    else:
        print("Login failed!")
    cursor.close()
login_employee("kim@yahoo.com","123")


login_customer("daodao@gmail.com", "123")

def login_employee(email, pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM employee " \
          "where Email = %s and Password =%s"
    val = (email,pwd)
    cursor.execute(sql, val)
    dataset = cursor.fetchone()
    if dataset != None:
        print(dataset)
    else:
        print("Login failed")
    cursor.close()


login_employee("putin@gmail.com", "123")

