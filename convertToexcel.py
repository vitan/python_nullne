#!/usr/bin/env python2.7
#author:    nullne
#email:     co.pangolin@gmaill.com
# handle file may looks like following(cols=3):
# something     otherthing   anotherthing
import xlwt
import sys
import argparse

def splitbyspace(i, cols):
    arr = []
    for  x in range(0,cols - 1):
        i =  i.lstrip()
        tmp = i.split(' ', 1)
        arr.append(tmp[0])
        i = tmp[1]
    arr.append(tmp[1].lstrip()[:-1])
    return arr

def output(output, sheet, filename, cols):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet)
    n = 0


    with open(filename, "r") as f:
        lines = f.readlines()
        if len(lines) >= 1:
            lines = lines[1:]
            for i in lines:
                res = splitbyspace(i,cols)
                sh.write(n, 0, res[0])
                sh.write(n, 1, res[1])
                sh.write(n, 2, res[2])
                n +=1

        else:
            return "empty file"
    book.save(output)

def main():
    output('sheet', 'table', handlefile, 3)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', default='result.d', help='filename')
    args = parser.parse_args()
    handlefile = args.file
    main()
