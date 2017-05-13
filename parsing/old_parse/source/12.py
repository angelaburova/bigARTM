# -*- coding: utf-8 -*-

def fun(arr, i):
    for k in range(len(arr)):
        arr[k] = arr[k].replace("\n", "")
    if len(arr[0]) > 4:
        for k in range(len(arr)):
            if not k % 2 == 0:
                s1 = arr[k]
                s2 = arr[k - 1]
                arr[k] = s2
                arr[k - 1] = s1

    result = ''
    for j in arr:
        result += j + " "
    result += "\n"
    return result


f = open('autors.txt', 'r')
lines = f.readlines()
f.close()
autors = []
f = open('autors.txt', 'w+')
c = 0
for i in lines:
    autors = i.split(" ")
    c +=1
    res = fun(autors, c)
    f.write(res)
f.close()