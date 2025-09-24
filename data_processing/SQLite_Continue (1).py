import sqlite3
import pandas as pd

# Nhập số khách hàng từ người dùng
try:
    N = int(input("Nhập số khách hàng muốn lấy: "))
except ValueError:
    print("Vui lòng nhập một số nguyên hợp lệ!")
    exit()

sqliteConnection = None

try:
    # Kết nối database
    sqliteConnection = sqlite3.connect('../database/Chinook_Sqlite.sqlite')
    print('DB Init')

    # Query: tổng giá trị mua hàng theo khách hàng từ bảng Invoice
    query = f'''
    SELECT c.CustomerId, 
           c.FirstName || ' ' || c.LastName AS CustomerName,
           SUM(i.Total) AS TotalPurchase
    FROM Customer c
    JOIN Invoice i ON c.CustomerId = i.CustomerId
    GROUP BY c.CustomerId
    ORDER BY TotalPurchase DESC
    LIMIT {N};
    '''

    # Thực hiện query và lưu vào DataFrame
    df = pd.read_sql_query(query, sqliteConnection)
    print(df)

except sqlite3.Error as error:
    print('Error occurred -', error)

finally:
    if sqliteConnection is not None:
        sqliteConnection.close()
        print('SQLite Connection closed')
