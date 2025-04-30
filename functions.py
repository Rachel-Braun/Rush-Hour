import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from PIL import Image, ImageSequence, ImageDraw
from matplotlib import animation


def end(game):
    gif = Image.open(r"D:\Users\User\Pictures\כפיים.gif")
    frames = [frame.copy() for frame in ImageSequence.Iterator(gif)]

    im = game.ax.imshow(frames[0])
    game.ax.axis('off')

    def update(i):
        im.set_data(frames[i])
        return [im]

    game.ani = animation.FuncAnimation(game.fig, update, frames=len(frames), interval=gif.info.get('duration', 100))
    plt.show()


def draw_ellipse_direction(draw, game, constant_index, index, coefficient, condition):
    while condition(index):
        if game.boardIsFilled[index][constant_index]:
            break

        x, y = game.xValues[index], game.yValues[constant_index]
        draw.ellipse((x + 15, y + 15, x + 108, y + 108), fill="white")
        index += coefficient


def draw_ellipse_not_direction(draw, game, constant_index, index, coefficient, condition):
    while condition(index):
        if game.boardIsFilled[constant_index][index]:
            break

        x, y = game.xValues[constant_index], game.yValues[index]
        draw.ellipse((x + 15, y + 15, x + 108, y + 108), fill="white")
        index += coefficient

def do_buttons(game, car):
    draw = ImageDraw.Draw(game.BACKGROUND)

    if car.direction:
        draw_ellipse_direction(draw, game, constant_index=car.y, index=car.x - 1, coefficient=-1, condition=lambda index:index>=0)
        draw_ellipse_direction(draw, game, constant_index=car.y, index= car.x + car.length, coefficient=1, condition=lambda index:index<6)
    else:
        draw_ellipse_not_direction(draw, game, constant_index=car.x, index=car.y - 1, coefficient=-1, condition=lambda index:index>=0)
        draw_ellipse_not_direction(draw, game, constant_index=car.x, index=car.y + car.length, coefficient=1, condition=lambda index:index<6)


# פונקציית ציור
def draw_board(game):
    temp = game.BACKGROUND.copy()
    for car in game.cars:
        temp.paste(car.img, tuple([game.xValues[car.x], game.yValues[car.y]]), car.img)
    return temp


def reset(game):
    for car in game.cars:
        if car.selected:
            car.selected = False
    game.BACKGROUND = game.background_copy.copy()


def is_x_and_y_in_car(game, car, x, y):
    return game.xValues[car.x] <= x <= game.xValues[car.x] + car.img.width and \
           game.yValues[car.y] <= y <= game.yValues[car.y] + car.img.height

# עדכון התצוגה
def update_display(game):
    game.ax.clear()
    game.ax.imshow(draw_board(game))
    game.ax.set_title("RUSH HOUR")
    game.ax.axis('off')
    game.fig.canvas.draw()
    plt.show()


# תגובה ללחיצת עכבר
def onclick(event, game):
    if event.xdata is None or event.ydata is None:
        return

    x, y = int(event.xdata), int(event.ydata)
    car_selected = next((car for car in game.cars if is_x_and_y_in_car(game, car, x, y)), None)

    if car_selected is not None:
        reset(game)
        car_selected.selected = True
        do_buttons(game, car_selected)
        update_display(game)
        return

    car_selected = next((car for car in game.cars if car.selected), None)
    if car_selected is None or game.BACKGROUND.getpixel([x, y]) != (255, 255, 255, 255):
        reset(game)
        update_display(game)
        return

    # אם המכונית נבחרה ולחצו במקום חדש – הזז את המכונית
    x, y = get_value(game, x, y, car_selected)

    if x == -1 or y == -1:
        return

    if car_selected.i == 0 and x == 4 and y == 2:
        end(game)
        return

    game.sign_is_filled(car_selected, x, y)
    car_selected.x = x
    car_selected.y = y
    reset(game)
    update_display(game)
    return


def get_value(game, x, y, car):
    if x < game.xValues[0] or y < game.yValues[0]:
        return -1, -1
    # x
    if car.direction:
        for i in range(len(game.xValues)):
            if game.xValues[i] > x:
                return i - 1 if i <= car.x else i - car.length, car.y

        return len(game.xValues) - car.length if game.xValues[-1] + car.img.height > x else -1, car.y
    # y
    for i in range(len(game.yValues)):
        if game.yValues[i] > y:
            return car.x, i - 1 if i <= car.y else i - car.length

    return car.x, len(game.yValues) - car.length if game.yValues[-1] + car.img.height > y else -1
