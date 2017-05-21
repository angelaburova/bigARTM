import os
import re
from shutil import copyfile

def get_files(path):
    files_name = []
    print "geting files"
    for root, dirs, files in os.walk(path):
        for name in files:
            fullname = os.path.join(root, name)
            if re.search(r".txt", name):
                files_name.append(fullname)
                print name
    return files_name

cur_path = os.getcwd() + "\\separate"
files = get_files(cur_path)

for file in files:
    copyfile(file, os.getcwd() + "/source/" + os.path.basename(file))
    os.system('python utils/merge.py')
    copyfile("out.txt", "../src/out.txt")


