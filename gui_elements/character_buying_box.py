import pygame
from gui_elements import buttons
from database import queries

pygame.init()
font = pygame.font.SysFont('Arial', 22)
coin = pygame.image.load('../assets/misc/coin.png')


class Character_Buying_Box:
    def __init__(self, width, height, pos, champion_id, name, image, hp, attack, defense, energy, price, owned=False,
                 show_owned=True, reward=False, reward_level=0):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.surf = pygame.Surface((width, height))
        self.surf.set_alpha(128)
        self.surf.fill((0, 0, 0))
        self.champion_id = champion_id
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
        self.champ_price = price
        self.price = font.render(str(price), True, '#FFFFFF')
        self.price_rect = self.price.get_rect(topleft=(self.top_rect.centerx - 70, self.top_rect.centery + 120))
        self.coins = coin
        self.coins_rect = self.coins.get_rect(topleft=(self.top_rect.centerx - 100, self.top_rect.centery + 120))
        self.buy_button = buttons.Button('BUY', 60, 25, (self.top_rect.centerx + 10, self.top_rect.centery + 120), font)
        self.owned = owned
        self.show_owned = show_owned
        self.reward = reward
        self.reward_level = reward_level
        self.claim_button = buttons.Button('CLAIM', 60, 25, (self.top_rect.centerx + 10, self.top_rect.centery + 120), font)

    def draw(self, screen, logged_in_user):
        screen.blit(self.surf, self.top_rect)
        screen.blit(self.name, self.name_rect)
        screen.blit(self.image, self.image_rect)
        screen.blit(self.hp, self.hp_rect)
        screen.blit(self.attack, self.attack_rect)
        screen.blit(self.defense, self.defense_rect)
        screen.blit(self.energy, self.energy_rect)
        if self.owned:
            if self.show_owned:
                owned_text = font.render('OWNED', True, '#FFFFFF')
                owned_text_rect = owned_text.get_rect(
                    center=(self.top_rect.midbottom[0], self.top_rect.midbottom[1] - 20))
                screen.blit(owned_text, owned_text_rect)
        else:
            if self.reward:
                if logged_in_user.get_lvl() < self.reward_level:
                    reward_level_text = font.render("Level " + str(self.reward_level), True, '#FFFFFF')
                    reward_level_text_rect = reward_level_text.get_rect(
                        center=(self.top_rect.midbottom[0], self.top_rect.midbottom[1] - 20))
                    screen.blit(reward_level_text, reward_level_text_rect)
                else:
                    if self.claim_button.draw(screen):
                        self.owned = True
                        queries.add_user_champion(logged_in_user.get_userId(), self.champion_id)
            else:
                screen.blit(self.price, self.price_rect)
                screen.blit(self.coins, self.coins_rect)
                if self.buy_button.draw(screen):
                    if logged_in_user.get_money() >= int(self.champ_price):
                        self.owned = True
                        queries.add_user_champion(logged_in_user.get_userId(), self.champion_id)
                        return self.champ_price
                    else:
                        return -1
