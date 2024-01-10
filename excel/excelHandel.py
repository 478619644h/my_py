import xlrd


def readExcel(filePath,sheetName):
    data = xlrd.open_workbook(filePath)
    table = data.sheet_by_name(sheetName)
    rowNum = table.nrows
    colNum = table.ncols
    startRow = 7
    str = ''' <data name="%s">
                    <field length="%s"  type="%s"></field>
               </data>'''

    strScale = '''<data name="%s">
                     <field length="%s" scale="%s" type="%s"></field>
                  </data>'''

    strArrayStart = '''<data name="%s">
            <array>
                <struct>'''

    strArrayEnd = ''' </struct>
            </array>
        </data>'''
    for i in range(rowNum - startRow):
       row = i + startRow
       name = table.cell(row, 7).value
       if name == "输出":
           break
       require = table.cell(row, 11).value



       val = table.cell(row, 9).value

       if val == "ARRAY":
           flag = table.cell(row, 10).value
           if flag == "START":
              print(strArrayStart%(name))
           if flag == "END":
              print(strArrayEnd)
           continue


       type = val.split("(")[0].lower()

       temp = val.split("(")[1]

       length = temp.split(")")[0]
       if temp.find(",") != -1:
           l1 = length.split(",")[0]

           scale = length.split(",")[1].split(")")[0]
           print(strScale % (name, l1, scale, type))
           continue



       print(str%(name, length,type))


def readExcelHead(filePath,sheetName):
    data = xlrd.open_workbook(filePath)
    table = data.sheet_by_name(sheetName)
    rowNum = table.nrows
    colNum = table.ncols
    startRow = 3
    str = ''' <data name="%s">
                    <field length="%s"  type="%s"></field>
               </data>
               '''

    strScale = '''<data name="%s">
                     <field length="%s" scale="%s" type="%s"></field>
                  </data>
                  '''

    strArrayStart = '''<data name="%s">
            <array>
                <struct>
                '''

    strArrayEnd = '''</struct>
            </array>
        </data>
        '''



    sysHeadStart = '''<sys-header>
        <data name="SYS_HEAD">
            <struct>
            '''

    sysHeadEnd = '''</struct>
        </data>
    </sys-header>
    '''

    appHeadStart = '''<app-header>
        <data name="APP_HEAD">
            <struct>
            '''

    appHeadEnd = ''' </struct>
        </data>
    </app-header>
    '''

    localHeadStart = ''' <local-header>
        <data name="LOCAL_HEAD">
            <struct>'''

    localHeadEnd = '''</struct>
        </data>
    </local-header>
    '''

    arrayStr = ""

    body = ""

    for i in range(rowNum - startRow):
       row = i + startRow
       name = table.cell(row, 7).value

       isF = True

       if name == "输出":
           break

       if len(name) == 0:
           continue

       strRow = ""
       val = table.cell(row, 9).value
       headType = table.cell(row, 10).value
       if val == "ARRAY" or headType == "LOCAL_HEAD":
           continue
           # isF = False
           # flag = table.cell(row, 12).value
           # if flag == "START":
           #    strRow = strArrayStart%(name)
           # if flag == "END":
           #    strRow = strArrayEnd


       if isF:


           type = val.split("(")[0].lower()
           temp = val.split("(")[1]

           length = temp.split(")")[0]
           if temp.find(",") != -1 and isF:
               isF = False
               l1 = length.split(",")[0]

               scale = length.split(",")[1].split(")")[0]
               strRow = strScale % (name, l1, scale, type)



           if isF:
              strRow = str%(name, length,type)



       if headType == "SYS_HEAD":
           sysHeadStart += strRow

       if headType == "APP_HEAD":
           appHeadStart += strRow


       if headType == "BODY":
           body += strRow

    finalStr = sysHeadStart + sysHeadEnd + appHeadStart + appHeadEnd  + body
    print(finalStr)



def readExcelDataCoulum(filePath,sheetName):
    data = xlrd.open_workbook(filePath)
    table = data.sheet_by_name(sheetName)
    rowNum = table.nrows
    colNum = table.ncols

    for i in range(rowNum):
        tablename = table.cell(i, 17).value
        if tablename == "T_PRD_FINANCE":
            column = table.cell(i,20).value
            column_name = table.cell(i,21).value
            print("comment on column T_PRD_FINANCE_MID.%s is '%s'；"%(column,column_name))




if __name__ == "__main__":
    readExcelDataCoulum("./财富E站通数据接口字段映射分析V1.7.xls","字段映射分析")
    #readExcel("./BOQHD_TS_P_49_IT优化项目群_ESB_新二代支付系统_字段映射文档_V2.3.2.xls","PAY20009")
    #readExcelHead("./BOQHD_TS_P_49_IT优化项目群_ESB_新二代支付系统_字段映射文档_V2.3.2.xls", "HEAD")