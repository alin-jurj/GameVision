import pygame
import login_page

pygame.init()

FPS = 60
YELLOW_SPACESHIP_IMAGE = pygame.image.load('assets/monster.png')
background = pygame.image.load('assets/background_login_resized.png')
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def main():
    clock = pygame.time.Clock()

    input_box1 = login_page.InputBox(WIDTH / 2.4, HEIGHT / 1.7, 220, 30)
    input_box2 = login_page.InputBox(WIDTH / 2.4, HEIGHT / 1.5, 220, 30, hidden=True)
    input_boxes = [input_box1, input_box2]

    login_button = pygame.Rect(WIDTH / 2.4, HEIGHT / 1.3, 220, 30)

    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        mouseX, mouseY = pygame.mouse.get_pos()

        if login_button.collidepoint((mouseX, mouseY)):
            if click:
                for box in input_boxes:
                    print(box.get_text())

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True

        screen.blit(YELLOW_SPACESHIP_IMAGE, (0, 0))
        pygame.draw.rect(screen, (0, 255, 255), login_button, 2)

        for box in input_boxes:
            box.draw(screen, background, input_boxes)

        pygame.display.update()

    pygame.quit()


main()
