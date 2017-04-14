# -*- coding: utf-8 -*-

import os
import re

path_separate = os.getcwd() + "\\source"

try:
    os.mkdir(path_separate)
except OSError as e:
    print "папочка уже создана"

path_autors = path_separate + "\\autors.txt"
path_titles = path_separate + "\\titles.txt"
path_texts = path_separate + "\\texts.txt"

file_1 = open(path_autors, "r")
autors_list = file_1.readlines()
print str(len(autors_list))

file_1 = open(path_titles, "r")
titles_list = file_1.readlines()
print str(len(titles_list))

file_1 = open(path_texts, "r")
texts_list = file_1.readlines()
print str(len(texts_list))

out = open ("out.txt", "w+")

for i in range(len(autors_list)):
    if len(autors_list[i]) < 3 or len(titles_list[i]) < 3 or len(texts_list[i]) < 3:
        continue

    out.write(" |autors ")
    out.write(autors_list[i].replace("\n", ""))
    out.write(" |title ")
    out.write(titles_list[i].replace("\n", ""))
    out.write(" |text ")
    out.write(texts_list[i].replace("\n", ""))
    out.write("\n")

print "success"

