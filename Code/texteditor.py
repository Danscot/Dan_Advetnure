
import pygame


class TextEditor:

    def __init__(self):

        self.box = pygame.image.load("../Assets/dialog_box.png")

        self.x_position = 700

        self.y_position = 100

        self.box = pygame.transform.scale(self.box, (self.x_position, self.y_position))

        self.texts = []

        self.text_index = 0

        self.letter_index = 0

        self.font = pygame.font.Font("../Assets/dialog_font.ttf", 24)

        self.reading = False

    def render(self, screen):

        if self.reading:

            self.letter_index += 1

            if self.letter_index >= len(self.texts[self.text_index]):

                self.letter_index = self.letter_index

            screen.blit(self.box, (0, 0))

            text = self.font.render(self.texts[self.text_index][0:self.letter_index], False, (0, 0, 0))

            screen.blit(text, (self.x_position - 600, self.y_position - 70))

    def execute(self, dialog=[]):

        if self.reading:

            self.next_text()

        else:

            self.reading = True

            self.text_index = 0

            self.texts = dialog

    def next_text(self):

        self.text_index += 1

        self.letter_index = 0

        if self.text_index >= len(self.texts):

            self.reading = False

