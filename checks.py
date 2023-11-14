import streamlit as st
import easyocr
import cv2
import re
from matplotlib import pyplot as plt
import numpy as np

from flair.data import Sentence
from flair.models import SequenceTagger

import sys
sys.path.append("darknet")
import detector

typesOfInfo = []
class CreditCard:
    def isValid(num):
        
        sum = CreditCard.doubleAndAdd(num) + CreditCard.addOdd(num)
        if(sum%10==0) and (CreditCard.size(num)>=13 and CreditCard.size(num)<=16) and CreditCard.prefix(num):
            return num
        else: return None
    
    def prefix(num):
        num=str(num)
        if(num[0]=='4' or num[0]=='5' or num[0]=='6' or num[0:2]=='37'):
            return True
        else: return False

    def size(num):
        num = str(num)
        return len(num)
    
    def doubleAndAdd(num):
        num = str(num)
        sum = 0
        if(CreditCard.size(num)%2==0): i = 0
        else: i = 1
        while(i<len(num)):
            sum+=CreditCard.digit(int(num[i])*2)
            i+=2
        return sum

    def digit(num):
        num=int(num)
        if(num//10==0):
            return num
        else:
            num = str(num)
            sum = 0
            sum+=int(num[0]) + int(num[1])
            return sum
    
    def addOdd(num):
        num = str(num)
        sum = 0
        if(CreditCard.size(num)%2==0): i = 1
        else: i = 0
        while(i<len(num)):
            sum+=int(num[i])
            i+=2
        return sum

def name_check(text):
    tagger = SequenceTagger.load('ner')
    sentence = Sentence(text)
    tagger.predict(sentence)
    #print(sentence.to_tagged_string())
    dets = []
    if(sentence.labels):
        for i in sentence.labels:
            if(i.score>0.5):
                print(i.unlabeled_identifier.split('"')[1])
                dets.append(i.unlabeled_identifier.split('"')[1])
    dets = [i for i in dets if i is not None]
    if(dets) and ("Names" not in typesOfInfo): typesOfInfo.append("Names")
    return dets
    #print(sentence.labels[0].unlabeled_identifier.split('"'))

def address_check(text):
    addressmodel = SequenceTagger.load('./names/best-model.pt')
    sentence = Sentence(text)
    addressmodel.predict(sentence)
    #print(text)
    #print(sentence)
    dets = []
    for i in sentence.labels:
        if (i.score > 0.6) and (i.value != 'Building_Number'):
            #print(i.unlabeled_identifier.split('"')[1])
            dets.append(i.unlabeled_identifier.split('"')[1])
    dets = [i for i in dets if i is not None]
    #print(dets)
    if(dets) and ("Address" not in typesOfInfo): typesOfInfo.append("Address")
    return dets

def darknet_detector(img):
    darknet_coords, darknet_classes= detector.License_test(img)
    for i in darknet_classes:
        if 'Vehicle Registration Number' not in typesOfInfo: typesOfInfo.append('Vehicle Registration Number')
    return darknet_coords

def Phone_test(text):
    bigList = re.findall(r"((?<!\d)(?<!\d)(\+91)?[ -]?\d\d\d[ -]?\d\d[ -]?\d[ -]?\d\d\d\d(?!\d))",text)
    r"((?<!\d)(?<!\d)(\+91)?[ -]?\d\d\d[ -]?\d\d[ -]?\d[ -]?\d\d\d\d(?!\d))"
    smallList = [i[0] for i in bigList]
    if(smallList) and ("Phone Number" not in typesOfInfo): typesOfInfo.append("Phone Number")
    return smallList

def Landline_test(text):
    bigList = re.findall(r"((?<!\d)\d\d\d[ -]?\d\d\d\d[ -]?\d\d\d\d(?!\d))",text)
    smallList = [i[0] for i in bigList]
    if(smallList) and ("Landline Number" not in typesOfInfo): typesOfInfo.append("Landline Number")
    return smallList
  
def Pan_test(text):
    bigList = re.findall(r"[A-Z]{5}\d{4}[A-Z]",text)
    smallList = [i[0] for i in bigList]
    if(smallList) and ("PAN Number" not in typesOfInfo): typesOfInfo.append("PAN Number")
    return smallList

def IP_test(text):
    bigList = re.findall(r"((?<!\d)(?!10\.)(?!192\.168\.)(?!172\.(1[6-9]|2[0-9]|3[0-1])\.)(([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])(?!\d))",text)
    smallList = [i[0] for i in bigList]
    if(smallList) and ("IP Address" not in typesOfInfo): typesOfInfo.append("IP Address")
    return smallList

def Aadhar_test(text):
    bigList = re.findall(r"((\d\d\d\d[ ]?\d\d\d\d[ ]?\d\d\d\d(?!\d)))",text)
    smallList = [i[0] for i in bigList]
    if(smallList) and ("Aadhar Number" not in typesOfInfo): typesOfInfo.append("Aadhar Number")
    return smallList

def License_test(text):
    bigList = re.findall(r"(((AP|AR|AS|BR|CG|DL|GA|GJ|HR|HP|JK|JH|KA|KL|LD|MP|MH|ML|MZ|NL|OD|OR|PY|PB|RJ|SK|TN|TS|TR|UP|UK|UA|WB|AN|CH|DN|DD|LA|OT) ?\d\d ?\w\w ?\d\d\d\d))",text)
    smallList = [i[0] for i in bigList]
    print(smallList)
    if(smallList) and ("Vehicle Registration Number" not in typesOfInfo): typesOfInfo.append("Vehicle Registration Number")
    return smallList

def CC_test(text):
    bigList1 = re.findall(r"[Vv][Ii][Ss][Aa]",text)
    bigList2 = re.findall(r"\d\d/\d\d",text)
    bigList3 = re.findall(r"[Mm][Aa][Ss][Tt][Ee][Rr] ?[Cc][aA][rR][dD]",text)

    ccResult = []
    if(not (bigList1 or bigList2 or bigList3)):
        ccList = text.split()
        for i in ccList:
            i = i.replace("-","")
            i = i.replace(" ","")
            if i.isdigit():
                ccResult.append(CreditCard.isValid(i))

    hugeList = bigList1 + bigList2 + bigList3 + ccResult
    #print(hugeList)
    hugeList = [i for i in hugeList if i is not None]
    #print("===============================================================================================================")
    if(hugeList) and ("Credit Card Number" not in typesOfInfo): typesOfInfo.append("Credit Card Number")
    return hugeList

def main_check(text,img):
    
    flagList = []
    flagList = name_check(text) + address_check(text) + Phone_test(text) + IP_test(text) + License_test(text) + CC_test(text)
    darknetCoords = darknet_detector(img)
    flagList = [i for i in flagList if i is not None]
    print(flagList)
    return flagList,darknetCoords, typesOfInfo