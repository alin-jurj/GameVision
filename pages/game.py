import random
import pygame
import math
import cv2
from camera.camera_controls import countFingers, hands_videos, detectHandsLandmarks
from camera.hand_detector import HandDetector
import game_result
from models import skill

pygame.init()

FPS = 60
background = pygame.image.load('../assets/main_menu.png')
WIDTH, HEIGHT = 1280, 720
color = pygame.Color('#2C7950')
FONT = pygame.font.Font(None, 72)
button_font = pygame.font.SysFont('Arial', 28)
text_font = pygame.font.SysFont('Arial', 32)
back = pygame.image.load('../assets/misc/back.png')
punch_img = pygame.image.load('../assets/skills/punch.png')
fireball_img = pygame.image.load('../assets/skills/fireball.png')
path_to_char = '../assets/characters/body/'
path_to_icons = '../assets/icons/'
text_get_ready = FONT.render('GET READY!', True, '#FF0000')
text_you_lost = FONT.render('YOU LOST!', True, '#FF0000')
text_you_won = FONT.render('YOU WON!', True, '#FF0000')
red = (255, 0, 0)
green = (0, 255, 0)


class Champion:
    def __init__(self, x, y, name, max_hp, strength, image):
        self.y = y
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.alive = True
        self.strength = strength
        self.update_time = pygame.time.get_ticks()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_hp(self, new_hp):
        self.hp = new_hp

    def update_x(self, new_x):
        self.rect.center = (new_x, self.y)

    def update_image(self, new_image):
        self.image = new_image

    def attack_skill(self, target):
        rand = random.randint(15, 25)
        damage = self.strength + rand
        target.hp -= damage
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        if target.hp < 1:
            target.hp = 0
            target.alive = False
        self.update_time = pygame.time.get_ticks()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def verify_alive(self):
        if self.hp < 1:
            self.hp = 0
            self.alive = False

    def get_hp(self):
        return self.hp


def selections(position_x, position_y, enemy_hp, skl):
    try:
        return 'game,' + str(position_x) + ',' + str(position_y) + ',' + str(enemy_hp) + ',' + str(skl)
    except:
        return TypeError


def read_selections(data):
    data = data.split(',')
    try:
        return int(data[1]), int(data[2]), int(data[3]), int(data[4])
    except:
        return IndexError


class HealthBar:
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, screen, hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 250, 40))
        pygame.draw.rect(screen, green, (self.x, self.y, 250 * ratio, 40))


