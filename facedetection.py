"""
Author : Kartikeyan Gupta
Date : 30-03-2019 

---This is a simple read-made IoT project
---I have used haarcascade_frontalface_default to detect faces in an image
---Install opencv in raspberry pi and install paho.mqtt
---create a demo account in thingsboard and you are good to good
---A detailed explanation of the code will be updated soon
"""

import numpy as np
import cv2

#---import when using raspberry pi to capture images
#import picamera

#---import if you are connecting to ThingsBoard - opensourse IoT based platform
import paho.mqtt.client as mqtt

import json

""" Used this code to capture image using RPi and store it as classroom.jpg"""
#camera = picamera.PiCamera()
#camera.capture('classroom.jpg')
#image = cv2.imread('classroom.jpg')

""" this block of code is declaration for the connection variable to ThingsBoard"""
iot_hub = "demo.thingsboard.io"
port = 1883
username="sn6aAHNLreNVY1EPHYgG"#put your access token here 
password=""
topic="v1/devices/me/telemetry"

""" This block of code connect to thingsboard using mqtt connection """
"""" if you dont want to connect this comment it """
client = mqtt.Client()
client.username_pw_set(username,password)
client.connect(iot_hub,port)
print("connection sucess")


"""This block is used to capture image in a laptop with webcam . If you are using raspberry Pi just comment the whole block"""
""" Here to capture image you have to press 'space' once captured a perfect image press 'esc' to move to the facedetection part"""
cam = cv2.VideoCapture(0)
cv2.namedWindow("capture")
while True:
    ret, frame = cam.read()
    cv2.imshow("capture", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "myimage.png"
        cv2.imwrite(img_name, frame)
        print("Captured image")		
cam.release()
cv2.destroyAllWindows()

"""This is where I am declaring the face_cascade"""
face_cascade = cv2.CascadeClassifier('C:/Users/kartikeyan/Desktop/iot_project/haarcascade_frontalface_default.xml')

"""To use image captured by RPi change the image source to 'classroom.jpg' """
"""comment all the connection methods if no connection made"""
image = cv2.imread(img_name)
print(image)
grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(grayImage)
print(type(faces))
data = dict()
if len(faces) == 0:
	print("No faces found")
	data["Number of students present : "]="0"
	data_out=json.dumps(data)
	client.publish(topic,data_out,0)
else:
	print (faces)
	print (faces.shape)
	print ("Number of faces detected: " + str(faces.shape[0]))
	for (x,y,w,h) in faces:
		cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),1)
		
	cv2.rectangle(image, ((0,image.shape[0] -25)),(270, image.shape[0]), (255,255,255), -1)
	cv2.putText(image, "Number of faces detected: " + str(faces.shape[0]), (0,image.shape[0] -10), cv2.FONT_HERSHEY_TRIPLEX, 0.5,  (0,0,0), 1)
	data["Number of students present : "]=str(faces.shape[0])
	data_out=json.dumps(data)
	client.publish(topic,data_out,0)
	cv2.imshow('Image with faces',image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()