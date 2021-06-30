from determine_LP import *

def binary_image(image):

    #convert to gray image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #blur image, decrease noise, kernel = 7x7
    blur = cv2.GaussianBlur(gray,(7,7),0)
    
    # Applied inversed thresh_binary
    binary = cv2.threshold(blur, 80, 255,
                     cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    #kernel 3x3
    kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    #dilation binary image
    thre_mor = cv2.morphologyEx(binary, cv2.MORPH_DILATE, kernel3)

    return thre_mor

if __name__ == "__main__":
    image = cv2.imread("./images/bs6.jpg")
    wpod_net_model = load_model("./model/wpod-net.json")
    plate_image = plate_image(image, wpod_net_model)
    binary_plate_image = binary_image(plate_image)
    cv2.imshow('binary_plate_image', binary_plate_image)
    cv2.waitKey()


