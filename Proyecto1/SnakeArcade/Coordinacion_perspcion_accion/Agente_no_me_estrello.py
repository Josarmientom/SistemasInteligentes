from mss import mss
import numpy as np
import cv2
from PIL import Image
from time import sleep
import pyautogui

class Agent():
  def __init__(self):
    self.apple = [7, 12]
    self.is_apple = True
    self.there_is_plan = False
    self.initial = True
    self.head = [7, 3]
    pass
    
  def program(self, percepts):
    print('I thinking...')
  
  def sensor(self):
    #bounding_box = {'top': 200, 'left': 0, 'width': 900, 'height': 800} # Joseph
    bounding_box = {'top': 202, 'left': 30, 'width': 542, 'height': 480} # Sebastian
    #bounding_box = {'top': 167, 'left': 28, 'width': 544, 'height': 481} # Universidad
    with mss() as stc:
      img = np.array(stc.grab(bounding_box))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)
    imgSmall = img_pil.resize((17,15), resample=Image.BILINEAR)
    result = cv2.cvtColor(np.array(imgSmall), cv2.COLOR_RGB2BGR)

    matrix = np.zeros(shape=(15,17))

    count_apple = 0
    for i in range(15):
      for j in range(17):
        b,g,r = result[i,j]
        if b == max(result[i,j]):
          matrix[i,j] = 1
        elif g == max(result[i,j]):
          matrix[i,j] = 0
        else:
          matrix[i,j] = 2
          self.apple = [i,j]
          count_apple += 1
    
    # Fragmento que se ejecuta solo una vez al inicio
    if self.initial == True:
      self.initial = False
      self.there_is_plan = True
      matrix[7][4] = 3
      self.print_matrix(matrix)
      self.plan = self.program(matrix)
    # Fragmento que se ejecuta cuando no se encuentra la manzana
    elif count_apple == 0:
      self.is_apple = False
      self.there_is_plan = False
      self.head = [self.apple[0], self.apple[1]]
    # Fragmento que se ejecuta cuando se encuentra la manzana
    elif self.there_is_plan == False:
      self.there_is_plan = True
      matrix[self.head[0]][self.head[1]] = 3
      self.plan = self.program(matrix)
      self.print_matrix(matrix)

  def action(self, action):
    pyautogui.keyDown(action)
    sleep(0.5)

  def print_matrix(self, matrix):
    for i in range(15):
      for j in range(17):
        print(int(matrix[i,j]), end=' ')
      print()
    
    print('\nApple: ', self.apple)


agent = Agent()
while True:
  agent.sensor()