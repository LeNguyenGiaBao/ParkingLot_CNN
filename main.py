from determine_LP import * 
from binary_image import *
from get_characters import * 
from predict_character import *
from sql import *
import time
from sklearn import preprocessing
import numpy as np
from playsound import playsound
import tkinter as tk
import cv2
from PIL import ImageTk, Image
import PIL
from pyzbar import pyzbar
from threading import Thread
from time import strftime ,gmtime
from datetime import datetime


previour_time = time.time()

frame_image = 1

url = "http://192.168.1.2:4747/video"


# load model
wpod_net = load_model("model/wpod-net.json")

json_file = open('model/MobileNets_character_recognition.json', 'r')
loaded_model_json = json_file.read()

model = model_from_json(loaded_model_json)
model.load_weights("model/License_character_recognition_weight.h5")

labels = preprocessing.LabelEncoder()
labels.classes_ = np.load('model/license_character_classes.npy')

json_file.close()



'''convert cv2 image to image tkinter to set image to label'''
def cv2_to_imageTK(image):
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
	imagePIL = PIL.Image.fromarray(image)
	imgtk = ImageTk.PhotoImage(image = imagePIL)
	return imgtk

'''check bottom string of the plate, ==5 and is a number'''
def check_bot_string(string):
	return (string.isdigit() and len(string) ==5)


'''where bike into the park, get plate of the bike, and save data( id card, plate, time in )'''
def BikeIn():
	try:
		plate = get_plate()
		clear_data()
		threadXeVao = Thread(target = play_sound_xevao)
		threadXeVao.start()

		
		lbPlate_ip['text'] = plate

		insert_data(lb_code['text'] ,plate, frame_image)
	except:
		print("No License plate is founded!")

'''where bike out, get plate, compare, and save data(time out, state)'''
def BikeOut():
	threadXeRa = Thread(target = play_sound_xera)
	threadXeRa.start()

	plate = get_plate()
	lbPlate_ip['text'] = plate


	data = get_by_mssv(lb_code['text'])[0]

	image = data[6]
	image = np.frombuffer(image, dtype=np.uint8)
	img = cv2.imdecode(image, 1)

	imgtk = cv2_to_imageTK(img)
	lb_image_saved.imgtk = imgtk
	lb_image_saved.configure(image = imgtk)

	lbPlate_saved['text'] = data[2]

	update_data(lb_code['text'])

	if(lbPlate_saved['text'] == lbPlate_ip['text']):
		lbPlate_saved['bg'] = '#57f542'
		lbPlate_ip['bg'] = '#57f542'

	else:
		lbPlate_saved['bg'] = 'red'
		lbPlate_ip['bg'] = 'red'	

	lb_time_park['text'] = 'Vào: ' + str(data[4]) + '\n Ra: ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\nTG Gởi: ' + str(datetime.now() - data[4])

'''clear 2 label plate, image saved'''
def clear_data():
	lbPlate_saved['bg'] = '#F0F0F0'	
	lbPlate_ip['bg'] = '#F0F0F0'

	lbPlate_saved['text'] = ''	
	lbPlate_ip['text'] = ''	
	lb_time_park['text'] = ''

	image = cv2.imread('images/gray.jpg')
	imgtk = cv2_to_imageTK(image)
	lb_image_saved.imgtk = imgtk
	lb_image_saved.configure(image = imgtk)


'''get plate, input: frame_image: global variable'''
def get_plate():
	global frame_image
	image = plate_image(frame_image, wpod_net)
	image_binary = binary_image(image)
	list_top, list_bot = get_characters(image_binary)

	flag_top = False
	for j in range(5):
		string_top = string_LP(list_top, model, labels)
		if(len(string_top)!=4):
			continue
		if(string_top[0].isdigit() and string_top[1].isdigit() and string_top[-1].isdigit() and not string_top[2].isdigit()):
			flag_top = True
			break

	if not(flag_top):
		for k in range(2):
			if not(string_top[0].isdigit()):
				string_top = string_top.replace(string_top[0], '')
			if not(string_top[-1].isdigit()):
				string_top = string_top.replace(string_top[-1], '')


	flag_bot = False
	for i in range(5):
		string_bot = string_LP(list_bot, model, labels)
		if(check_bot_string(string_bot)):
			flag_bot = True
			break
	# print(string_bot)
	if not (flag_bot):
		for item in string_bot:
			if not (item.isdigit()):
				string_bot = string_bot.replace(item, '')

	plate = string_top + ' - ' + string_bot
	return plate

''''''
def image_to_label_saved(image):
	# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGBA)
	# imagePIL = PIL.Image.fromarray(image)
	imgtk = cv2_to_imageTK(image)
	lb_image_saved.imgtk = imgtk
	lb_image_saved.configure(image = imgtk)



'''display clock'''
def time_clock(): 
    string = strftime("%H:%M:%S\n%d-%m-%Y", gmtime())
    lb_clock.config(text = string) 
    lb_clock.after(1000, time_clock) 


def play_sound_xevao():
	playsound('audio/xevao.mp3')

def play_sound_xera():
	playsound('audio/xera.mp3')


