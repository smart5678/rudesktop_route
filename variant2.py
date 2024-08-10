import numpy as np
from PIL import Image


class Cursor:
    def __init__(self, x=0, y=0, direction='N'):
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


class Field:
    def __init__(self):
        self.points: dict[(int, int): int] = dict()
        self.points[(0, 0)] = 0


class Path:
    def __init__(self):
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.points: list[(int, int)] = [(0, 0)]

    def add_point(self, x, y):
        self.points.append((x, y))
        if x > self.max_x:
            self.max_x = x
        if x < self.min_x:
            self.min_x = x
        if y > self.max_y:
            self.max_y = y
        if y < self.min_y:
            self.min_y = y

    def plot(self):
        size_x = self.max_x - self.min_x + 1
        size_y = self.max_y - self.min_y + 1
        bitmap = np.zeros(
            (size_x, size_y),
            dtype=float
        )

        for point in self.points:
            bitmap[point[0] - self.min_x][point[1] - self.min_y] += 1

        bitmap = bitmap * 254 / bitmap.max()

        img = Image.fromarray(np.astype(bitmap, np.uint8), mode='L')
        img.show()


path = Path()
field = Field()
cursor = Cursor()

while True:
    if cursor.x <= -512 or cursor.x >= 512 or cursor.y <= -512 or cursor.y >= 512:
        break

    if field.points.get((cursor.x, cursor.y), 0) == 0:
        field.points[(cursor.x, cursor.y)] = 1
        cursor.rotate_right()
    else:
        field.points[(cursor.x, cursor.y)] = 0
        cursor.rotate_left()

    cursor.move()
    path.add_point(cursor.x, cursor.y)


print(f'Количество пройденных точек: {len(field.points)}')
print(f'Длинна маршрута: {len(path.points)}')
path.plot()