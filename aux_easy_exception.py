import easygui as g
def easy_exception(msg,title=None):
    g.msgbox(msg,title=title)
    raise Exception(msg)
def easy_finish(msg,title=None):
    g.msgbox(msg,title=title)