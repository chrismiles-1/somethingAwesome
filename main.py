#!/usr/bin/sh

# Author: Chris Miles
# Date:   8-Apr-2015
# License: Creative Commons

# Cellular Automaton Simulation:
# Conway's Game of Life (see: Wikipedia entry)
# Goals of the program:
#     1. allows editing of initial configurations of CGL
#     2. allows viewing and saving of initial seed
#     3. allows simulation of CGL based on initial seed
#     4. allows saving of each iteration as an image file (BMP?)

# DONE(TODO): allow editing of the board
# DONE(TODO): make the grid look nice
# DONE(TODO): save frame as image
# OBSOLETE(TODO): Check input of board, make sure it matches size specified
# DONE(TODO): Basic rules and applying the rules to a sample configuration
# DONE(TODO): Loading initial configurations
# DONE(TODO): Run simulations based on configurations
# DONE(TODO): use global (constants)
# DONE(TODO): check for the key events for loading and saving data
# DONE(TODO): draw status according to situation
# DONE(TODO): divide into 3 frames: board, status, controls

import copy

import pygame

import board


# globals, not constants but please don't modify
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 480
FPS = 60
TIMED_TEXT_LIFE = 5
CONTROL_PANEL_HEIGHT = 32
SIMULATION_PANEL_HEIGHT = 416
STATUS_PANEL_HEIGHT = 32
CELL_WIDTH = 5
CELL_HEIGHT = 5
CELL_GAP = 1
COLOR_WHITE = pygame.Color(255, 255, 255, 255)
COLOR_BLACK = pygame.Color(0, 0, 0, 255)
COLOR_GREY = pygame.Color(122, 122, 122, 255)


# use pygame.Font
class Text(object):
    def __init__(self, x, y, surface, text):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("arial", 13)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.surface = surface

    def draw(self):
        # draw onto the surface
        self.surface.blit(self.text, pygame.Rect(self.x, self.y, self.text.get_width(), self.text.get_height()))


class TimedText(Text):
    def __init__(self, x, y, surface, text, life_timer):
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("arial", 12)
        self.text = self.font.render(text, True, (0, 0, 0))
        self.surface = surface
        self.life_timer = life_timer  # how long this text will live for


