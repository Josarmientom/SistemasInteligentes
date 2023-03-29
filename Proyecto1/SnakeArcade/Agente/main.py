'''
Programa final del agente que juega al snake
'''
from time import sleep
import cv2
from mss import mss
import numpy as np
import pyautogui

#bounding_box = {'top': 200, 'left': 0, 'width': 900, 'height': 800} # Joseph
bounding_box = {'top': 202, 'left': 30, 'width': 542, 'height': 480} # Sebastian
#bounding_box = {'top': 167, 'left': 28, 'width': 544, 'height': 481} # universidad

class Agent_snake():
    # Smart agent structure: sensor, program, actuator ******
    def __init__(self) -> None:
        self.initial_state()

    def sensor(self) -> tuple:
        '''
        Sensor obtains only the apple position
        '''
         # take screenshot with mss
        with mss() as sct:
            img = np.array(sct.grab(bounding_box)) 
        # obtain the matrix of the image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # travel the image and find the apple
        i_div = bounding_box['height'] // (15)
        j_div = bounding_box['width']// (17)
        for i in range(0, 15):
            for j in range(0, 17):
                tmp = img[i*i_div + i_div//2, j*j_div + j_div//2]
                if max(tmp) == tmp[0]:
                    # apple found
                    return (i, j)
        return self.apple

    def actuator(self, instruct) -> None:
        # instruct is a dictionary with the path to the apple
        current = self.head
        stack = []
        while current != self.prev_head:
            stack.append(self.direction(current, instruct[current]))
            current = instruct[current]
        self.prev_head = self.head

        for i in stack[::-1]:
            pyautogui.press(i)
            sleep(0.001)

    def program(self, perception) -> dict:
        # needs the apple positions by perception, and use the memory to find the best path
        self.set_apple(perception)
        print(self.memory)
        print(self.head)
        print(self.apple)
        print(self.score)
        path = self.path(self.memory, self.head, self.apple)
        self.update_memory(path)
        return path

    def run(self):
        while True:
            perseption = self.sensor()
            path = self.program(perseption)
            self.actuator(path)

    # Auxiliar methods

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
    
    def set_apple(self, apple):
        self.apple = apple
        self.memory[apple] = -1

    def np_where(self, matrix, value) -> tuple:
        return (np.where(matrix == value)[0][0], np.where(matrix == value)[1][0])

    def manhattan_distance(self, a, b) -> int:
        # a & b are tuples (x, y) of two points
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, matrix, node) -> list:
        neighbors = []
        if node[0] != 0:
            if matrix[node[0] - 1][node[1]] <= 0:
                neighbors.append((node[0] - 1, node[1]))
        if node[0] != 14:
            if matrix[node[0] + 1][node[1]] <= 0:
                neighbors.append((node[0] + 1, node[1]))
        if node[1] != 0:
            if matrix[node[0]][node[1] - 1] <= 0:
                neighbors.append((node[0], node[1] - 1))
        if node[1] != 16:
            if matrix[node[0]][node[1] + 1] <= 0:
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
            for neighbor in self.neighbors(matrix, current):
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
        while True:
            new_node = self.snake_neighbor(node_tmp, value)
            if new_node:
                path[node_tmp] = new_node
                value -= 1
                node_tmp = new_node
            else:
                tail = node_tmp
                break

        # update the memory and the head
        self.head = self.apple
        current = self.head
        value = self.score + 5
        while True:
            self.memory[current] = value
            if value != 0:
                value -= 1
            if current == tail:
                break
            current = path[current]
    
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
    sleep(2)
    agent = Agent_snake()
    agent.run()
