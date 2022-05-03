import pygame
from gui_elements import login_page,buttons,after_login
from database import queries
WIDTH, HEIGHT = 1280, 720
FPS = 60
bkg_reg = pygame.image.load('assets/regi.png')
def register(screen):
    username_field = login_page.InputBox(WIDTH / 2.4, HEIGHT / 2.1, 220, 30)
    password_field = login_page.InputBox(WIDTH / 2.4, HEIGHT / 1.9, 220, 30, hidden=True)
    Confirmpassword_field = login_page.InputBox(WIDTH / 2.4, HEIGHT / 1.7, 220, 30, hidden=True)
    email_field = login_page.InputBox(WIDTH / 2.4, HEIGHT / 1.5, 220, 30)
    
    input_boxes = [username_field,password_field,Confirmpassword_field,email_field]

    #login_button = buttons.Button(WIDTH / 2.4, HEIGHT / 1.3, login_image, 0.35)
    #back_button = buttons.Button(WIDTH / 2.4, HEIGHT / 1.15, back_image, 0.35)
    #login_button = buttons.Button('LOG IN',100, 30, (590,540))
    register_button = buttons.Button('REGISTER',90, 35, (590,520))
    text = ""
    err=False
    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(bkg_reg, (0, 0))
        if register_button.draw(screen) == True:
            try:
                login_page.verify_empty(input_boxes)
                row=queries.search_username(username_field)
                
                if row:
                    err=True
                    text="Already exists an account with the same username"
                else:
                    err=False
                    row=queries.search_email(email_field)
                    if row:
                      err=True
                      text="Already exists an account with the same email"
                    else:
                       err=False
                       if password_field.get_text()!=Confirmpassword_field.get_text():
                            err=True
                            text="Password and confirm password does not match"
                       else:
                            err=False
                            queries.add_user(username_field,password_field,email_field)
                for box in input_boxes:
                    box.reset_text()
            except Exception:
                err=True
                text = "Cannot leave empty text boxes"
        if err:
            login_page.invalid(text,screen,2.2,1.7)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.draw(screen, bkg_reg, input_boxes)
        pygame.display.update()
        

       

        