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
text_store = FONT.render('INVENTORY', True, '#FFFFFF')
text_money = text_font.render('NOT ENOUGH MONEY', True, '#FF0000')


def inventory(screen, logged_in_user):
    clock = pygame.time.Clock()

    back_button = image_buttons.ImageButton(back, 1, (1136, 24))
    champion_button = buttons.Button("CHAMPIONS", 200, 45, (80, 120), button_font)
    icon_button = buttons.Button("ICONS", 200, 45, (80, 170), button_font)
    rewards_button = buttons.Button("REWARDS", 200, 45, (80, 220), button_font)

    owned_champs = queries.get_owned_champions(logged_in_user.get_userId())
    owned_champs_ids = []
    for row in owned_champs:
        owned_champs_ids.append(row[0])

    owned_icons = queries.get_owned_icons(logged_in_user.get_userId())

    initial_pos = (300, 120)
    pos = initial_pos
    i = 1
    character_boxes = []
    for row in owned_champs:
        image = pygame.image.load(path_to_char + row[1] + '.png')
        resized_image = scale_image(image, 0.8)

        owned = True
        show_owned = False

        character_box = character_buying_box.Character_Buying_Box(240, 295, pos, row[0], row[1], resized_image,
                                                                  str(row[2]), str(row[3]), str(row[4]), str(row[5]),
                                                                  str(row[6]), owned, show_owned)
        character_boxes.append(character_box)

        if i % 3 == 0:
            pos = (initial_pos[0], pos[1] + 300)
        else:
            pos = (pos[0] + 256, initial_pos[1])

        i += 1

    initial_pos = (300, 120)
    pos = initial_pos
    i = 1
    icon_boxes = []
    for row in owned_icons:
        image = pygame.image.load(path_to_icons + row[1] + '.png')

        owned = True
        show_owned = False
        equip = True

        owned_icon_box = icon_box.IconBox(200, 190, pos, row[0], row[1], image, 0, owned, show_owned, equip)
        icon_boxes.append(owned_icon_box)

        if i % 4 == 0:
            pos = (initial_pos[0], pos[1] + 220)
        else:
            pos = (pos[0] + 220, initial_pos[1])

        i += 1

    reward = queries.get_champion_by_name('Mako')
    if reward[0] in owned_champs_ids:
        owned_reward = True
    else:
        owned_reward = False
    reward_image = pygame.image.load(path_to_char + reward[1] + '.png')
    resized_reward_image = scale_image(reward_image, 0.8)
    reward_box = character_buying_box.Character_Buying_Box(240, 310, initial_pos, reward[0], reward[1],
                                                           resized_reward_image, str(reward[2]), str(reward[3]),
                                                           str(reward[4]), str(reward[5]), str(reward[6]), owned_reward,
                                                           True, True, 5)

    run = True
    main = False

    blit = 0
    duration = 100
    draw_characters = True
    draw_icons = False
    draw_rewards = False

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
            draw_rewards = False

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
            draw_rewards = False

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

        if rewards_button.draw(screen):
            draw_characters = False
            draw_icons = False
            draw_rewards = True

        if draw_rewards:
            reward_box.draw(screen, logged_in_user)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    if main:
        main_page.main_page(screen, logged_in_user)
