import os
import re
from shutil import copyfile

dict_file_name = "utils/new_dict.txt"
stop_file_name = "utils/stop5k.txt"

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

def bin_search(arr, word):
   l=0
   r=len(arr)
   while(r-l > 1):
      m = (r + l) // 2
      if word < arr[m]:
         r=m
      else:
         l=m
   return l if arr[l]==word else -1


def correct_text(orig_name, out_name):
    print "file: " + orig_name
    file1 = open(orig_name, "r")
    text = file1.read()
    text_words=text.split(" ")
    print "number of word before script = " + str(len(text_words))
    file_stop = open(stop_file_name, "r")
    words = file_stop.read()
    stop_words = words.split("\n")
    stop_words.sort()

    file_lemm = open(dict_file_name, "r")
    lemm_str = file_lemm.readlines()
    lemm_arr_form = []
    lemm_arr_orig = []

    for string in lemm_str:
        string=string.replace("\n", "")
        w = string.split(" ")
        lemm_arr_form.append(w[0])
        lemm_arr_orig.append(w[1])

    new_text=""
    for i in text_words:
       word = i
       index = bin_search(lemm_arr_form, word)
       if index != -1:
           word=lemm_arr_orig[index]

       if bin_search(stop_words, word) != -1:
          word=""
       else:
          word=word+" "
       new_text+=word
    a=new_text.split(" ")
    print "number of word after script = " + str(len(a))
    file2=open(out_name,"w")
    file2.write(new_text)


cur_path = os.getcwd() + "\\separate"
files = get_files(cur_path)
for file in files:
    correct_text(file, os.getcwd() + "/source/" + os.path.basename(file))

os.system('python utils/merge.py')

copyfile("out.txt", "../src/out.txt")
