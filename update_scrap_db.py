
'''
This script is used to update the scrap database in the local server.
'''

import pandas as pd
import psycopg2 as pg

import sys
sys.path.insert(0, "C:\\Users\\elliott.good\\Desktop\\Python Scripts")
import SQL_query as sql

def main():
	
	print("---Update Scrap Database---")
	data = get_data()
	push_to_db(data)

def get_data():
	'''
	This function get Apollo Fail data and matches it to an 
	employee/shift/job/etc. where possible.
	Args
		None
	Returns:
		dataframe
	'''

	query_string = sql.query_to_text("C:\\Users\\elliott.good\\Desktop\\" +
		"SQL scripts\\Apollo_fail_cases_v2.sql")
	fail_matchups = sql.connect_to_Apollo(query_string)

	# add employee shift lkp and week of columns
	fail_matchups["employee shift lkp"] = '' # no longer used
	fail_matchups["week of"] = fail_matchups["fail_hotpick_date"].apply(
		lambda x: x if x.weekday() == 6 else x - \
		pd.DateOffset(weekday=6,weeks=1))

	print("Fail matchup data obtained. Getting product details...")

	# get list of lpn's to be used in query
	lpns = list(fail_matchups["lpn"].unique())
	lpn_text_list = sql.list_to_text(lpns)
	# get product details for each lpn
	query_string = '''
		SELECT u.lpn
			,i.gtin
			,SPLIT_PART(i."name", '-', 1) AS style_num
			,SPLIT_PART(i."name", '-', 2) AS color
			,SPLIT_PART(i."name", '-', 3) AS size
		FROM hotpick_requests h
		JOIN units u ON h.original_unit_id = u.id
		JOIN inventory_items i ON u.gtin = i.gtin
		WHERE u.lpn IN
	''' + lpn_text_list

	product_details = sql.connect_to_Artemis(query_string)[["lpn", "style_num", "color", "size"]]
	# join data
	fail_matchups = fail_matchups.merge(product_details, on="lpn", how="left")

	print("Done. Getting employees' employment type.")

	# add employment type by employee - temp or fulltime
	employment_type = pd.read_excel("employee_employment_type.xlsx")[["employee", "employment"]]
	employment_type = employment_type.rename(columns={"employee":"employee_responsible"})
	employment_type
	fail_matchups = fail_matchups.merge(employment_type, on="employee_responsible", how="left")
	
	print("Complete.")

	return(fail_matchups)

def push_to_db(df):
	'''
	Pushes Apollo Fail data to local database. Deletes previous data to avoid
	duplicates. Does not save historical data past 100 days.
	Args
		df: dataframe in to overwrite the scrap database in the local server
	Returns
		Nothing. Pushses data to database
	'''
	print("Loading data to db...")

	# convert df to list of tuples for inserting into SQL db
	data = df.values.tolist()
	data = [tuple(row) for row in data]

	# create query for inserting each row of data
	placeholders = ','.join(["%s"]*len(data))
	insert_query = "INSERT INTO scrap VALUES{}".format(placeholders)

	# connect to database
	connection_string = '''
	                    dbname='postgres'
	                    user='postgres'
	                    host='localhost'
	                    password='Avery011#'
	                    port='5432'
	                    '''
	connection = pg.connect(connection_string)
	cur = connection.cursor()
	# remove old data
	cur.execute("DELETE FROM scrap")
	# run query and commit changes
	cur.execute(insert_query, data)
	connection.commit()
	connection.close()

	input("Finished. Press enter to close")

if __name__ == "__main__":
	main()
