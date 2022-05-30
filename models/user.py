class User:
    def __init__(self, userId, username, email, wins, losses, lvl, xp, money, equipped_icon):
        self.userId = userId
        self.username = username
        self.email = email
        self.wins = wins
        self.losses = losses
        self.lvl = lvl
        self.xp = xp
        self.money = money
        self.equipped_icon = equipped_icon

    def get_userId(self):
        return self.userId

    def get_username(self):
        return self.username

    def get_lvl(self):
        return self.lvl

    def get_xp(self):
        return self.xp

    def get_money(self):
        return self.money

    def set_money(self, price):
        self.money = self.money - price

    def get_equipped_icon(self):
        return self.equipped_icon
