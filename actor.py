import pygame

import state
from anim import Animator

class Kinematics:
    """
    Class that handles basic physics
    calculations for actors (or anything
    with a rect controlling its position).
    """
    def __init__(self, parent ,x , y, rect):
        """
        Initializes parent, velocity, and
        acceleration in 2D. If you want to
        change these values, set them
        directly:
        @vel_x controls x velocity.
        @vel_y controls y velocity.
        @accel_x controls x acceleration.
        @accel_y controls y acceleration.

        @parent : Anything with a rect attribute controlling
        their position. Any updates and reversions
        will take place on this object's rect.
        """
        self.parent = parent
        self.vel_x = 0
        self.vel_y = 0
        self.accel_x = 0
        self.accel_y = 0
        self.level = 1
        self.max_level = 3

        self.x = x
        self.y = y
        self.rect = rect

        self.old_x = x
        self.old_y = y

        #self.last_revert_time = 0

    def updateX(self, tilemap, movement):
        """
        Update x velocity based on acceleration,
        update x position in parent based on velocity.
        """
        self.vel_x += self.accel_x
        self.old_x = self.parent.rect.x
        self.parent.rect.x = self.parent.rect.x + self.vel_x 

        self.x += self.vel_x 
        pos = (self.x,self.parent.rect.bottom)
        
        for rect in tilemap.physics_rects_around((self.x, self.y)):
            if self.rect.colliderect(rect):
                if self.vel_x > 0:
                    correction = rect.left - self.rect.right
                else:
                    correction = rect.right - self.rect.left
                
                self.parent.rect.x += correction
                self.x += correction
                self.vel_x = 0

                for tile in tilemap.tiles_around(pos):
                    if((tile['type'] == 'lava') or (tile['type'] == 'traps')):
                        self.x = 0
                        self.y = 0
                    elif(tile['type'] == 'portal'):
                        self.level += 1
                        if(self.level <= self.max_level):
                            self.map_level = f'map{self.level}.json'
                            #print(self.map_level)
                            tilemap.load(self.map_level)
                            self.x = 50
                            self.y = 600
                return
        #self.x += self.vel_x


        """
        frame_movementx = (movement[0] + self.vel_x)
        self.x += frame_movementx

        for prect in tilemap.physics_rects_around((self.x,self.y)):
            if self.rect.colliderect(prect):
                #self.revertX()
                pass
        """
        



    def updateY(self, tilemap, movement):
        """
        Update x velocity based on acceleration,
        update x position in parent based on velocity.
        """
        self.vel_y += self.accel_y 
        self.old_y = self.parent.rect.y
        self.parent.rect.y = self.parent.rect.y + self.vel_y

        self.y += self.vel_y
        pos = (self.x,self.parent.rect.bottom)
        #print(f"{self.parent.rect.bottom=}")
        #player_rect = self.parent.rect.copy()
        #player_rect.y += 1

        for rect in tilemap.physics_rects_around((self.x,self.parent.rect.bottom)):     #adds grass and stone blocks to colliders for wall jump
            for tile in tilemap.tiles_around(pos):
                if((tile['type'] == 'grass') or (tile['type'] == 'stone')):
                    self.parent.game.colliders.add(Collider(rect))

            if self.rect.colliderect(rect):
                #print(f"{rect.top=}, {self.vel_y=}")
                if self.vel_y > 0:
                    correction = rect.top - self.rect.bottom
                else:
                    correction = rect.bottom - self.rect.top
                #print(correction)
                self.parent.rect.y += correction
                self.y += correction
                self.vel_y = 0

                for tile in tilemap.tiles_around(pos):
                    if((tile['type'] == 'lava') or (tile['type'] == 'traps')):
                        self.x = 50
                        self.y = 600
                #self.parent.rect.y = int(self.parent.rect.y / tilemap.tile_size) * tilemap.tile_size
                #self.y = self.parent.rect.y
                return
        #self.y += self.vel_y




        """
        frame_movementy = (movement[1] + self.vel_y)
        self.y += frame_movementy

        print(f"Player Y: {self.parent.rect.y}, Internal Y: {self.y}, Velocity Y: {self.vel_y}")

        for rect in tilemap.physics_rects_around((self.x,self.y)):
            if self.rect.colliderect(rect):
                print("Collision detected. Reverting Y.")
                if self.vel_y > 0:
                    self.revertY()
                    self.grounded = True
                elif self.vel_y < 0:
                    self.revertY()
                
                #self.vel_y = 0
        """
                
        


    def revertX(self):
        """
        Revert parent's x position to previous state
        with no velocity.
        """
        self.vel_x = 0
        self.parent.rect.x = self.old_x

    def revertY(self):
        """
        Revert parent's y position to previous state
        with no velocity.
        """
        self.vel_y = 0
        self.parent.rect.y = self.old_y
        self.parent.y = self.old_y / self.parent.game.tilemap.tile_size

        """
        current_time = pygame.time.get_ticks()

        if current_time - self.last_revert_time > 500:
            self. last_revert_time = current_time
            self.vel_y = 0
            self.parent.rect.y = self.old_y
        """

