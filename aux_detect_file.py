import os
import easygui as g
def detect_csv(detect_dir="."):
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
    if len(excel_file)==0:
        print("Not csv file in {}".format(detect_dir))
    else:
        for f in excel_file:
            os.remove(os.path.join(detect_dir,f))
    ## remove the Rplots.pdf in detect_dir
    try:
        os.remove(os.path.join(detect_dir,"Rplots.pdf"))
    except:
        print("Not Rplots.pdf in {}".format(detect_dir))