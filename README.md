# HQrack
A PoC application of demonstrating use of OCR to beat popular trivia app HQ

## Disclaimer
This application is intended for learning purposes only! Cheating is against the terms and policy of HQ Trivia, its also a rotten thing to do. No liability will be held as a result of misuse of this application. 

## Usage
Most of the HQ answers can be solved with a trivial google search, the trick is to get that answer and input the selection within the 10 second window.

This solution uses google tesseract for optical character recognition (OCR) and a series of steps to optimize the time it takes for the user to make an answer choice. This is built for android and screen input is taken by adb.  

Requires python 3.x 
Requires android phone + adb
Requires tesseract 

You will need to get your own google search engine keys to use, config variables need to be set before using.


## Notes

Code may need to be modifies if HQ updates their interface (i.e. may need to change ocr approach) (see test folder for sample images of what will work)

I just wanted to see if it was possible and will not continue to support further iterations. 


