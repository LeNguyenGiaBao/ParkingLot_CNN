from determine_LP import *
from binary_image import *

# https://www.pyimagesearch.com/2015/04/20/sorting-contours-using-python-and-opencv/
def sort_contours(cnts,reverse = False):
    i = 0		#left to right
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                        key=lambda b: b[1][i], reverse=reverse))
    return cnts

def cut_image_to_2_images(image):
	h, w = image.shape
	bot = int(h*0.55)
	top = int(h*0.45)
	image_top = image[0:bot, 0:w]
	image_bottom = image[top:h, 0:w]
	return image_top, image_bottom

def get_characters_from_image(image):

	#get contour
	cont  = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

	#characters
	crop_characters = []

	digit_w, digit_h = 30, 60

	for c in sort_contours(cont):
	    (x, y, w, h) = cv2.boundingRect(c)
	    ratio = h/w
	    if 1<=ratio<=5: # Only select contour with defined ratio
	        if h/image.shape[0]>=0.3: # Select contour which has the height larger than 50% of the plate

	            # Sperate number and gibe prediction
	            curr_num = image[y:y+h,x:x+w]
	            curr_num = cv2.resize(curr_num, dsize=(digit_w, digit_h))
	            _, curr_num = cv2.threshold(curr_num, 220, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
	            crop_characters.append(curr_num)

	return crop_characters

def get_characters(image):
	image_top, image_bottom = cut_image_to_2_images(image)
	charater_top = get_characters_from_image(image_top)
	charater_bot = get_characters_from_image(image_bottom)

	return charater_top, charater_bot

if __name__ == "__main__":
	image = cv2.imread("./images/bs5.jpg")
	wpod_net_model = load_model("./model/wpod-net.json")
	plate_image = plate_image(image, wpod_net_model)
	binary_plate_image = binary_image(plate_image)
	charater_top, charater_bot = get_characters(binary_plate_image)
	for character in charater_top:
		cv2.destroyAllWindows()
		cv2.imshow('top', character)
		cv2.waitKey()

	for character in charater_bot:
		cv2.destroyAllWindows()
		cv2.imshow('bottom', character)
		cv2.waitKey()