class Player(pygame.sprite.Sprite):
    
    """
    Class for the player's sprite. Contains components
    for animation and kinematics as well as specialized
    state objects.
    """
    def __init__(self, x, y, game=None):
        """
        Sets up animator, kinematic, and state components.
        @x : Starting x location
        @y : Starting y location
        """
        super().__init__()
        self.game = game
        self.x = x
        self.y = y
        # scale by 3 because the original sprites are small
        self.anim = Animator('slimesprite.png', 5, 1, scale_by = 1)

        #scaled_image = pygame.transform.scale(self.anim.surf, (self.anim.rect.w // 2, self.anim.rect.h // 2))
        #self.rect = scaled_image.get_rect(topleft=(x, y))

        # animations start at 0 and go until 4, all on the 0th row
        # may be different depending on your sprite sheet
        self.anim.registerAnim("stand", (0, 0))
        # this produces [(1,0), (1,0), (1,0)... (0,0), (0,0)...]
        # so on and so forth. 20 frames of animation total
        run_frames = [(1,0)]*6 + [(0,0)]*4 + [(2,0)]*6 + [(0,0)]*4
        # the * syntax here means "unpack". basically unrolling
        # a list into a series of sequential arguments 
        self.anim.registerAnim("run", *run_frames)
        self.anim.registerAnim("jump", (3, 0))
        self.anim.registerAnim("fall", (4, 0))
        self.anim.registerAnim("slide", (2, 0))

        self.rect = pygame.Rect(
            x, y, 16, 16     #x, y, self.anim.rect.w, self.anim.rect.h
        )

        self.kinem = Kinematics(self, x, y, self.rect)
        self.kinem.accel_y = 0.5  # this is the gravity force right here
        # note that downward y is actually positive! negative y is upward

        # initial state = Standing
        self.state = state.StandingState(self)

    def delgateToState(self, method, *args):
        """
        Helper function for functionality controlled
        by state objects. Updates the state if need be.
        @method : Method to call on the state object. 
        Should usually be some variation of `self.state.####`.
        @args : Any number of arguments that should be
        passed into the corresponding state method.
        """
        new_state = method(*args)
        if new_state:
            self.state = new_state

    def processInput(self, pressed):
        """
        Process input using the `pygame.key.get_pressed` method.
        @pressed : A sequence of booleans; one for each key. Should
        be whatever comes out of `pygame.key.get_pressed` (some sort
        of ScanCodeGenerator thing).
        """
        self.delgateToState(self.state.processInput, pressed)

    def update(self, colliders, tilemap, movement=(0,0)):

        """
        Updates state of the player and performs movement.
        Also checks for collisions and reverts movement
        if need be.
        @colliders : Sprite group of walls/floors. Should
        be some variation of `pygame.sprite.Group`.
        """
        self.delgateToState(self.state.update)

        self.kinem.updateX(tilemap, movement)

        #collisions_x = pygame.sprite.spritecollide(self, colliders, False)
        
        #if collisions_x:
            #self.kinem.revertX()
            #self.rect.x = self.kinem.rect.x

        #if pygame.sprite.spritecollideany(self, colliders):
            #self.kinem.revertX()
        self.kinem.updateY(tilemap, movement)

        #collisions_y = pygame.sprite.spritecollide(self, colliders, False)
        
        #if collisions_y:
            #self.kinem.revertY()
            #self.rect.y = self.kinem.rect.y
        

        #if pygame.sprite.spritecollideany(self, colliders):
            #self.kinem.revertY()

        self.rect.x = self.kinem.x
        self.rect.y = self.kinem.y
        


    def render(self, surf):
        """
        Renders the current state of the player to the
        provided Surface.
        @surf : Surface to write to (usually the main screen).
        """
        surf.blit(
            self.anim.surf, self.rect, area=self.anim.rect
        )
        #pygame.draw.rect(surf, (255,0,0), self.rect, width=2)      #debug: shows player hitbox
        self.anim.next()

class Collider(pygame.sprite.Sprite):
    """
    Stationary sprites meant to primary be used for walls and floors.
    """
    def __init__(self, rect, color=None):
        """
        @rect : Position and dimensions of the collider.
        Should be a `pygame.Rect`.
        @color : Color to fill for the collider. If `None`,
        will be transparent.
        """
        super().__init__()
        self.rect = rect
        self.color = color
    
    def render(self, surf):
        """
        Renders the collider to a surface. Only useful 
        if the collider is non-transparent.
        @surf : Surface to write to (usually the main screen).
        """
        if self.color:
            pygame.draw.rect(surf, self.color, self.rect)