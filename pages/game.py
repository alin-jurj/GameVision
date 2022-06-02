import random
import pygame
import cv2
from camera.camera_controls import countFingers, hands_videos, detectHandsLandmarks
from pages import main_page
from database import queries
from gui_elements import image_buttons, buttons, character_buying_box, icon_box
from camera.hand_detector import HandDetector
from game_result import game_result
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
text_get_ready = FONT.render('GET READY!', True, '#FF0000')
text_you_lost = FONT.render('YOU LOST!', True, '#FF0000')
text_you_won = FONT.render('YOU WON!', True, '#FF0000')
red = (255, 0, 0)
green = (0, 255, 0)


class Fighter():
    def __init__(self, x, y, name, max_hp, strength, image):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.alive = True
        self.strength=strength
        self.frame_index = 0
        self.action = 0  # 0.idle, 1.attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def attack_skill(self, target):
        rand = random.randint(15, 25)
        damage = self.strength + rand
        target.hp -= damage
        # check if target has died
        if target.alive < 1:
            target.hp = 0
            target.alive = False
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        # check if target has died
        if target.alive < 1:
            target.hp = 0
            target.alive = False
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def selections(position_x, position_y):
    return 'game,' + str(position_x) + ',' + str(position_y)


def read_selections(data):
    data = data.split(',')
    return int(data[1]), int(data[2])


class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, screen, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
def game(screen, n, logged_in_user, map_choice, player_champion, enemy_champion, player_skills, enemy_skills):
    clock = pygame.time.Clock()

    back_button = image_buttons.ImageButton(back, 1, (1136, 24))

    camera_video = cv2.VideoCapture(0)
    camera_video.set(3, 1280)
    camera_video.set(4, 960)

    # Create named window for resizing purposes.
    cv2.namedWindow('Fingers Counter', cv2.WINDOW_NORMAL)

    detector = HandDetector(detectionCon=0.8, maxHands=1)

    run = True
    main = False

    player_position_x = 100
    player_position_y = 500

    enemy_position_x=700
    enemy_position_y=500
    # enemy_position_x, enemy_position_y = read_selections(n.send(selections(player_position_x, player_position_y)))
    start_count = 100
    go = 0
    playerX_change = 0
    last_change = 1
    player_champ_img = player_champion.get_image()
    enemy_champ_img = enemy_champion.get_image()
    movement_x = []
    x_counter = 0

    player = Fighter(player_position_x, player_position_y, 'Knight', 30, 10, 3, player_champ_img)
    enemy = Fighter(enemy_position_x, enemy_position_y, 'Bandit', 30, enemy_champ_img)

    player_healthbar=HealthBar(100,250, 100, 100)
    enemy_healthbar=HealthBar(900,250, 100, 100)

    while run:
        pointIndex = 0
        screen.fill((0, 0, 0))
        screen.blit(map_choice, (0, 0))
        clock.tick(FPS)

        # Read a frame.
        ok, frame = camera_video.read()

        hands, img = detector.findHands(frame)

        if hands:
            lmList = hands[0]['lmList']
            pointIndex = lmList[8][0:2]
            print(pointIndex)
            cv2.circle(img, pointIndex, 20, (200, 0, 200), cv2.FILLED)

        # Check if frame is not read properly then continue to the next iteration to read the next frame.
        if not ok:
            continue

        # Flip the frame horizontally for natural (selfie-view) visualization.
        frame = cv2.flip(frame, 1)

        # Perform Hands landmarks detection on the frame.
        frame, results = detectHandsLandmarks(frame, hands_videos, display=False)

        # Check if the hands landmarks in the frame are detected.
        if results.multi_hand_landmarks:
            # Count the number of fingers up of each hand in the frame.
            frame, fingers_statuses, count = countFingers(frame, results, display=False)
            print(fingers_statuses)

        # Display the frame.
        cv2.imshow('Fingers Counter', frame)

        # enemy_position_x, enemy_position_y = read_selections(n.send(selections(player_position_x, player_position_y)))
        player.draw(screen)
        enemy.draw(screen)

        player_healthbar.draw(screen, player.hp)
        enemy_healthbar.draw(screen, enemy.hp)
        #screen.blit(player_champ_img, (player_position_x, player_position_y))
        #screen.blit(enemy_champion.get_image(), (enemy_position_x, enemy_position_y))
        if player.alive==False:
            game_result.game_result(screen, logged_in_user,map_choice, text_you_lost)
        if enemy.alive==False:
            game_result.game_result(screen, logged_in_user,map_choice, text_you_won)
        if start_count != 0:
            screen.blit(text_get_ready, (500, 60))
            start_count -= 1

        if start_count == 0:
            go = 1

        if x_counter == 3:
            x_counter = 0
            movement_x = []

        if pointIndex != 0:
            movement_x.append(pointIndex[0])  # index[0] -> coordonata x a degetului aratator, index[1] -> coordonata y
            x_counter += 1
        if start_count != 0:
            screen.blit(text_get_ready, (500, 60))
            start_count -= 1

        if y_counter == 3:
            y_counter = 0
            movement_y = []

        if pointIndex != 0:
            movement_y.append(pointIndex[1])  # index[1] -> coordonata y a degetului aratator
            y_counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:  # If any key is pressed
                if event.key == pygame.K_LEFT:
                    playerX_change = -8
                if event.key == pygame.K_RIGHT:
                    playerX_change = 8

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        if len(movement_x) == 3:
            if movement_x[2] > (movement_x[1] + 3) and movement_x[1] > (movement_x[0] + 3):
                playerX_change = -15
            elif movement_x[2] < (movement_x[1] - 3) and movement_x[1] < (movement_x[0] - 3):
                playerX_change = 15
            else:
                playerX_change = 0
        if len(movement_y) == 3:
            if movement_y[2] > (movement_y[1] + 3) and movement_y[1] > (movement_y[0] + 3):
                if player_position_x+50 >= enemy_position_x:
                    player.attack(enemy)
            elif movement_y[2] < (movement_y[1] - 3) and movement_y[1] < (movement_y[0] - 3):
                if player_position_x+200 >= enemy_position_x:
                    for i in range(enemy_position_x-player_position_x-30, 10):
                        screen.blit(pygame.image.load(player_skills), (player_position_x+30+i, player_position_y))
                    player.attack_skill(enemy)
        if last_change > 0 and playerX_change < 0:
            player_champ_img = pygame.transform.flip(player_champ_img, True, False)
            last_change = playerX_change

        if last_change < 0 and playerX_change > 0:
            player_champ_img = pygame.transform.flip(player_champ_img, True, False)
            last_change = playerX_change

        player_position_x = player_position_x + playerX_change

        if player_position_x <= 0:
            player_position_x = 0
        elif player_position_x >= 1060:
            player_position_x = 1060

        pygame.display.update()

    camera_video.release()
    cv2.destroyAllWindows()

    if main:
        main_page.main_page(screen, logged_in_user)