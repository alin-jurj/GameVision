import pygame
from gui_elements import login_page, buttons
from pages.main_page import main_page
import database.connectors as cn
import mysql.connector

pygame.init()

FPS = 60
monster = pygame.image.load('assets/monster.png')
background = pygame.image.load('assets/background_login_resized.png')
login_image = pygame.image.load('assets/login.png')
back_image = pygame.image.load('assets/back.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('red2')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 32)

pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def verify_empty(input_boxes):
    for box in input_boxes:
        if box.get_text() == "":
            raise Exception("Cannot leave empty text boxes")


def invalid(text):
    text = FONT.render(text, True, color)
    screen.blit(text, (WIDTH / 2.4, HEIGHT / 1.9))


def login():
    clock = pygame.time.Clock()

    input_box1 = login_page.InputBox(WIDTH / 2.4, HEIGHT / 1.7, 220, 30)
    input_box2 = login_page.InputBox(WIDTH / 2.4, HEIGHT / 1.5, 220, 30, hidden=True)
    input_boxes = [input_box1, input_box2]

    login_button = buttons.Button(WIDTH / 2.4, HEIGHT / 1.3, login_image, 0.35)
    back_button = buttons.Button(WIDTH / 2.4, HEIGHT / 1.15, back_image, 0.35)

    text = ""
    err = False
    run = True
    while run:

        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        if login_button.draw(screen) == True:
            try:
                verify_empty(input_boxes)
                db = mysql.connector.connect(
                    host=cn.host,
                    user=cn.user,
                    passwd=cn.passwd,
                    database=cn.database
                )

                mycursor = db.cursor()
                mycursor.execute("SELECT * FROM User WHERE username=%s AND password=%s",
                                 (input_box1.get_text(), input_box2.get_text()))
                row = mycursor.fetchone()
                if row == None:
                    text = "Invalid username and password"
                    err = True
                else:
                    run = False
                    err = False
                for box in input_boxes:
                    box.reset_text()
            except Exception:
                err = True
                text = "Cannot leave empty text boxes"

        if back_button.draw(screen) == True:
            print("BACK")

        if err:
            invalid(text)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            for box in input_boxes:
                box.handle_event(event)

        screen.blit(monster, (0, 0))

        for box in input_boxes:
            box.draw(screen, background, input_boxes)

        pygame.display.update()

    main_page()


login()
