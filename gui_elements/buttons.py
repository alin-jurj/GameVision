import pygame

pygame.init()


class Button:
    def __init__(self, text, width, height, pos, font):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#2C7950'
        self.text_surf = font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        self.clicked = False

    def draw(self, screen):
        execute = False
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=10)
        screen.blit(self.text_surf, self.text_rect)

        mouseX, mouseY = pygame.mouse.get_pos()

        if self.top_rect.collidepoint((mouseX, mouseY)):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                execute = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return execute
