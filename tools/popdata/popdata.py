import os
import shutil as sh

def j(*args):
    return os.path.join(*args)

def fp(*args):
    return os.path.join(".",*args)

def main():
    fold=j("..","..","data")
    if not os.path.isdir(fold) and not os.path.exists(fold):
        os.mkdir(fold)
    os.system(f"cd {j('..','volgen')}&&python3 {fp('main.py')}")
    sh.copyfile(j("..","volgen","out.json"),j("..","..","data","size.json"))

def init():
    main()
    print("Done!!!")

if __name__=="__main__":
    init()