import os
import pandas as pd
import subprocess
def detect_csv(detect_dir="R_plugin"):
    excel_file=[file for file in os.listdir(detect_dir) if "csv" in os.path.splitext(file)[1] and "~" not in file]
    if len(excel_file)>1:
        raise Exception("More than 1 csv input in the directory: {}".format(excel_file)) 
    return(excel_file)

def detect_excel(detect_dir="."):
    excel_file=[file for file in os.listdir(detect_dir) if "xls" in file and "~" not in file]
    if len(excel_file)>1:
        raise Exception("More than 1 excel input in the directory: {}".format(excel_file)) 
    elif len(excel_file)==0:
        raise Exception("No xlsx file in the directory.") 
    return(excel_file)

def remove_csv(detect_dir="R_plugin"):
    ## remove the csv files in detect_dir
    excel_file=[file for file in os.listdir(detect_dir) if "csv" in os.path.splitext(file)[1] and "~" not in file]
    try:
        os.remove(os.path.join("./R_plugin",excel_file[0]))
    except:
        print("Not csv file in {}".format(detect_dir))
    ## remove the Rplots.pdf in detect_dir
    try:
        os.remove(os.path.join("./R_plugin","Rplots.pdf"))
    except:
        print("Not Rplots.pdf in {}".format(detect_dir))
def verbose_shell(code_split):
    print("-"*50,code_split,"-"*50)
    p = subprocess.Popen(code_split,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for e2 in  p.communicate():
        if e2!=None:
            e2=str(e2).split("\\r\\n")
            [print(e3) for e3 in e2]