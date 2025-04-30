import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from data import PATH
import functions

matplotlib.use("TkAgg")


class Car:
    def __init__(self, x, y, i, game, direction=0):
        self.x = x
        self.y = y
        self.i = i
        self.direction = direction
        self.selected = False
        self.img = Image.open(PATH + str(i) + '.png').convert("RGBA")
        self.img = self.img.resize((int(self.img.width * (7 / 6)),
                                   int(self.img.height * (7 / 6))),
                                   Image.NEAREST)
        self.length = 2 if i < 9 else 3
        if self.length == 3:
            self.img = self.img.resize((self.img.width, self.img.height - 25),
                                       Image.NEAREST)

        if direction:
            self.img = self.img.rotate(270, expand=True)
            for i in range(self.length):
                game.boardIsFilled[x + i][y] = True
        else:
            for i in range(self.length):
                game.boardIsFilled[x][y + i] = True


class Game:
    def __init__(self, size_of_board):
        self.size_of_board = size_of_board
        self.xValues = [112, 244, 379, 511, 644, 778]
        self.yValues = [125, 256, 384, 517, 646, 775]
        self.BACKGROUND = Image.open("D:\\Users\\User\\Downloads\\49c2442b-5584-47dc-b862-8b6e59c797bb.png").convert(
            "RGBA")
        self.background_copy = self.BACKGROUND.copy()
        self.boardIsFilled = [[False] * 6 for _ in range(6)]
        self.cars = []
        self.fig, self.ax = plt.subplots()

    def start(self):
        cid = self.fig.canvas.mpl_connect('button_press_event', lambda event: functions.onclick(event, self))
        functions.update_display(self)

    def sign_is_filled(self, car, new_x, new_y):
        if car.direction:
            for i in range(car.x, car.x + car.length):
                self.boardIsFilled[i][car.y] = False
            for i in range(new_x, new_x + car.length):
                self.boardIsFilled[i][new_y] = True
        else:
            for i in range(car.y, car.y + car.length):
                self.boardIsFilled[car.x][i] = False
            for i in range(new_y, new_y + car.length):
                self.boardIsFilled[new_x][i] = True

