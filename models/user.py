class User:
    def __init__(self, userId, username, email, wins, losses, lvl, xp, money):
        self.userId = userId
        self.username = username
        self.email = email
        self.wins = wins
        self.losses = losses
        self.lvl = lvl
        self.xp = xp
        self.money = money

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
