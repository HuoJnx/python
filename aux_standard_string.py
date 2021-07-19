
def all_char(x):
    import re
    #strip the punctuations
    
    return(x)


def header_for_R(x):
    import re
    from xpinyin import Pinyin
    ##convert Chinese into pinyin
    p=Pinyin()
    Pin_x=p.get_pinyin(x)

    #strip all not belongs to 0-9, a-z, A-Z,and _
    Pin_x=re.sub("[^A-Za-z0-9_]","_",Pin_x)

    #num at first, add 'zzz' in front of the num
    Pin_x=re.sub("(^[0-9])",r"zzz\1",Pin_x)

    #strip the '_' at the end
    if len(Pin_x)>1:
        Pin_x=Pin_x.rstrip("_")
    else:
        pass

    #add an "X" to the head if the first are "_"
    if Pin_x[0]=="_":
        Pin_x="X"+Pin_x
    ## replase all all the non
    return(Pin_x)
