import pandas as pd

def find_sensor_name(sensor_str):
    #extracts sensor name by splitting slashes
    list_sensor = sensor_str.split("\\")
    return list_sensor[6] + "_" + list_sensor[7]

def find_sensor_id(sensor_str):
    #extracts sensor id from sensor name
    list_sensor = sensor_str.split("_")
    return list_sensor[0] + "_" + list_sensor[1] + "_" + list_sensor[2] + "_" + list_sensor[3] + "_" + list_sensor[4]

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

    count = 0
    csv_list = []
    for item in df_csv:
        if len(item) > 3:
            csv_list.append(item.strip("\r").split(","))

    return csv_list

def create_removal_list_mps2(csv_list, removal_list, bay):
    '''
    Appends to a running python list all the mps2 sensors to remove.

    Inputs:
    df: a pandas dataframe of an excel sheet

    col_name: a string containing the name of the column in excel with the log of the MPS2 failure

    removal_list: the removal python list to be appended to

    bay: a string containing the name of the LEO bay the excel and config file are about

    Output:
    None (appends to a running list)
    '''

    for item in csv_list:
        if len(item[1]) > 0:
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_MPS-2_soilTemp]")
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_MPS-2_MWP]")
    

def create_removal_list_5tm(csv_list, removal_list, bay):
    '''
    Appends to a running python list all the 5TM sensors to remove.

    Inputs:
    df: a pandas dataframe of an excel sheet

    col_name: a string containing the name of the column in excel with the log of the MPS2 failure

    removal_list: the removal python list to be appended to

    bay: a string containing the name of the LEO bay the excel and config file are about

    Output:
    None (appends to a running list)
    '''
    for item in csv_list:
        if len(item[2]) > 0:
            removal_list.append("[LEO-" + bay + "_" + item[0] +"_5TM_VWC]")
            removal_list.append("[LEO-" + bay + "_" + item[0] + "_5TM_bulkPerm]")
            removal_list.append("[LEO-" + bay + "_" + item[0] +"_5TM_soilTemp]")

def read_csv(csv_src):
    df = pd.read_csv(csv_src)
    csv_list = []

    #adds each column of csv as list into new list (list of lists)
    for column in df:
        li = df[column].tolist()
        li.append(column)
        csv_list.append(li)

    #removes non float and non int values
    for item in csv_list:
        if type(item[0]) != type(25.2) and type(item[0]) != type(25):
            csv_list.remove(item)
    
    #generates list of invalid sensors
    invalid_sensors = []
    for item in csv_list:
        if item[0] == -9999:
            invalid_sensors.append(find_sensor_name(item[1]))

    return invalid_sensors

def main():
    src_csv = "leo_center_sdi12-export-check 2.csv"
    src_excel = "subsoil SDI12 Sensor Status CENTER.xlsx"
    list_mps2 = []
    list_5tm = []

    sheets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]

    #creates list of logged removed sensors
    for sheet in sheets:
            csv_list = load_sheet(src_excel, sheet)
            create_removal_list_mps2(csv_list, list_mps2, "C")
            create_removal_list_5tm(csv_list, list_5tm, "C")

    invalid_sensors = read_csv(src_csv)
    invalid_ids = []

    #checks if any of the invalid sensors have been logged as removed
    for sensor in invalid_sensors:
        sensor_id = find_sensor_id(sensor)
        if sensor_id not in invalid_ids:
            invalid_ids.append(sensor_id)
    
    

main()