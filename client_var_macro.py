
# this program identifies employees that have less rows in the first pivot table

import os

import xlwings as xw
import pandas as pd


def get_start_range(sheet,col, header):
    ''' 
    Checks first 20 rows to see where data frame begins
    sheet = sheet number (int) and col (str) is the column to check,
    and header (str) is the column name to find.
    '''
        
    range_str = col+"1:"+col+"20"
    cell_list = xw.Range(sheet, range_str).value
    row_num = cell_list.index(header) + 1
    range_str = col+str(row_num)
    
    return(range_str)
    
def get_df(sheet):
    ''' 
    Pulls all data from table and sets column headers.
    Sheet is an int, either 0 or 1 for this file.
    NOTE: Excel file must have first two tabs with table data and
    both tables must be sorted by sum of loaned to OT hours.
    '''
    
    col = "B"
    if sheet == 1:
        header = "employee_ssn"
    else:
        header = "GEMSID"
        
    range_start = get_start_range(sheet,col,header)
    data = xw.Range(sheet, range_start).table.value
    df = pd.DataFrame(data[1:],columns=data[0])     #skips first row for column headers
    
    return(df)
    
def rm_rows(df,col_name,containing_str):
    '''
    Removes rows containing specified text. For example, the extra rows
    showing totals can be removed by specifying the string "Total"
    '''
    
    df = df[df[col_name].str.contains(containing_str) == False]
    
    return(df)
    
    
def get_client_count(df):
    '''
    Groups the dataframe by employee and counts the number of clients by 
    employee. Returns dataframe.
    '''
    
    eid = df.columns[0]     # get the column name of employee ID's
    
    new_df = df.groupby(eid, as_index=False).size()     # use as_index so eids in index can be converted back to cells in dataframe
    new_df = new_df.reset_index()                       # groupby defaults index to column grouping, resets index to get dataframe
    new_df.columns = [new_df.columns[0], new_df.columns[0]+"_client_num"]   # creates column name based on first column
    new_df.columns = ["EmployeeID", new_df.columns[1]]                      # column names of first column must match for merge later
    
    return(new_df)
    
    
def get_valid_eids(df):
    '''
    Pulls employee IDs where they have loaned_to_OT hours > 0.
    This shorten the list of variances used later. Returns series.
    Note: accepts a dataframe that has not been grouped yet.
    '''
    
    col = df.columns[0]                             # get column name
    new_df = df.groupby(col, as_index=False).sum()  
    
    valid_eids = new_df[new_df["Sum of loaned_to_ot"] > 0][col]     # pulls a series of employee ID's that have hours for loaned to OT
    
    return(valid_eids)
    
    
def get_eid_var(df1, df2):
    '''
    Merges dataframes via their employee IDs and selects those that have a variances
    between the number of clients in AS and CA. Additionally, it reduces the list by
    removing employee's that don't have hours in loaned to OT.
    '''
    
    merged = df1.merge(df2, how="left", on="EmployeeID")
    merged = merged[merged.employee_ssn_client_num > merged.GEMSID_client_num]
    
    return(merged)
    

def refine_list(df, col, filter_series):
    '''
    Takes a data frame and filters by column values appearing in series.
    '''
    
    new_df = df[df[col].isin(filter_series)]
    
    return(new_df)
    
    
def main():

    wb = xw.Workbook.caller()

    # get data and remove extra rows showing totals
    df1 = get_df(1)
    df2 = get_df(2)
    df1 = rm_rows(df1, "employee_ssn", "Total")
    df2 = rm_rows(df2, "GEMSID", "Total")
    
    # get employee by client count data frames for each
    client_count1 = get_client_count(df1)
    client_count2 = get_client_count(df2)
    
    # merge data frames for variance analysis
    client_var = get_eid_var(client_count1, client_count2)
    
    # filter client variance list with the list of employee's who have loaned
    # to OT hours greater than 0
    
    valid_eids = get_valid_eids(df1)    # must be un-grouped df and we only need to look at employees on sheet 1
    final = refine_list(client_var, "EmployeeID", valid_eids)
    
    # print list of employee IDs to file; if none, print 'None'
    
    eids = list(final.EmployeeID)
    if not eids:
        xw.Range('bldg1_empl', 'F3').value = "None"
    else:
        xw.Range('bldg1_empl', 'F3').value = eids
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
