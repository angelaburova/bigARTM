# -*- coding: utf-8 -*-
def newstr(arr):
    ss = ''
    for j in range(len(arr)):
        if j % 2 == 0:
            ss += arr[j]+'_'
        else:
            ss += arr[j]+' '
    return ss

f = open('separate/autors.txt', 'r')
lines = f.readlines()
f.close()
autors = []
f2 = open('separate/autors.txt', 'w+')
for i in lines:
    autors = i.split()
    a = newstr(autors)
    f2.write(a + '\n')

