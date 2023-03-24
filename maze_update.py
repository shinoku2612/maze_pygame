import random
import pygame
import json
from maze_displayer import display, load_JSON_file, BOARD_SIZE

WINDOW = pygame.display.set_mode(BOARD_SIZE)


def load_text_file(file_name):
    file = open(file_name + '.txt', 'r')
    data = file.readlines()
    file.close()
    return data


def update_JSON_file(file_name, new_JSON):
    file = open(file_name + '.json', 'w')
    file.write(new_JSON)
    file.close()


def play():
    ACTION_LIST = load_text_file('action')
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for action in ACTION_LIST:
            maze = load_JSON_file('maze_metadata')
            pygame.time.wait(100)
            display(WINDOW, maze)

            WIDTH, HEIGHT, OBSTACLES, BOT, COIN = maze.values()
            action = action.strip()
            if action == "down":
                BOT[0] += 1
            elif action == "up":
                BOT[0] -= 1
            elif action == "left":
                BOT[1] -= 1
            elif action == "right":
                BOT[1] += 1
            else:
                continue

            if BOT == COIN:

                # Get new random position of coin
                NEW_COIN_Y = random.randint(0, HEIGHT)
                NEW_COIN_X = random.randint(0, WIDTH)

                # If this coordinate is in obstacle list, do it again
                while ([NEW_COIN_Y, NEW_COIN_X] in maze['obstacles']):
                    NEW_COIN_Y = random.randint(0, HEIGHT)
                    NEW_COIN_X = random.randint(0, WIDTH)

                COIN = [NEW_COIN_Y, NEW_COIN_X]
                pygame.time.delay(5000)

            NEW_MAZE = {
                "width": WIDTH,
                "height": HEIGHT,
                "obstacles": OBSTACLES,
                "bot": BOT,
                "coin": COIN
            }
            json_maze = json.dumps(NEW_MAZE)
            update_JSON_file('maze_metadata', json_maze)


if __name__ == "__main__":
    play()
