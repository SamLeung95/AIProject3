
# coding: utf-8

# In[15]:

from PIL import Image
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys
from sklearn.externals import joblib
import warnings
from sklearn import svm


# In[16]:

def getMean(arr):
    
    avg = sum(arr) / len(arr)
    
    return avg

def threshold(img_arr, img_name):
    avgArr = []
    newArr = img_arr
    for row in img_arr:
        for pixel in row:
            avg=getMean(pixel[:3])
            avgArr.append(avg)
            
    threshold = getMean(avgArr)
    
    for row in newArr:
        for pixel in row:
            if(getMean(pixel[:3])>threshold):
                for x in range(3):
                    pixel[x]=255;
            else:
                for x in range(3):
                    pixel[x]=0;
            
            if(img_name.lower().endswith(('.png', '.gif', 'bmp'))):
                pixel[3]=255
                
    return newArr


# In[17]:

def img_to_array(img_path):
    
    img = Image.open(img_path)
    img = img.resize((100,100), Image.ANTIALIAS)
    img = np.array(img)
    img = threshold(img, img_path)
    img = img.ravel()
    
    return img


# In[20]:

def main():
    
    warnings.filterwarnings("ignore")
    loop=True
    img=None
    
    while loop==True:
        try:
            
            user_input="None"
            
            if len(sys.argv)==2:
                if(not os.path.isfile(sys.argv[1])):
                    print("Invalid file name.")
                else:
                    clf = joblib.load('SVMdump.pkl') 
                    print(clf.predict(img_to_array(img_name)))
                sys.exit()
                    
            elif len(sys.argv)==1:
                user_input=input("Train or classify image: ")
            
            if(user_input.lower()=="t" or user_input.lower()=="train"):
                image_names=[]
                training=[]
                classification=[]
                
                img_dir=input("Enter training set location: ")
                img_dir_2=[img_dir + "\\" + d for d in os.listdir(img_dir)]
                img_classes=[d for d in os.listdir(img_dir)]
                
                for directories in img_dir_2:
                    image_names.append([d for d in os.listdir(directories)])
                
                for classes in range(len(img_classes)):
                    for image_name in range(len(image_names[classes])):
                        file_loc=img_dir + "\\" + img_classes[classes] + "\\" + image_names[classes][image_name]
                        training.append(img_to_array(file_loc))
                        classification.append(img_classes[classes])
                
                clf = svm.LinearSVC()
                clf.fit(training, classification)
                print("Finished Training!")
                
                joblib.dump(clf, 'SVMdump.pkl')
                
                loop=False
                      
            elif(user_input.lower()=="c" or user_input.lower()=="classify"):
                
                clf = joblib.load('SVMdump.pkl') 
                
                repeat=True
                
                while repeat==True:
                    img_name=input("Enter image name: ")
                    
                    valid_choice=False
                    
                    if(not os.path.isfile(img_name)):
                        print("Invalid file name, please try again.")
                        valid_choice=True
                    else:
                        print(clf.predict(img_to_array(img_name)))
                    
                    
                    while valid_choice==False:
                        
                        repeat_choice=input("Pick another image? ")

                        if(repeat_choice.lower()=="y" or repeat_choice.lower()=="yes"):
                            valid_choice=True
                        elif(repeat_choice.lower()=="n" or repeat_choice.lower()=="no"):
                            valid_choice=True
                            repeat=False
                        else:
                            print("Not a valid choice. Chose (y)es or (n)o.")
                    
                loop=False
                
            elif(user_input.lower()=="exit"):
                sys.exit()
                
            else:
                
                if user_input=="None":
                    loop=False
                    print("Invalid command line arguments.")
                else:
                    loop=True
                    print("Invalid input, please try again.")
            
        except FileNotFoundError:
            loop=True
            print("Invalid image, please try again.")



# In[19]:

main()


# In[ ]:



