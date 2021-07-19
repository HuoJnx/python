
def all_char(x):
    import string
    from zhon import hanzi
    import re
    #strip the punctuations
    x=re.sub("[{}]".format(hanzi.punctuation+string.punctuation+"-"),"_",x)
    #convert space into '_'
    x=re.sub("_+","_",x)#strip for multiple '_'
    return(x)


def header_for_R(x):
    import re
    from xpinyin import Pinyin
    ##convert Chinese into pinyin
    p=Pinyin()
    Pin_x=p.get_pinyin(x)
    #strip the punctuations
    Pin_x=all_char(Pin_x)
    #num at first, add 'zzz' in front of the num
    Pin_x=re.sub("(^[0-9])",r"zzz\1",Pin_x)
    #replace " " with "_"
    Pin_x=re.sub("\s",r"_",Pin_x)
    #strip the '_' at the end
    Pin_x=Pin_x.rstrip("_")
    if Pin_x[0]=="_":
        Pin_x="X"+Pin_x
    return(Pin_x)