root = tk.Tk()
root.title('Parking Lot')
root.geometry("+30+30")

canvas = tk.Canvas(root, height=700, width=1300)
canvas.pack()


#GUI-WEBCAM
webcam_frame = tk.Frame(root)#, bg='gray')
webcam_frame.place(relwidth=0.26, relheight=0.66, relx=0.01, rely = 0.15)


#GUI-IPCAM
ipcam_frame = tk.Frame(root)#, bg = 'yellow')
ipcam_frame.place(relwidth=0.35, relheight=1, relx = 0.28)

#Image saved frame
image_saved_frame = tk.Frame(root)#, bg = 'red')
image_saved_frame.place(relwidth=0.35, relheight=1, relx = 0.64)

#clock frame
clock_frame = tk.Frame(root)#, bg='blue')
clock_frame.place(relwidth=0.26, relheight=0.14, relx=0.01, rely=0.01)

#money frame
time_frame = tk.Frame(root)#, bg = 'yellow')
time_frame.place(relwidth=0.26, relheight=0.17, relx=0.01, rely=0.82)

# webcam
lb1 = tk.Label(webcam_frame, text= "SCAN CARD HERE", font=("Courier", 27))#, fg='red')#, bg ='black')
lb1.place(relx=0, rely=0.01, relheight=0.1,relwidth=1)

lb_webcam = tk.Label(webcam_frame)#, bg='cyan')
lb_webcam.place(relx=0, rely = 0.12, relwidth = 1, relheight=0.77)

lb2 =tk.Label(webcam_frame, text= "CODE:", font=("Courier", 24), fg='red')#, bg ='black')
lb2.place(relx =0, rely =0.9)

lb_code = tk.Label(webcam_frame, font=("Courier", 24), fg='red')#, bg ='black')
lb_code.place(relx = 0.33 , rely = 0.9)



#clock frame 
lb_clock = tk.Label(clock_frame, font = ("Courier", 30, "bold"))#, fg='red')
lb_clock.place(relx=0, rely=0, relwidth=1, relheight=1)



lb_ipcam = tk.Label(ipcam_frame)#, bg = 'purple')
lb_ipcam.place(relx=0, rely = 0.09, relwidth = 1, relheight=0.7)

lb3 = tk.Label(ipcam_frame, text = 'IP CAMERA', font=("Courier", 27), fg = 'black')#, bg= 'magenta')
lb3.place(relx=0, rely = 0.01, relwidth =1, relheight=0.07)

lbPlate_ip = tk.Label(ipcam_frame, font=("Courier", 27), fg = 'black')#, bg= 'magenta')
lbPlate_ip.place(relx=0, rely = 0.8, relheight=0.18, relwidth=1)



#image saved frame
lb_image_saved = tk.Label(image_saved_frame)#, bg = 'green')
lb_image_saved.place(relx=0, rely = 0.09, relwidth = 1, relheight=0.7)


lb4 = tk.Label(image_saved_frame, text = 'IMAGE SAVED', font=("Courier", 27), fg = 'black')#, bg= 'yellow')
lb4.place(relx=0, rely = 0.01, relwidth =1, relheight=0.07)

lbPlate_saved = tk.Label(image_saved_frame, font=("Courier", 27), fg = 'black')#, bg= '#57f542')
lbPlate_saved.place(relx=0, rely = 0.8, relheight=0.18, relwidth=1)

# time_frame
lb_time_park = tk.Label(time_frame, font=("Courier", 16))
lb_time_park.place(relx=0, rely=0, relheight=1, relwidth=1)



def CAM():
	cap = cv2.VideoCapture(0)

	def showCam():
		global previour_time
		_, frame = cap.read()
		barcodes = pyzbar.decode(frame)
		if(barcodes!=[]):
			threadReadBarcode = Thread(target = decode_barcode(barcodes))
			threadReadBarcode.start()
		imgtk = cv2_to_imageTK(frame)
		lb_webcam.imgtk = imgtk
		lb_webcam.configure(image=imgtk)
		lb_webcam.after(10, showCam)
		

	threadShowCam=Thread(target=showCam)
	threadShowCam.start()



def decode_barcode(barcode):
	lb_code['text'] = barcode[0][0].decode("utf-8")

	global previour_time
	if(time.time() - previour_time > 3):
		if(len(get_by_mssv(lb_code['text'])) >0):
			BikeOut()
		else:
			BikeIn()
		previour_time = time.time()

def IPCAM():
	ipcam= cv2.VideoCapture(url)

	def read_ipcam():
		global frame_image
		ret1, frame1 = ipcam.read()
		frame_image = frame1
		imgtk2 = cv2_to_imageTK(frame1)
		lb_ipcam.imgtk = imgtk2
		lb_ipcam.configure(image = imgtk2)
		lb_ipcam.after(10, read_ipcam)
	threadReadIP=Thread(target=read_ipcam)
	threadReadIP.start()


thread1= Thread(target=CAM)
thread1.start()
IPCAM()
thread3 = Thread(target=time_clock)
thread3.start()

root.mainloop()



