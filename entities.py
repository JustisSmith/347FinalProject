import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}             # Dictionary of collisions

        self.action = ''                                                                          # Actions for different animations ex. run, idle, jump
        self.anim_offset = (-3, -3)
        self.flip = False                                                                   
        self.set_action('idle')

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):                                                                 # Changes the animation depending on the action
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def update(self, tilemap, movement=(0,0)):
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])         # Movement

        self.pos[0] += frame_movement[0]                                        # Collision in the x direction
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]                                        # Collision in the y direction
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:                                                    # If facing right, flip is false
            self.flip = False
        if movement[0] < 0:                                                    # If facing left, flip is true and player is fliped in x direction
            self.flip = True

        self.velocity[1] = min(5, self.velocity[1] + 0.1)          # Terminal velocity set at 5 otherise self.velocity[1] += 0.1

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Player(PhysicsEntity):                                               # Inherites from the Physics Entity class to create the player
    def __init__(self, game, pos, size):
        super().__init__(game, 'player',  pos, size)

        self.air_time = 0

    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement = movement)

        self.air_time += 1                                                  
        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:                                                # Sets the animation to jump if in the air
            self.set_action('jump')
        elif movement[0] != 0:                                               # If moving in x direction, set the animation to run
            self.set_action('run')
        else:                                                                # Else the animation is idle
            self.set_action('idle')