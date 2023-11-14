import checks
import ocr
import cv2
import numpy as np
import streamlit as st
import imgedit
import time

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

file = st.file_uploader("Input image here:", type = ['png','jpg','jpeg'])

if file:
    st.markdown('''
        <style>
            .uploadedFile {display: none}
        <style>''',
        unsafe_allow_html=True)
    
    img = cv2.imdecode(np.fromstring(file.read(), np.uint8), 1)
    with st.spinner("Processing..."):
        start = time.time()
        text,ocrResults = ocr.Read_Image(img)
        flagsList,darknetCoords,info = checks.main_check(text,img)
        coordList = ocr.get_coords(flagsList,ocrResults)

        blurImg = imgedit.blur_image(img,coordList,darknetCoords)
        blurImg = cv2.cvtColor(blurImg,cv2.COLOR_BGR2RGB)
        
        imgedit.highlight_flags(img,coordList,darknetCoords)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        end = time.time()
    
    print((end-start)," s")
    st.image(img)
    st.image(blurImg)
    img = None
    blurImg = None