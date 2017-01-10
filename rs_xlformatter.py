'''
This file takes all the excel files ending in '.xls' from it's parent directory
and copy/pastes values in column B of each file to remove the formulas so it can 
be uploaded to the small package file upload on the Portal.
'''


import xlwings as xw
import os




def get_file_list():
    path = os.path.abspath("..")
    file_list = []
    
    for file in os.listdir(".."):
        if file[-4:] == ".xls":
            file_list.append(path+"\\"+file)
        
    return(file_list)


def set_row_vals():
    ''' Note: must have active link to a workbook'''
    vals = xw.Range("B:B").value
    list_vals = []
    
    xw.Range("B:B").number_format = "@"
    for cell in vals:
        list_vals.append([cell])    # to insert a column vector the list must be a list of list ([[a],[b],...])
    
    xw.Range("B:B").value = list_vals   # set values
    
def cycle_files():
    files = get_file_list()
    new_path = "RS_small_pckg\\uploads"
    
    for file in files:
        wb = xw.Workbook(file, app_visible=False)
        set_row_vals()
        wb.xl_workbook.SaveAs(file.replace("RS_small_pckg",new_path), xw.FileFormat.xlExcel8)
        
    
def main():
    cycle_files()
    
    
if __name__ == '__main__':
    main()