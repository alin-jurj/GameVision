class Skill:
    def __init__(self, skill_id, champion_id, skill_name, type, ranged, damage, energy_cost):
        self.skill_id = skill_id
        self.champion_id = champion_id
        self.skill_name = skill_name
        self.type = type
        self.ranged = ranged
        self.damage = damage
        self.energy_cost = energy_cost
