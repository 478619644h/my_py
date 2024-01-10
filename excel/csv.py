import xlrd

startRow = 1
def readExcel(filePath,sheetName):
    data = xlrd.open_workbook(filePath)
    table = data.sheet_by_name(sheetName)
    rowNum = table.nrows
    colNum = table.ncols

    dictA = {}

    for i in range(rowNum - startRow):
        row = i + startRow
        function_name = str(table.cell(row, 7).value)
        model_name = str(table.cell(row, 8).value)
        if not dictA.__contains__(model_name):
            setA = {function_name}
            dictA[model_name] = setA
        else:
            dictA[model_name].add(function_name)
    index = 1
    for key, value in dictA.items():
        table



def writeExcel(filePath,sheetName):
    excel_file = xlrd.open_workbook(filePath)


if __name__ == "__main__":
    readExcel("UAT-2.xls","Sheet1")