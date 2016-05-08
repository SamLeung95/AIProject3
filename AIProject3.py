
# coding: utf-8

# In[1]:

from PIL import Image
from PIL import ImageFilter
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
import time
import os
import sys
import math
import random
from scipy.ndimage.filters import gaussian_filter
from sklearn.externals import joblib
import warnings
from sklearn import svm


# In[2]:

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


# In[3]:

def img_to_array(img_path):
    
    img = Image.open(img_path)
    img = img.resize((100,100), Image.ANTIALIAS)
    img = np.array(img)
    img = threshold(img, img_path)
    img = gaussian_filter(img, sigma=2)
    img = img.ravel()
    
    return img


# In[4]:

def test_acc():

    random.seed(422)
    
    image_names=[]
    training=[]
    classification=[]
               
    img_dir=input("Enter training set location: ")
    img_dir_2=[img_dir + "\\" + d for d in os.listdir(img_dir)]
    img_classes=[d for d in os.listdir(img_dir)]
    
    k_input=input("How many times: ")

    for directories in img_dir_2:
        image_names.append([d for d in os.listdir(directories)])
                
    for classes in range(len(img_classes)):
        
        for image_name in range(len(image_names[classes])):
            file_loc=img_dir + "\\" + img_classes[classes] + "\\" + image_names[classes][image_name]
            training.append(img_to_array(file_loc))
            classification.append(img_classes[classes])
    
    combined_array=list(zip(training, classification))
    random.shuffle(combined_array)
    training, classification = zip(*combined_array)
    
    bin_size=math.floor(len(training)/int(k_input))
    test_bin=[]
    test_bin_class=[]
    testing=[]
    classes=[]
    correct=0
    incorrect=0
    count=0
    
    for item in range(len(training)):
        if count==bin_size:
            count=0
            testing.append(test_bin)
            classes.append(test_bin_class)
            test_bin=[]
            test_bin_class=[]
            
        test_bin.append(training[item])
        test_bin_class.append(classification[item])
        count+=1
        
    clf = svm.LinearSVC()
    
    for x in range(len(testing)):
        validation=testing[x]
        validation_class=classes[x]
        final_arr=[]
        final_class=[]
        
        for y in range(1,len(testing)):
            final_arr.extend(testing[(x+y)%len(testing)])
            final_class.extend(classes[(x+y)%len(testing)])
        
        clf.fit(final_arr, final_class)
        
        for z in range(len(validation)):
            print("Class: ", validation_class[z])
            print("Prediction: ")
            prediction=clf.predict(validation[z])
            print(prediction)
            if validation_class[z]==prediction:
                print("correct!")
                correct+=1
            else:
                print("Incorrect :C")
                incorrect+=1
    print("Correct: ", correct)
    print("Inorrect: ", incorrect)
    print("Final accuracy:",correct/(correct+incorrect),"%")
    
    os._exit(1)


# In[5]:

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
                os._exit(1)
                    
            elif len(sys.argv)==1:
                user_input=input("(T)rain, (c)lassify image, or te(s)t for accuracy: ")
            
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
            
            elif(user_input.lower()=="s" or user_input.lower()=="test"):
                test_acc()
            elif(user_input.lower()=="exit"):
                os._exit(1)
                
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


# In[6]:

main()


# In[ ]:



