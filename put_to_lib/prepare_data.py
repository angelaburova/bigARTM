import os
import re
from shutil import copyfile

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


def correct_text(orig_name,dict_file_name, stop_file_name):
    print "file: " + orig_name
    file1 = open(orig_name, "r")
    text = file1.read()
    text_words=text.split(" ")
    print "number of words before preparing data = " + str(len(text_words))
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
    print "number of words after preparing data = " + str(len(a))
    file2=open(orig_name,"w")
    file2.write(new_text)

def preapre_data(path_out, path_dict, path_stop):
    correct_text(path_out, path_dict, path_stop)
