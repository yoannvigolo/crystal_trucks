# transcription of the original game.c/game.h files

import io
from contextlib import redirect_stdout

MAX_NB_TRUCKS = 9
MAX_WIDTH = 30
MAX_HEIGHT = 20

# https://en.wikipedia.org/wiki/Linear_congruential_generator glibc
_MODULUS = 1 << 31
_MULTIPLIER = 1103515245
_INCREMENT = 12345

_prng = 0
cristals = []
f = open("sample.txt", "w")


def srand(seed: int) -> None:
    global _prng
    _prng = seed


def rand() -> int:
    global _prng
    _prng = (_MULTIPLIER * _prng + _INCREMENT) % _MODULUS
    return _prng & 0x7FFFFFFF


def init_game(seed: int):
    srand(seed)
    global cristals
    nb_trucks = rand() % (MAX_NB_TRUCKS - 1) + 1
    width = rand() % (MAX_WIDTH - 10) + 10
    height = rand() % (MAX_HEIGHT - 10) + 10
    for y in range(height):
        for x in range(width):
            nb_crystals = rand() % 5
            if nb_crystals < 3:
                cristals.append(nb_crystals)
            else:
                cristals.append(0)

    f.write(f"trucks: {nb_trucks}\n")
    f.write(f"width: {width}\n")
    f.write(f"height: {height}\n")

    f.write("### Grid ###\n")
    for y in range(height):
        for x in range(width):
            nb_cristals = cristals[x + y * width]
            if nb_cristals:
                f.write(str(nb_cristals))
            else:
                f.write(" ")
        f.write("\n")

    f.write("### End Grid ###\n\n")
    f.write("Start!\n")

    # Create command
    roundNbr = 2
    lineEnd = False
    writeMove(1, 1, 0, 0)
    for y in range(height):
        for x in range(width):
            nb_cristals = cristals[x + y * width]
            print(x)
            if not lineEnd:
                if x == (width - 1):
                    lineEnd = True
                    writeMove(roundNbr, 1, x, y+1)
                    roundNbr += 1

                if posContainCristal(x, y, width):
                    writeDig(roundNbr, 1, x, y)
                    roundNbr += 1
                    writeMove(roundNbr, 1, x+1, y)
                    roundNbr += 1
                else:
                    writeMove(roundNbr, 1, x+1, y)
                    roundNbr += 1

            else:
                if x == 0:
                    lineEnd = False
                    writeMove(roundNbr, 1, x, y+1)
                    roundNbr += 1

                if nb_cristals:
                    f.write(f"{roundNbr} DIG 1 {x} {y}\n")
                    roundNbr += 1
                    writeMove(roundNbr, 1, x - 1, y)
                    roundNbr += 1
                else:
                    writeMove(roundNbr, 1, x - 1, y)
                    roundNbr += 1


def posContainCristal(xTruckPos, yTruckPos, mapWidth):
    nb_cristals = cristals[xTruckPos + yTruckPos * mapWidth]
    if nb_cristals:
        return True
    else:
        return False


def writeDig(roundNbr, truckNbr, xPos, yPos):
    f.write(f"{roundNbr} DIG {truckNbr} {xPos} {yPos}\n")


def writeMove(roundNbr, truckNbr, xPos, yPos):
    f.write(f"{roundNbr} MOVE {truckNbr} {xPos} {yPos}\n")


def display_cristals(width, height, cristals):
    print("\n### Grid ###")
    for y in range(height):
        for x in range(width):
            nb_cristals = cristals[x + y * width]
            if nb_cristals:
                print(nb_cristals, end="")
            else:
                print(" ", end="")
        print()
    print("### End Grid ###")
