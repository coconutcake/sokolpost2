
import pyodbc

# Specifying the ODBC driver, server name, database, etc. directly
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=LAPMATEUSZ\INSERTNEXO;DATABASE=Nexo_test;UID=sa;PWD=')

# Using a DSN, but providing a password as well
cnxn = pyodbc.connect('DSN=test;PWD=')

# Create a cursor from the connection
cursor = cnxn.cursor()