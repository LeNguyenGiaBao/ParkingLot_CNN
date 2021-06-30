from determine_LP import *
from binary_image import *
from get_characters import *
from sklearn import preprocessing

def predict_from_model(image,model,labels):
    image = cv2.resize(image,(80,80))
    image = np.stack((image,)*3, axis=-1)
    prediction = labels.inverse_transform([np.argmax(model.predict(image[np.newaxis,:]))])
    return prediction

def string_LP(list_image, model, labels):
	final_string=''
	for i in list_image:
		title = np.array2string(predict_from_model(i,model,labels))
		final_string+=title.strip("'[]")
	return final_string

if __name__ == "__main__":
	image = cv2.imread("./images/bs6.jpg")
	wpod_net_model = load_model("./model/wpod-net.json")
	plate_image = plate_image(image, wpod_net_model)
	binary_plate_image = binary_image(plate_image)
	charater_top, charater_bot = get_characters(binary_plate_image)

	json_file = open('./model/MobileNets_character_recognition.json', 'r')
	loaded_model_json = json_file.read()

	model = model_from_json(loaded_model_json)
	model.load_weights("./model/License_character_recognition_weight.h5")

	labels = preprocessing.LabelEncoder()
	labels.classes_ = np.load('./model/license_character_classes.npy')

	json_file.close()

	print(string_LP(charater_top, model, labels))
	print(string_LP(charater_bot, model, labels))