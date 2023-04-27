"""
Ship module creation abstract class and sub-classes
"""
from abc import ABC, abstractmethod
import pygame
import math
from pygame.math import Vector2


class Module(pygame.sprite.Sprite):
    """
    abstract class to define the module methods used in module 
    subclasses managed in different ways

    """

    def __init__(self, angle_to_y, module_type, color, x, y, parent=None):
        """
        initalize instance of a module

        args:
            angle_to_y: int, 90 clockwise degree increments from vertical orientation i.e. 90 = gun facing right 
            module_type: str, Engine Hull Command Laser. Maps to different sprites (managed globally)
            color: str, tier of the module. different tiers have different health/damage
            x: int, x coordinate in pix to draw module attach point in (0, 0 is top left of screen)
            y: int, y coordinate in pix to draw module attach point in (0, 0 is top left of screen)
            parent: instance of module which this module is attached to

        """
        super().__init__(self)
        colors_hp = {
            "Green": 20,
            "Yellow": 40,
            "Red": 75,
            "Blue": 125,
            "Purple": 200,
        }

        # loads sprite assuming that it is in appropriate folder with
        # the name of the sprite color (NOT type/color)
        # TODO: replace with new global function with wrapped procesing
        self.image = pygame.image.load(
            f"Media/module_renders/{module_type}/{color}")

        self._orientation = angle_to_y

        # returns vector to bottom center (attachment) NOT centroid!
        self._radius = self.set_orientation(angle_to_y)

        # get coords to initialize sprite from input args
        self._position = pygame.Vector2(x, y)

        # attachment points will be acessed by ship and controller ? methods
        # for checking closeness. will need a local and global vector
        self._attachment_points = self.initialize_slots()

        self._type = module_type
        self._parent = parent
        self._children = []
        self._hp = colors_hp[color]
        self.available_slots = 3  # override for laser/eng/large hull
        # probably will need a property for containing the sprite?

    def initialize_slots(self):
        """
        generates available attachment points 
        """
        top_slot = Vector2(0, self.image.get_height)
        right_slot = Vector2(.5*self.image.get_width, .5*self.image.get_height)
        left_slot = Vector2(-.5*self.image.get_width, .5*self.image.get_height)
        return [top_slot, right_slot, left_slot]

    def draw(self, surface):
        """
        draws the module at its designated position on a Surface (ship or space)

        args: 
            Surface: surface (pygame.sprite.Sprite) which contains other modules
        """

        blit_position = self.get_position - self._radius
        surface.blit(self.image, blit_position)

    def set_orientation(self, deg_from_y_ax):
        """
        rotates the module for placement on a new ship

        args: 
            angle_to_y: int, 90 clockwise degree increments from vertical orientation i.e. 90 = gun facing right 

        note: the position
        """
        rotation = math.radians(self._orientation)
        self.image = pygame.transform.rotate(self.image, -deg_from_y_ax)
        x_scaling = -.5*math.sin(rotation)+.5
        y_scaling = .5*math.cos(rotation)+.5

        # creates a vector which will give pixels from "attachment point" of module to top left of sprite
        # attachments are on the "bottom" of most sprites, when welded onto ship
        return Vector2(self.image.get_width * x_scaling, self.image.get_height * y_scaling)

    def damage(self, amount):
        """
        damages module by an amount (reduces hp)

        args: 
            amount: int, hp to be subtracted 
        """
        self._hp = max(self._hp - amount, 0)
        if self._hp == 1:
            self.die()
        # kill the module if hp reaches zero

    @property
    def get_parent(self):
        """
        returns private parent attribute
        """
        return self._parent

    @property
    def get_children(self):
        """
        returns list of child modules (including children children...)
        """
        return self._children

    def add_child(self, new_child):
        """
        adds attaching module the child list of all parent modules in chain
        """
        self._children += new_child
        self._parent.add_child(new_child)
        # hopefully this line recursively adds children to all chained modules

    def attach_module(self, new_child, location):
        """
        attaches new child module to this module
        """

        if self.available_slots > 0:
            self.available_slots.remove(location)
            self.add_child(new_child)
            self.available_slots -= 1

    def remove_module(self, removed_module):
        """
        removes module from the children list and adds a free attach slot
        """
        # this may not work if the children list has identical instances
        if removed_module in self._children:
            self._children.remove(removed_module)
            self.available_slots += 1

    def die(self):
        """
        destroys a module (removes sprite from all groups)
        """

        # also kills child modules!!
        for child in self.get_children():
            child.die()
            self._children.remove(child)

        self.kill()
        #  TODO: add in an animation
        # TODO: add in a sound

    @property
    def get_position(self):
        """
        method to represent getting the position from a module for displaying
        """
        return self._position

    def change_velocity(self):
        """
        method to change velocity of a module
        """
        pass


class Laser(Module):
    """
    Class for lasers which manages firing lasers, and makes sure they don't have attachments
    """

    def __init__(self):
        # calls init of overall module class
        super().__init__()
        self._power = self._hp * .5
        self.available_slots = 0

        # TODO: add projectile class
        # self._muzzle_velocity = Vector2()

    def fire(self):
        """
        fires laser of damage power (attribute)   
        """
        pass


class Command(Module):
    """
    Class which manages the central module of a ship. Death triggers an event

    Note: command module does start with 1 laser
    """

    def __init__(self):
        # calls init of overall module class
        super().__init__(0, "Command", "Red", 0, 0, parent=None)
        # command module will always be at the center of a ship (I hope)
        self._radius = Vector2(.5*self.image.get_width, .5 *
                               self.image.get_height)

    def damage(self, amount):
        """
        damages central module by an amount (reduces hp). If reaches zero, destroy + raise event

        args: 
            amount: int, hp to be subtracted 
        """
        self._hp = max(self._hp - amount, 0)
        if self._hp == 0:
            for child in self.get_children():
                child.die()
                self._children.remove(child)

        # end the game if hp reaches zero
        # TODO: create event callback in main game loop for death

    def fire(self):
        """
        fires laser of damage power (attribute)   
        TODO: create object/velocity callback in main game

        """
        pass
