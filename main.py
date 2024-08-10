import numpy as np
from PIL import Image

field = np.zeros((1024, 1024), dtype=np.uint8)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cursor:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def rotate_left(self):
        if self.direction == 'N':
            self.direction = 'W'
        elif self.direction == 'W':
            self.direction = 'S'
        elif self.direction == 'S':
            self.direction = 'E'
        else:
            self.direction = 'N'

    def rotate_right(self):
        if self.direction == 'N':
            self.direction = 'E'
        elif self.direction == 'E':
            self.direction = 'S'
        elif self.direction == 'S':
            self.direction = 'W'
        else:
            self.direction = 'N'

    def move(self):
        if self.direction == 'N':
            self.y += 1
        elif self.direction == 'W':
            self.x -= 1
        elif self.direction == 'E':
            self.x += 1
        else:
            self.y -= 1


cursor = Cursor(512, 512, 'N')
path = np.zeros((1024, 1024), dtype=float)

while True:
    if cursor.x <= 0 or cursor.x >= 1023 or cursor.y <= 0 or cursor.y >= 1023:
        break

    if field[cursor.x][cursor.y] == 0:
        field[cursor.x][cursor.y] = 1
        cursor.rotate_right()
    else:
        field[cursor.x][cursor.y] = 0
        cursor.rotate_left()

    cursor.move()
    path[cursor.x][cursor.y] += 1


path = path * 254 / path.max()

img = Image.fromarray(np.astype(path, np.uint8), mode='L')
print(path.max())
img.show()
