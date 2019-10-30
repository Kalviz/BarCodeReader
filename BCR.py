import os.path
import pdf2image
from PIL import Image
import time

from PyPDF2 import PdfFileReader, PdfFileWriter
import os.path
from pyzbar import pyzbar
import argparse
import cv2

import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')

#newpath = r'C:\Program Files\arbitrary' 


#DECLARE CONSTANTS
PDF_PATH = "test.pdf"
DPI = 200
OUTPUT_FOLDER = None
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'jpg'
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False
outdirName = 'output/'
scanneddirName = 'scanned/'
indirName = 'input/'
tempdirName = 'temp/'

if not os.path.exists(indirName):
    os.makedirs(indirName)
if not os.path.exists(outdirName):
    os.makedirs(outdirName)
if not os.path.exists(tempdirName):
    os.makedirs(tempdirName)    

def split(path, name_of_split):
    pdf = PdfFileReader(path)
    out_path = 'output/'
    #print('inside split')
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output = os.path.join(out_path,f'{name_of_split}{page}.pdf')
        with open(output, 'wb') as output_pdf:
            pdf_writer.write(output_pdf)


def pdftopil(PDF_PATH):   
    start_time = time.time()
    pil_images = pdf2image.convert_from_path(PDF_PATH, dpi=DPI, output_folder='temp', first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD, use_cropbox=USE_CROPBOX, strict=STRICT)
    print ("Time taken : " + str(time.time() - start_time))
    return pil_images

def save_images(pil_images,lf):
    #This method helps in converting the images in PIL Image file format to the required image format
    index = 1
    text = ''
    for image in pil_images:
        filename = lf.replace("pdf", "jpg")
        image.save(os.path.join(indirName,lf.replace("pdf", "jpg")))
        index += 1
        image = cv2.imread(os.path.join(indirName,lf.replace("pdf", "jpg")))
        #print(filename)
        
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:            
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            print('barcodeData :'+barcodeData)
            #text = "{} ({})".format(barcodeData,barcodeType)
            text = barcodeData
            
        
        if text!='':
            os.rename(os.path.join(outdirName,lf),os.path.join(outdirName,text+'.pdf'))
        else:
            print('text empty')
            os.rename(os.path.join(outdirName,lf),os.path.join(outdirName,'Error_'+lf))


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path        
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = '2'
        else:
            allFiles.append(entry)
                
    return allFiles

if __name__ == '__main__':    
    pdffiles = getListOfFiles(scanneddirName)
    for pdf in pdffiles:
        path = 'test.pdf'
        split(os.path.join(scanneddirName,pdf), pdf)        
    
    listOfFiles = getListOfFiles(outdirName)        
    for lf in listOfFiles:
        #os.rename(os.path.join('input/',lf),os.path.join('input.',str(x)+'.pdf'))
        pil_images = pdftopil(os.path.join(outdirName,lf))
        save_images(pil_images,lf)
    #pil_images = pdftopil()
    #save_images(pil_images)

