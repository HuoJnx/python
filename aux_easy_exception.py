import easygui as g
def aux_easy_exception(msg,title=None):
    g.msgbox(msg,title=title)
    raise Exception(msg)