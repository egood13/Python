


import psycopg2 as pg
import mysql.connector
import pandas as pd

def connect_to_Artemis(sql):
	''' pass a SQL query to return the data in a dataframe '''
	connection_string = """dbname='da4vufus9h81aq' 
                       user = 'read' 
                       host = 'ec2-54-156-218-26.compute-1.amazonaws.com' 
                       password = 'p7663c81910e7fc4093125e117ea284b8252091cb0473ea822729c758997e65b3'"""
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
	host = '172.16.3.26'
	user = 'elliot.good'
	password = 'j3#R947eXwi7'
	database = 'tmc_production'

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
	connection_string = """dbname='teespring' 
                       user = 'datamonster' 
                       host = 'teespring-dw.cmd75dj8gldi.us-east-1.redshift.amazonaws.com' 
                       password = '92u9xT<X9$>mQ?xf'
                       port = '5439'"""
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
	host = 'teespringdb-next-read-slave.cxxlyodz53xk.us-east-1.rds.amazonaws.com'
	user = 'bdb-2015-10'
	password = '2DnsKcqxRPEAhJ4pqgJvd'
	database = 'TeespringDB'

	connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
	cursor = connection.cursor()
	cursor.execute(sql)
	rows = cursor.fetchall()
	cols = cursor.column_names

	cursor.close()
	connection.close()

	return(pd.DataFrame(rows, columns=cols))
