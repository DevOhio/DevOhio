import pyodbc
import pandas as pd

if __name__ == '__main__':

    # Dynamically pull your driver. Helpful when co-developing and developers are using different drivers
    driver_name = ''
    driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    if driver_names:
        driver_name = driver_names[0]
        print(f"Driver name used:\t{driver_name}")
    else:
        print("No driver found for SQL Server. Closing program.")
        exit()

    # If your SQL Server is running locally on your computer keep "localhost", else enter you server name. Replace "ProjectDB" with the name of the database you are accessing on the SQL Server
    cnxn = pyodbc.connect(f"Driver={driver_name};"
                          "Server=localhost;"
                          "Database=ProjectDB;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM UserRegistry')

    # Save the query results to a variable. Once a fetchall() is used once it can't be used again later.
    sql_data = cursor.fetchall()

    print("\nSQL Data:")
    for row in sql_data:
        print('row = %r' % (row,))

    # The variable, sql_data, is saved as a list. This will create a dictionary using the column names as the key so the column names can be used. Otherwise there will be one column with the value being the list of row values from SQL.
    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))
            for row in sql_data]

    # Replace the column names with your own.
    df = pd.DataFrame(data, columns=['ID', 'UserName', 'TimeStamp'])

    print("\nDataFrame:")
    print(df)

