from mss import mss
import numpy as np
import cv2
from PIL import Image

class Agent():
  def __init__(self):
    pass
    
  def program(self, percepts):
    for p in percepts:
      if p == 'BUMP':
        return 'TURN'
    return 'FORWARD'
  
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

    for i in range(15):
      for j in range(17):
        b,g,r = result[i,j]
        if b == max(result[i,j]):
          matrix[i,j] = 1
        elif g == max(result[i,j]):
          matrix[i,j] = 0
        else:
          matrix[i,j] = 2
    return matrix

  def print_matrix(self, matrix):
    for i in range(15):
      for j in range(17):
        print(int(matrix[i,j]), end=' ')
      print()


agent = Agent()
agent.print_matrix(agent.sensor())