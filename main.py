import pyodbc
import pandas as pd

if __name__ == '__main__':

    driver_name = ''
    driver_names = [x for x in pyodbc.drivers() if x.endswith(' for SQL Server')]
    if driver_names:
        driver_name = driver_names[0]
        print(f"Driver name used:\t{driver_name}")
    else:
        print("No driver found for SQL Server. Closing program.")
        exit()

    
    cnxn = pyodbc.connect(f"Driver={driver_name};"
                          "Server=localhost;"
                          "Database=ProjectDB;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM UserRegistry')

    sql_data = cursor.fetchall()

    print("\nSQL Data:")
    for row in sql_data:
        print('row = %r' % (row,))

    desc = cursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row))
            for row in sql_data]

    df = pd.DataFrame(data, columns=['ID', 'UserName', 'TimeStamp'])

    print("\nDataFrame:")
    print(df)