class App(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.clock = pygame.time.Clock()

        # self.seed = [[0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0],
        #     [0, 1, 1, 1, 0],
        #     [0, 0, 0, 0, 0],
        #     [0, 0, 0, 0, 0]]

        self.board = board.LifeBoard()
        # self.board.set_board(self.seed)

        self.control_surface = self.screen.subsurface(pygame.Rect(0, 0, SCREEN_WIDTH, CONTROL_PANEL_HEIGHT))
        self.simulation_surface = self.screen.subsurface(pygame.Rect(0, CONTROL_PANEL_HEIGHT, SCREEN_WIDTH,
                                                                     SIMULATION_PANEL_HEIGHT))
        self.status_surface = self.screen.subsurface(pygame.Rect(0, CONTROL_PANEL_HEIGHT + SIMULATION_PANEL_HEIGHT,
                                                                 SCREEN_WIDTH, STATUS_PANEL_HEIGHT))

        self.texts = []
        self.status = None
        self.status_texts = {
            "loading": TimedText(0, 0, self.status_surface, "loading seed", TIMED_TEXT_LIFE),
            "saving": TimedText(0, 0, self.status_surface, "saving seed", TIMED_TEXT_LIFE),
            "screenshot": TimedText(0, 0, self.status_surface, "saving frame as bmp", TIMED_TEXT_LIFE)
        }
        self.cur_status_text = None

        # control texts
        self.control_hints = Text(0, 0, self.control_surface,
                                  "q: step simulation forward | w: save current frame | e:"
                                  "read a specified (hardcoded) frame | r: save current frame as image")

        self.board.load_seed("seedToLoad.csv")

    def run(self):
        self.screen.fill(COLOR_WHITE)

        while self.running:
            self.clock.tick(FPS)
            self.draw_grid()
            self.draw_cells()
            self.draw_edge()

            self.draw_controls()
            self.draw_status()

            pygame.display.flip()

            # need to draw first since screenshot will be just white otherwise

            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    # q: run simulation
                    # w: save current frame
                    # e: read a specified (hardcoded) frame
                    # r: save current frame as image
                    if event.key == pygame.K_q:
                        self.board.run()
                    if event.key == pygame.K_w:
                        self.board.save_seed('seedToSave.csv')
                        self.status = "saving"
                    if event.key == pygame.K_e:
                        self.board.load_seed('seedToLoad.csv')
                        self.status = "loading"
                    if event.key == pygame.K_r:
                        # save the simulation surface as a BMP
                        pygame.image.save(self.simulation_surface, "seed.bmp")
                        self.status = "screenshot"
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        # get position and change the board at the position
                        # do maths and make this correspond to the board position
                        # top bar and bottom bar are taken for the status
                        # the simulation surface are within x:0-600, y: 32-448
                        pos = pygame.mouse.get_pos()
                        # check its within the actual board space
                        if CONTROL_PANEL_HEIGHT <= pos[1] <= CONTROL_PANEL_HEIGHT + (
                            CELL_HEIGHT + CELL_GAP) * self.board.get_height():
                            if pos[0] <= (CELL_WIDTH + CELL_GAP) * self.board.get_width():
                                # within the board's surface
                                # translate to board x,y
                                x = pos[0] / (CELL_WIDTH + CELL_GAP)
                                y = (pos[1] - CONTROL_PANEL_HEIGHT) / (CELL_HEIGHT + CELL_GAP)
                                # print "x:", x
                                # print "y:", y

                                self.board.invert_cell(x, y)
                elif event.type == pygame.QUIT:
                    self.running = False

            # reset screen last
            self.screen.fill(COLOR_WHITE)

    def draw_status(self):
        if self.status is not None:
            self.cur_status_text = copy.copy(self.status_texts[self.status])
            self.status = None

        if self.cur_status_text is not None:
            self.cur_status_text.life_timer -= 1.0 / FPS
            if self.cur_status_text.life_timer <= 0:
                self.cur_status_text = None
            else:
                self.cur_status_text.draw()

    def draw_controls(self):
        self.control_hints.draw()

    def draw_grid(self):
        width = SCREEN_WIDTH
        height = SIMULATION_PANEL_HEIGHT
        step = CELL_WIDTH

        for w in xrange(step, width, step + 1):
            pygame.draw.line(self.simulation_surface, COLOR_GREY, (w, 0), (w, height))
        for h in xrange(step, height, step + 1):
            pygame.draw.line(self.simulation_surface, COLOR_GREY, (0, h), (width, h))

    def draw_edge(self):
        # print self.board.get_width(), self.board.get_height()
        pygame.draw.line(self.simulation_surface, COLOR_BLACK, (self.board.get_width() * (CELL_WIDTH + CELL_GAP), 0),
                         (self.board.get_width() * (CELL_WIDTH + CELL_GAP),
                          self.board.get_height() * (CELL_HEIGHT + CELL_GAP)))
        pygame.draw.line(self.simulation_surface, COLOR_BLACK, (0, self.board.get_height() * (CELL_HEIGHT + CELL_GAP)),
                         (self.board.get_width() * (CELL_WIDTH + CELL_GAP),
                          self.board.get_height() * (CELL_HEIGHT + CELL_GAP)))

    def draw_cells(self):
        height = self.board.get_height()
        width = self.board.get_width()

        step = CELL_WIDTH + CELL_GAP
        draw_x = 0
        draw_y = 0

        for row in self.board.get_board():
            for item in row:
                if item == 1:
                    pygame.draw.rect(self.simulation_surface, COLOR_BLACK,
                                     pygame.Rect((draw_x, draw_y, CELL_WIDTH, CELL_HEIGHT)))
                draw_x += step
            draw_y += step
            draw_x = 0

            # following code causes row-column inverse bug. above code solves it
            # for row_count in range(height):
            #     for column_count in range(width):
            #         if self.board.get_board()[column_count][row_count] == 1:
            #             pygame.draw.rect(self.simulation_surface, COLOR_BLACK,
            #                              pygame.Rect((draw_x, draw_y, CELL_WIDTH, CELL_HEIGHT)))
            #         # draw item
            #         # get new cell
            #         # draw cell in requested locations
            #         # done
            #         draw_x += step
            #     draw_y += step
            #     draw_x = 0


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
