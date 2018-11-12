import cv2
import os
import numpy as np
import time
from os import listdir
from os.path import isfile, join
start_t = time.time()
FOL = './Dataset'
FOLDER = './types/type 2'
destinationName = "pre-procesessed img"
directory_list = list()
for root, dirs, files in os.walk(FOL, topdown=False):
    for name in dirs:
        directory_list.append(os.path.join(root, name))
new_directory_list = []


for i in range(len(directory_list)):
    folders = directory_list[i]
    name_folder = folders.find('/')
    names = str(folders[name_folder+9:name_folder+13])
    new_directory_list.append(FOL+'/'+names+"/")
   # print(new_directory_list[i])
with open('dataset.txt','w') as f:
    for item in new_directory_list:
        f.write('%s\n' % item)
file_names = [f for f in listdir(FOLDER) if isfile(join(FOLDER, f))]
print(len(file_names))
destination_plate_raw = os.path.join(FOLDER, destinationName)
hey = os.mkdir(destination_plate_raw)
for i in range(len(file_names)):
    ind = file_names[i]
    print(file_names[i])
    name = ind.find('_')
    wait = str(ind[name+1:name+11])
    img = cv2.imread(FOLDER + '/'+file_names[i])
    height, width, rgb = img.shape
    newImg = cv2.resize(img,(224,224))
    if img is None:
        print("\nerror: image not read from file \n\n")
        os.system("pause")         
    img_gray = cv2.cvtColor(newImg, cv2.COLOR_BGRA2GRAY)
    bilateral = cv2.bilateralFilter(img_gray, 9, 20, 20)
    kernel = np.ones((6,6),np.uint8)
    
    arrX = []
    arrY = []
    arX = []
    arY = []
    
    closing = cv2.morphologyEx(bilateral, cv2.MORPH_CLOSE, kernel)
    threshold = cv2.adaptiveThreshold(closing, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresholdAgain = cv2.adaptiveThreshold(bilateral, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    pixel = cv2.countNonZero(threshold)
    zeros = (height*width) - pixel
    print(abs(zeros))
    
    if abs(zeros) > 100:
        for i in range(0,224):
            for j in range(0,224):
                if threshold[i][j] == 0:
                    arrX.append(i)
                    arrY.append(j)
    else:
        for i in range(0,224):
            for j in range(0,224):
                if thresholdAgain[i][j] == 0:
                    arX.append(i)
                    arY.append(j)
    #print("(",xMin,xMax,"),(",yMin,yMax,")")
    try:
        if abs(zeros) > 100:
            crop = img_gray[min(arrX): max(arrX), min(arrY):max(arrY)]
        else:
            crop = img_gray[min(arX): max(arX), min(arY):max(arY)]
    except ValueError:
        print('skipped',file_names[i])
    try:
        new = cv2.resize(crop,(224,224))
    except cv2.error:
        print('skipped',file_names[i])
    cv2.imwrite(FOLDER+"/"+destinationName+'/'+wait+'.jpg', new)
    print(int(time.time()-start_t))
    #cv2.imwrite(file_names, new)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

