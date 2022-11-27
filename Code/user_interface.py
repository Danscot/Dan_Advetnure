import pygame


class UI:

    def __init__(self, player, monster):

        self.player = player

        self.monster = monster

        self.monster_rect = self.monster.rect

        self.player_rect = self.player.rect

        self.screen = pygame.display.get_surface()

        self.health_bar_rect = pygame.Rect(0, 10, 160, 25)

        self.magic_bar_rect = pygame.Rect(0, 45, 140, 25)

        self.monster_bar = pygame.Rect(self.monster.position[0], self.monster.position[1], self.monster_rect.width + 100, self.monster_rect.height + 254)

    def show_bar(self, current, max_amount, bar_rect, color):

        # drawing bars background of the player

        pygame.draw.rect(self.screen, (60, 61, 63), bar_rect)

        # converting state to pixel

        ratio = current/max_amount

        current_width = bar_rect.width * ratio

        current_rect = bar_rect.copy()

        current_rect.width = current_width

        # drawing the bar

        pygame.draw.rect(self.screen, color, current_rect)

        pygame.draw.rect(self.screen, "#222222", bar_rect, 3)

    def display(self):

        # drawing the bar

        self.show_bar(self.player.health, self.player.stats["health"], self.health_bar_rect, "red")

        self.show_bar(self.player.magic, self.player.stats["magic"], self.magic_bar_rect, "Blue")



