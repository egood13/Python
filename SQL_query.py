


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
