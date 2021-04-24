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
![data_grapth](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/data_graph.png)

## Detect Plate License
- Model: [WPOD-NET](https://openaccess.thecvf.com/content_ECCV_2018/papers/Sergio_Silva_License_Plate_Detection_ECCV_2018_paper.pdf)  
![wpod_net](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/wpod-net.png)
## Process Image  
- Image --> Gray Image --> Binary Image --> Dilation --> Find Contours --> Sort --> List of characters

## Trainning
![Accuracy](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/Accuracy.png)
![Loss](https://github.com/LeNguyenGiaBao/ParkingLot_CNN/blob/master/Loss.png)
## Predict  
- CNN Model: MobileNetV2 + Fine turning model
- Output classes: 36
- Total param:

