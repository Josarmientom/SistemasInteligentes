import keyboard
from threading import Event
from time import sleep, time
from mss import mss
import numpy as np
from PIL import Image
import pyautogui

locate_board = pyautogui.locateOnScreen('/home/sebas/Documents/SistemasInteligentes/Proyecto1/board.png')
bounding_box = {'top': locate_board[1], 'left': locate_board[0], 'width': locate_board[2], 'height': locate_board[3]}

bound_1 = (0, 0)
bound_2 = (0, 16)
bound_3 = (14, 0)
bound_4 = (14, 16)

bounds_list = [bound_1, bound_2, bound_3, bound_4]

def bounds(jump):
    # Extract the image
    while True:
        with mss() as sct:
            img = sct.grab(bounding_box)
        img_pil = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")

        imgSmall = img_pil.resize((17,15), resample=Image.BILINEAR)
        # what information do we need?

        for i in bounds_list:
            tmp = imgSmall.getpixel((i[1], i[0]))
            if max(tmp) == tmp[2]:
                if i == bound_1:
                    dir = 'down'
                elif i == bound_2:
                    dir = 'left'
                elif i == bound_3:
                    dir = 'right'
                else:
                    dir = 'up'
                if dir == jump:
                    continue
                return True, dir

def actuator(instruct) -> None:
    # instruct is a dictionary with the path to the apple
    pyautogui.press(instruct)

sleep(1)
jump = 'down'
while True:
    bound = bounds(jump)
    in_corner = bound[0]
    if in_corner:
        print('Esquina!!')
        jump = bound[1]
        actuator(jump)
