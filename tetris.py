import random
from ai import Ai
import pygame, sys
from utils import *


import pygame.freetype as ft


class Frame(object):
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250,25)
        self.default_font = ft.Font(FONT_PATH)

        self.screen = pygame.display.set_mode(WIN_RES)
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        pygame.time.set_timer(pygame.USEREVENT+1, 150)

    def draw_background(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pygame.draw.rect(self.screen, 'black',
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def disp_msg(self, msg, fcolor, topleft):
        x,y = topleft
        for line in msg.splitlines():
            self.default_font.render_to(self.screen, (x, y),
                text=line, fgcolor=fcolor, size=30 * 1.4, bgcolor=(0, 0, 0))
            y+=14

    def center_msg(self, msg):
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *WIN_RES))
        for i, line in enumerate(msg.splitlines()):
            text_surface, _ = self.default_font.render(line, (255, 0, 255), size=30)
            text_rect = text_surface.get_rect(center=(WIN_W // 2, WIN_H // 2))
            self.screen.blit(text_surface, text_rect)

    def draw_matrix(self, matrix, offset):
        off_x, off_y  = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen,COLORS[val],
                        pygame.Rect((off_x+x) * TILE_SIZE, (off_y+y) * TILE_SIZE,
                            TILE_SIZE, TILE_SIZE),0)

    def update(self, tetris):
        self.screen.fill(color=BG_COLOR) # set màu nền
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        if tetris.gameover:# or self.nbPiece >= maxPiece:
            self.center_msg("""Game Over!\nYour score: %dPress space to continue""" % tetris.score)
        else:
            if tetris.paused:
                self.center_msg("Paused")
            else:
                pygame.draw.line(self.screen, (255,255,255), (FIELD_RES[0]+1, 0), (FIELD_RES[0]+1, WIN_H-1))
                self.disp_msg("Next:", 'white', (FIELD_RES[0] + TILE_SIZE, TILE_SIZE))
                self.disp_msg('Score:', 'white', (FIELD_RES[0]+TILE_SIZE, TILE_SIZE*7))
                self.disp_msg(str(tetris.score), 'orange', (FIELD_RES[0] + TILE_SIZE, TILE_SIZE * 9))
                self.disp_msg('Level', 'white', (FIELD_RES[0] + TILE_SIZE, TILE_SIZE * 11))
                self.disp_msg(str(tetris.level), 'orange',(FIELD_RES[0] + TILE_SIZE*2, TILE_SIZE * 13))

                self.disp_msg('Lines', 'white',(FIELD_RES[0] + TILE_SIZE, TILE_SIZE * 15))
                self.disp_msg(str(tetris.lines), 'orange',(FIELD_RES[0] + TILE_SIZE*2, TILE_SIZE * 17))

                self.draw_background()
                self.draw_matrix(tetris.board, (0,0))
                self.draw_matrix(tetris.stone, (tetris.stone_x, tetris.stone_y))
                self.draw_matrix(tetris.next_stone, (FIELD_W+2,3))
        pygame.display.update()



class Tetris(object):
    
    def __init__(self, user, playWithUI, seed):
        self.user = user
        self.nbPiece = 0
        random.seed(seed)
        self.next_stone = SHAPES[random.randint(0, len(SHAPES)-1)]
        self.playWithUI = playWithUI
        self.fast_mode = not user 
        self.frame = Frame()
        
        self.init_game()

    def new_stone(self):
        self.stone = self.next_stone[:]
        self.next_stone = SHAPES[random.randint(0, len(SHAPES)-1)]
        self.stone_x = int(FIELD_W / 2 - len(self.stone[0])/2)
        self.stone_y = 0
        self.nbPiece += 1
        self.computed = False

        if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()
        self.level = 1
        self.score = 0
        self.lines = 0
        self.gameover = self.paused = False

    def add_cl_lines(self, n):
        linescores = [0, 40, 100, 300, 1200]
        self.lines += n
        self.score += linescores[n] * self.level
        if self.lines >= self.level*6:
            self.level += 1

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > FIELD_W - len(self.stone[0]):
                new_x = FIELD_W - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def drop(self, manual):
        if not self.gameover and not self.paused:
            self.score += 1 if manual else 0
            self.stone_y += 1
            if check_collision(self.board, self.stone, (self.stone_x, self.stone_y)):
                self.board = join_matrixes(self.board, self.stone, (self.stone_x, self.stone_y))
                self.new_stone()
                cleared_rows = 0

                for i, row in enumerate(self.board):
                    if 0 not in row:
                        self.board = remove_row(self.board, i)
                        cleared_rows += 1
                self.add_cl_lines(cleared_rows)
                return True
        return False

    def insta_drop(self):
        if not self.gameover and not self.paused:
            while(not self.drop(True)):
                pass

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board, new_stone, (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def quit(self):
        if self.playWithUI:
            self.frame.center_msg("Exiting...")
            pygame.display.update()
        sys.exit()

    def speed_up(self):
        self.fast_mode = not self.fast_mode
        if self.fast_mode:
            pygame.time.set_timer(pygame.USEREVENT+1, 2000)
            self.insta_drop()
        else:
            pygame.time.set_timer(pygame.USEREVENT+1, 25)

    def executes_moves(self, moves):
        key_actions = {
            'ESCAPE':    self.quit,
            'LEFT':        lambda:self.move(-1),
            'RIGHT':    lambda:self.move(+1),
            'DOWN':        lambda:self.drop(True),
            'UP':        self.rotate_stone,
            'p':        self.toggle_pause,
            'SPACE':    self.start_game,
            'RETURN':    self.insta_drop
        }
        for action in moves:
            key_actions[action]()

        if self.fast_mode:
            self.insta_drop()


    def run(self, weights, limitPiece):
        self.gameover = False
        self.paused = False

        #dont_burn_my_cpu = pygame.time.Clock()
        while 1:

            if self.nbPiece >= limitPiece and limitPiece > 0:
                self.gameover = True

            if self.playWithUI:
                self.frame.update(self)

            if self.gameover:
                return self.lines*1000 + self.nbPiece

            if self.playWithUI:
                if self.user:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.USEREVENT+1:
                            self.drop(False)
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_LEFT:
                                self.move(-1)
                            elif event.key == pygame.K_RIGHT:
                                self.move(1)
                            elif event.key == pygame.K_UP:
                                self.rotate_stone()
                            elif event.key == pygame.K_DOWN:
                                self.insta_drop()
                            elif event.key == pygame.K_p:
                                    self.toggle_pause()
                else:
                    if not self.computed:
                        self.computed = True
                        Ai.choose(self.board, self.stone, self.next_stone, self.stone_x, weights, self)

                    if self.playWithUI:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            elif event.type == pygame.USEREVENT+1:
                                self.drop(False)
                            elif event.type == pygame.QUIT:
                                    self.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == eval("pygame.K_s"):
                                    self.speed_up()
                                elif event.key == eval("pygame.K_p"):
                                    self.toggle_pause()
                                

            #dont_burn_my_cpu.tick(maxfps)


if __name__ == '__main__':
    # weights = [-7.079322515535496, 0.4084491347254038, -7.402904430910445, -2.7844637476685787] #21755 lignes
    weights = [-8.089717098754974, 4.901749501569805, -6.339604236296072, -3.51763821076156]
    result = Tetris(user=False, playWithUI=True, seed=4).run(weights, -1)
    # print(result)
    # app = Tetris(True, 5).run2()
