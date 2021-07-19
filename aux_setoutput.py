import arrow
import os

def get_time(accu="sec"):
    if accu=="sec":
        now=arrow.now().format("YYYYMMDD_HH_mm_ss")
    elif accu=="day":
        now=arrow.now().format("YYYYMMDD")
    return(now)

def set_path_time(arg_list=None,accu="sec"):
    from aux_standard_string import all_char 
    now=get_time(accu)
    output_dir="output"+"_"+now
    if arg_list:
        arg="_".join(arg_list)
        arg=all_char(arg)
        output_dir+=" ({})".format(arg)
    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass
    return(output_dir,now)

def get_path_time(arg_list=None,accu="sec"):
    from aux_standard_string import all_char 
    now=get_time(accu)
    output_dir="output"+"_"+now
    if arg_list:
        arg="_".join(arg_list)
        arg=all_char(arg)
        output_dir+=" ({})".format(arg)
    return(output_dir,now)

def mkdir(out_dir="output"):
    try:
        os.mkdir(out_dir)
    except FileExistsError:
        pass
    return(out_dir)
