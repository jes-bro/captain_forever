# Simple pygame program

import pygame
# Import and initialize the pygame library
# pygame.init()

# # Set up the drawing window
# screen = pygame.display.set_mode([500, 500])

# # Run until the user asks to quit
# running = True
# while running:

#     # Did the user click the window close button?
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Fill the background with white
#     screen.fill((255, 255, 255))

#     # Draw a solid blue circle in the center
#     pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

#     # Flip the display
#     pygame.display.flip()

# # Done! Time to quit.
# pygame.quit()

# Initialise pygame
pygame.init()

# Set window size
size = width, height = 600, 600
screen = pygame.display.set_mode(size)

# Clock
clock = pygame.time.Clock()

# Load image
image = pygame.image.load("../assets/sprites/player_ship_smol.png")

# Set the size for the image
DEFAULT_IMAGE_SIZE = (75, 75)

# Scale the image to your needed size
image = pygame.transform.scale(image, DEFAULT_IMAGE_SIZE)
# pygame.image.save(image, "../assets/sprites/ship.png")

# Set a default position
DEFAULT_IMAGE_POSITION = (200, 200)

# Prepare loop condition
running = False

# Event loop
while not running:

    # Close window event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True

    # Background Color
    screen.fill((0, 0, 0))

    # Show the image
    screen.blit(image, DEFAULT_IMAGE_POSITION)

    # Part of event loop
    pygame.display.flip()
    clock.tick(30)
