class Particle:
    def __init__(self, game, p_type, pos, velocity = [0,0], frame = 0):
        self.game = game
        self.type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animations = self.game.assets['particle/' + p_type].copy()
        self.animations.frame = frame

    def update(self):
        kill = False
        if self.animations.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animations.update()

        return kill
    
    def render(self, surf, offset=(0,0)):
        img = self.animations.img()
        surf.blit(img, (self.pos[0] - offset[0] - img.get_width() // 2, self.pos[1] - offset[1] - img.get_height() // 2))