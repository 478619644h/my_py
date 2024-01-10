import xlrd
import csv

def readExcel(filePath,sheetName):
    data = xlrd.open_workbook(filePath)
    table = data.sheet_by_name(sheetName)
    rowNum = table.nrows
    colNum = table.ncols
    startRow = 1
    file = open("123456.txt", "r")
    lines = file.readlines()
    for line in lines:
        line = line.strip()  # 去掉每行头尾空白
        #print(line)
        for i in range(rowNum - startRow):
            row = i + startRow
            name = table.cell(row, 0).value
            #print("line %s contains %s contains %s"%(line,name,line.__contains__(name)))
            if line.__contains__(name):
                print(line)



if __name__ == "__main__":
     readExcel("0803.xls","Sheet1")