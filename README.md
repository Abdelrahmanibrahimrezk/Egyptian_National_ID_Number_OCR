# Egyptian National ID_Number OCR

## About
One of the most challenger tasks is to detect Arabic numbers. Here we will detect the Egyptian National ID numbers.
Here you will fined my pre trained mode arabic_numbers.traineddata, It's trained on Egyptian national id's numbers. 
You need to add the trained model in tessdata and install the requirments.
![out](https://user-images.githubusercontent.com/89320483/187497213-846ff1f5-6e5f-496d-9b0c-a8bf48b0b6d8.png)


## Installation on Colab
Install using `pip`

Installing pytesseract:
``` bash
pip install pytesseract
```
Installing tesseract-ocr:
``` bash
!sudo apt-get install tesseract-ocr
```
Moving the trained model to tessdata:
``` bash
!mv /content/arabic_numbers.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
```

## Run
``` bash
!python egypt_id_ocr.py --input /content/ID_2.jfif
```
