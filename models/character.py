
class Character:
    def __init__(self, hp, attack, defense, energy, block_status=False):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.energy = energy

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