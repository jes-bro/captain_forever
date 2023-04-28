import pygame
import math


class Controller(Ship):
    def __init__(self, ship, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = 0  # initial
        self.vx = 0
        self.vy = 0
        self.ship = ship

    def move_forward(self):
        self.x += self.vx
        self.y += self.vy

    def move_backward(self):
        self.x -= self.vx
        self.y -= self.vy

    def rotate(self, angle):
        self.angle += angle
        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        self.vx = math.cos(math.radians(self.angle)) * self.speed
        self.vy = -math.sin(math.radians(self.angle)) * self.speed

    def move(self, input_key):
        if input_key.type == pygame.KEYDOWN:
            if input_key.key == pygame.K_a:  # Rotate counterclockwise
                self.ship.rotate(-1)
            elif input_key.key == pygame.K_d:  # Rotate clockwise
                self.ship.rotate(1)
            elif input_key.key == pygame.K_w:  # Forward
                self.ship.move_forward()
            elif input_key.key == pygame.K_s:  # Backward
                self.ship.move_backward()
        elif input_key.type == pygame.KEYUP:
            if input_key.key in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):
                self.ship.stop_moving()

    def update(self):
        for event in pygame.event.get():
            self.move(event)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.ship.accelerate()
            elif event.key == pygame.K_a:
                self.ship.rotate(clockwise=False)
            elif event.key == pygame.K_d:
                self.ship.rotate(clockwise=True)
