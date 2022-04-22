import pygame

pygame.init()

FPS = 60
background = pygame.image.load('assets/main_menu.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('red2')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 32)

pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def main_page():
    clock = pygame.time.Clock()

    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
