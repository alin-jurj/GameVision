import pygame
bkgreg = pygame.image.load('assets/regi.png')

def draw(screen):
    running=True
    while running:
        screen.fill("white")
        #screen.blit(bkgreg, (0, 0))
        #clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                pygame.quit()
        pygame.display.update()