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


def do_buttons(game, car):
    draw = ImageDraw.Draw(game.BACKGROUND)
    # x, y = car.x, car.y

    if car.direction:
        start = car.x - 1
        while start >= 0:
            if game.boardIsFilled[start][car.y]:
                break

            x, y = game.xValues[start], game.yValues[car.y]
            draw.ellipse((x + 15, y + 15, x + 108, y + 108), fill="white")
            start -= 1
        start = car.x + car.length
        while start < 6:
            if game.boardIsFilled[start][car.y]:
                break

            x, y = game.xValues[start], game.yValues[car.y]
            draw.ellipse((x + 15, y + 15, x + 108, y + 108), fill="white")
            start += 1
    else:
        start = car.y - 1
        while start >= 0:
            if game.boardIsFilled[car.x][start]:
                break

            x, y = game.xValues[car.x], game.yValues[start]
            draw.ellipse((x + 15, y + 15, x + 108, y + 108), fill="white")
            start -= 1
        start = car.y + car.length
        while start < 6:
            if game.boardIsFilled[car.x][start]:
                break

            x, y = game.xValues[car.x], game.yValues[start]
            draw.ellipse((x + 15, y + 15, x + 108, y + 108), fill="white")
            start += 1


# פונקציית ציור
def draw_board(game):
    temp = game.BACKGROUND.copy()
    for car in game.cars:
        temp.paste(car.img, tuple([game.xValues[car.x], game.yValues[car.y]]), car.img)
    return temp


def reset(game):
    for car1 in game.cars:
        if car1.car_selected['active']:
            car1.car_selected['active'] = False
    game.BACKGROUND = game.background_copy.copy()


# תגובה ללחיצת עכבר
def onclick(event, game):
    if event.xdata is None or event.ydata is None:
        return

    x, y = int(event.xdata), int(event.ydata)
    for car in game.cars:
        # אם לחצו על המכונית – הפוך ל־selected
        if (game.xValues[car.x] <= x <= game.xValues[car.x] + car.img.width and
                game.yValues[car.y] <= y <= game.yValues[car.y] + car.img.height):
            reset(game)
            car.car_selected["active"] = True
            do_buttons(game, car)
            game.update_display()
            print("מכונית נבחרה", car.x)
            print("מכונית נבחרה", car.y)
            return

    for car in game.cars:
        if car.car_selected["active"]:
            print(game.BACKGROUND.getpixel([x, y]))
            if game.BACKGROUND.getpixel([x, y]) != (255, 255, 255, 255):
                reset(game)
                game.update_display()
                return
            # אם המכונית נבחרה ולחצו במקום חדש – הזז את המכונית
            x, y = get_value(game, x, y, car)

            if x == -1 or y == -1: return
            if car.i == 0 and x == 4 and y == 2:
                end(game)
                return
            # boardIsFilled
            game.signIsFillled(car, x, y)

            reset(game)

            car.x = x
            car.y = y
            car.car_selected["active"] = False
            game.update_display()
            return
    reset(game)


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
