import pygame

from Code.map import MapManager

from Code.entity import *

from Code.texteditor import TextEditor

from Code.user_interface import UI

pygame.init()


class Game:

    def __init__(self):

        # creating the screen surface

        self.screen = pygame.display.set_mode((0, 0))

        pygame.display.set_caption("Dan_Adventure")

        # initializing the player

        self.player = Player("player", 0, 0)

        self.monsters = Enemy("enemy", self.player, "enemy1")

        # initializing the map

        self.map_manager = MapManager(self.player)

        # initializing text

        self.text = TextEditor()

        # initializing the ui

        self.ui = UI(self.player, self.monsters)

    def update(self):

        self.map_manager.update()

    def handle_input(self):

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()

        elif pressed[pygame.K_DOWN]:
            self.player.move_down()

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def run(self):

        # game loop

        running = True

        clock = pygame.time.Clock()

        while running:

            self.player.save_position()

            self.handle_input()

            self.update()

            self.map_manager.draw()

            self.text.render(self.screen)

            self.ui.display()

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE:

                        self.map_manager.check_npc_collision(self.text)
            clock.tick(60)

        pygame.quit()
