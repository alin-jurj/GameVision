import pygame
from pages import main_page
from database import queries
from gui_elements import image_buttons, buttons, character_buying_box, icon_box
from play import scale_image

pygame.init()

FPS = 60
background = pygame.image.load('../assets/main_menu.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('#2C7950')
FONT = pygame.font.Font(None, 72)
button_font = pygame.font.SysFont('Arial', 28)
text_font = pygame.font.SysFont('Arial', 32)
back = pygame.image.load('../assets/misc/back.png')
path_to_char = '../assets/characters/body/'
path_to_icons = '../assets/icons/'
text_store = FONT.render('STORE', True, '#FFFFFF')
text_money = text_font.render('NOT ENOUGH MONEY', True, '#FF0000')


def store(screen, logged_in_user):
    clock = pygame.time.Clock()

    back_button = image_buttons.ImageButton(back, 1, (1136, 24))
    champion_button = buttons.Button("CHAMPIONS", 200, 45, (80, 120), button_font)
    icon_button = buttons.Button("ICONS", 200, 45, (80, 170), button_font)
    skins_button = buttons.Button("SKINS", 200, 45, (80, 220), button_font)

    buyable_champs = queries.get_buyable_champions()

    owned_champs_ids = []
    owned_champs = queries.get_owned_champions(logged_in_user.get_userId())
    for row in owned_champs:
        owned_champs_ids.append(row[0])

    buyable_icons = queries.get_buyable_icons()

    owned_icons_ids = []
    owned_icons = queries.get_owned_icons(logged_in_user.get_userId())
    for row in owned_icons:
        owned_icons_ids.append(row[0])

    initial_pos = (300, 120)
    pos = initial_pos
    i = 1
    character_boxes = []
    for row in buyable_champs:
        image = pygame.image.load(path_to_char + row[1] + '.png')
        resized_image = scale_image(image, 0.8)

        owned = False
        if row[0] in owned_champs_ids:
            owned = True

        character_box = character_buying_box.Character_Buying_Box(240, 310, pos, row[0], row[1], resized_image,
                                                                  str(row[2]), str(row[3]), str(row[4]), str(row[5]),
                                                                  str(row[6]), owned)
        character_boxes.append(character_box)

        if i % 3 == 0:
            pos = (initial_pos[0], pos[1] + 256)
        else:
            pos = (pos[0] + 256, initial_pos[1])

        i += 1

    initial_pos = (300, 120)
    pos = initial_pos
    i = 1
    icon_boxes = []
    for row in buyable_icons:
        image = pygame.image.load(path_to_icons + row[1] + '.png')

        owned = False
        if row[0] in owned_icons_ids:
            owned = True

        buy_icon_box = icon_box.IconBox(200, 190, pos, row[0], row[1], image, int(row[2]), owned)
        icon_boxes.append(buy_icon_box)

        if i % 4 == 0:
            pos = (initial_pos[0], pos[1] + 220)
        else:
            pos = (pos[0] + 220, initial_pos[1])

        i += 1

    run = True
    main = False

    blit = 0
    duration = 100
    draw_characters = True
    draw_icons = False
    draw_skins = False

    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        screen.blit(text_store, (80, 60))

        if back_button.draw(screen):
            run = False
            main = True

        if champion_button.draw(screen):
            draw_characters = True
            draw_icons = False
            draw_skins = False

        if draw_characters:
            for box in character_boxes:
                price = box.draw(screen, logged_in_user)
                if price != -1 and price is int:
                    logged_in_user.set_money(int(price))
                    queries.update_user_money(logged_in_user.get_userId(), logged_in_user.get_money())
                if price == -1:
                    blit = 1

        if icon_button.draw(screen):
            draw_characters = False
            draw_icons = True
            draw_skins = False

        if draw_icons:
            for box in icon_boxes:
                price = box.draw(screen, logged_in_user)
                if price != -1 and price is int:
                    logged_in_user.set_money(int(price))
                    queries.update_user_money(logged_in_user.get_userId(), logged_in_user.get_money())
                if price == -1:
                    blit = 1

        if blit:
            duration -= 1
            screen.blit(text_money, (300, 60))
            if duration == 1:
                blit = 0
                duration = 100

        if skins_button.draw(screen):
            draw_characters = False
            draw_icons = False
            draw_skins = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    if main:
        main_page.main_page(screen, logged_in_user)
