'''
Programa final del agente que juega al snake
'''
from time import sleep
import cv2
from mss import mss
import numpy as np
import pyautogui
from PIL import Image
import signal

bounding_box = {'top': 168, 'left': 28, 'width': 543, 'height': 479} # Joseph
#bounding_box = {'top': 202, 'left': 30, 'width': 542, 'height': 480} # Sebastian
#bounding_box = {'top': 167, 'left': 28, 'width': 544, 'height': 481} # Universidad

class Agent_snake():
    # Smart agent structure: sensor, program, actuator ******
    def __init__(self) -> None:
        self.initial_state()

    def sensor(self) -> tuple:
        '''
        Sensor obtains only the apple position
        '''
        # If is the first time, return the default apple position
        if self.start:
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
                        matrix[i][j] = 2
                        return (i, j)

    def actuator(self, stack, nodes) -> None:
        i = len(stack)-1
        j = 0
        while nodes:
            with mss() as sct:
                img = np.array(sct.grab(bounding_box))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(img)

                imgSmall = img_pil.resize((17,15), resample=Image.BILINEAR)
                result = cv2.cvtColor(np.array(imgSmall), cv2.COLOR_RGB2BGR)
                val = result[nodes[j]]
                if self.start:
                    self.start = False
                    pyautogui.press(stack[i])
                    j += 1
                    i -= 1
                else:
                    print(j)
                    print(nodes[j])
                    print(val)
                    
                    if max(val) == val[0]:
                        pyautogui.press(stack[i])
                        i -= 1
                        j += 1
                        if j == len(nodes):
                            self.score += 1
                            return        
        

    def program(self, perception) -> dict:
        # needs the apple positions by perception, and use the memory to find the best path
        self.set_apple(perception)
        print(self.memory)
        print(self.head)
        print(self.apple)
        print(self.score)
        path = self.path(self.memory, self.head, self.apple)
        if path is None:
            print('*'*100,'\nNo hay camino\n', '*'*100)
        self.update_memory(path)
        return path

    def run(self):
        while True:
            perseption = self.sensor()            
            path = self.program(perseption)
            instruct, nodes = self.instructions(path)
            print(instruct)
            print(nodes)
            self.actuator(instruct, nodes)
            # This funtion wait until the apple change of position
            while(self.apple_in_position()):
                pass

    # Auxiliar methods

    # Temporal method for testing
    def apple_in_position(self):
        with mss() as sct:
            img = np.array(sct.grab(bounding_box))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img)

        imgSmall = img_pil.resize((17,15), resample=Image.BILINEAR)
        result = cv2.cvtColor(np.array(imgSmall), cv2.COLOR_RGB2BGR)
        val = result[self.apple]
        print(val)
        if max(val) == val[2]:
            return True
        else:
            return False 

    def initial_state(self):
        # initial state of the snake
        self.start = True
        self.score = 0
        self.memory = np.zeros(shape=(15, 17))
        self.memory[7][1] = 1
        self.memory[7][2] = 2
        self.memory[7][3] = 3
        self.memory[7][4] = 4
        self.head = (7, 4)
        self.prev_head = (7, 4)
        self.apple = (7, 12)
        self.memory[self.apple] = -1

    def direction(self, node, neighbor) -> str:
        # node and neighbor are tuples (x, y)
        if node[0] == neighbor[0]:
            if node[1] > neighbor[1]:
                return 'right'
            else:
                return 'left'
        else:
            if node[0] > neighbor[0]:
                return 'down'
            else:
                return 'up'
            
    def instructions(self, instruct):
        # instruct is a dictionary with the path to the apple
        current = self.head
        stackIns = []
        stackNod = []
        aux = self.prev_head
        while current != self.prev_head:
            stackIns.append(self.direction(current, instruct[current]))
            stackNod.append(current)
            current = instruct[current]
        self.prev_head = self.head
        stackNod.append(aux)
        stackNod.reverse()
        return stackIns, stackNod
    
    def set_apple(self, apple):
        self.apple = apple
        self.memory[apple] = -1

    def np_where(self, matrix, value) -> tuple:
        return (np.where(matrix == value)[0][0], np.where(matrix == value)[1][0])

    def manhattan_distance(self, a, b) -> int:
        # a & b are tuples (x, y) of two points
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, matrix, node, g_score) -> list:
        neighbors = []
        if node[0] != 0:
            if matrix[node[0] - 1][node[1]] - g_score - 1 <= 0:
                neighbors.append((node[0] - 1, node[1]))
        if node[0] != 14:
            if matrix[node[0] + 1][node[1]] - g_score - 1 <= 0:
                neighbors.append((node[0] + 1, node[1]))
        if node[1] != 0:
            if matrix[node[0]][node[1] - 1] - g_score - 1 <= 0:
                neighbors.append((node[0], node[1] - 1))
        if node[1] != 16:
            if matrix[node[0]][node[1] + 1] - g_score - 1 <= 0:
                neighbors.append((node[0], node[1] + 1))
        return neighbors

    def path(self, matrix, start, goal) -> dict:
        tree = {}
        closed_set = set()
        open_set = set()
        g_score = {}
        f_score = {}
        open_set.add(start)
        g_score[start] = 0
        f_score[start] = self.manhattan_distance(start, goal)
        while open_set:
            current = min(open_set, key=lambda o: f_score[o])
            if current == goal:
                return tree
            closed_set.add(current)
            open_set.remove(current)
            for neighbor in self.neighbors(matrix, current, g_score[current]):
                if neighbor in closed_set:
                    continue
                tentative_g_score = g_score[current] + 1
                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue
                tree[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.manhattan_distance(neighbor, goal)
        return None
    
    def update_memory(self, path):
        # use the path to update the ubications of the snake

        # add snake nodes to the path
        node_tmp = self.head
        value = self.score + 4
        snake = dict()
        while True:
            new_node = self.snake_neighbor(node_tmp, value)
            if new_node:
                snake[node_tmp] = new_node
                value -= 1
                self.memory[node_tmp] = 0
                node_tmp = new_node
            else:
                self.memory[node_tmp] = 0
                tail = node_tmp
                break

        # update the memory and the head

        current = self.apple
        value = self.score + 5
        while current != self.head:
            self.memory[current] = value
            if value != 0:
                value -= 1
            current = path[current]
        
        while current != tail:
            self.memory[current] = value
            if value != 0:
                value -= 1
            else:
                break
            current = snake[current]
        self.head = self.apple
    
    def snake_neighbor(self, node, value) -> tuple:
        # return a node with a menor value than the node given
        if node[0] != 0:
            if 0 < self.memory[node[0] - 1][node[1]] == value - 1:
                return (node[0] - 1, node[1])
        if node[0] != 14:
            if 0 < self.memory[node[0] + 1][node[1]] == value - 1:
                return (node[0] + 1, node[1])
        if node[1] != 0:
            if 0 < self.memory[node[0]][node[1] - 1] == value - 1:
                return (node[0], node[1] - 1)
        if node[1] != 16:
            if 0 < self.memory[node[0]][node[1] + 1] == value - 1:
                return (node[0], node[1] + 1)
        return None

if __name__ == '__main__':
    with pyautogui.hold('alt'):
        pyautogui.press('tab')
    agent = Agent_snake()
    agent.run()
