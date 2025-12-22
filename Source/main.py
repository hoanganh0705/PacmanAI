import sys

import pygame
import random

from Algorithms.Ghost_Move import Ghost_move_level4
from Algorithms.SearchAgent import SearchAgent
from Object.Food import Food
from Object.Player import Player
from Object.Wall import Wall
from Utils.utils import DDX, isValid2
from constants import *
from Object.Menu import Menu, Button

# Initial Pygame --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PacMan')
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font_2 = pygame.font.SysFont('Comic Sans MS', 100)

class Game:
    def __init__(self, level=1, map_name=""):
        self.N = 0
        self.M = 0
        self.Score = 0
        self._state_PacMan = 0
        self._map = []
        self._wall = []
        self._road = []
        self._food = []
        self._ghost = []
        self._food_Position = []
        self._ghost_Position = []
        self._visited = []
        self.PacMan = None
        self.Level = level
        self.Map_name = map_name
        self.pac_can_move = True
        self.done = False
        self.is_moving = False
        self.timer = 0
        self.status = 0
        self.delay = GAME_DELAY
        self.result = []
        self.new_PacMan_Pos = []
        self._ghost_new_position = []

    def readMapInFile(self, map_name: str):
        f = open(map_name, "r")
        x = f.readline().split()
        self.N, self.M = int(x[0]), int(x[1])
        self._map = []
        for _ in range(self.N):
            line = f.readline().split()
            _m = []
            for j in range(self.M):
                _m.append(int(line[j]))
            self._map.append(_m)

        x = f.readline().split()
        MARGIN["TOP"] = max(0, (HEIGHT - self.N * SIZE_WALL) // 2)
        MARGIN["LEFT"] = max(0, (WIDTH - self.M * SIZE_WALL) // 2)
        self.PacMan = Player(int(x[0]), int(x[1]), IMAGE_PACMAN[0])

        f.close()

    def check_Object(self, row, col):
        if self._map[row][col] == WALL:
            self._wall.append(Wall(row, col, BLUE))
        else:
            pass  # hidden else later

        if self._map[row][col] == FOOD:
            self._food.append(Food(row, col, BLOCK_SIZE, BLOCK_SIZE, YELLOW))
            self._food_Position.append([row, col])

        if self._map[row][col] == MONSTER:
            self._ghost.append(Player(row, col, IMAGE_GHOST[len(self._ghost) % len(IMAGE_GHOST)]))
            self._ghost_Position.append([row, col])

    def initData(self):
        self.N = self.M = self.Score = self._state_PacMan = 0
        self._map = []
        self._wall = []
        self._road = []
        self._food = []
        self._ghost = []
        self._food_Position = []
        self._ghost_Position = []

        self.readMapInFile(map_name=self.Map_name)
        self._visited = [[0 for _ in range(self.M)] for _ in range(self.N)]

        for row in range(self.N):
            for col in range(self.M):
                self.check_Object(row, col)

    def Draw(self, _screen):
        for wall in self._wall:
            wall.draw(_screen)
        for road in self._road:
            road.draw(_screen)
        for food in self._food:
            food.draw(_screen)
        for ghost in self._ghost:
            ghost.draw(_screen)

        self.PacMan.draw(_screen)

        text_surface = my_font.render('Score: {Score}'.format(Score=self.Score), False, RED)
        screen.blit(text_surface, (0, 0))

    def generate_Ghost_new_position(self, _type: int = 0):
        _ghost_new_position = []
        if _type == 1:
            for idx in range(len(self._ghost)):
                [row, col] = self._ghost[idx].getRC()

                rnd = random.randint(0, 3)
                new_row, new_col = row + DDX[rnd][0], col + DDX[rnd][1]
                while not isValid2(self._map, new_row, new_col, self.N, self.M):
                    rnd = random.randint(0, 3)
                    new_row, new_col = row + DDX[rnd][0], col + DDX[rnd][1]

                _ghost_new_position.append([new_row, new_col])

        elif _type == 2:
            for idx in range(len(self._ghost)):
                [start_row, start_col] = self._ghost[idx].getRC()
                [end_row, end_col] = self.PacMan.getRC()
                _ghost_new_position.append(Ghost_move_level4(self._map, start_row, start_col, end_row, end_col, self.N, self.M))

        return _ghost_new_position

    def check_collision_ghost(self, pac_row=-1, pac_col=-1):
        Pac_pos = [pac_row, pac_col]
        if pac_row == -1:
            Pac_pos = self.PacMan.getRC()
        for g in self._ghost:
            Ghost_pos = g.getRC()
            if Pac_pos == Ghost_pos:
                return True
        return False

    def animate_entity_movement(self, entity, new_row, new_col):
        [old_row, old_col] = entity.getRC()
        if old_row < new_row:
            entity.move(1, 0)
        elif old_row > new_row:
            entity.move(-1, 0)
        elif old_col < new_col:
            entity.move(0, 1)
        elif old_col > new_col:
            entity.move(0, -1)

    def finalize_entity_position(self, entity, new_row, new_col):
        entity.setRC(new_row, new_col)

    def change_direction_PacMan(self, new_row, new_col):
        [current_row, current_col] = self.PacMan.getRC()
        self._state_PacMan = (self._state_PacMan + 1) % len(IMAGE_PACMAN)

        if new_row > current_row:
            self.PacMan.change_state(-90, IMAGE_PACMAN[self._state_PacMan])
        elif new_row < current_row:
            self.PacMan.change_state(90, IMAGE_PACMAN[self._state_PacMan])
        elif new_col > current_col:
            self.PacMan.change_state(0, IMAGE_PACMAN[self._state_PacMan])
        elif new_col < current_col:
            self.PacMan.change_state(180, IMAGE_PACMAN[self._state_PacMan])

    def randomPacManNewPos(self, row, col):
        for [d_r, d_c] in DDX:
            new_r, new_c = d_r + row, d_c + col
            if isValid2(self._map, new_r, new_c, self.N, self.M):
                return [new_r, new_c]

    def run(self):
        self._ghost_new_position = []
        self.result = []
        self.new_PacMan_Pos = []
        self.initData()
        self.pac_can_move = True

        self.done = False
        self.is_moving = False
        self.timer = 0

        self.status = 0
        self.delay = GAME_DELAY

        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    showMenu()
                    return

            if self.delay > 0:
                self.delay -= 1

            if self.delay <= 0:
                if self.is_moving:
                    self.timer += 1
                    # Ghost move
                    if len(self._ghost_new_position) > 0:
                        for idx in range(len(self._ghost)):
                            [old_row_Gho, old_col_Gho] = self._ghost[idx].getRC()
                            [new_row_Gho, new_col_Gho] = self._ghost_new_position[idx]

                            self.animate_entity_movement(self._ghost[idx], new_row_Gho, new_col_Gho)

                            if self.timer >= ANIMATION_DURATION:
                                self.finalize_entity_position(self._ghost[idx], new_row_Gho, new_col_Gho)

                                self._map[old_row_Gho][old_col_Gho] = EMPTY
                                self._map[new_row_Gho][new_col_Gho] = MONSTER

                                # check touch Food
                                for index in range(len(self._food)):
                                    [row_food, col_food] = self._food[index].getRC()
                                    if row_food == old_row_Gho and col_food == old_col_Gho:
                                        self._map[row_food][col_food] = FOOD

                    # Pacman move
                    if len(self.new_PacMan_Pos) > 0:
                        [old_row_Pac, old_col_Pac] = self.PacMan.getRC()
                        [new_row_Pac, new_col_Pac] = self.new_PacMan_Pos

                        self.animate_entity_movement(self.PacMan, new_row_Pac, new_col_Pac)

                        if self.timer >= ANIMATION_DURATION or self.PacMan.touch_New_RC(new_row_Pac, new_col_Pac):
                            self.is_moving = False
                            self.finalize_entity_position(self.PacMan, new_row_Pac, new_col_Pac)
                            self.Score -= 1

                            # check touch Food
                            for idx in range(len(self._food)):
                                [row_food, col_food] = self._food[idx].getRC()
                                if row_food == new_row_Pac and col_food == new_col_Pac:
                                    self._map[row_food][col_food] = EMPTY
                                    self._food.pop(idx)
                                    self._food_Position.pop(idx)
                                    self.Score += 20
                                    break
                            self.new_PacMan_Pos = []

                    if self.check_collision_ghost():
                        self.pac_can_move = False
                        self.done = True
                        self.status = -1

                    if len(self._food_Position) == 0:
                        self.status = 1
                        self.done = True

                    if self.timer >= ANIMATION_DURATION:
                        self.is_moving = False
                else:
                    # _type = [0:don't move(default), 1:Random, 2:A*]
                    if self.Level == 3:
                        self._ghost_new_position = self.generate_Ghost_new_position(_type=1)
                    elif self.Level == 4:
                        self._ghost_new_position = self.generate_Ghost_new_position(_type=2)
                    else:
                        self._ghost_new_position = self.generate_Ghost_new_position(_type=0)

                    self.is_moving = True
                    self.timer = 0

                    if not self.pac_can_move:
                        continue

                    [row, col] = self.PacMan.getRC()

                    # cài đặt thuật toán ở đây, thay đổi ALGORITHM trong file constants.py
                    # thuật toán chỉ cần trả về vị trí mới theo format [new_row, new_col] cho biến new_PacMan_Pos
                    # VD: new_PacMan_Pos = [4, 5]
                    # thuật toán sẽ được cài đặt trong folder Algorithms

                    search = SearchAgent(self._map, self._food_Position, row, col, self.N, self.M)
                    if self.Level == 1 or self.Level == 2:
                        if len(self.result) <= 0:
                            self.result = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL1"])
                            if len(self.result) > 0:
                                self.result.pop(0)
                                self.new_PacMan_Pos = self.result[0]

                        elif len(self.result) > 1:
                            self.result.pop(0)
                            self.new_PacMan_Pos = self.result[0]

                    elif self.Level == 3 and len(self._food_Position) > 0:
                        self.new_PacMan_Pos = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL3"], visited=self._visited)
                        self._visited[row][col] += 1

                    elif self.Level == 4 and len(self._food_Position) > 0:
                        self.new_PacMan_Pos = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL4"], depth=4, Score=self.Score)

                    if len(self._food_Position) > 0 and (len(self.new_PacMan_Pos) == 0 or [row, col] == self.new_PacMan_Pos):
                        self.new_PacMan_Pos = self.randomPacManNewPos(row, col)
                    if len(self.new_PacMan_Pos) > 0:
                        self.change_direction_PacMan(self.new_PacMan_Pos[0], self.new_PacMan_Pos[1])
                        if self.check_collision_ghost(self.new_PacMan_Pos[0], self.new_PacMan_Pos[1]):
                            self.pac_can_move = False
                            self.done = True
                            self.status = -1

            screen.fill(BLACK)
            self.Draw(screen)
            pygame.display.flip()
            clock.tick(FPS)

        handleEndGame(self.status, self.Score)


# ------------------------------------------


done_2 = False


def handleEndGame(status: int, Score: int):
    global done_2
    done_2 = False
    try:
        bg = pygame.image.load("images/gameover_bg.png")
        bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
        bg_w = pygame.image.load("images/win.jpg")
        bg_w = pygame.transform.scale(bg_w, (WIDTH, HEIGHT))
    except pygame.error as e:
        print(f"Error loading end game images: {e}")
        # Fallback: use solid colors
        bg = pygame.Surface((WIDTH, HEIGHT))
        bg.fill(RED)
        bg_w = pygame.Surface((WIDTH, HEIGHT))
        bg_w.fill(GREEN)

    def clickContinue():
        global done_2
        done_2 = True

    def clickQuit():
        pygame.quit()
        sys.exit(0)

    btnContinue = Button(WIDTH // 2 - 300, HEIGHT // 2 - 50, 200, 100, screen, "CONTINUE", clickContinue)
    btnQuit = Button(WIDTH // 2 + 50, HEIGHT // 2 - 50, 200, 100, screen, "QUIT", clickQuit)

    delay = GAME_DELAY
    while not done_2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if delay > 0:
            delay -= 1
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if status == -1:
            screen.blit(bg, (0, 0))
        else:
            screen.blit(bg_w, (0, 0))
            text_surface = my_font_2.render('Your Score: {Score}'.format(Score=Score), False, RED)
            screen.blit(text_surface, (WIDTH // 4 - 65, 10))

        btnQuit.process()
        btnContinue.process()

        pygame.display.flip()
        clock.tick(FPS)

    showMenu()


def showMenu():
    _menu = Menu(screen)
    level, map_name = _menu.run()
    game = Game(level=level, map_name=map_name)
    game.run()


if __name__ == '__main__':
    showMenu()
    pygame.quit()
