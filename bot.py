import numpy as np
from PIL import ImageGrab
import pyautogui
import cv2
import time
import win32api, win32con

def locateOnScreen(path):
	screen_x, screen_y = pyautogui.size()
	while True:
		printscreen_pil = ImageGrab.grab(bbox=(0, 0, screen_x, screen_y))

		img_bgr = cv2.cvtColor(np.array(printscreen_pil), cv2.COLOR_BGR2RGB)
		img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

		template = cv2.imread(path, 0)
		w, h = template.shape[::-1]

		res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
		threshold = .7
		loc = np.where(res >= threshold)

		for pt in zip(*loc[::-1]):
			if len(loc[0]) > 0:
				return pt[0], pt[1], w, h

def check_red(x, y, w, h):
	printscreen_pil = ImageGrab.grab(bbox=(0, 0, 800, 640))

	img_bgr = cv2.cvtColor(np.array(printscreen_pil), cv2.COLOR_BGR2RGB)

	bar_img = img_bgr[y : y+h, x: x+w]

	for row in bar_img:
		for px in row:
			mask_blue = px[0] < 50
			mask_green = px[1] < 50
			mask_red = px[2] > 150
			if mask_blue & mask_green & mask_red:
				return True
	return False

def start():
	x_hunger, y_hunger, w_hunger, h_hunger = locateOnScreen('imgs/red.jpg')
	#while True:
	if check_red(x_hunger, y_hunger, w_hunger, h_hunger):
		print 'Hungry'
		x_feed, y_feed, w_feed, h_feed = locateOnScreen('imgs/feed.jpg')

		pyautogui.moveTo(x_feed + w_feed / 2, y_feed + h_feed / 2, .5)
		pyautogui.click()
		print 'Clicking on Feed Button'
		time.sleep(1)

		x_ok, y_ok, w_ok, h_ok = locateOnScreen('imgs/ok.jpg')
		pyautogui.moveTo(x_ok + w_ok / 2, y_ok + h_ok / 2, .5)
		pyautogui.click()
		print 'Clicking on Ok Button'

		start()
	else:
		print 'waiting'
		time.sleep(2)
		start()
start()