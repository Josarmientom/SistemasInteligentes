import numpy as np
import cv2
from mss import mss
from PIL import Image
import time

def color(arr):
    if arr[0] == max(arr):
        return 'B'
    elif arr[1] == max(arr):
        return 'G'
    else:
        return 'R'

#bounding_box = {'top': 200, 'left': 0, 'width': 900, 'height': 800}
bounding_box = {'top': 202, 'left': 30, 'width': 542, 'height': 480}

while True:
    start = time.time()
    with mss() as sct:
        img = np.array(sct.grab(bounding_box))

    #img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    imgSmall = img_pil.resize((17,15), resample=Image.BILINEAR)

    #result = imgSmall.resize(img_pil.size, Image.NEAREST)

    #result = cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR)
    result = cv2.cvtColor(np.array(imgSmall), cv2.COLOR_RGB2BGR)


    cv2.imshow('screen', result)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break

    end = time.time()
    print(end - start)
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            print(color(result[i,j]), end=' ')
        print()
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()