'''
Sensor que detecta las casillas centrales de la matriz total, lo que nos ahorra tiempo de procesamiento de imagenes
'''
import cv2
from mss import mss
from PIL import Image
import numpy as np

#bounding_box = {'top': 200, 'left': 0, 'width': 900, 'height': 800} # Joseph
bounding_box = {'top': 202, 'left': 30, 'width': 542, 'height': 480} # Sebastian
#bounding_box = {'top': 167, 'left': 28, 'width': 544, 'height': 481} # universidad

class Agent_sensor():
    def __init__(self):
        self.start = True
        self.apple = (7, 12)

    def sensor(self):
        # If is the first time, return the default apple position
        if self.start:
            self.start = False
            return (7, 12)
        
        # While cicle wait until an apple appears in the game
        while True:
            with mss() as sct:
                img = np.array(sct.grab(bounding_box))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(img)

            imgSmall = img_pil.resize((17,15), resample=Image.BILINEAR)
            img = cv2.cvtColor(np.array(imgSmall), cv2.COLOR_RGB2BGR)

            matrix = np.zeros(shape=(15,17))

            for i in range(0, 15):
                for j in range(0, 17):
                    tmp = img[i, j]
                    if max(tmp) == tmp[2]:
                        self.apple = (i, j)
                        print(self.apple)
                        matrix[i][j] = 2
                        return (i, j)

    def apple_in_position(self):
        with mss() as sct:
            img = np.array(sct.grab(bounding_box))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)

        imgSmall = img_pil.resize((17,15), resample=Image.BILINEAR)
        result = cv2.cvtColor(np.array(imgSmall), cv2.COLOR_RGB2BGR)
        val = result[self.apple] 
        if max(val) == val[2]:
            return True
        else:
            return False
    
    def run(self):
        count = 0
        while True:
            print("Iteracion ", count, ": ", agent.sensor())
            count += 1
            while self.apple_in_position():
                pass

if __name__ == '__main__':
    agent = Agent_sensor()
    agent.run()