# -*- coding: utf-8 -*-

import os
import re
from string import punctuation


path_separate = os.getcwd() + "\\separate"
path_autors = path_separate + "\\autors.txt"
path_titles = path_separate + "\\titles.txt"
path_texts = path_separate + "\\texts.txt"
open(path_autors, "w+")
open(path_titles, "w+")
open(path_texts, "w+")


def get_files(path):
    files_name = []
    print "get files"
    for root, dirs, files in os.walk(path):
        for name in files:
            fullname = os.path.join(root, name)
            if re.search(r".txt", name):
                files_name.append(fullname)
                print name
    return files_name

def delete_pun(line):
    pun = punctuation + u'-«'
    for char in pun:
        line = line.replace(char, u"")
    line =line.lower()

    line = re.sub(ur"\d", u'', line)
    line = re.sub(ur" . ", u' ', line)
    line = re.sub(ur"^. ", u' ', line)
    line = re.sub(ur" .$", u' ', line)
    line = re.sub(ur" .. ", u' ', line)
    line = re.sub(ur"^.. ", u' ', line)
    line = re.sub(ur" ..$", u' ', line)
    line = re.sub(ur"^.$", u'', line)
    line = re.sub(ur"^..$", u'', line)

    return line

def delete_short_word(text_input):
    text = []

    for i in range(len(text_input)):
        text_input[i] = delete_pun(text_input[i])

    i = 0
    while(i<len(text_input)):
        if re.search(ur"^\s*\n", text_input[i]):
            text_input.pop(i)
        elif len(text_input[i])<3:
            text_input.pop(i)
        i+=1

    if len(text_input)>0:
        university = [u"алексеева", u"туполева", u"лобачевского" , u"университет", u"университета"]
        for k in range(len(university)):
            index = text_input[0].find(university[k])
            if index>-1 and index<130:
                text_input[0] = text_input[0][index + len(university[k]):]

    for i in range(len(text_input)):
        text.append(text_input[i])

    for i in range(len(text)):
        text[i] = text[i].replace("\n", " ")

    return text

def separate_to_articles():
    cur_path = os.getcwd() + "\\text"
    files = get_files(cur_path)

    try:
        os.mkdir(path_separate)
    except OSError as e:
        print "папочка уже создана"

    print "separate_to_articles"

    for name in files:
        file = open(name, "r")
        lines_utf8 = file.readlines()
        lines = []
        for i in range(len(lines_utf8)):
            lines.append(lines_utf8[i].decode('utf-8'))

        for i in range(len(lines)):
            if re.search(ur"УДК", lines[i]) and not re.search(ur"[а-яё]", lines[i]):
                start = i
                end = -1
                for k in range(i+1, len(lines)):
                    if re.search(ur"УДК", lines[k]) and not re.search(ur"[а-яё]", lines[i]) :
                        end = k
                        break
                if end == -1:
                    end = len(lines)

                autor_end = -1
                autor = u""
                for k in range(i+1, end):
                    if re.search(ur".[\.][ ]?.[\.]", lines[k]) and not re.search(ur"университет", lines[k]):
                        autor_end = k
                        autor += lines[k].replace(u"\n", u" ")
                        index = k+1
                        while(re.search(ur".[\.][ ]?.[\.]", lines[index]) and not re.search(ur"университет", lines[index]) and not re.search(ur"/", lines[index]) and not re.search(ur"-", lines[index]) and not re.search(ur":", lines[index])):
                            autor += lines[index].replace(u"\n", u"")
                            autor_end = index
                            index+=1
                        break



                autor = (autor.split("("))[0]
                for char in punctuation:
                    autor = autor.replace(char, u"")
                autor = re.sub(ur"\d", u'', autor)
                autor = autor.lower()
                while re.search(u"[ ][а-яё][ ][а-яё][ ]", autor):
                    init = re.search(u"[ ][а-яё][ ][а-яё][ ]", autor)
                    init = init.group(0)
                    autor = autor.replace(init, init[0:2] + init[3:])
                while re.search(u"^[а-яё][ ][а-яё][ ]", autor):
                    init = re.search(u"^[а-яё][ ][а-яё][ ]", autor)
                    init = init.group(0)
                    autor = autor.replace(init, init[0:1] + init[2:])

                title = u""
                title_end = -1
                for k in range(autor_end + 1, end):
                    if re.search(ur"[А-ЯЁ]+", lines[k]):
                        title += (" " + lines[k].replace(u"\n", u" "))
                        title_end = k
                        index = k + 1
                        while(not re.search(ur"[а-яё]", lines[index])):
                            title_end = index
                            title += (" " + lines[index].replace(u"\n", u" "))
                            index +=1
                        break
                title = delete_pun(title)

                text = lines[title_end+1:end]
                text_1 = delete_short_word(text)

                file_1 = open(path_autors, "a")
                file_1.write(autor.encode('utf-8') + "\n")
                file_1 = open(path_titles, "a")
                file_1.write(title.encode('utf-8') + "\n")
                file_1 = open(path_texts, "a")
                for i in range(len(text_1)):
                    file_1.write(text_1[i].encode('utf-8'))
                file_1.write("\n")

separate_to_articles()
os.system('python utils/delete_initials.py')
