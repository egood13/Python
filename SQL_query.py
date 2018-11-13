


import psycopg2 as pg
import mysql.connector
import pandas as pd

def connect_to_Artemis(sql):
	''' pass a SQL query to return the data in a dataframe '''
	connection_string = """'dbname' 
                       user = 'username' 
                       host = 'hostname' 
                       password = 'password'"""
	connection = pg.connect(connection_string)
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cols = [desc[0] for desc in cursor.description]

	cursor.close()
	connection.close()

	return(pd.DataFrame(rows, columns=cols))

def connect_to_Apollo(sql):
	''' pass a SQL query to return the data in a dataframe '''
	host = 'hostname'
	user = 'username'
	password = 'password'
	database = 'databasename'

	connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cols = cursor.column_names

	cursor.close()
	connection.close()

	return(pd.DataFrame(rows, columns=cols))


def connect_to_Redshift(sql):
	''' pass a SQL query to return the data in a dataframe '''
	connection_string = """dbname='databasename' 
                       user = 'username' 
                       host = 'hostname' 
                       password = 'password'
                       port = 'portnumber'"""
	connection = pg.connect(connection_string)
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cols = [desc[0] for desc in cursor.description]

	cursor.close()
	connection.close()

	return(pd.DataFrame(rows, columns=cols))


def connect_to_RDS(sql):
	''' pass a SQL query to return the data in a dataframe '''
	host = 'hostname'
	user = 'username'
	password = 'password'
	database = 'databasename'

	connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cols = cursor.column_names

	cursor.close()
	connection.close()

	return(pd.DataFrame(rows, columns=cols))


def connect_to_local(sql):
	''' 
	pass a SQL query to return the data in a dataframe 
	Args
		sql: text of the query to be used in querying the database
	Returns
		dataframe
	'''
	connection_string = '''<connection details>'''
	connection = pg.connect(connection_string)
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cols = [desc[0] for desc in cursor.description]

	cursor.close()
	connection.close()

	return(pd.DataFrame(rows, columns=cols))

def query_to_text(fulL_filepath):
	''' 
	Pass the full filepath of a sql query to return it as text 
	Args
		full_filepath: string of the form "C:\\Users\\user\\sub_folder\\filename.sql"
	Returns
		string with whitespace formatting matching the source file
	'''

	with open(fulL_filepath, 'r') as f_in:
		lines = f_in.read()
	query_string = textwrap.dedent('''{}'''.format(lines))
	return(query_string)

def list_to_text(lpn_list):
	'''
	Helper funciton used to convert lpn's found in a query to a text list of 
	the form "(x1, x2, ..., xn)". Useful when the list is in the hundreds +
	Args
		lpn_list: list of (string) lpns pulled from dataframe
	Returns
		string of the form "(x1, x2, ..., xn)"
	'''

	text_list = "("
	last_lpn = lpn_list[-1]
	for lpn in lpn_list:
		text_list += "'"
		text_list += lpn
		if lpn == last_lpn:
			text_list += "')"
		else:
			text_list += "', "
	return(text_list)

