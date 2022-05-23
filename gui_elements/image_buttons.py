import pygame

pygame.init()


class ImageButton:
    def __init__(self, image, scale, pos, name=""):
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        self.pos = pos
        self.top_rect = self.image.get_rect(topleft=self.pos)
        self.name = name
        self.clicked = False

    def draw(self, screen):
        execute = False
        screen.blit(self.image, self.top_rect)

        mouseX, mouseY = pygame.mouse.get_pos()

        if self.top_rect.collidepoint((mouseX, mouseY)):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                execute = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return execute

    def get_name(self):
        return self.name
