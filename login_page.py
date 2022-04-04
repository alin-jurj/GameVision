import pygame

pygame.init()
clock = pygame.time.Clock()
color = pygame.Color('gray99')
FONT = pygame.font.Font(None, 32)

FPS = 60
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class InputBox:

    def __init__(self, x, y, height, width, text='', hidden=False):
        self.rect = pygame.Rect(x, y, height, width)
        self.color = color
        self.text = text
        self.hidden = hidden
        if self.hidden is False:
            self.text_surface = FONT.render(text, True, color)
        else:
            self.text_surface = FONT.render(len(text) * '*', True, color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN:
            if self.active is True:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.key == pygame.K_RETURN:
                        print(self.text)
                        self.text = ''
                    else:
                        self.text = self.text + event.unicode

        if self.hidden is False:
            self.text_surface = FONT.render(self.text, True, color)
        else:
            self.text_surface = FONT.render(len(self.text) * '*', True, color)

    def draw(self, screen, background, boxes=[]):
        for box in boxes:
            box.draw(screen, background)
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text

    def reset_text(self):
        self.text = ''
