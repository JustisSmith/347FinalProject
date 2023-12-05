import pygame.locals as keys
import pygame

class PlayerState:
    """
    Base class for the player's state machine.
    """
    def __init__(self, parent, anim=None, flip=False, jump=False, slide=False):
        """
        Initialize parent (the player), an animation
        to switch to on entry for the state, and
        the horizontal orientation.
        @parent : Reference to the player object.
        @anim : Name of the animation to play on
        entry, if any.
        @flip : Horizontal flip for the animation
        as a boolean.
        """
        self.parent = parent
        self.flip = flip
        self.jump = jump
        self.slide = slide
        if anim:
            self.parent.anim.change(anim)
        self.parent.anim.flipHoriz(flip)

    def processInput(self, pressed):
        """
        Stub method for processing input from the
        keyboard. Passes because some states may
        block input.
        @pressed : A sequence of booleans; one for each key.
        """
        pass
    
    def update(self):
        """
        Stub method for a frame-by-frame update. 
        Passes because some states may only process 
        input without updating.
        """
        pass
        
class StandingState(PlayerState):
    """
    State for when the player is standing still.
    """
    def __init__(self, parent, flip=False, jump=False):
        """
        Initialize and set the horizontal speed
        to be still.
        @parent : Reference to the player object.
        @flip : Horizontal flip for the animation
        as a boolean.
        """
        super().__init__(parent, "stand", flip, jump)
        self.parent.kinem.vel_x = 0
        self.parent.kinem.accel_y = 0.5

    def processInput(self, pressed):
        """
        If left is pressed, the player should begin
        running to the left (non-flipped is facing
        right so flip equals True here). Otherwise
        if right is pressed, begin running to the
        right.
        @pressed : A sequence of booleans; one for each key.
        """
        if not pressed[keys.K_SPACE]:
            self.jump = True
        if pressed[keys.K_LEFT]:
            return RunningState(self.parent, flip=True)
        if pressed[keys.K_RIGHT]:
            return RunningState(self.parent, flip=False)
        if pressed[keys.K_SPACE] and self.jump == True:
            return FirstJumpState(self.parent, self.flip)      
    
class RunningState(PlayerState):
    """
    State for when the player is running along the ground.
    """
    def __init__(self, parent, flip=False, jump=False):
        """
        Initialize and set the horizontal speed
        to be moving in the appropriate direction.
        @parent : Reference to the player object.
        @flip : Horizontal direction for the animation
        and movement as a boolean. True for right, False
        for left.
        """
        super().__init__(parent, "run", flip, jump)
        self.parent.kinem.vel_x = -5 if flip else 5

    def processInput(self, pressed):
        """
        If moving left and left key is released, switch
        to standing still. Else if moving right and right
        key is released, switch to standing still.
        @pressed : A sequence of booleans; one for each key.
        """
        if not pressed[keys.K_SPACE]:
            self.jump = True
        if pressed [keys.K_SPACE] and self.jump == True:
            return FirstJumpState(self.parent, self.flip)
        if self.flip and not pressed[keys.K_LEFT]:
            return StandingState(self.parent, self.flip)
        if not self.flip and not pressed[keys.K_RIGHT]:
            return StandingState(self.parent, self.flip)

class FirstJumpState(PlayerState):
    """
    State for the first jump.
    """
    def __init__(self, parent, flip=False, jump=False):
        super().__init__(parent, "jump", flip, jump)
        self.parent.kinem.vel_y = -10
        self.parent.kinem.vel_x = 0

    def processInput(self, pressed):
        if pressed[keys.K_LEFT]:
            self.parent.kinem.vel_x = -5
            self.flip = True
            self.parent.anim.flipHoriz(flip=True)
        if pressed[keys.K_RIGHT]:
            self.parent.kinem.vel_x = 5
            self.flip = False
            self.parent.anim.flipHoriz(flip=False)

    def update(self):
        if self.parent.kinem.vel_y == 0:
            return FirstFallingState(self.parent, self.flip)
        
class FirstFallingState(PlayerState):
    """
    State for when the player is falling after first jump
    """
    def __init__(self, parent, flip=False):
        super().__init__(parent, "fall", flip)

    def processInput(self, pressed):
        if pressed[keys.K_LEFT]:
            self.parent.kinem.vel_x = -5
            self.flip = True
            self.parent.anim.flipHoriz(flip=True)
        if pressed[keys.K_RIGHT]:
            self.parent.kinem.vel_x = 5
            self.flip = False
            self.parent.anim.flipHoriz(flip=False)
        
    def update(self):
        if self.parent.kinem.vel_y == 0:
            return StandingState(self.parent, self.flip)
        if pygame.sprite.spritecollideany(self.parent, self.parent.game.colliders, collided=pygame.sprite.collide_rect_ratio(1.2)):
            return WallSlideState(self.parent, self.flip)      
        
