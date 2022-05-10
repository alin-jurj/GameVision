import pygame
from gui_elements import input_box, buttons
from pages import main_page, register_page
from database import queries

# import database.connectors as cn


pygame.init()

FPS = 60
monster = pygame.image.load('../assets/icons/monster.png')
background = pygame.image.load('../assets/background_login_resized.png')
bkgreg = pygame.image.load('../assets/regi.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('red2')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 32)
gui_font = pygame.font.SysFont('Arial', 16)
clock = pygame.time.Clock()
pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def login():
    input_box1 = input_box.InputBox(WIDTH / 2.4, HEIGHT / 1.7, 220, 30)
    input_box2 = input_box.InputBox(WIDTH / 2.4, HEIGHT / 1.5, 220, 30, hidden=True)
    input_boxes = [input_box1, input_box2]

    login_button = buttons.Button('LOG IN', 100, 30, (590, 540), gui_font)
    register_button = buttons.Button('REGISTER', 100, 30, (590, 580), gui_font)
    delete_table_button = buttons.Button('DELETE TABLE', 100, 30, (200, 300), gui_font)
    create_table_button = buttons.Button('CREATE TABLE', 100, 30, (200, 420), gui_font)

    text = ""
    err = False
    run = True
    main = 0

    while run:

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        if login_button.draw(screen) == True:
            try:
                input_box.verify_empty(input_boxes)
                row = queries.logs(input_box1, input_box2)
                if row == None:
                    err = True
                    text = "Invalid username and password"

                else:
                    err = False
                    run = False
                    main = 1

                for box in input_boxes:
                    box.reset_text()
            except Exception:
                err = True
                text = "Cannot leave empty text boxes"

        if register_button.draw(screen) == True:
            register_page.register(screen)
        if delete_table_button.draw(screen) == True:
            queries.delete_table()
        if create_table_button.draw(screen) == True:
            queries.create_table()
        if err:
            input_box.invalid(text, screen, 2.4, 1.9)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            for box in input_boxes:
                box.handle_event(event)

        screen.blit(monster, (0, 0))

        for box in input_boxes:
            box.draw(screen, background, input_boxes)

        pygame.display.update()

    if main == 1:
        main_page.main_page(screen)

    pygame.quit()


login()
