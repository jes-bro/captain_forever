import pygame
import math


class Controller:
    def __init__(self, Ship):
        self.Ship = Ship

    def update(self):
        for event in pygame.event.get():
            self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.Ship.accelerate()
            elif event.key == pygame.K_a:
                self.Ship.rotate(clockwise=False)
            elif event.key == pygame.K_d:
                self.Ship.rotate(clockwise=True)
