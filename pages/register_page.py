import pygame
from gui_elements import input_box, buttons
from database import queries

WIDTH, HEIGHT = 1280, 720
FPS = 60
bkg_reg = pygame.image.load('../assets/regi.png')
gui_font = pygame.font.SysFont('Arial', 16)


def register(screen):
    username_field = input_box.InputBox(WIDTH / 2.4, HEIGHT / 2.1, 220, 30)
    password_field = input_box.InputBox(WIDTH / 2.4, HEIGHT / 1.9, 220, 30, hidden=True)
    Confirmpassword_field = input_box.InputBox(WIDTH / 2.4, HEIGHT / 1.7, 220, 30, hidden=True)
    email_field = input_box.InputBox(WIDTH / 2.4, HEIGHT / 1.5, 220, 30)

    input_boxes = [username_field, password_field, Confirmpassword_field, email_field]
    back_button = buttons.Button('BACK', 100, 30, (100, 50), gui_font)

    register_button = buttons.Button('REGISTER', 90, 35, (590, 520), gui_font)
    text = ""
    err = False
    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(bkg_reg, (0, 0))
        if back_button.draw(screen) == True:
            run = False
        if register_button.draw(screen) == True:
            try:
                input_box.verify_empty(input_boxes)
                row = queries.search_username(username_field)

                if row:
                    err = True
                    text = "Already exists an account with the same username"
                else:
                    err = False
                    row = queries.search_email(email_field)
                    if row:
                        err = True
                        text = "Already exists an account with the same email"
                    else:
                        err = False
                        if password_field.get_text() != Confirmpassword_field.get_text():
                            err = True
                            text = "Password and confirm password does not match"
                        else:
                            err = False
                            queries.add_user(username_field, password_field, email_field)
                for box in input_boxes:
                    box.reset_text()
            except Exception:
                err = True
                text = "Cannot leave empty text boxes"
        if err:
            input_box.invalid(text, screen, 2.2, 1.7)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.draw(screen, bkg_reg, input_boxes)
        pygame.display.update()
