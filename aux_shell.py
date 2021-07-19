import subprocess
def verbose_shell(code_split):
    print("-"*50,code_split,"-"*50)
    p = subprocess.Popen(code_split,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for e2 in  p.communicate():
        if e2!=None:
            e2=str(e2).split("\\r\\n")
            [print(e3) for e3 in e2]