import matplotlib
matplotlib.use("TkAgg")
from classes_of_game import Game, Car
import data


def main():
    challenge = data.challenges_array[0]
    game=Game(6)

    game.cars = [Car(
                    challenge[i]['x'],
                    challenge[i]['y'],
                    challenge[i]['number_of_car'],
                    game, challenge[i]['direction']
                )
                for i in range(len(challenge))]

    game.start()

main()
