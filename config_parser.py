import pandas as pd
import sys

'''
*** REQUIRES PANDAS LIBRARY INSTALLED TO PYTHON ***

Things to Change: (in main function)
f_path_excel: string with filepath extension or name to excel workbook containing log of broken SDI12 sensors
f_path_ini: string with filepath extension or name to config file of SDI12 sensors 
'''

def find_bay(f_excel, f_ini):
    '''
    Ensures that the excel workbook and config file are about sensors in the same bay

    Inputs:
    f_excel: a string containing the filepath extension to the excel workbook
    f_ini: a string containing the filepath extension to the config file 

    Output:
    A string denoting the LEO bay the excel and config file are about
    '''

    if "center" in f_ini and "CENTER" in f_excel:
        return "C"
    
    if "east" in f_ini and "EAST" in f_excel:
        return "E"
    
    if "west" in f_ini and "WEST" in f_excel:
        return "W"
    
    return "Error"
    
def load_sheet(f_excel, sheet):
    '''
    Loads an excel sheet from a workbook into a pandas dataframe

    Inputs:
    f_excel: a string containing the filepath extension to the excel workbook
    sheet: a string denoting the sheet name to be loaded into the dataframe

    Output:
    A pandas dataframe of the excel sheet
    '''
    df = pd.read_excel(f_excel, sheet_name=sheet, usecols=[0, 2, 3])
    df_csv = df.to_csv(header=False, index=False)
    df_csv = df_csv.split("\n")

    #create list of items in csv
    csv_list = []
    for item in df_csv:
        if len(item) > 3:
            csv_list.append(item.strip("\r").split(","))

    return csv_list

def create_removal_list_mps2(csv_list, removal_list, bay):
    '''
    Appends to a running python list all the mps2 sensors to remove.

    Inputs:
    csv_list: a list of csv-type string items
    removal_list: the python removal list of MPS-2 sensors to be appended to
    bay: a string containing the name of the LEO bay the excel and config file are about
    '''

    for item in csv_list:
        if len(item[1]) > 0:
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_MPS-2_soilTemp]")
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_MPS-2_MWP]")
    

def create_removal_list_5tm(csv_list, removal_list, bay):
    '''
    Appends to a running python list all the 5TM sensors to remove.

    Inputs:
    csv_list: a list of csv-type string items
    removal_list: the python removal list of 5TM sensors to be appended to
    bay: a string containing the name of the LEO bay the excel and config file are about
    '''

    for item in csv_list:
        if len(item[2]) > 0:
            removal_list.append("[LEO-" + bay + "_" + item[0] +"_5TM_VWC]")
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_5TM_bulkPerm]")
            removal_list.append("[LEO-" + bay + "_" + item[0] +"_5TM_soilTemp]")

def test_types(df, col_name, sheet):

    '''
    testing tool to find all types of data stored in a column of an excel workbook
    '''
    for index, row in df.iterrows():
        if type(row[col_name]) != float:
            x = 5
        print(sheet + row.iloc[0] + str(type(row[col_name])))


def find_sensors(f_ini):
    '''
    Generates a dictionary of each sensor in the config file

    Inputs:
    f_ini: a string containing the filepath extension of the config file

    Output:
    A python dict of all the sensors within the config file
    '''
    sensors = {}

    with open(f_ini, "r") as file:
        lines = file.readlines()
    
    #manually inputs first [General] block
    sensors[lines[0]] = lines[0:12]

    #iterates through each line of the config file
    #inputs head of block as key of dict
    i = 12
    while i < len(lines):
        if lines[i][0] == "[":
            list_lines = lines[i:i+14]
            sensors[lines[i].strip("\n")] = list_lines
            i = i+13
        i+=1
    return sensors

def main():
    #change me!
    f_path_excel = "subsoil SDI12 Sensor Status WEST.xlsx"
    f_path_ini = "leo_west_sdi12-export.ini"

    sheets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
    removal_list_mps2 = []
    removal_list_5tm = []
    bay = find_bay(f_path_excel, f_path_ini)

    #checks if config file and excel file talk about same bay
    if bay == "Error":
        print("Error: Excel workbook and config file not about same bay")
        sys.exit(0)

    #generates removal list of all dead sensors logged in each sheet of excel workbook
    for sheet in sheets:
        csv_list = load_sheet(f_path_excel, sheet)
        create_removal_list_mps2(csv_list, removal_list_mps2, bay)
        create_removal_list_5tm(csv_list, removal_list_5tm, bay)
    

    #only adds sensors that are working to python list of new config file lines
    lines_to_write = []
    count = 0
    dict_sensors = find_sensors(f_path_ini)
    for k, v in dict_sensors.items():
        if k not in removal_list_5tm and k not in removal_list_mps2:
            for line in v:
                lines_to_write.append(line)
                count+=1
    
    print(len(removal_list_5tm)/3 + len(removal_list_mps2)/2)
    #generates updated config file
    #change 1st argument of open() fn to change the name of the updated config file.
    new_f = open(f_path_ini.strip(".ini") + "-updated.ini", "w" )
    for line in lines_to_write:
        new_f.write(line)


    #happy guy
    print("sensor total: " + str(count))
    print(":) done")

main()





def test():
    '''
    used to test/debug instead of running main everytime
    '''

    f_path_excel = "subsoil SDI12 Sensor Status WEST.xlsx"
    f_path_ini = "leo_west_sdi12-export.ini"


    sheets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
    removal_list_mps2 = []
    removal_list_5tm = []
    bay = find_bay(f_path_excel, f_path_ini)

    #checks if config file and excel file talk about same bay
    if bay == "Error":
        print("Error: Excel workbook and config file not about same bay")
        sys.exit(0)

    #generates removal list of all dead sensors logged in each sheet of excel workbook


    for sheet in sheets:
        csv_list = load_sheet(f_path_excel, sheet)
        create_removal_list_mps2(csv_list, removal_list_mps2, bay)
        create_removal_list_5tm(csv_list, removal_list_5tm, bay)
    
    len_dict = {}
    for item in removal_list_mps2:
        if len(item) in len_dict:
            len_dict[len(item)] += 1
        else:
            len_dict[len(item)] = 1

    print(len_dict)
    print(type(csv_list[2][1]))
