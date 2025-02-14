
Config_parser
Author: Ankit Garg (email: ankitgarg@arizona.edu or ankit195300@gmail.com)
Date created: 08/08/2024


Purpose:
This python script is used update a config (.ini) file when sensors from that file have been removed. The script interacts with the config file using a log of removed sensors to remove each removed sensor from the config file. This script is currently set up to work with the SDI12 sensor config file and removal log, but can easily be updated/modified to accommodate for other sensor types and config file types. 



Required Libraries:
-Pandas (https://pandas.pydata.org)
-Sys (already installed into python)

The easiest way to install pandas is through pip. Open a terminal application and type "pip install pandas" to install.



How to use:
1. Ensure that this script, the config file, and the excel workbook of the removal log are all in the same directory (folder). Open/run python from this directory as well.

2. Open this directory in a code editor such as VSCode. This can be ran from the terminal as well, although it will be more difficult to edit the correct variable and path names.

3. In the "main" function located at the bottom of the script file, edit the variables "f_path_excel" and "f_path_ini" to be the file name of the excel workbook with the removed sensors log and the file name of the config file, respectively. 

4. Run the script. The updated config file will appear in the same directory as everything else. The updated config file will have the same file name as the old config file with an added "-updated" identifier in the file name. The original config file will NOT be modified.

