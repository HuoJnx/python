import warnings
import re
import pandas as pd
import numpy as np
def auto_read(path,sheet_name):

    global df,df_o
    df_unit=pd.read_csv("XY_Unit.tsv",sep="\t")
    df_unit=df_unit.query("Type=='L'")
    try:
        y_unit=df_unit[df_unit["Sheet_name"]==sheet_name]["y_unit"].iloc[0]
    except:
        y_unit=""
    #df_o
    df_o=pd.read_excel(path,sheet_name=sheet_name,skiprows=1)
    ## sort the df_o by ["Normal","NGT","STZ","HFD","HFD+STZ"]
    try:
        grouby_key="Type"
        df_o.groupby(grouby_key)
    except:
        grouby_key="Group"
    ## some special supports
    df_o=special_support(df_o,sheet_name,grouby_key)
    ## drop bad rows
    df_o=drop_row(df_o)

    ##special order for plot
    df_o=special_sort(df_o,grouby_key)

    ##write in the sample size for the groups
    df_o=sample_size(df_o,grouby_key)

    ##coercion
    df_o.iloc[:,2:]=df_o.iloc[:,2:].astype("float64")

    #df
    df=df_o.copy()
    df=df.melt(id_vars=["ID",grouby_key],var_name="x",value_name="y")
    #strip x
    sheet_name=sheet_name.split("_")[0]
    if sheet_name=="GTT" or sheet_name=="ITT":
        df["x"]=df["x"].map(lambda x:x.strip("分钟"))
        x_unit="Time (min)"
    elif sheet_name in df_unit.Sheet_name.to_list():
        #print(df)
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
    #standardize header to "ID","Type","x","y"
    df.columns=["ID","Type","x","y"]
    #coercion
    df.x=df.x.astype("float64")
    return df,df_o,x_unit,y_unit

def auto_read_bar(path,sheet_name):
    df_unit=pd.read_csv("XY_Unit.tsv",sep="\t")
    df_unit=df_unit.query("Type=='B'")
    try:
        y_unit=df_unit[df_unit["Sheet_name"]==sheet_name]["y_unit"].iloc[0]
    except:
        y_unit=""
    x_unit=""
    df_o=pd.read_excel(path,sheet_name=sheet_name,skiprows=1)
    
    ## write in the sample size for the groups
    try:
        grouby_key="Type"
        df_temp=df_o[grouby_key].copy()
    except:
        grouby_key="Group"

    ## some special supports
    df_o=special_support(df_o,sheet_name,grouby_key)

    ## drop bad rows
    df_o=drop_row(df_o)

    ## sort the df_o by ["Normal","NGT","STZ","HFD","HFD+STZ"]
    df_o=special_sort(df_o,grouby_key)
    
    ##write in the sample size for the groups
    df_o=sample_size(df_o,grouby_key)

    ##
    df=df_o.copy()
    df=df.melt(id_vars=["ID",grouby_key],var_name="x",value_name="y")
    df.columns=["ID","Type","x","y"]
    return df,df_o,x_unit,y_unit
def drop_row(df_o):
    #delete ID==0 & '删除'
    df_o=df_o.query("ID!=0 & ID!='删除'")
    #delete ID with "***"
    df_o.ID=df_o.ID.astype("string")
    df_o=df_o[~df_o.ID.str.contains("\*\*\*")]
    #delete rows with some NAN
    n_row,n_col=df_o.shape
    df_o.dropna(axis=0,how="any",thresh=n_col*0.9,inplace=True)
    #reset the index after drop
    df_o.index=range(len(df_o))
    print("Dropped.")
    return(df_o)
def special_support(df_o,sheet_name,grouby_key):
    if sheet_name=="ITT":
        df_o.iloc[:,2:]=df_o.iloc[:,2:].div(df_o.iloc[:,2],axis="index")*100
        print("Special support for {}.".format(sheet_name))
    elif sheet_name=="Weight":
        df_o.iloc[:,2:]=df_o.iloc[:,2:].sub(df_o.iloc[:,2],axis="index")
        print("Special support for {}.".format(sheet_name))
    elif sheet_name=="MRI":
        df_o=df_o.reindex(columns=["ID",grouby_key,"Fat","Fluid","Lean"])
    elif sheet_name=="Organ_weight":
        df_o=df_o.reindex(columns=["ID",grouby_key,"Liver","Inguinal fat","Gonadal fat"])
    elif sheet_name=="Tongue":
        df_o=df_o.reindex(columns=["ID",grouby_key,"r"])
    elif sheet_name=="cell_area":
        ratio=np.mean([1360/232.1,1024/174.7])
        ratio_s=np.square(ratio)
        df_o["Adipocyte area"]=df_o["Adipocyte area"]/ratio_s
    elif sheet_name=="cell_number":
        df_o=df_o.iloc[:,0:3]
    else:
        ##print("Don't need special support.")
        pass
    return(df_o)

def special_sort(df_o,grouby_key):
    cats=[]
    special_order=pd.read_csv("special_sort.tsv",sep="\t")
    for col in special_order.columns:
        cat=special_order.loc[:,col].dropna().to_list()
        cats.append(cat)

    for cat in cats:
        #print(df_o[grouby_key])
        #print(df_o[grouby_key].isin(cat))
        if not df_o[grouby_key].isin(cat).all():#如果有其中1个不匹配,那就不搞。
            continue
        if len(cat)==len(df_o[grouby_key].value_counts()):#如果种类数量不对，那也不搞。
            print(cat)
            from pandas.api.types import CategoricalDtype
            sort_order=CategoricalDtype(cat,ordered=True)
            df_o[grouby_key] = df_o[grouby_key].astype(sort_order)
            df_o=df_o.sort_values(grouby_key)
            break#找到了就挑出循环
    return(df_o)

def sample_size(df_o,grouby_key):
    group_n_dict={}
    for key,df in df_o.groupby(grouby_key):
        n_sample=df.shape[0]
        group_n_dict[key]="{} (n={})".format(key,n_sample)
    df_o[grouby_key]=df_o[grouby_key].map(group_n_dict)
    print("Sample size counted.")
    return(df_o)