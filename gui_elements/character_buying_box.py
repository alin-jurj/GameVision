import pygame
from gui_elements import buttons

pygame.init()
font = pygame.font.SysFont('Arial', 22)
coin = pygame.image.load('../assets/misc/coin.png')


# , image, hp, attack, defense, energy, price
class Character_Buying_Box:
    def __init__(self, width, height, pos, name, image, hp, attack, defense, energy, price):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.surf = pygame.Surface((width, height))
        self.surf.set_alpha(128)
        self.surf.fill((0, 0, 0))
        self.name = font.render(name, True, '#FFFFFF')
        self.name_rect = self.name.get_rect(center=(self.top_rect.midtop[0], self.top_rect.midtop[1] + 20))
        self.image = image
        self.image_rect = self.image.get_rect(center=(self.top_rect.centerx, self.top_rect.centery - 30))
        self.hp = font.render("HP: " + str(hp), True, '#FFFFFF')
        self.hp_rect = self.hp.get_rect(topleft=(self.top_rect.centerx - 100, self.top_rect.centery + 60))
        self.attack = font.render("Attack: " + str(attack), True, '#FFFFFF')
        self.attack_rect = self.attack.get_rect(topleft=(self.top_rect.centerx + 10, self.top_rect.centery + 60))
        self.defense = font.render("Defense: " + str(defense), True, '#FFFFFF')
        self.defense_rect = self.defense.get_rect(topleft=(self.top_rect.centerx + 10, self.top_rect.centery + 90))
        self.energy = font.render("Energy: " + str(energy), True, '#FFFFFF')
        self.energy_rect = self.energy.get_rect(topleft=(self.top_rect.centerx - 100, self.top_rect.centery + 90))
        self.price = font.render(str(price), True, '#FFFFFF')
        self.price_rect = self.price.get_rect(topleft=(self.top_rect.centerx - 70, self.top_rect.centery + 120))
        self.coins = coin
        self.coins_rect = self.coins.get_rect(topleft=(self.top_rect.centerx - 100, self.top_rect.centery + 120))
        self.buy_button = buttons.Button('BUY', 60, 25, (self.top_rect.centerx + 10, self.top_rect.centery + 120), font)

    def draw(self, screen):
        screen.blit(self.surf, self.top_rect)
        screen.blit(self.name, self.name_rect)
        screen.blit(self.image, self.image_rect)
        screen.blit(self.hp, self.hp_rect)
        screen.blit(self.attack, self.attack_rect)
        screen.blit(self.defense, self.defense_rect)
        screen.blit(self.energy, self.energy_rect)
        screen.blit(self.price, self.price_rect)
        screen.blit(self.coins, self.coins_rect)
        if self.buy_button.draw(screen) == True:
            print('pressed')
