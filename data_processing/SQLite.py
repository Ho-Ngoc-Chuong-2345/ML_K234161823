import sqlite3
import pandas as pd

try:
    # Connect to DB and create a cursor
    sqliteConnection = sqlite3.connect('../database/Chinook_Sqlite.sqlite')
    cursor = sqliteConnection.cursor()
    print ('DB Init')
    # Write a query and execute it with cursor
    query = 'SELECT * FROM InvoiceLine LIMIT 5;'
    cursor.execute(query)
    # Fetch and output result
    df = pd.DataFrame(cursor.fetchall())
    print(df)
    # Close the cursor
    cursor.close()
# Handle errors
except sqlite3.Error as error:
    print ('Error occurred - ', error)
# Close DB Connection irrespective of success or failure
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('SQLite Connection closed')


