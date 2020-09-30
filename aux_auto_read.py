import warnings
import re
import pandas
def auto_read(path,sheet_name):

    global df,df_o
    yunit_dict={"FBG":"Glucose (mM)","GTT":"Glucose (mM)","Weight":"Weight (g)","TG":"TG (mM)","TC":"TC (mM)",
               "HDL":"HDL (mM)","LDL":"LDL (mM)"}
    try:
        y_unit=yunit_dict[sheet_name]
    except:
        y_unit=""
        warnings.warn("The supported sheet names are as listed: {}, the unsupported sheet names will get no x_units and y_units".format(", ".join(yunit_dict.keys())))
    #df_o
    df_o=pd.read_excel(path,sheet_name=sheet_name,skiprows=1)
        #delete ID==0 & '删除'
    df_o=df_o.query("ID!=0 & ID!='删除'")
        #delete rows with some NAN
    n_row,n_col=df_o.shape
    df_o.dropna(axis=0,how="any",thresh=n_col*0.9,inplace=True)
        #reset the index after drop
    df_o.index=range(len(df_o))
        #write in the sample size for the groups
    group_n_dict={}
    try:
        grouby_key="Type"
        df_o.groupby(grouby_key)
    except:
        grouby_key="Group"
    for key,df in df_o.groupby(grouby_key):
        n_sample=df.shape[0]
        group_n_dict[key]="{} (n={})".format(key,n_sample)
    df_o[grouby_key]=df_o[grouby_key].map(group_n_dict)
    #df
    df=df_o.copy()
    df=df.query("ID!=0 & ID !='删除'")
    df=df.melt(id_vars=["ID",grouby_key],var_name="x",value_name="y")
    #strip x
    sheet_name=sheet_name.split("_")[0]
    if sheet_name=="GTT":
        df["x"]=df["x"].map(lambda x:x.strip("分钟"))
        x_unit="Time (min)"
    elif sheet_name in yunit_dict.keys():
        prefix=df.at[0,"x"][0]
        if (prefix=="D") or (prefix=="P"):
            x_unit="Time (Day)"
            df["x"]=df["x"].map(lambda x:x.strip("D"))
            df["x"]=df["x"].map(lambda x:x.strip("P"))
        elif (prefix=="W"):
            x_unit="Time (Week)"
            df["x"]=df["x"].map(lambda x:x.strip("W"))
    else:
        x_unit=""
        df["x"]=df["x"].map(lambda x:x.strip("D"))
        df["x"]=df["x"].map(lambda x:x.strip("P"))
        df["x"]=df["x"].map(lambda x:x.strip("W"))
    #coercion
    df["x"]=df["x"].astype("float64")
    #standardize header to "ID","Type","x","y"
    df.columns=["ID","Type","x","y"]
    return df,df_o,x_unit,y_unit