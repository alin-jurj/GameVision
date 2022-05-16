import pygame
from network import Network
from gui_elements import buttons, map_selector

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


def selections(map):
    return 'play,' + str(map) + ','


def read_selections(data):
    data = data.split(',')
    return int(data[1])


def play(screen):
    clock = pygame.time.Clock()

    run = True

    n = Network()

    map1 = map_selector.Map(map1_img, 0.25, (80, 460))
    map2 = map_selector.Map(map2_img, 0.25, (480, 460))
    map3 = map_selector.Map(map3_img, 0.25, (880, 460))

    ready_button = buttons.Button('READY', 200, 45, (540, 650), button_font)

    selected_map = -1
    enemy_selected_map = read_selections(n.send(selections(selected_map)))

    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        clock.tick(FPS)

        enemy_selected_map = read_selections(n.send(selections(selected_map)))

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

        if ready_button.draw(screen):
            print('Ready')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()


if __name__ == '__main__':
    play(screen=pygame.display.set_mode((WIDTH, HEIGHT)))
