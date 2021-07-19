def t_plus(data_list,loose=False,fromat_digits=True):
    from scipy import stats
    n_type=len(data_list)
    if loose==False:
        levenep=stats.levene(*data_list)[1]
    else:
        levenep=0.2
    #print("levene p: {}".format(levenep))
    if levenep>0.1:
        if n_type==2:
            method="t-test"
            post_method="non_needed"
            p=stats.ttest_ind(*data_list,nan_policy="raise")[1]
        else:
            method="aov"
            post_method="tukey"
            p=stats.f_oneway(*data_list)[1]
    else:
        if n_type==2:
            method="mann"
            post_method="non_needed"
            try:
                p=stats.mannwhitneyu(*data_list,alternative="two-sided")[1]
            except:#有时候体重增长量的话，大家一开始都是0
                p=1
        else:
            method="kru"
            post_method="dunn_holm"
            try:
                p=stats.kruskal(*data_list,nan_policy="raise")[1]
            except:
                p=1
    if fromat_digits==True:
        try:
            levenep=round(levenep,4)
            p=round(p,4)
        except:
            print(levenep,p)
    print("{}, {},p={}".format(method,post_method,p))
    return(levenep,method,post_method,p)

def pos_hoc(df,method,post_method,fromat_digits=True):
    import scikit_posthocs
    from pandas import DataFrame as DF
    if post_method=="tukey":
        post_out=scikit_posthocs.posthoc_tukey(df,val_col="y",group_col="Type")
    elif post_method=="dunn_holm":
        post_out=scikit_posthocs.posthoc_dunn(df,val_col="y",group_col="Type",p_adjust="holm")
    elif post_method=="non_needed":
        post_out=DF([[9,9],[9,9]])
    post_out.index.name="{}+{}".format(method,post_method)
    print(post_out)
    if fromat_digits==True:
        post_out=post_out.applymap(lambda x:1 if x>0.06 else x)
        post_out=post_out.applymap(lambda x:round(x,4))
    return(post_out)

def melt_post(post_result,e):
    import numpy as np
    method=post_result.index.name
    arr=post_result.values
    arr_in=np.tril_indices(arr.shape[0],k=0)#tril_indices用于获得下三角的index和columns，k=0是把对角线也干掉，k=-1是不干掉对角线
    arr[arr_in]=9
    post_result[:]=arr#这一步就获得了上三角矩阵
    temp=post_result.reset_index()
    temp_melt=temp.melt(id_vars=temp.columns[0],var_name="pair",value_name="p")
    post_melt=temp_melt.query("p<0.06")#筛选出＜0.06的
    post_melt["method"]=method#获得方法
    post_melt["x"]=e#获得时间
    post_melt.columns=["pair2","pair1","p","method","x"]
    post_melt=post_melt.reindex(columns=["pair1","pair2","p","method","x"])
    return(post_melt)