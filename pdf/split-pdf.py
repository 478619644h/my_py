
import os
import struct
import shutil
import fitz
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter


#设置tesseract 本地安装位置
pytesseract.pytesseract.tesseract_cmd='/usr/local/bin/tesseract'
#ocr读取图片文字
def ocr_image(path):
    img = Image.open(path)
    text = pytesseract.image_to_string(img,lang='chi_sim')
    lines = text.split('\n');
    uses = ['姓名','公司工号','执业登记编号']
    print('--------------')
    res = [];
    for use in uses:
     for line in lines:
         if use in line:
             temp = []
             if '，' in line:
                res.append(line.split('，')[1].strip())
             elif ' ' in line:
                res.append(line.split(' ')[1].strip())

    return res

#pdf转图片
def pyMuPDF_fitz(pdfPath, imagePath,name):
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 1.33333333  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.save(imagePath + '/' + str(name) + '.png')  # 将图片写入指定的文件夹内



def decode_unigb_utf16_h(data):
    decoded_text = ''
    for i in range(0, len(data), 2):
        char_code = struct.unpack('>H', data[i:i + 2])[0]
        decoded_text += chr(char_code)
    return decoded_text

def split_pdf(input_path, start_page, end_page):
    pdf = PdfReader(input_path)

    # 确保起始页和结束页在有效范围内
    start_page = max(0, start_page - 1)
    end_page = min(end_page, len(pdf.pages))
    for page in range(start_page, end_page):
        output = PdfWriter()
        pagehandle = pdf.pages[page]
        book_code = decode_unigb_utf16_h(pagehandle.extract_text().split('\n')[18].encode())
        output.add_page(pagehandle)
        # 指定拆分后的输出文件名
        output_filename = f"./splitpdf/{book_code}.pdf"

        with open(output_filename, "wb") as output_file:
            output.write(output_file)
        pyMuPDF_fitz(output_filename,'./img',book_code)
        res = ocr_image('./img/'+book_code+'.png')
        print(res)
        shutil.copy(output_filename,'./result/' + '_'.join(res) + '.pdf')
        print(f"拆分成功！已保存为 {output_filename}")


def remove_files_by_folder(folder_path):
    folder_list = list()
    for folder in os.listdir(folder_path):
        if os.path.isdir(folder):
            folder_list.append(folder)
    for file in folder_list:
        rm_path = os.path.join(folder_path, file)
        print(rm_path)
        shutil.rmtree(rm_path)



# 设置文件夹路径、设置需要拆分的页码范围，遍历文件夹下的所有PDF文件
folder_path = "./"
img_path = './img'
split_file_path = './splitpdf'
result = './result'
if __name__ == '__main__':
    remove_files_by_folder(folder_path)
    if not os.path.exists(img_path):
       os.mkdir(img_path)
    if not os.path.exists(split_file_path):
       os.mkdir(split_file_path)
    if not os.path.exists(result):
       os.mkdir(result)
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            split_pdf(pdf_path, 1, 10)  # 提取前3页并保存，范围可修改




