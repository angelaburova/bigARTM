# -*- coding: utf-8 -*-
import csv
import os

def print_rows(table, rows, offset=0):
    n_col = len(table[0])
    for i in range(offset, offset + rows):
        for k in range(n_col):
            print str(table[i][k]) + "\t",
        print
    print

def read_csv(filename):
    file = open(filename, "r")
    reader = csv.reader(file)

    table = []
    names = []

    header = reader.next()
    size = len(header) - 1
    for row in reader:
        new_row = []
        for i in range(1, size + 1):
            new_row.append(float(row[i]))
        table.append(new_row)
        names.append(row[0])
    return [header, names, table, size]

def write_csv(filename, header, names, table):
    new_table = []
    new_table.append(header)
    for i in range(len(names)):
        new_row = []
        new_row.append(names[i])
        r = []
        for col in table[i]:
            new_row.append(str(col))
        new_table.append(new_row)

    file = open(filename, "w+")
    for row in new_table:
        file.write(",".join((row)) + "\n")

def find_sparse(table):
    n_row = len(table)
    n_col = len(table[0])

    size = n_row * n_col
    is_null = 0
    for i in range(n_row):
        for k in range(n_col):
            if table[i][k] == 0.0 :
                is_null += 1

    sparse = float(is_null)/ float(size)
    return sparse

def find_sparse_for_out(table):
    n_row = len(table)
    size = 0
    is_null = 0
    for i in range(n_row):
        for k in range(len(table[i])):
            size += 1
            if table[i][k][1] == 0.0:
                is_null += 1

    sparse = float(is_null)/ float(size)
    return sparse

def find_duplicates(table):
    n_col = len(table)
    for k in range(n_col):
        for i in range(20):
            for j in range(i + 1, 20):
                if table[k][i][0] == table[k][j][0]:
                    table[k][i][1] += table[k][j][1]
                    table[k].pop(j)
    return table

def for_sort(pair):
    return pair[1]

def find_duplicates_in_coeff(table):
    n_col = len(table)
    for k in range(n_col):
        for j in range(k + 1, n_col):
            for i in range(15):
                for g in range(15):
                    if table[k][i][0] == table[j][g][0]:
                        if table[k][i][1] < table[j][g][1]:
                            table[j][g][1] *= 0.3
                        else:

                            table[k][i][1] *= 0.3
    for col in range(len(table)):
        table[col].sort(key=for_sort, reverse=True)
        table[col] = norm(table[col])
    return table

def norm(col):
    sum = 0.0
    for i in col:
        sum += i[1]
    coeff = 1.0/sum
    for i in range(len(col)):
        col[i][1] = col[i][1] * coeff
    return col


def reg(table, size):
    n_col = len(table[0])
    for row in range(len(table)):
        sum = 0.0
        for i in range(n_col):
            sum += table[row][i]
        avg = float(sum) / float(size)
        for i in range(n_col):
            table[row][i] -= avg
            if table[row][i] < 0.0:
                table[row][i] = 0.0
    return table

def find_top_words(table, names):
    n_row = len(table)
    n_col = len(table[0])

    new_table = []
    for k in range(n_col):
        col = []
        for i in range(n_row):
            col.append([names[i], table[i][k]])

        col = norm(col)
        col.sort(key=for_sort, reverse=True)

        new_table.append(col)
    return new_table

def print_top_words(table):
    n_col = len(table)
    for k in range(n_col):
        print "sbj" + str(k) + ": ",
        for i in range(15):
            print table[k][i][0] + " ",
        print


def delete_noise(table):
    n_col = len(table)

    for i in range(n_col):
        size = len(table[i])
        for k in range(int(size*0.15), size):
            table[i][k][0] = 0.0
        table[i] = norm(table[i])
    return table

def post_regularization(model):
    file_for_read = "tmp_phi.csv"
    phi = model.get_phi()

    phi.to_csv(file_for_read, header=True, sep=',', index=True, encoding='utf-8')
    out = read_csv(file_for_read)

    header = out[0]
    names = out[1]
    table = out[2]
    size = out[3]

    table = reg(table, size)
    rev_table = find_top_words(table, names)
    rev_table = find_duplicates(rev_table)
    rev_table = find_duplicates_in_coeff(rev_table)
    rev_table = delete_noise(rev_table)
    print_top_words(rev_table)
    print
    print find_sparse_for_out(rev_table)

    os.remove(file_for_read)
