# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 10:13:01 2022

@author: bokey

Run command : streamlit run app.py [-- script args]

"""

import streamlit as st
import numpy as np
from PIL import Image
import cv2
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def main():
    st.set_page_config(layout="wide")
    st.title('imp3: Image pre-processing pipeline')
    st.header('Interactive tool for image pre-processing and automated pipeline creation')
    st.sidebar.title('Parameters control panel')
    st.sidebar.markdown("""---""")


    # step 0: Accept image input

    uploaded_file = st.file_uploader("Upload image file")
        
    if uploaded_file is not None:
        # To read file as bytes:
        #step 0 : read the file 
        imput_im = Image.open(uploaded_file)
        imput_im_np = np.array(imput_im.convert('RGB'))
        im = imput_im_np

        #user input to resize the image or not
        # create a hprizontal line
        # Section 0: resize the image
        st.markdown("""---""")
        st.subheader("resize input image")
        resize = st.radio('resize the image?', ['no', 'yes'], horizontal=True,)
        
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            st.image(im)
            st.write("resolution of input image: ", im.shape)
        with col2:
            if resize == "no":
                st.image(im)
                st.write("resolution remains unchanged: ", im.shape) 
            elif resize == "yes":
                
                st.sidebar.subheader("Controls for image resizer")
                #step 1: resize the image
                width = st.sidebar.slider('width', 0, 1000, 500)
                height = st.sidebar.slider('height', 0, 1000, 500)
                st.sidebar.markdown("""---""")
                im = cv2.resize(im, (width, height))
                st.image(im)
                st.write("resolution of resized image: ", im.shape)


        # Section 1: map the image to different color spaces
        st.markdown("""---""")
        st.subheader("map input image to different color spaces")
        #step 1: map the colore spce
        color_space = st.radio('chage to following color space:', ['rgb','Gray scale','hsv', 'lab', 'brg', 'ch_one',
                                                                            'ch_two',
                                                                            'ch_three',
                                                                            'merge_first_two_ch',
                                                                            'merge_last_two_ch', 'merge_last_first_ch'], horizontal=True,)
        col1, col2 = st.columns( [0.5, 0.5])

        with col1:
            st.image(im)
            st.write("resolution of input image: ", im.shape)
        with col2:
            if color_space == "Gray scale":
                im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)
                st.image(im)
                st.write(im.shape)
            elif color_space == "rgb":
                st.image(im)
            elif color_space == "hsv":
                im = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
                st.image(im)
            elif color_space == "lab":
                im = cv2.cvtColor(im, cv2.COLOR_RGB2LAB)
                st.image(im)
            elif color_space == "brg":
                im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
                st.image(im)
            elif color_space == "ch_one":
                im, _, _ = cv2.split(im)
                st.image(im)
            elif color_space == "ch_two":
                _, im, _ = cv2.split(im)
                st.image(im)
            elif color_space == "ch_three":
                _, _, im = cv2.split(im)
                st.image(im)
            elif color_space == "merge_first_two_ch":
                im[:, :, 2] = np.zeros((im.shape[0], im.shape[1]))
                #ch3 = np.zeros(ch3.shape)
                st.write(im.shape)
                #im = cv2.merge([ch1, ch2, ch3])
                st.image(im)
            elif color_space == "merge_last_two_ch":
                im[:, :, 0] = np.zeros((im.shape[0], im.shape[1]))
                #im = cv2.merge([ch2, ch3])
                st.image(im)
            elif color_space == "merge_last_first_ch":
                im[:, :, 1] = np.zeros((im.shape[0], im.shape[1]))
                #im = cv2.merge([ch1, ch3])
                st.image(im)

        # Section 3: Smoothing
        st.markdown("""---""")
        st.subheader("smooting")
        blur_method = st.radio('chage to following color space:', ['None','Averaging', 'Gaussian', 
                                                                    'Median', 'Bilateral'], horizontal=True,)
        col3, col4 = st.columns( [0.5, 0.5])

        with col3:
            st.image(im)
            #width, height = imput_im.size
            st.write("current state of the image")
        with col4:
            if color_space == "None":
                pass
            elif blur_method == "Averaging":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Averaging smooting")
                filter_ = st.sidebar.slider('Adjust the filter size', min_value=1, max_value=11, value=5, step=2)
                im = cv2.blur(im,(filter_,filter_))
                st.image(im)
            elif blur_method == "Gaussian":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Gaussian smooting")
                filter_ = st.sidebar.slider('Adjust the filter size', min_value=1, max_value=11, value=7, step=2)
                im = cv2.GaussianBlur(im,(filter_,filter_),0)
                st.image(im)
            elif blur_method == "Median":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Median smooting")
                filter_ = st.sidebar.slider('Adjust the filter size', min_value=1, max_value=11, value=5, step=2)
                im = cv2.medianBlur(im,filter_)
                st.image(im)
            elif blur_method == "Bilateral":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Bilateral smooting")
                sigma_color = st.sidebar.slider('Adjust para 1 (sigma color)', min_value=1, max_value=11, value=9, step=1)
                sigma_space = st.sidebar.slider('Adjust para 2 (sigma space)', min_value=1, max_value=150, value=75, step=1)
                im = cv2.bilateralFilter(im,sigma_color,sigma_space,sigma_space)
                st.image(im)
        
        # Section 2: change the brightness and contrast
        st.markdown("""---""")
        st.subheader("Brightness and contrast")
        st.sidebar.subheader("Controls for Brightness and contrast")
        #step 2: change the brightness and contrast
        col1, col2 = st.columns( [0.5, 0.5])
        with col1:
            st.image(im)
            st.write("current state of the image")
        with col2:
            st.sidebar.markdown("""---""")
            brightness = st.sidebar.slider('brightness', -100, 100, 0)
            contrast = st.sidebar.slider('contrast', -100, 100, 0)
            im = cv2.addWeighted(im, 1 + contrast/100., im, 0, brightness)
            st.image(im)
            st.write("Output image after brightness and contrast adjustment")

        # Section 4: intensity histogram and histogram equalization
        st.markdown("""---""")
        st.subheader("Histogram")
        
        hist_radio = st.radio('Compute Histogram:', ['None','Histogram', 'Simple Histigram_equilisation (NEED GRAY SCALE AS INPUT)', 'Adaptive Histogram Equalization (CLAHE) (NEED GRAY SCALE AS INPUT)'], horizontal=True,)

        col11, col12 = st.columns( [0.5, 0.5])

        with col11:
            st.image(im)
            #width, height = imput_im.size
            st.write("current state of the image")
        with col12:
            if hist_radio == "None":
                pass
            elif hist_radio == "Histogram":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Histigram")
                if len(im.shape) == 2:
                    histogram= cv2.calcHist([im], [0], None, [256], [0, 256])
                    plt.figure(1)
                    plt.title("Histogram of input One chaneel image") 
                    plt.xlabel('Bins')
                    plt.ylabel('Number of pixels')
                    plt.xlim([0, 256])
                    plt.plot(histogram)
                    st.pyplot(plt.figure(1))
                else:
                    plt.figure(1)
                    plt.title("Histogram of input 3 channel image") 
                    plt.xlabel('Bins')
                    plt.ylabel('Number of pixels')
                    colors = ("b", "g", "r")
                    
                    for i, col in enumerate(colors):
                            hist = cv2.calcHist([im], [i], None, [256], [0, 256])
                            plt.plot(hist, color=col)
                            plt.xlim([0, 256])

                    st.pyplot(plt.figure(1))
            elif hist_radio == "Simple Histigram_equilisation (NEED GRAY SCALE AS INPUT)":
                st.sidebar.markdown("""---""")
                # code for histogram equalization
                im = cv2.equalizeHist(im)
                st.image(im)
            elif hist_radio == "Adaptive Histogram Equalization (CLAHE) (NEED GRAY SCALE AS INPUT)":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Histigram_equilisation")
                # User input for CLAHE
                clipLimit = st.sidebar.slider('Adjust the clip limit', min_value=1, max_value=10, value=2, step=1)
                tileGridSize = st.sidebar.slider('Adjust the tile grid size', min_value=1, max_value=10, value=8, step=1)
                # code for histogram equalization using CLAHE
                clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(tileGridSize,tileGridSize))
                im = clahe.apply(im)
                st.image(im)

        # Section 5: thresholding
        st.markdown("""---""")
        st.subheader("thresholding")
        st.sidebar.subheader("Controls for thresholding")
        thresh_method = st.radio('chage to following color space:', ['None','Thresholding', 'Adaptive thresholding', 
                                                                    'Otsu thresholding', ''], horizontal=True,)

        col13, col14 = st.columns( [0.5, 0.5])

        with col13:
            st.image(im)
            #width, height = imput_im.size
            st.write("current state of the image")
        with col14:
            if thresh_method == "None":
                pass
            elif thresh_method == "Thresholding":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Thresholding")
                threshold = st.sidebar.slider('Adjust the thresdhold. Anything greater (re lesser than in case of INV) than this value will be set to white (255)', min_value=0, max_value=255, value=150, step=1)
                thresh_type = st.radio('Specify thresholding type:', ['Binary', 'Binary Inverse'], horizontal=True,)
                if thresh_type == "Binary":
                    thresh_type_cv = cv2.THRESH_BINARY
                elif thresh_type == "Binary Inverse":
                    thresh_type_cv = cv2.THRESH_BINARY_INV
                _, im = cv2.threshold(im, threshold, 255, thresh_type_cv)
                st.image(im)
            elif thresh_method == "Adaptive thresholding":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Adaptive thresholding")
                kernel_ada_thre = st.sidebar.slider('Adjust the block size', min_value=1, max_value=50, value=11, step=2)
                val_ada_thre = st.sidebar.slider('C Value', min_value=1, max_value=50, value=9, step=1)
                thresh_type = st.radio('Specify thresholding type:', ['Binary', 'Binary Inverse'], horizontal=True,)
                adaptive_startegy = st.radio('Specify adaptive strategy:', ['mean', 'gaussian', 'calib cb'], horizontal=True,)
                if thresh_type == "Binary":
                    thresh_type_cv = cv2.THRESH_BINARY
                elif thresh_type == "Binary Inverse":
                    thresh_type_cv = cv2.THRESH_BINARY_INV

                if adaptive_startegy == "mean":
                    adaptive_startegy_cv = cv2.ADAPTIVE_THRESH_MEAN_C
                elif adaptive_startegy == "std":
                    adaptive_startegy_cv = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
                elif adaptive_startegy == "calib cb":
                    adaptive_startegy_cv = cv2.CALIB_CB_ADAPTIVE_THRESH
                im = cv2.adaptiveThreshold(im, 255, adaptive_startegy_cv, thresh_type_cv, kernel_ada_thre, val_ada_thre)
                st.image(im)
            elif thresh_method == "Otsu thresholding":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Otsu thresholding")
                ret, im = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + 
                                                cv2.THRESH_OTSU)   
                st.image(im)
                st.write("Otsu threshold is :", ret)
                
        # Section 6: edge detection
        st.markdown("""---""")
        st.subheader("canny")
        edge_option = st.radio('Edge detection:', ['None', 'Sobel','Lanlasian', 'Canny'], horizontal=True,)
        col5, col6 = st.columns( [0.5, 0.5])

        with col5:
            st.image(im)
            #width, height = imput_im.size
            st.write("current state of the image")
        with col6:
            if edge_option == "None":
                pass
            elif edge_option == "Sobel":
                sobelx = cv2.Sobel(im, cv2.CV_64F, 1, 0)
                sobely = cv2.Sobel(im, cv2.CV_64F, 0, 1)
                im = cv2.bitwise_or(sobelx, sobely)
                st.image(im)
            elif edge_option == "Lanlasian":
                im = cv2.Laplacian(im, cv2.CV_64F)
                im = np.unit8(np.absolute(lap))
                st.image(im)
            elif edge_option == "Canny":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for canny")
                slider3 = st.sidebar.slider('Adjust minVal', min_value=0, max_value=255, value=150, step=1)
                slider4 = st.sidebar.slider('Adjust maxVal', min_value=0, max_value=255, value=255, step=1)
                im = cv2.Canny(im, slider3, slider4)
                st.image(im)
        
        # Section 7: dialate/erode
        st.markdown("""---""")
        st.subheader("Dialate/Erode")
        dia_ero_option = st.radio('Operations o0n the detected edges:', ['None', 'Dialate','Erode'], horizontal=True,)

        col7, col8 = st.columns( [0.5, 0.5])

        with col7:
            st.image(im)
            #width, height = imput_im.size
            st.write("current state of the image")
        with col8:
            if dia_ero_option == "None":
                pass
            elif dia_ero_option == "Dialate":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Dialate")
                kernel_side = st.sidebar.slider('kernel size', min_value=1, max_value=11, value=5, step=2)
                iterations = st.sidebar.slider('iterations', min_value=1, max_value=11, value=1, step=1)
                kernel = np.ones((kernel_side, kernel_side))
                im = cv2.dilate(im, kernel, iterations)
                st.image(im)
            elif dia_ero_option == "Erode":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for Erode")
                slider5 = st.sidebar.slider('Adjust the filter size', min_value=1, max_value=11, value=7, step=2)
                im = cv2.GaussianBlur(im,(slider,slider),0)
                st.image(im)

        # Section 8: find contours
        st.markdown("""---""")
        st.subheader("find countours")
        contour_option = st.radio('Operations o0n the detected edges:', ['None','Detect contours'], horizontal=True,)

        col9, col10 = st.columns( [0.5, 0.5])

        with col9:
            st.image(im)
            #width, height = imput_im.size
            st.write("current state of the image")
        with col10:
            if contour_option == "None":
                pass
            elif contour_option == "Detect contours":
                st.sidebar.markdown("""---""")
                st.sidebar.subheader("Controls for contour detection")
                img_cont = imput_im_np.copy()
                ret_method_op = st.sidebar.radio('Option retrival method', ['RETR_EXTERNAL','RETR_TREE', 'RETR_LIST', 'RETR_CCOMP',], horizontal=True,)
                approx_method_op = st.sidebar.radio('Option approximation method', ['CHAIN_APPROX_NONE', 'CHAIN_APPROX_SIMPLE'], horizontal=True,)
                filter_area = st.sidebar.radio('Filter contours based on area', ['Yes', 'No'], horizontal=True,)
                filter_peri = st.sidebar.radio('Filter contours based on peri', ['Yes', 'No'], horizontal=True,)
                if filter_area == "Yes":
                    slider6 = st.sidebar.slider('Display contours within this area:', min_value=1, max_value=20000, value=(1000, 2000), step=100)
                if filter_peri == "Yes":   
                    slider7 = st.sidebar.slider('Display Conours within this perimeter:', min_value=1, max_value=10000, value=(1000, 2000), step=100)
                
                if ret_method_op == "RETR_EXTERNAL":
                    ret_method = cv2.RETR_EXTERNAL
                elif ret_method_op =="RETR_TREE":
                    ret_method = cv2.RETR_TREE
                elif ret_method_op =="RETR_LIST":
                    ret_method = cv2.RETR_LIST
                elif ret_method_op =="RETR_CCOMP":
                    ret_method = cv2.RETR_CCOMP


                if approx_method_op == "CHAIN_APPROX_NONE":
                    approx_method = cv2.CHAIN_APPROX_NONE
                elif approx_method_op == "CHAIN_APPROX_SIMPLE":
                    approx_method = cv2.CHAIN_APPROX_SIMPLE
                contours, hierarchy = cv2.findContours(im, ret_method, approx_method)
                for i, cnt in enumerate(contours):
                    area = cv2.contourArea(cnt)
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.2 * peri, True)
                    if filter_area == "Yes":
                        if slider6[0] <=area <= slider6[1]:
                            cv2.drawContours(img_cont, cnt, -1, (255, 0, 255), 7)
                        
                    elif filter_peri == "Yes":
                        if slider7[0] <= peri <= slider7[1]:
                            cv2.drawContours(img_cont, cnt, -1, (255, 0, 255), 7)
                    else:
                        cv2.drawContours(img_cont, cnt, -1, (255, 0, 255), 7)
                    st.sidebar.write("*************************contour detected", i, "******************************")
                    st.sidebar.write("Number for vetices in this contour is:", len(approx))
                    st.sidebar.write("area is:", area)
                    st.sidebar.write("perimeter is:", peri)

                    
                st.image(img_cont)
        
        # Section 9: shape matching with Hu moment on contour
        st.markdown("""---""")
        st.subheader("shape matching with Hu moment on contour")
        # Section 10: feature extraction
        st.markdown("""---""")
        st.subheader("Feature extraction")
        st.markdown("""---""")
        # Section 11: feature matching
        st.subheader("Feature Matching")
        st.markdown("""---""")
        # Section 12: template matching and removal
        st.subheader("Template matching and removal, expecting gray image as imput template image can be color or gray")
        
        template_option = st.radio('options for template detection:', ['None','template matching'], horizontal=True,)

        col15, col16 = st.columns( [0.5, 0.5])

        with col15:
            st.image(im)
            #width, height = imput_im.size
            st.write("current state of the image")
        with col16:
            if template_option == "None":
                pass
            elif template_option == "template matching":
                uploaded_template_file = st.file_uploader("Upload template image file")
                if uploaded_template_file is not None:
                    # To read file as bytes:
                    #step 0 : read the file 
                    imput_template_im = Image.open(uploaded_template_file)
                    imput_template_im_np = np.array(imput_template_im.convert('RGB'))
                    imput_template_im_gray = cv2.cvtColor(imput_template_im_np, cv2.COLOR_RGB2GRAY)
                    st.image(imput_template_im_gray)
                    h, w = imput_template_im_gray.shape
                    comparison_method = st.sidebar.radio('Choose coparison method:', ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                                                                                        'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 
                                                                                        'cv2.TM_SQDIFF_NORMED'], horizontal=True,)
                    if comparison_method == "cv2.TM_CCOEFF":
                        comparison_method_val = cv2.TM_CCOEFF
                    elif comparison_method == "cv2.TM_CCOEFF_NORMED":
                        comparison_method_val = cv2.TM_CCOEFF_NORMED
                    elif comparison_method == "cv2.TM_CCORR":
                        comparison_method_val = cv2.TM_CCORR
                    elif comparison_method == "cv2.TM_CCORR_NORMED":
                        comparison_method_val = cv2.TM_CCORR_NORMED
                    elif comparison_method == "cv2.TM_SQDIFF":
                        comparison_method_val = cv2.TM_SQDIFF
                    elif comparison_method == "cv2.TM_SQDIFF_NORMED":
                        comparison_method_val = cv2.TM_SQDIFF_NORMED

                    compa_threshold = st.sidebar.slider('specify comparison threshold', min_value=0.0, max_value=1.0, value=0.8, step=0.0001)
                    res = cv2.matchTemplate(im, imput_template_im_gray, comparison_method_val)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                    if comparison_method_val in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                        location = min_loc
                        loc = np.where( res <= compa_threshold)
                        print("considering min val")
                        print(compa_threshold)
                    else:
                        location = max_loc
                        loc = np.where( res >= compa_threshold)
                        print("considering max val")
                        print(compa_threshold)

                    bottom_right = (location[0] + w, location[1] + h)
                    cv2.rectangle(im, location, bottom_right, 0, 6)
                    
                    for pt in zip(*loc[::-1]):
                        cv2.rectangle(im, pt, (pt[0] + w, pt[1] + h), 200, 2)
                    st.image(im)
        st.markdown("""---""")
        st.subheader("Shape detection with Hough Transform")
        st.markdown("""---""")
        st.subheader("Backgroud removal with the current best of deep learning")             

# call main fuction
if __name__=="__main__":
    main() 