class WallSlideState(PlayerState):
    """
    State for when player is sliding on wall
    """
    def __init__(self, parent, flip=False, jump=False, slide=False):
        super().__init__(parent, "stand", flip, jump)
        self.parent.kinem.accel_y = 0.01

    def processInput(self, pressed):
        if not pressed[keys.K_SPACE]:
            self.jump = True
        if pressed[keys.K_SPACE] and self.jump == True:
            return WallJumpState(self.parent, self.flip)
        if pressed[keys.K_LEFT]:
            self.parent.kinem.vel_x = -5
            self.flip = True
            self.parent.anim.flipHoriz(flip=True)
        if pressed[keys.K_RIGHT]:
            self.parent.kinem.vel_x = 5
            self.flip = False
            self.parent.anim.flipHoriz(flip=False)

    def update(self):
        if self.parent.kinem.vel_y == 0:
            return StandingState(self.parent, self.flip)
        
class WallJumpState(PlayerState):
    """
    State that launches player off wall after jump, player can not move
    """
    def __init__(self, parent, flip=False):
        super().__init__(parent, "jump", flip)
        self.parent.kinem.accel_y = 0.5
        self.parent.kinem.vel_y = -12

        player_rect = self.parent.rect.inflate(5, 0)

        for wall in self.parent.game.colliders:
            wall_rect = wall.rect
            if player_rect.colliderect(wall.rect):
                if self.parent.rect.midleft > wall_rect.midleft:
                    self.parent.kinem.vel_x = 8
                elif self.parent.rect.midleft < wall_rect.midleft:
                    self.parent.kinem.vel_x = -8

    def processInput(self, pressed):
        if pressed[keys.K_LEFT]:
            #self.parent.kinem.vel_x = -5
            self.flip = True
            self.parent.anim.flipHoriz(flip=True)
        if pressed[keys.K_RIGHT]:
            #self.parent.kinem.vel_x = 5
            self.flip = False
            self.parent.anim.flipHoriz(flip=False)

    def update(self):
        if self.parent.kinem.vel_y >= -6:
            return WallJumpState2(self.parent, self.flip)
        
class WallJumpState2(PlayerState):
    """
    State for when player can move in the air after wall jump
    """
    def __init__(self, parent, flip=False, slide = False):
        super().__init__(parent, "jump", flip, slide)
        
    def processInput(self, pressed):
        if pressed[keys.K_LEFT]:
            self.parent.kinem.vel_x = -5
            self.flip = True
            self.parent.anim.flipHoriz(flip=True)
        if pressed[keys.K_RIGHT]:
            self.parent.kinem.vel_x = 5
            self.flip = False
            self.parent.anim.flipHoriz(flip=False)

    def update(self):
        if self.parent.kinem.vel_y == 0:
            return WallFallingState(self.parent, self.flip)
        if pygame.sprite.spritecollideany(self.parent, self.parent.game.colliders, collided=pygame.sprite.collide_rect_ratio(1.2)):
            return WallSlideState(self.parent, self.flip)
        
class WallFallingState(PlayerState):
    """        
    State for when the player is falling after a wall jump
    """
    def __init__(self, parent, flip=False, slide = False):
        super().__init__(parent, "fall", flip, slide)

    def processInput(self, pressed):
        if pressed[keys.K_LEFT]:
            self.parent.kinem.vel_x = -5
            self.flip = True
            self.parent.anim.flipHoriz(flip=True)
        if pressed[keys.K_RIGHT]:
            self.parent.kinem.vel_x = 5
            self.flip = False
            self.parent.anim.flipHoriz(flip=False)

    def update(self):
        if self.parent.kinem.vel_y == 0:
            return StandingState(self.parent, self.flip)
        if not pygame.sprite.spritecollideany(self.parent, self.parent.game.colliders, collided=pygame.sprite.collide_rect_ratio(1.2)):
            self.slide = True
        if pygame.sprite.spritecollideany(self.parent, self.parent.game.colliders, collided=pygame.sprite.collide_rect_ratio(1.2)) and self.slide == True:
            return WallSlideState(self.parent, self.flip)