def game(screen, n, logged_in_user, map_choice, player_champion, enemy_champion, player_skills, enemy_skills):
    clock = pygame.time.Clock()

    camera_video = cv2.VideoCapture(0)
    camera_video.set(3, 1280)
    camera_video.set(4, 960)

    # Create named window for resizing purposes.
    cv2.namedWindow('Fingers Counter', cv2.WINDOW_NORMAL)

    detector = HandDetector(detectionCon=0.8, maxHands=1)

    run = True
    punch_counter = 0
    skill_counter = 0
    win_lose = 0
    end_game = False

    player_position_x = 100
    player_position_y = 500
    player_skill = 0

    try:
        enemy_position_x, enemy_position_y, player_hp, enemy_skill = read_selections(
            n.send(selections(player_position_x, player_position_y, int(enemy_champion.get_hp()), player_skill)))
    except:
        run = False
        win_lose = 1
        end_game = True

    start_count = 200
    go = 0
    player_x_change = 0
    last_change = 1
    player_champ_img = player_champion.get_image()
    enemy_champ_img = enemy_champion.get_image()
    movement_x = []
    x_counter = 0
    movement_y = []
    y_counter = 0

    player = Champion(player_position_x, player_position_y, player_champion.get_champion_name(),
                      int(player_champion.get_hp()), int(player_champion.get_attack()), player_champ_img)
    enemy = Champion(enemy_position_x, enemy_position_y, enemy_champion.get_champion_name(),
                     int(enemy_champion.get_hp()), int(enemy_champion.get_attack()), enemy_champ_img)

    player_healthbar = HealthBar(100, 100, int(player_champion.get_hp()), int(player_champion.get_hp()))
    enemy_healthbar = HealthBar(1000, 100, int(enemy_champion.get_hp()), int(enemy_champion.get_hp()))

    while run:
        pointIndex = 0
        screen.fill((0, 0, 0))
        screen.blit(map_choice, (0, 0))
        clock.tick(FPS)

        ok, frame = camera_video.read()

        hands, img = detector.findHands(frame)

        if hands:
            lmList = hands[0]['lmList']
            pointIndex = lmList[8][0:2]
            cv2.circle(img, pointIndex, 20, (200, 0, 200), cv2.FILLED)

        if not ok:
            continue

        frame = cv2.flip(frame, 1)

        frame, results = detectHandsLandmarks(frame, hands_videos, display=False)

        if results.multi_hand_landmarks:
            frame, fingers_statuses, count = countFingers(frame, results, display=False)
            print(fingers_statuses)

        cv2.imshow('Fingers Counter', frame)

        try:
            enemy_position_x, enemy_position_y, player_hp, enemy_skill = read_selections(
                n.send(selections(player_position_x, player_position_y, int(enemy.get_hp()), player_skill)))
        except:
            end_game = True
            win_lose = 1
            run = False
            break

        player.draw(screen)
        enemy.draw(screen)

        player.update_hp(player_hp)
        player.verify_alive()

        player_healthbar.draw(screen, player.hp)
        enemy_healthbar.draw(screen, enemy.hp)

        for i in player_skills:
            i.update_position(player_position_x, player_position_y)

        for i in enemy_skills:
            i.update_position(enemy_position_x, enemy_position_y)

        if not player.alive:
            end_game = True
            win_lose = 0
            run = False
            break

        if not enemy.alive:
            end_game = True
            win_lose = 1
            run = False
            break

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

        if len(movement_x) == 3:
            if movement_x[2] > (movement_x[1] + 3) and movement_x[1] > (movement_x[0] + 3):
                player_x_change = -15
            elif movement_x[2] < (movement_x[1] - 3) and movement_x[1] < (movement_x[0] - 3):
                player_x_change = 15
            else:
                player_x_change = 0

        if len(movement_y) == 3 and go:
            if movement_y[2] > (movement_y[1] + 3) and movement_y[1] > (movement_y[0] + 3):
                if math.fabs(player_position_x - enemy_position_x <= 100) and punch_counter == 0:
                    punch_counter = 5
                    player.attack(enemy)
            elif movement_y[2] < (movement_y[1] - 3) and movement_y[1] < (movement_y[0] - 3):
                if math.fabs(player_position_x - enemy_position_x) <= 200:
                    for i in range(0, player_position_x - enemy_position_x, 5):
                        player_skills[1].draw(screen)
                    skill_counter += 30
                    player.attack_skill(enemy)

        if enemy_skill == 1:
            enemy_skills[0].draw(screen)

        if punch_counter != 0:
            player_skills[0].draw(screen)
            player_skill = 1
            punch_counter -= 1
        else:
            player_skill = 0

        if last_change > 0 and player_x_change < 0:
            player_champ_img = pygame.transform.flip(player_champ_img, True, False)
            last_change = player_x_change
            player.update_image(player_champ_img)

        if last_change < 0 and player_x_change > 0:
            player_champ_img = pygame.transform.flip(player_champ_img, True, False)
            last_change = player_x_change
            player.update_image(player_champ_img)

        player_position_x = player_position_x + player_x_change

        if player_position_x <= 100:
            player_position_x = 100
        elif player_position_x >= 1100:
            player_position_x = 1100

        player.update_x(player_position_x)
        enemy.update_x(enemy_position_x)

        pygame.display.update()

    camera_video.release()
    cv2.destroyAllWindows()

    if end_game:
        if win_lose == 1:
            game_result.end_game_result(screen, logged_in_user, map_choice, text_you_won)
        else:
            game_result.end_game_result(screen, logged_in_user, map_choice, text_you_lost)
