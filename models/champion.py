class Champion:
    def __init__(self, image, champion_id, champion_name, hp, attack, defense, energy, price, block_status=False):
        self.image = image
        self.championId = champion_id
        self.championName = champion_name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.energy = energy
        self.price = price
        self.block_status = block_status

    def get_hp(self):
        return self.hp

    def set_hp(self, val):
        self.hp = val

    def get_attack(self):
        return self.attack

    def get_energy(self):
        return self.energy

    def get_block_status(self):
        return self.block_status

    def get_image(self):
        return self.image

    def get_champion_name(self):
        return self.championName
