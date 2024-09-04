from vehicle import Driver
from controller import Camera
import cv2
import time
from line import main 
import numpy as np
from scipy.integrate import quad
from scipy.misc import derivative
import torch

driver = Driver()
timestep = int(driver.getBasicTimeStep())
    
# kamera eklenmesi
camera = driver.getDevice("camera")
camera.enable(timestep)  # 'Camera' nesnesinin 'enable' yöntemini kullanın

camera2 = driver.getDevice("camera2")
camera2.enable(timestep)  # 'Camera' nesnesinin 'enable' yöntemini kullanın

cam_width = 1080 
cam_height = 720

# Sabit değişkenler hem pid hem araç için
speed = 20
Kp = 0.418
Ki = 0.21
Kd = -0.006

park = False
# Pid algoritması
def pid_controller(error,fin_time,start_time):
    P = -Kp * error
    (integral_value,_) = quad(lambda x: function(error),start_time,fin_time)
    I = -Ki * integral_value
    derivative_value = derivative(function,error,dx = (fin_time-start_time))
    D = -Kd * derivative_value 
    a = P + I + D
    return a

def function(x):
    return x

def get_detected_labels_with_area_filter(image, min_area=10):
    Width = image.shape[1]
    Height = image.shape[0]
    cv2.imshow("asd",image)
    cv2.waitKey(1)
    print(type(image))
    results = model(image)

    conf_threshold = 0
    label = None
    predictions = results.pred[0]

    for *box, conf, cls in predictions:

        if conf < conf_threshold:
            continue
        
        x1, y1, x2, y2 = map(int, box)
        print(cls,x1,x2)
        area = (x2 - x1) * (y2 - y1)

        if area > min_area:
            label = int(cls)

    return label 

model = torch.hub.load('ultralytics/yolov5', 'custom', path="/home/koesan/Belgeler/webots/controllers/my_controller2/best_93.pt")

start_time = time.time()  # Başlangıç zamanını kaydedin
last_prediction_time = time.time()
prediction_interval = 2
while driver.step() != -1:

    driver.setCruisingSpeed(speed) 
    start_time = time.time()

    # Kameradan görüntüyü alın
    kamera_goruntusu = camera.getImage()
    tabela_kamerası = camera2.getImage()

    # Görüntüyü kaydedin
    camera.saveImage("camera.png", 1)  # 'saveImage' yöntemini kullanın
    camera2.saveImage("camera2.png", 1)  # 'saveImage' yöntemini kullanın
    
    # Görüntüyü OpenCV ile okuyun
    img = cv2.imread("camera.png")
    img = cv2.resize(img, (cam_width,cam_height))

    img2 = cv2.imread("camera2.png")
    img2 = cv2.resize(img2, (416,416))

    if not park:

        fin_time = time.time()
        dev = main(img)
        #print(dev)
        rotation_angle = pid_controller(dev,fin_time,start_time)  
        #print(rotation_angle)
        driver.setSteeringAngle(rotation_angle)
        current_time = time.time()
        if current_time - last_prediction_time >= prediction_interval:
           clas = get_detected_labels_with_area_filter(img2,10)
           print(clas)
           last_prediction_time = current_time