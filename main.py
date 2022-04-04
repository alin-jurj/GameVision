import pygame
import login_page
import database.connectors as cn
import mysql.connector

pygame.init()

FPS = 60
YELLOW_SPACESHIP_IMAGE = pygame.image.load('assets/monster.png')
background = pygame.image.load('assets/background_login_resized.png')
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def verify_empty(input_boxes):
    for box in input_boxes:
        if box.get_text() == "":
            raise Exception("Cannot leave empty text boxes")


def login():
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
                        print("Invalid username and password")
                    else:
                        print("Login successful")
                    for box in input_boxes:
                        box.reset_text()
                except Exception as e:
                    print(e)

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


login()
