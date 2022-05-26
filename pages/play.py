import pygame
from network import Network
from gui_elements import buttons, map_selector, character_selector, image_buttons
from pages import main_page
from database import queries

pygame.init()

FPS = 60
background = pygame.image.load('../assets/play_page.png')
WIDTH, HEIGHT = 1280, 720
map1_img = pygame.image.load('../assets/maps/map_1.png')
map2_img = pygame.image.load('../assets/maps/map_2.png')
map3_img = pygame.image.load('../assets/maps/map_3.png')
green_check = pygame.image.load('../assets/misc/green_check.png')
red_check = pygame.image.load('../assets/misc/red_check.png')
button_font = pygame.font.SysFont('Arial', 20)
path_to_char = '../assets/characters/heads/'
FONT = pygame.font.Font(None, 56)
text_character = FONT.render('CHARACTER SELECT', True, '#FFFFFF')
text_stage = FONT.render('STAGE SELECT', True, '#FFFFFF')
back = pygame.image.load('../assets/misc/back.png')


def scale_image(image, scale):
    width = image.get_width()
    height = image.get_height()
    new_image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return new_image


def selections(map, character, ready):
    return 'play,' + str(map) + ',' + character + ',' + str(ready)


def read_selections(data):
    data = data.split(',')
    return int(data[1]), data[2], int(data[3])


def play(screen, logged_in_user):
    clock = pygame.time.Clock()

    run = True

    n = Network()

    map1 = map_selector.Map(map1_img, 0.25, (80, 460))
    map2 = map_selector.Map(map2_img, 0.25, (480, 460))
    map3 = map_selector.Map(map3_img, 0.25, (880, 460))

    ready_button = buttons.Button('READY', 200, 45, (540, 650), button_font)
    back_button = image_buttons.ImageButton(back, 1, (1136, 24))

    owned_champions = []
    images = []
    owned_champions_rows = queries.get_owned_champions(logged_in_user.get_userId())
    for row in owned_champions_rows:
        owned_champions.append(row[1])
        character = pygame.image.load(path_to_char + row[1] + '.png')
        images.append(character)

    character_sel = character_selector.CharacterSelector((120, 120), images, 0.9, owned_champions)

    main = 0
    selected_map = -1
    character_choice = ""
    player_ready = 0
    enemy_selected_map, enemy_character, enemy_ready = read_selections(
        n.send(selections(selected_map, character_choice, player_ready)))

    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        screen.blit(text_character, (80, 60))
        screen.blit(text_stage, (80, 400))
        screen.blit(back, (1136, 24))

        enemy_selected_map, enemy_character, enemy_ready = read_selections(
            n.send(selections(selected_map, character_choice, player_ready)))

        choice = character_sel.draw(screen)

        if choice:
            character_choice = choice

        if character_choice:
            selected_character = pygame.image.load('../assets/characters/body/' + character_choice + '.png')
            screen.blit(scale_image(selected_character, 1.2), (560, 140))

        if enemy_character:
            enemy_selected_character = pygame.image.load('../assets/characters/body/' + enemy_character + '.png')
            img_copy = enemy_selected_character.copy()
            flipped_character = pygame.transform.flip(img_copy, True, False)
            screen.blit(scale_image(flipped_character, 1.2), (1000, 140))

        if back_button.draw(screen):
            run = 0
            main = 1

        if map1.draw(screen):
            selected_map = 1

        if selected_map == 1:
            screen.blit(green_check, (80, 576))

        if enemy_selected_map == 1:
            screen.blit(red_check, (336, 576))

        if map2.draw(screen):
            selected_map = 2

        if selected_map == 2:
            screen.blit(green_check, (480, 576))

        if enemy_selected_map == 2:
            screen.blit(red_check, (736, 576))

        if map3.draw(screen):
            selected_map = 3

        if selected_map == 3:
            screen.blit(green_check, (880, 576))

        if enemy_selected_map == 3:
            screen.blit(red_check, (1136, 576))

        if player_ready == 1:
            screen.blit(green_check, (780, 315))

        if enemy_ready == 1:
            screen.blit(red_check, (1000, 315))

        if ready_button.draw(screen) and character_choice:
            if player_ready == 0:
                player_ready = 1
            else:
                player_ready = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    if main == 1:
        main_page.main_page(screen, logged_in_user)
