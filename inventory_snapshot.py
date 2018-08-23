
import psycopg2 as pg
import datetime

def main():
	import psycopg2 as pg
	from datetime import datetime
	# connect to Artemis
	print("Connecting to Artemis...")
	connection_string = """dbname='da4vufus9h81aq' 
						   user = 'read' 
						   host = 'ec2-54-156-218-26.compute-1.amazonaws.com' 
						   password = 'p7663c81910e7fc4093125e117ea284b8252091cb0473ea822729c758997e65b3'"""
	connected = False
	while not connected: # loop until connection successful
		try:
			conn = pg.connect(connection_string)
			cur = conn.cursor()
			connected = True
		except pg.OperationalError as e:
			print("Failed to connect to Artemis. Please check connection and press enter to try again.")
			input()
			connected = False

	print("Connection successful, getting inventory data...")
	# SQL statement
	sql = """SELECT i.gtin
					,i.name
					,i.color
					,i.size
					,i.location
					,i.created_at
					,i.updated_at
					,i.unallocated_quantity
					,i.netsuite_internal_id
					,i.lock_version
					,i.quantity_in_stock
					,NOW() as timestamp 
			FROM inventory_items i"""
	cur.execute(sql)

	# get data, record timestamp
	time = datetime.now().strftime('%b, %d, %Y %H:%M:%S')
	rows = cur.fetchall()
	cols = [desc[0] for desc in cur.description]
	print("Obtained data, loading to local server...")


	# connect to local server
	conn2 = pg.connect("dbname='postgres' user='postgres' host='localhost' password='Avery011#'")
	cur2 = conn2.cursor()

	# sql query
	placeholders = ','.join(['%s']*len(rows))
	insert_query = """INSERT INTO inventory_snapshot VALUES {}""".format(placeholders)
	cur2.execute(insert_query, rows)

	# commit changes to database and close connection
	conn2.commit()
	conn2.close()
	print("Completed. You should see inventory data for", time)
	input("Press enter to close")


if __name__ == '__main__':
	main()
