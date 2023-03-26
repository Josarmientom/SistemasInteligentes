'''
Sensor que detecta las casillas centrales de la matriz total, lo que nos ahorra tiempo de procesamiento de imagenes
'''
import cv2
from mss import mss
import numpy as np

#bounding_box = {'top': 200, 'left': 0, 'width': 900, 'height': 800} # Joseph
bounding_box = {'top': 202, 'left': 30, 'width': 542, 'height': 480} # Sebastian
#bounding_box = {'top': 167, 'left': 28, 'width': 544, 'height': 481} # universidad

def sensor():
   # take screenshot with mss
    with mss() as sct:
        img = np.array(sct.grab(bounding_box)) 
    # obtain the matrix of the image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # matrix = np.zeros(shape=(15, 17), dtype=np.int8)
    matrix = np.zeros(shape=(15,17))

    i_div = 480// (15)
    j_div = 542// (17)
    for i in range(0, 15):
        for j in range(0, 17):
            tmp = img[i*i_div + i_div//2, j*j_div + j_div//2]
            if max(tmp) == tmp[0]:
                matrix[i][j] = 1
            elif max(tmp) == tmp[1]:
                matrix[i][j] = 0
            else:
                matrix[i][j] = 2

    print(matrix)
    print("\n"*3)

if __name__ == '__main__':
    while True:
        sensor()