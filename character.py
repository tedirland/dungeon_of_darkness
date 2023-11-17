"""Character class and assorted methods"""
import math
from tkinter import SCROLL
import pygame
from constants import OFFSET, RED, SCALE, SCREEN_HEIGHT, SCREEN_WIDTH, SCROLL_THRESH, TILE_SIZE

class Character():
    """
        A class to represent a game character with animations and movement capabilities.

        Attributes:
        ----------
        flip : bool
            A flag to determine if the character image should be flipped horizontally.
        animation_list : list
            A collection of pygame.Surface objects for the character's animation frames.
        frame_index : int
            The index of the current animation frame within the animation list.
        action : int
            The character's current action state (0 for idle, 1 for run).
        update_time : int
            A timestamp to manage animation updates, set to the current time from pygame.
        running : bool
            A flag indicating if the character is in a running state.
        image : pygame.Surface
            The current frame image from the animation list.
        rect : pygame.Rect
            A pygame rectangle representing the character's position and size.

        Methods:
        -------
        __init__(self, x, y, animation_list):
            Initializes the character with the provided x, y coordinates, and animation frames.

        move(self, dx, dy):
            Updates the character's position by the specified amounts in the x (dx) and y (dy) directions.

        update(self):
            Updates the character's current action state and animation frame.

        update_action(self, new_action):
            Changes the character's action state and resets the animation settings.

        draw(self, surface):
            Draws the character on the given surface, flipping the image if necessary and outlining the character's rect.

        Parameters:
        ----------
        x : int
            The x-coordinate of the character's initial center position.
        y : int
            The y-coordinate of the character's initial center position.
        animation_list : list
            A list containing the animation frames for different actions.
        dx : int
            The change in the x-coordinate of the character's position.
        dy : int
            The change in the y-coordinate of the character's position.
        new_action : int
            The new action state to update the character's current action.
        surface : pygame.Surface
            The surface on which the character is to be drawn.

        Returns:
        -------
        None
        """
    def __init__(self,x, y, health, mob_animations, char_type):
        self.char_type = char_type
        self.flip = False
        self.animation_list = mob_animations[char_type]
        self.frame_index = 0
        self.coins = 0
        self.action = 0 #0: idle, 1:run
        self.update_time = pygame.time.get_ticks()
        self.running = False
        self.health = health
        self.alive = True
        
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,TILE_SIZE, TILE_SIZE)
        self.rect.center = (x,y)
    
    
    def move(self, dx, dy ):
        """Move is a method on the Character class.
        It takes in an two integers (`dx` and `dy`) that represent the speed the character is travelling along the x or y vectors. It toggles the animation between running and idle and flips the sprite if travelling in a negative vector on the x axis.
        Ultimately, the x and y coordinates are incremented by the provided dx and dy values"""
        screen_scroll = [0,0]
        self.running = False
        if dx != 0 or dy != 0:
            self.running = True
        if dx < 0:
            self.flip = True
        if dx > 0: self.flip = False
        # control diagonal speed
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2) /2)
            dy = dy *(math.sqrt(2) /2)

        self.rect.x += dx
        self.rect.y += dy

        # only apply to player
        if self.char_type == 0:

            # update scroll based on player position
            # move camera left and right
            if self.rect.right > (SCREEN_WIDTH - SCROLL_THRESH):
                screen_scroll[0] =  (SCREEN_WIDTH - SCROLL_THRESH) - self.rect.right
                self.rect.right = SCREEN_WIDTH - SCROLL_THRESH
            if self.rect.left <  SCROLL_THRESH:
                screen_scroll[0] = SCROLL_THRESH - self.rect.left
                self.rect.left = SCROLL_THRESH
                # move camera up and down
            if self.rect.bottom > (SCREEN_HEIGHT - SCROLL_THRESH):
                screen_scroll[1] =  (SCREEN_HEIGHT - SCROLL_THRESH) - self.rect.bottom
                self.rect.bottom = SCREEN_HEIGHT - SCROLL_THRESH
            if self.rect.top <  SCROLL_THRESH:
                screen_scroll[1] = SCROLL_THRESH - self.rect.top
                self.rect.top = SCROLL_THRESH
        return screen_scroll


    def ai(self, screen_scroll):

        # reposition mob based on screen scroll
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]


    def update(self):
        """
        Updates the character's animation state and frame based on its actions and timing.

        This method checks the character's current action (running or idle) and updates
        the action state accordingly. It then proceeds to handle the animation timing,
        updating the character's current frame and resetting the frame index if the end
        of the animation sequence is reached. This ensures the animation loops correctly.

        The method uses an 'animation_cooldown' variable to control the speed of the
        frame change, making the animation appear smoother.

        Attributes modified:
        -------------------
        self.image : pygame.Surface
            The current image of the character's animation frame is updated.
        self.frame_index : int
            The index of the current frame in the animation list is incremented or reset.
        self.update_time : int
            The timestamp of the last update is reset to the current time from pygame.

        Preconditions:
        --------------
        The 'self.animation_list' should be properly initialized with a list of frame sequences,
        where each sequence corresponds to an action.

        Postconditions:
        ---------------
        The character's image and frame index are updated, which will affect the character's
        appearance on the next draw call.

        Returns:
        --------
        None
        """

        # check if character is alive
        if self. health <= 0:
            self.health = 0
            self.alive = False
        # check what action the player is performing
        if self.running == True:
             self.update_action(1) #1: Run
        else:
            self.update_action(0) # 0 : Idle
        animation_cooldown = 70
        # handle animation
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() -self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        """
    Updates the character's current action state and resets the animation settings if the action changes.

    If the new action differs from the current action, this method will reset the animation to the first frame
    of the new action and update the timestamp for animation timing. This is typically called when the character's
    state changes, such as transitioning from idle to running or vice versa.

    Parameters:
    -----------
    new_action : int
        An integer representing the new action state of the character. For example, 0 for idle and 1 for running.

    Attributes modified:
    --------------------
    self.action : int
        The current action state of the character is updated to the new action.
    self.frame_index : int
        The index for the current frame is reset to 0 to start the new animation.
    self.update_time : int
        The timestamp of the last update is reset to the current time from pygame.

    Returns:
    --------
    None
    """
        if new_action != self.action:
            self.action = new_action
            # update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        """
    Draws the character's current image to the given surface, flipping the image if necessary.

    This method is responsible for drawing the character's current frame onto the game's surface.
    It checks if the image needs to be flipped horizontally based on the character's direction.
    After adjusting the image accordingly, it draws the image at the character's current position.
    Additionally, it draws a rectangle around the character's image, typically for debugging purposes
    to visualize the character's hitbox or collision area.

    Parameters:
    ----------
    surface : pygame.Surface
        The surface onto which the character's image is to be drawn. This is typically the main display
        surface that is presented to the player.

    Attributes accessed:
    -------------------
    self.image : pygame.Surface
        The current animation frame to be drawn for the character.
    self.flip : bool
        Indicates whether the character's image should be flipped horizontally.
    self.rect : pygame.Rect
        The rectangle that defines the position and size of the character for drawing.

    Note:
    -----
    The RED color used for drawing the rectangle should be predefined as a constant in the scope
    where this method is called, otherwise, a NameError will be raised.

    Returns:
    --------
    None
    """
        flipped_image = pygame.transform.flip(self.image,self.flip, False)
        if self.char_type == 0:
            surface.blit(flipped_image, (self.rect.x, self.rect.y -  SCALE * OFFSET))
        
        else:
            surface.blit(flipped_image, self.rect)
        pygame.draw.rect(surface,RED, self.rect, 1)
    