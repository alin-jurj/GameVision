import pygame
from gui_elements import input_box, buttons
from pages.main_page import main_page
import database.connectors as cn
import mysql.connector

pygame.init()

FPS = 60
background = pygame.image.load('assets/background_login_resized.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('red2')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 32)
button_font = pygame.font.SysFont('Arial', 20)

pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def verify_empty(input_boxes):
    for box in input_boxes:
        if box.get_text() == "":
            raise Exception("Cannot leave empty text boxes")


def invalid(text):
    text = FONT.render(text, True, color)
    screen.blit(text, (WIDTH / 2.4, HEIGHT / 1.9))


def login(screen):
    clock = pygame.time.Clock()

    input_box1 = input_box.InputBox(WIDTH / 2.4, HEIGHT / 1.7, 220, 30)
    input_box2 = input_box.InputBox(WIDTH / 2.4, HEIGHT / 1.5, 220, 30, hidden=True)
    input_boxes = [input_box1, input_box2]

    login_button = buttons.Button('LOG IN', 200, 45, (540, 540), button_font)
    back_button = buttons.Button('BACK', 200, 45, (540, 600), button_font)

    text = ""
    err = False
    run = True
    while run:

        go_main = 0
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
                    go_main = 1
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

        for box in input_boxes:
            box.draw(screen, background, input_boxes)

        pygame.display.update()

    if go_main:
        main_page(screen)


login(screen)
