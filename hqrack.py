from subprocess import Popen
from PIL import Image
import pytesseract
import argparse
import cv2
import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from colorama import init, Fore, Back, Style
import re
from threading import Thread



from googleapiclient.discovery import build

init()

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

################ CONFIG 
dirname=dirname = os.path.dirname(__file__)
adb="path to adb"
pytesseract.pytesseract.tesseract_cmd = 'path to tesseract'
service = build("customsearch", "v1",
                developerKey="custom search dev key from google")
cs_cx = "cx value from google for cso"

#Change this to 4 threads speed up request
def backup_definitions_thread(query):
    i = 0
    for choice in query:
        if i > 0:
            res = service.cse().list(
                q=choice,
                cx=cs_cx
            ).execute()
            if 'items' in res:
                uprint(Fore.CYAN + choice + Style.RESET_ALL + Fore.LIGHTGREEN_EX + res['items'][0]['snippet'] + Style.RESET_ALL)
        i = i + 1

        
 #Use adb to capture screen via batch file - when Enter pressed

while True:
    input("Press Enter to capture")
    p = Popen(os.path.join(dirname, 'input/retrieve.bat'))
    stdout, stderr = p.communicate()

    #Open screen.png run tessaract 
    image = cv2.imread("screen.png", 1)
    if not image is None:
        crop_img = image[250:1400, 20:1050]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # Thresholding
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        # BLUR
        #gray = cv2.medianBlur(gray, 3)

        # write the grayscale image to disk as a temporary file so we can
        # apply OCR to it
        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)

        # Extract text via tesseract
        #print(filename)
        text = pytesseract.image_to_string(Image.open(filename))
        text = re.sub(u"(\u2018|\u2019)", "'", text)
        #uprint("HQ Extracted Question: " + text)
        #print(repr(text))
        query = text.split('\n\n')

        thread = Thread(target=backup_definitions_thread, args=(query, ))
        #print(query)

        # Send into google search api - well have to use some real NLP etc. for higher accuracy.
        res = service.cse().list(
            q=query[0],
            cx=cs_cx
        ).execute()

        thread.start()

        # print(res['items'])
        count1 = 0
        count2 = 0
        count3 = 0
        #uprint(res)
        if 'items' in res:
            for snippet in res['items']:
                if (len(query) < 2):
                    query.append("placeholder")
                if (len(query) < 3):
                    query.append("placeholder")
                if (len(query) < 4):
                    query.append("placeholder")

                # check count of occurence against each option
                #count1 = count1 + snippet["snippet"].count(query[1])
                #count2 = count2 + snippet["snippet"].count(query[2])
                #count3 = count3 + snippet["snippet"].count(query[3])
                #extract = snippet["snippet"].encode('utf-8');
                extract = snippet["snippet"]

                #sen_extract = re.compile(re.escape(query[1]), re.IGNORECASE)
                #uprint(extract)
                extract = extract.replace(query[1], Fore.LIGHTRED_EX + query[1]+ Style.RESET_ALL)
                extract = extract.replace(query[1].lower(), Fore.LIGHTRED_EX + query[1].lower()+ Style.RESET_ALL)
                extract = extract.replace(query[2], Fore.YELLOW + query[2]+ Style.RESET_ALL)

                extract = extract.replace(query[2].lower(), Fore.YELLOW + query[2].lower()+ Style.RESET_ALL)

                extract = extract.replace(query[3], Fore.LIGHTGREEN_EX + query[3]+ Style.RESET_ALL)
                extract = extract.replace(query[3].lower(), Fore.LIGHTGREEN_EX + query[3].lower()+ Style.RESET_ALL)


                uprint(extract)
                #uprint('\n')
            #print(count1 + " " + count2 + " " + count3)
            #print(max(count1, count2, count3))
        else:
            uprint('Lookup Failed')

        thread.join()
        os.remove(filename)
