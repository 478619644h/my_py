
import configparser
import os
import struct
import shutil
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def read_config():
    config_path = './config.ini'
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
config = read_config()
def text(path):
   with pdfplumber.open(path) as pdf:
       for i,page in enumerate(pdf.pages):
           texts = page.extract_text().split('\n')
           book_no = ''
           name = ''
           work_no = ''
           for line in texts:
                if '执业登记编号' in line:
                    book_no = line.split(' ')[0].split('：')[1]
                if  '姓名' in line:
                    name = line.split('： ')[1]
                if  '公司工号' in line:
                    work_no = line.split('：')[1]
           file_name = config.get('config','file_name_format').format(name=name, work_no=work_no, book_no=book_no)
           split_pdf(path,i,file_name)


def split_pdf(input_path, page_no,name):
    pdf = PdfReader(input_path)
    # 确保起始页和结束页在有效范围内
    output = PdfWriter()
    page = pdf.pages[page_no]
    output.add_page(page)
    # 指定拆分后的输出文件名
    output_filename = f"./splitpdf/{name}.pdf"
    with open(output_filename, "wb") as output_file:
        output.write(output_file)
    print(f'生成:[{output_filename}]')
    


def remove_files_by_folder(folder_path,rm_paths):
    folder_list = list()
    for folder in os.listdir(folder_path):
        if os.path.isdir(folder) and folder in rm_paths:
            folder_list.append(folder)
    for file in folder_list:
        rm_path = os.path.join(folder_path, file)
        print(rm_path)
        shutil.rmtree(rm_path)



# 设置文件夹路径、设置需要拆分的页码范围，遍历文件夹下的所有PDF文件
folder_path = "./"
split_file_path = './splitpdf'
if __name__ == '__main__':
    remove_files_by_folder(folder_path,['splitpdf'])
    if not os.path.exists(split_file_path):
       os.mkdir(split_file_path)
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            print(f"开始按页切分文件:[{filename}]")
            pdf_path = os.path.join(folder_path, filename)
            text(pdf_path)
            print(f"完成按页切分文件:[{filename}]")




