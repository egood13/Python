'''
This file takes management hierarchical data that lists employees and all 
levels of their management (up to 9) and transforms the data to a one-to-
one relationship. Outpus a table that shows employee ID, manager ID,
and manager name for each manager of an employee.
'''


import pandas as pd
import sys
import datetime




def read_excel(sheet, cell):
    
    data = xw.Range(sheet, cell).table.values
    df = pd.DataFrame(data[1:], columns=data[0])
    
    return(df)

def extract_data(df):
    ''' Pass a df and the cols you wish to extract data from '''
    
    cols = ["EID", "MID", "Mgr_Name"]
    col_list = [["Emp ID","Level 1 Manager ID", "Level 1 Manager Name"],
                ["Emp ID","Level 2 Manager ID", "Level 2 Manager Name"],
                ["Emp ID","Level 3 Manager ID", "Level 3 Manager Name"],
                ["Emp ID","Level 4 Manager ID", "Level 4 Manager Name"],
                ["Emp ID","Level 5 Manager ID", "Level 5 Manager Name"],
                ["Emp ID","Level 6 Manager ID", "Level 6 Manager Name"],
                ["Emp ID","Level 7 Manager ID", "Level 7 Manager Name"],
                ["Emp ID","Level 8 Manager ID", "Level 8 Manager Name"],
                ["Emp ID","Level 9 Manager ID", "Level 9 Manager Name"]]
    
    new_df = pd.DataFrame(columns=cols)
    tempdf = pd.DataFrame(columns=cols)
    
    for level in col_list:
        tempdf[cols] = df[level]
        new_df = new_df.append(tempdf, ignore_index=True)
    
    new_df = new_df.dropna()
    return(new_df)
    
def filler(cell):
    '''This function takes a string and fills in leading zeroes.'''
    fill = '0000000'
    filled_cell = fill+cell
    filled_cell = filled_cell[-9:]
    filled_cell = filled_cell[:7]
    return(filled_cell)

def format_cols(df, cols):
    '''Formats a column to a string'''
    for col in cols:
        df[col] = df[col].astype(str)
        df[col] = df[col].apply(filler)
        
    return(df)
        

def main():
    
    wb = xw.Workbook.caller()
    
    data_df = read_excel("data","A1")
    df = extract_data(data_df)
    
    cols = ["EID", "MID"]
    format_cols(ndf, cols)
    
    xw.Range("hierarchy", "A2").value = df
    











