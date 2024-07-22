# necesery imports
import pygame
import random
import math

    # Classes
# player class
class Player:
    def __init__(self, x, y, image, size):
        self.x = x
        self.y = y
        self.vertical_speed = 0
        self.horizontal_speed = 0
        self.angle = 0
        self.image = image
        self.size = size
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self, speed, type):
        global current_direction
        #print(current_direction)
        #print(player.horizontal_speed, player.vertical_speed)
        print(speed)
        print(type)
        #print(self.x, self.y)
        if type == "horizontal":
            #if speed > 0:
            #    speed -= 1
            #elif speed < 0:
            #    speed += 1
            #else:
            #    speed = 0
            player.vertical_speed = int(speed)
            self.x += speed
        elif type == "vertical":
            #if speed > 0:
            #    speed -= 1
            #elif speed < 0:
            #    speed += 1
            #else:
            #    speed = 0
            player.horizontal_speed = int(speed)
            self.y += speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

# initialize pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((800, 600))
# setting up the title and icon
pygame.display.set_caption("Asteroids")
icon = pygame.image.load("asteroid1.png")
pygame.display.set_icon(icon)

# creating the player
player_image = pygame.image.load("spaceship.png")
resized_player_image = pygame.transform.scale(player_image, (64, 64))
player = Player(400, 300, resized_player_image, 64)
current_direction = [[],[]]
speed = 5

# main loop
running = True
clock = pygame.time.Clock()
while running:

    # setting the background color
    screen.fill((0, 0, 0))

    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            #if event.key == pygame.K_w and event.key == pygame.K_a:
              #  print("wa keys pressed")
                #player.move("diagonal left", speed)
            #elif event.key == pygame.K_w and event.key == pygame.K_d:
             #   print("wd keys pressed")
                #player.move("diagonal right", speed)
            if event.key == pygame.K_a:
                print("a key pressed")
                #player.move("left", speed)
                player.horizontal_speed -= speed
            elif event.key == pygame.K_d:
                print("d key pressed")
                #player.move("right", speed)
                player.horizontal_speed += speed
            elif event.key == pygame.K_w:
                print("w key pressed")
                #player.move("up", speed)
                player.vertical_speed -= speed
            elif event.key == pygame.K_s:
                print("s key pressed")
                #player.move("down", speed)
                player.vertical_speed += speed
            elif event.key == pygame.K_q:
                print("q key pressed")
                #player.angle += 90
            elif event.key == pygame.K_e:
                print("e key pressed")
                #player.angle -= 90

    # getting the current directions
    print(player.horizontal_speed, player.vertical_speed)
    if player.horizontal_speed > 0:
        current_direction[0] = "right"
    if player.horizontal_speed < 0:
        current_direction[0] = "left"
    if player.vertical_speed > 0:
        current_direction[1] = "down"
    if player.vertical_speed < 0:
        current_direction[1] = "up"
    if player.horizontal_speed == 0:
        current_direction[0] = ""
    if player.vertical_speed == 0:
        current_direction[1] = ""
    
    print(current_direction)

    # moving the player in the directions
    if current_direction[1] == "up" or current_direction[1] == "down":
        player.move( player.vertical_speed, "vertical")
    if current_direction[0] == "left" or current_direction[0] == "right":
        player.move( player.horizontal_speed, "horizontal")
            
    # drawing the player
    player.draw()

    # updating the display
    clock.tick(60)
    pygame.display.update()

# quiting the game
pygame.quit()