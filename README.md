# ParkingLot_CNN

## Dataset:
- MNIST Dataset
- Includes number and character images (10 numbers and 26 characters)
- More than 1000 images per class
- Read from csv file
- Source: Kaggle
- Link:   
    [Character](https://www.kaggle.com/sachinpatel21/az-handwritten-alphabets-in-csv-format)  
    [Number](https://www.kaggle.com/c/digit-recognizer/data?select=train.csv)  
![data_grapth](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/images/data_graph.png)

## Detect Plate License
- Model: [WPOD-NET](https://openaccess.thecvf.com/content_ECCV_2018/papers/Sergio_Silva_License_Plate_Detection_ECCV_2018_paper.pdf)  
![wpod_net](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/images/wpod-net.png)
## Process Image  
- Image --> Gray Image --> Binary Image --> Dilation --> Find Contours --> Sort --> List of characters

## Model
- CNN Model: MobileNetV2 + Fine turning model
- Output classes: 36


## Trainning
![Accuracy](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/images/Accuracy.png)
![Loss](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/images/Loss.png)

## Using

- Change username, password of your account MySQL
- Uncomment line 15-19 in sql.py and run file to create database. 
- Connect with IP Camera (recommend DroidCam on Android or IOS)
- Replace "url" by your address ip camera
- Put the QR Code in front of the camera and license plate image in front of your ip camera

Check In

![UI](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/images/demo_1.jpg)

Check Out (with another license plate)

![UI](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/images/demo.jpg)


