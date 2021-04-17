import cv2
import numpy as np
from local_utils import detect_lp
from keras.models import model_from_json
from os.path import splitext

def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        # print("Loading model successfully...")
        return model
    except Exception as e:
        print(e)

def preprocess_image(image,resize=False):
    # img = cv2.imread(image_path)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img

def get_plate(image, wpod_net, Dmax=608, Dmin=256):
    vehicle = preprocess_image(image)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    return LpImg, cor



def plate_image(image, wpod_net):
    LpImg,cor = get_plate(image, wpod_net)

    plate_img = cv2.convertScaleAbs(LpImg[0], alpha=(255.0))
    return plate_img

if __name__ =="__main__":
    image = cv2.imread("bs6.jpg")
    wpod_net_model = load_model("wpod-net.json")
    plate_image = plate_image(image, wpod_net_model)
    cv2.imshow('plate_image', plate_image)
    cv2.waitKey()