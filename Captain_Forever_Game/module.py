"""
Ship module creation abstract class and sub-classes
"""
from abc import ABC, abstractmethod


class Module(ABC):
    """
    abstract class to define the controller methods used in control subclasses
    """

    def __init__(self, parent, color):
        """
        initalize instance of a module

        args:
            parent: instance of module which this module is attached to
            color: tier of the module
        """
        colors_hp = {
            "Green": 20,
            "Yellow": 40,
            "Red": 75,
            "Blue": 125,
            "Purple": 200,
        }
        self._parent = parent
        self._children = None
        self._hp = colors_hp[color]
        self.available_slots = 3  # override for laser/eng/large hull
        # probably will need a property for containing the sprite?

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

    def attach_module(self, new_child):
        """
        attaches new child module to this module
        """
        if self.available_slots > 0:
            self._children += new_child
            self.available_slots -= 1

    def remove_module(self, removed_module):
        """
        removes module from the children list and adds a free attach slot
        """
        # this may not work if the children list has identical instances
        if removed_module in self._children:
            self._children.remove(removed_module)
            self.available_slots += 1

    def kill_children(self):
        """
        destroys any child modules
        """
        # unsure about how to implement this method
        for child in self.get_children():
            child.destroy()
            self._children.remove(child)

    def destroy(self):
        """
        destroys a module
        """
        pass

    @abstractmethod
    def position(self):
        """
        method to represent getting the position from a module for displaying
        """
        pass

    @abstractmethod
    def change_velocity(self):
        """
        method to change velocity of a module
        """
        pass


class PygameModule(Module):
    """
    Class for modules that depend on pygame
    """

    def move(self):
        """
        prompts player for input to create a tic tac toe move on text board
        """
        moving_player = super().board.next_move()
        move_coords = input(
            f"{moving_player}: Input row, column between 0 0 and 2 2: "
        )
        try:
            row = int(move_coords[0])
            column = int(move_coords[2])
            super().board.mark(row, column)
        except (ValueError, IndexError):
            print("Please input a valid empty square")
            self.move()
