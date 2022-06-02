class Skill:
    def __init__(self, x, y, skill_id, champion_id, skill_name, type, ranged, damage, energy_cost, image):
        self.x = x
        self.skill_id = skill_id
        self.champion_id = champion_id
        self.skill_name = skill_name
        self.type = type
        self.ranged = ranged
        self.damage = damage
        self.energy_cost = energy_cost
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update_position(self, new_x, new_y):
        self.rect.center = (new_x, new_y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
