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

    def add_money(self, add):
        self.money = self.money + add

    def set_xp(self, add):
        self.xp = self.xp + add
        if self.xp >= 1000:
            self.xp = 0
            self.lvl = self.lvl + 1

    def get_equipped_icon(self):
        return self.equipped_icon

    def set_equipped_icon(self, icon_id):
        self.equipped_icon = icon_id

    def add_wins(self):
        self.wins = self.wins + 1

    def get_wins(self):
        return self.wins

    def add_losses(self):
        self.losses = self.losses + 1

    def get_losses(self):
        return self.losses
