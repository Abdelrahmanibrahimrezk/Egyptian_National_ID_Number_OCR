# -*- coding: utf-8 -*-
"""Egypt_ID_OCR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lgqjd9Lgsy4BvYRBOGriWCVKoQBCefVg
"""

import argparse
from matplotlib import pyplot
import pytesseract
from tkinter import *
# from PIL import ImageTk,Image
import cv2
import numpy as np
import argparse
import imutils
from pytesseract import Output
import cv2 
import numpy as np
from PIL import ImageFont, ImageDraw, Image


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, help="Image's input path")
args = vars(ap.parse_args())
# print(args["input"])
def gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

def threshold_ara_num(img):
    th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)#292 041802 00995 94 754 2758446 47
    return img

def threshold_word(img):
    th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)#292 041802 00995 94 754 2758446 47
    return img

def resize_ara_num(img):
    #scale_percent = 50  # percent of original size
    width = 712
    height = 512
    dim = (width, height)
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img
def threshold_eng_num(img):
    th, img = cv2.threshold(img, 100, 255, cv2.THRESH_TRUNC)#292 041802 00995 94 754 2758446 47
    return img
def increase_contrast(img):
    # -----Converting image to LAB Color model-----------------------------------
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    #cv2.imshow("lab", lab)

    # -----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    #cv2.imshow('l_channel', l)
    #cv2.imshow('a_channel', a)
    #cv2.imshow('b_channel', b)

    # -----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    #cv2.imshow('CLAHE output', cl)

    # -----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl, a, b))
    #cv2.imshow('limg', limg)

    # -----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    #cv2.imshow('final', final)
    return final

def extract_ara_num(img):
    #num=3

    # focus on the number section
    #img = cv2.imread("test/7.jpg")
    original = resize_ara_num(img)
    img = resize_ara_num(img)
    h,w,ch=img.shape
    img = img[int(h/1.8):int(h/1.08), int(w/2.8):int(w/1)]
    copy=img


    
    ##############################

    count = 0
    # in the loop untill reading the number
    while (True):
        count = count + 1
        #cv2.imshow('image0', img)
        #cv2.waitKey(0)

        img = gray(img)
        #img = gaussian_blur(img)
        #img=remove_noise(img)
        #img=canny(img)
        img = threshold_eng_num(img)

        # img= remove_noise(img)

        #cv2.imwrite("test_croped/"+str(7)+".jpg", img)

        #cv2.imshow("img", img)
        #cv2.waitKey(0)

        res = pytesseract.image_to_string(img, lang="arabic_numbers").split()
        
        #print(res)
        if res != []:
            for i in res:
                if len(i) > 13 and len(i) < 15:
                    # d = pytesseract.image_to_data(img, output_type=Output.DICT)
                    # n_boxes = len(d['level'])
                    # for i in range(n_boxes):
                        # (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                    cv2.rectangle(original, (int(w/2.3), int(h/1.5)), (int(w/1.009),int(h/1.08)), (0, 255, 0), 2)

                    fontpath = "arial.ttf" # <== download font
                    font = ImageFont.truetype(fontpath, 32)
                    img_pil = Image.fromarray(original)
                    draw = ImageDraw.Draw(img_pil)
                    draw.text((int(w/2.3), int(h/1.5)),i[::-1], font = font,fill=(255, 255, 255, 128))
                    original = np.array(img_pil)

                    # cv2.putText(original, reshaped_text, (int(w/2.3), int(h/1.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    cv2.imwrite('out.png', original)
                    return i

        f_res=""
        for i in range(1,len(res)+1):
            if i >1:
                temp=res[len(res) - i]
                temp+=f_res
                f_res = temp
            else:
                f_res+= res[len(res) - i]

            if len(f_res)==14:
                cv2.rectangle(original, (int(w/2.3), int(h/1.5)), (int(w/1.009),int(h/1.08)), (0, 255, 0), 2)
                fontpath = "arial.ttf" # <== download font
                font = ImageFont.truetype(fontpath, 32)
                img_pil = Image.fromarray(original)
                draw = ImageDraw.Draw(img_pil)
                draw.text((int(w/2.3), int(h/1.5)),f_res[::-1], font = font,fill=(255, 255, 255, 128))
                original = np.array(img_pil)
                # cv2.putText(original, reshaped_text, (int(w/2.3), int(h/1.5)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2,)
                cv2.imwrite('out.png', original)
                return f_res


        img = increase_contrast(copy)
        if count > 1:
            img = increase_contrast(img)

           
        if count == 3:
            return "please re-capture the image"
        continue
#open text file
img=cv2.imread(args['input'])
ara_num_res=extract_ara_num(img)
print(ara_num_res[::-1])
text_file = open("output.txt", "w",encoding='utf-8')
 
#write string to file
text_file.write(ara_num_res[::-1])
 
#close file
text_file.close()