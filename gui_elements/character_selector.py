import pygame
from gui_elements import image_buttons

pygame.init()


class CharacterSelector:
    def __init__(self, pos, images, scale, names):
        self.pos = pos
        self.images = images
        self.scale = scale
        self.names = names

        start_pos = self.pos
        pos = self.pos
        i = 1
        self.character_buttons = []

        for image in self.images:
            self.character_buttons.append(image_buttons.ImageButton(image, self.scale, pos, self.names[i - 1]))

            if i % 3 == 0:
                pos = (start_pos[0], pos[1] + 128)
            else:
                pos = (pos[0] + 128, pos[1])

            i += 1

    def draw(self, screen):
        for button in self.character_buttons:
            if button.draw(screen):
                return button.get_name()
