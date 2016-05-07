~~~~~~~~~~~~~~~~~

~~Installation~~

Following must be installed:
-Numpy
-Pillow
-matplotlib
-sklearn

----Training----
Included are the pkl files so there is no need to train the SVM.
However, if the pkl files do not work, follow these steps:

1.) Start up the code without any command-line arguments with
  'python Project3.py'
2.) A prompt will come up asking whether you would like to train or classify
3.) Type 't' or 'train' (Without quotes and it is case insensitive)
4.) Next, type the name of the folder with the training set ('Training', in this case. Also without quotes)

*note**
-Training sets must have subfolders with appropriate names signifying what the images within should be classified as
-Each image must also be the same size, have the same bit depth, and have the same type (Only 24 bit dept .jpgs have been tested)
*******
~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~
~~Usage~~

---Classifying---

Images can be classified in 2 ways
-Through command line (Unable to test, recommended not to use)
-From inside the program

*note**
SVM must be trained first!
*******

=================

This program supports only classifying one image from the command line.

'python Project3.py image.jpg'

=================

You can also classify the images inside the program:

1.) Start up the code without any command-line arguments with
  'python Project3.py image.jpg'
2.) A prompt will come up asking whether you would like to train or classify
3.) Type 'c' or 'classify' (Without quotes and it is case insensitive)
4.) Type the name of the image with the extension. The image must be in the same folder as the .py file
5.) Predicted class will be outputted
6.) You will be given a choice to classify another image, type 'y' or 'yes' to chose another, and 'n' or 'no' to exit
7.) If 'yes' is chosen, go back to step 4

~~~~~~~~~~~~~~~~~
