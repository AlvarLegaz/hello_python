# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 18:26:32 2020

@author: Vonliendres
"""

from PIL import Image
import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

host = "http://192.168.2.176/image/jpeg.cgi"
user ='admin'
password = '10331466'

print("Visor Camara IP");
print("Host:",host)
print("User:",user)

response = requests.get(host,auth=(user,password))

if(response.status_code!=200):
    print("Error: codigo ",response.status_code)
else:
    img = Image.open(BytesIO(response.content))
    plt.imshow(img)
	img.show()