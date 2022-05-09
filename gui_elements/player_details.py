import pygame

pygame.init()
coin = pygame.image.load('assets/misc/coin.png')


class Player_Details:
    def __init__(self, width, height, pos, font, username, level, xp, money, icon):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.color = '#2C7950'
        self.icon = icon
        self.level = level
        self.xp = xp
        self.text = font.render("Name: " + username, True, '#FFFFFF')
        self.text_rect = self.text.get_rect(topleft=(self.top_rect.centerx - 40, self.top_rect.centery - 62))
        self.level = font.render("Level: " + str(level), True, '#FFFFFF')
        self.level_rect = self.level.get_rect(topleft=(self.top_rect.centerx - 40, self.top_rect.centery - 30))
        self.xp = font.render("Xp: " + str(xp) + "/1000", True, '#FFFFFF')
        self.xp_rect = self.xp.get_rect(topleft=(self.top_rect.centerx - 40, self.top_rect.centery + 2))
        self.money = font.render(str(money), True, '#FFFFFF')
        self.money_rect = self.money.get_rect(topleft=(self.top_rect.centerx, self.top_rect.centery + 34))
        self.coins = coin
        self.coins_rect = self.coins.get_rect(topleft=(self.top_rect.centerx - 40, self.top_rect.centery + 36))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.top_rect, border_radius=10)
        screen.blit(self.text, self.text_rect)
        screen.blit(self.level, self.level_rect)
        screen.blit(self.xp, self.xp_rect)
        screen.blit(self.money, self.money_rect)
        screen.blit(self.coins, self.coins_rect)
        screen.blit(self.icon, self.top_rect)