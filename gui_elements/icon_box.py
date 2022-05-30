import pygame
from gui_elements import buttons
from database import queries

pygame.init()
font = pygame.font.SysFont('Arial', 22)
coin = pygame.image.load('../assets/misc/coin.png')


class IconBox:
    def __init__(self, width, height, pos, icon_id, name, image, price, owned=False, show_owned=True):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.surf = pygame.Surface((width, height))
        self.surf.set_alpha(128)
        self.surf.fill((0, 0, 0))
        self.icon_id = icon_id
        self.name = font.render(name, True, '#FFFFFF')
        self.name_rect = self.name.get_rect(center=(self.top_rect.midtop[0], self.top_rect.midtop[1] + 20))
        self.image = image
        self.image_rect = self.image.get_rect(center=(self.top_rect.centerx, self.top_rect.centery))
        self.icon_price = price
        self.price = font.render(str(price), True, '#FFFFFF')
        self.price_rect = self.price.get_rect(topleft=(self.top_rect.centerx - 50, self.top_rect.centery + 65))
        self.coins = coin
        self.coins_rect = self.coins.get_rect(topleft=(self.top_rect.centerx - 80, self.top_rect.centery + 65))
        self.buy_button = buttons.Button('BUY', 60, 25, (self.top_rect.centerx + 10, self.top_rect.centery + 65), font)
        self.owned = owned
        self.show_owned = show_owned

    def draw(self, screen, logged_in_user):
        screen.blit(self.surf, self.top_rect)
        screen.blit(self.name, self.name_rect)
        screen.blit(self.image, self.image_rect)
        if self.owned:
            if self.show_owned:
                owned_text = font.render('OWNED', True, '#FFFFFF')
                owned_text_rect = owned_text.get_rect(
                    center=(self.top_rect.midbottom[0], self.top_rect.midbottom[1] - 20))
                screen.blit(owned_text, owned_text_rect)
        else:
            screen.blit(self.price, self.price_rect)
            screen.blit(self.coins, self.coins_rect)
            if self.buy_button.draw(screen):
                if logged_in_user.get_money() >= int(self.icon_price):
                    self.owned = True
                    queries.add_user_icon(logged_in_user.get_userId(), self.icon_id)
                    return self.icon_price
                else:
                    print("Not enough money")
                    return -1
