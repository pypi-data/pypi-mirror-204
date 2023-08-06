# imp3 (Image pre-preocessing pipeline) :
Interactive tool for image pre-processing and automated pipeline creation

## Installation
run following command in terminal
```bash
pip install imp3
```

## Usage
```bash
imp3.run
```
- Above command will lauch the app on default port 8501. 
- Open the browser and go to http://localhost:8501
- Select the image and then select the appropriate set of operations you want to perform on that perticular image. 
- play with the parameters interatively untill you reach at optimal configuration.

```bash
imp3.run --port 8080
```
Above command can be used to specify the port on which you want to run the app.

## UI
add video 
![alt text](https://github.com/bokey007/imp3/blob/main/media/demo.gif)

# Following is the list of currently supported operations:

## 0. Resize input image

## 1. map the image to different color spaces
    Folowwing methods are available:
    a. 'rgb'
    b. 'Gray scale'
    c. 'hsv', 
    d. 'lab', 
    e. 'brg', 
    f. 'ch_one',
    g. 'ch_two',
    h. 'ch_three',
    i. 'merge_first_two_ch',
    j. 'merge_last_two_ch', 
    k. 'merge_last_first_ch'

## 2. change the brightness and contrast

## 3. Smoothingth
    Folowwing methods are available:
    a. avg
    b. gaussian
    c. median
    d. bilateral

## 4. intensity histogram and histogram equalization

## 5. thresholding
    Folowwing methods are available:
    a. thresh
    b. adaptive_thresh
    c. otsu

## 6. edge detection
    Folowwing methods are available:
    a. sobel
    b. laplasian
    c. canny


## 7. dialate / erode

## 8. find countours

## 9. shape matching with Hu moment on contour

## 10. feature extraction
    
## 11. Feature Matching

## 12. Template matching and removal
    
Development tools:

1. setuptools (https://pypi.org/project/setuptools/): Used to create a python package
2. pipreqs (https://pypi.org/project/pipreqs/): Used to create requirements.txt file
3. twine (https://pypi.org/project/twine/): Used to upload the package to pypi.org
4. Github Actions (): Used to automate the process of uploading the package to pypi.org
5. pytest (https://pypi.org/project/pytest/): Used to write unit tests
6. wheel (https://pypi.org/project/wheel/): Used to create a wheel file

