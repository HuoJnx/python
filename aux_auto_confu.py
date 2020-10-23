import sklearn
def auto_confu(y_true,y_pred):
    confu=sklearn.metrics.confusion_matrix(y_true,y_pred)
    tn, fp, fn, tp=confu.ravel()
    return(tn, fp, fn, tp)