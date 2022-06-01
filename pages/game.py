from curses.panel import bottom_panel
import random
import pygame
from pages import main_page
from database import queries
from gui_elements import image_buttons, buttons, character_buying_box, icon_box

pygame.init()

font = pygame.font.SysFont('Times New Roman', 26)
FPS = 60
clock = pygame.time.Clock()
# map1 = pygame.image.load('../assets/maps/map_1.png')
# map2 = pygame.image.load('../assets/maps/map_2.png')
# map3 = pygame.image.load('../assets/maps/map_3.png')
WIDTH, HEIGHT ,bottom_panel= 1280, 720,  150
color = pygame.Color('#2C7950')
FONT = pygame.font.Font(None, 72)
button_font = pygame.font.SysFont('Arial', 28)
text_font = pygame.font.SysFont('Arial', 32)
back = pygame.image.load('../assets/misc/back.png')
path_to_char = '../assets/characters/body/'
path_to_icons = '../assets/icons/'

red = (255, 0, 0)
green = (0, 255, 0)

def draw_text(screen,text,font, text_col, x, y):
    img = font.render(text,True, text_col)
    screen.blit(img,x,y)

def draw_panel(screen):
    draw_text(screen,f'{knight.name} HP: {knight.hp}', font, red, 100, HEIGHT-200)
    draw_text(screen,f'{enemy.name} HP: {enemy.hp}', font, red, 100, HEIGHT-200)

class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potions):
        self.name=name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.potions= potions
        self.alive = True
        self.animation_list = []
        self.frame_index=0
        self.action = 0 #0.idle, 1.attack, 2:hurt, 3:dead
        self.update_time=pygame.time.get_ticks()
        #load idle images
        temp_list = []
        for i in range(8):
            img= pygame.image.load(f'../assets/img/{self.name}/Idle/{i}.png').convert_alpha()
            temp_list.append(img)
        #load attack images
        temp_list = []
        for i in range(8):
            img= pygame.image.load(f'../assets/img/{self.name}/Attack/{i}.png').convert_alpha()
            temp_list.append(img)
        #load hurt images
        temp_list = []
        for i in range(8):
            img= pygame.image.load(f'../assets/img/{self.name}/Hurt/{i}.png').convert_alpha()
            temp_list.append(img)
        #load dead_images
        temp_list = []
        for i in range(8):
            img= pygame.image.load(f'../assets/img/{self.name}/Dead/{i}.png').convert_alpha()
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect= self.image.get_rect()
        self.rect.center = (x,y)

    def update(self):
        animation_cooldown=100
        #handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.idle()
    
    def idle(self):
        self.action = 0
        self.frame_index=0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        rand= random.randint(-5,5)
        damage = self.strength + rand
        target.hp -= damage
        #check if target has died
        if target.alive <1:
            target.hp = 0
            target.alive = False

        self.action = 1
        self.frame_index=0
        self.update_time = pygame.time.get_ticks()

    def draw(self,screen):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x=x
        self.y=y
        self.hp=hp
        self.max_hp = max_hp
    
    def draw(self,screen,hp):
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150,20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150*ratio,20))





def game(screen, logged_in_user, map_choice, player_champion, enemy_champion, player_skills, enemy_skills):
    

    back_button = image_buttons.ImageButton(back, 1, (1136, 24))
    knight= Fighter(200,260, 'Knight',30,10,3)
    enemy= Fighter(200,260, 'Bandit',30,10,3)
    run = True
    main = False

    while run:
        screen.fill((0, 0, 0))
        screen.blit(map_choice, (0, 0))
        clock.tick(FPS)

        if back_button.draw(screen):
            run = False
            main = True

        knight.update()
        knight.draw()

        #player1 action

        # if knight.alive == True:
        #     if current_fighter == 1:
        #         action_cooldown+=1
        #         if action_cooldown >= action_wait_time:
        #             knight.attack(enemy)
        #             current_fighter+=1
        #             action_cooldown=0
        # # player2 action
        # if enemy.alive==True:
        #     action_cooldown +=1
        #     if action_cooldown >= action_wait_time:
        #         enemy.attac(knight)
        #         current_fighter +=1
        #         action_cooldown = 0
        
        # if current_fighter > 2:
        #     current_fighter=1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    if main:
        main_page.main_page(screen, logged_in_user)
