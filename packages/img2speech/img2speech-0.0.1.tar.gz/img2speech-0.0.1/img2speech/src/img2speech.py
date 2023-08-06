from gtts import gTTS
import easyocr
import cv2
import numpy as np
import os
import warnings
from langdetect import detect
import pypdfium2 as pdfium
import urllib.request

warnings.filterwarnings("ignore")

lang_dict = {"ENGLISH": "en", "HINDI": "hi", "TELUGU": "te", "KANNADA": "kn"}


def preprocess(path_to_image):
    img = cv2.imread(path_to_image)
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rgb_planes = cv2.split(img)
    result_planes = []

    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    img = cv2.merge(result_planes)

    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)  # increases the white region in the image
    img = cv2.erode(img, kernel, iterations=1)  # erodes away the boundaries of foreground object

    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    im_format = (os.path.splitext(path_to_image)[1])
    cv2.imwrite("output" + im_format, img)
    return img


def image_to_sound(path_to_image, lang, pre_process="NO"):
    try:

        if path_to_image[:4] == "http":
            dir_path = os.getcwd()
            urllib.request.urlretrieve(path_to_image, os.path.join(dir_path, 'output.jpg'))
            path_to_image = os.path.join(dir_path, 'output.jpg')

        if path_to_image[-3:] == "pdf":

            dir_path = os.getcwd()
            filepath = path_to_image
            pdf = pdfium.PdfDocument(filepath)
            page = pdf[0]
            pil_image = page.render(scale=2).to_pil()
            pil_image.save(os.path.join(dir_path, 'output.jpg'))
            pil_image.close()
            path_to_image = os.path.join(dir_path, 'output.jpg')

        if pre_process == "YES":
            print("Internal Image processing in progress.........")
            image = preprocess(path_to_image)
            print("Internal Image Pre-processing done.")

        if lang == "ENGLISH":
            print("Image processing in progress..........")
            reader = easyocr.Reader(['en'])  # this needs to run only once to load the model
            if pre_process == "YES":
                result = reader.readtext(image, detail=0, paragraph=True, batch_size=4,
                                         rotation_info=[90, 180, 270])

            else:
                result = reader.readtext(path_to_image, detail=0, paragraph=True, batch_size=4,
                                         rotation_info=[90, 180, 270])

            text = ""
            for words in result:
                text += words
                text += '\n'

            print("Image to text conversion done.")

            if detect(text) != lang_dict[lang]:
                print("The Language chosen and Language in the image do not match!")
                return
            # print(text)
            print("Converting to speech..........")



        elif lang == "HINDI" or lang == "KANNADA" or lang == "TELUGU":
            print("Image processing in progress...........")
            reader = easyocr.Reader(['en', lang_dict[lang]])
            if pre_process == "YES":
                result = reader.readtext(image, detail=0, paragraph=True, batch_size=4,
                                         rotation_info=[90, 180, 270])

            else:
                result = reader.readtext(path_to_image, detail=0, paragraph=True, batch_size=4,
                                         rotation_info=[90, 180, 270])

            text = ""
            for words in result:
                text += words
                text += '\n'

            print("Image to text conversion done.")
            if detect(text) != lang_dict[lang]:
                print("The Language chosen and Language in the image do not match!")
                return

            # print(text)
            print("Converting to speech.........")

        sound = gTTS(text, lang=lang_dict[lang])
        print("The audio file has been generated.")
        return text, sound


    except Exception as bug:
        print("The image is either empty or an invalid language is selected. Try again!")
        print(bug)
        return

