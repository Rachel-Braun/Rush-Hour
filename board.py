import matplotlib
matplotlib.use("TkAgg")
from classes_of_game import Game, Car
import data






def main():
    challenge = data.challenges_array[1]
    game=Game(6)
    for i in range(len(challenge)):
        game.cars.append(Car(challenge[i]['x'], challenge[i]['y'], challenge[i]['number_of_car'], game, challenge[i]['direction']))

    game.start()

main()
