import pygame
from gui_elements import buttons, player_details, character_buying_box
from pages import leaderboard, play
from play import scale_image
from database import queries

pygame.init()

FPS = 60
background = pygame.image.load('../assets/main_menu.png')
monster = pygame.image.load('../assets/icons/monster.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('#2C7950')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.Font(None, 72)
button_font = pygame.font.SysFont('Arial', 20)
player_font = pygame.font.SysFont('Arial', 25)
game_name = FONT.render('ULTIMATE REFLEX FIGHTER', True, '#B2B600')

pygame.display.set_caption("ULTIMATE REFLEX FIGHTER")


def main_page(screen, logged_in_user):
    clock = pygame.time.Clock()

    play_button = buttons.Button('PLAY', 200, 45, (110, 360), button_font)
    store_button = buttons.Button('STORE', 200, 45, (110, 420), button_font)
    inventory_button = buttons.Button('INVENTORY', 200, 45, (110, 480), button_font)
    leaderboard_button = buttons.Button('LEADERBOARD', 200, 45, (110, 540), button_font)
    profile_button = buttons.Button('PROFILE', 200, 45, (110, 600), button_font)
    settings_button = buttons.Button('SETTINGS', 200, 45, (110, 660), button_font)

    player = player_details.Player_Details(360, 140, (900, 60), player_font, logged_in_user.get_username(),
                                           logged_in_user.get_lvl(), logged_in_user.get_xp(),
                                           logged_in_user.get_money(), monster)

    random_champ_row = queries.select_random_champion(logged_in_user.get_userId())
    if random_champ_row:
        character = pygame.image.load('../assets/characters/body/' + random_champ_row[0] + '.png')
        resized_image = scale_image(character, 0.8)

        character_box = character_buying_box.Character_Buying_Box(240, 310, (900, 400), random_champ_row[0],
                                                                  resized_image,
                                                                  random_champ_row[1],
                                                                  random_champ_row[2], random_champ_row[3],
                                                                  random_champ_row[4], random_champ_row[5])

    run = True
    leaderboard_page = 0
    play_page = 0
    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        screen.blit(game_name, (280, 260))

        if play_button.draw(screen):
            play_page = 1
            run = False

        store_button.draw(screen)
        inventory_button.draw(screen)

        if leaderboard_button.draw(screen):
            leaderboard_page = 1
            run = False

        profile_button.draw(screen)
        settings_button.draw(screen)
        player.draw(screen)

        if random_champ_row:
            character_box.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    if play_page == 1:
        play.play(screen, logged_in_user)

    if leaderboard_page == 1:
        leaderboard.draw(screen, logged_in_user)
