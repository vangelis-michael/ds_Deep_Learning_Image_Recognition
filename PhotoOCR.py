#We'll have to import OS to check the working directory available here as it isnt same thing as on a local machine
import os
os.getcwd()

#Make a directory to keep all files when uploaded
os.mkdir('NewFolder')
os.listdir()
os.chdir('/content/NewFolder')

#Use this to import files from your local system
from google.colab import files
uploaded = files.upload()

#Save the contents of the upload immediately
for name, data in uploaded.items():
  with open(name, 'wb') as f:
    f.write(data)
    print ('saved file', name)
    
#List the contents of the new folder created
os.listdir()

# Install some OCR libraries
!pip install pillow
!pip install pytesseract
!apt-get install tesseract-ocr 
!apt-get install libtesseract-dev
!pip install tesseract

from PIL import Image
import pytesseract
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

# import the sample image
img = Image.open('test-european.jpg')

#create an array so we can see the pixels (rgb)
iar = np.array(img)

#plot the image using the pixel array
plt.imshow(iar)

#printing the text contained on the image
result = pytesseract.image_to_string(img)

#stripping the text
result = result.strip()

#splitting the lines to make the text readable
result = result.splitlines()

#check the result
result

