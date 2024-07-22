# necesery imports
import pygame
import random
import math
import threading

    # Classes
# player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, size):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.vertical_speed = 0
        self.horizontal_speed = 0
        self.direction = ""
        self.angle = 0
        self.per_angle = 0
        self.image = image
        self.size = size
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        # rotating the player image according to the angle
        self.image = pygame.transform.rotate(self.image, self.per_angle)
        self.per_angle = 0

        print(self.x, self.y)
        
        # drawing the player
        screen.blit(self.image, self.rect)

    def change_direction(self, direction):
        self.direction = direction

    def move(self, speed):
        if player.direction == "left":
            self.horizontal_speed -= speed
        elif player.direction == "right":
            self.horizontal_speed += speed
        elif player.direction == "up":
            self.vertical_speed -= speed
        elif player.direction == "down":
            self.vertical_speed += speed

        self.y += self.vertical_speed
        self.x += self.horizontal_speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.angle = angle + 180
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self, speed):
        #print(self.angle)
        self.x += math.sin(math.radians(self.angle)) * speed
        self.y += math.cos(math.radians(self.angle)) * speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

# asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_point = random.choice(spawn_points)
        #print(self.spawn_point)
        self.x = self.spawn_point[0]
        self.y = self.spawn_point[1]
        self.x = self.x
        self.y = self.y
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.randint(-3,3)
        self.image = random.choice(resized_asteroid_images)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def rotate(self):
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.angle >= 360 or self.angle <= -360:
            self.angle = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))
        print(self.angle)

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self, speed):
        self.x += math.cos(math.radians(self.angle)) * speed
        self.y += math.sin(math.radians(self.angle)) * speed
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
# ufo class
class Ufo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(0, 800)# currently they spawn inside the screen, but I will make them spaw outside the screen later on
        self.y = random.randint(0, 600)# currently they spawn inside the screen, but I will make them spaw outside the screen later on
        self.angle = 0
        self.image = resized_ufo_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def draw(self):
        screen.blit(self.image, self.rect)
    
    def move(self):
        # here I will implement some more complex movement later on
        pass


# Functions

# function to rotate the asteroids
def rotation():
    while running:
        for asteroid in asteroids:
            asteroid.rotate()
        clock.tick(120)

# function to handle the asteroids
def asteroid_loop():
    #rotate_thread = threading.Thread(target=rotation)
    while running:
    #    if not rotate_thread.is_alive():
    #        rotate_thread.start()
        # checking if the asteroids have hit the outer walls + 300 pixels of the screen
        for asteroid in asteroids:
            if asteroid.x <= 0 - 300 + asteroid.image.get_width() / 2 or asteroid.x >= 800 + 300 - asteroid.image.get_width() / 2 or asteroid.y <= 0 - 300 + asteroid.image.get_height() / 2 or asteroid.y >= 600 + 300 - asteroid.image.get_height() / 2:
                asteroids.remove(asteroid)
    
        # moving the asteroids
        for asteroid in asteroids:
            asteroid.move(random.randint(1, 3))

        clock.tick(60)


# initialize pygame
pygame.init()
# setting up the screen
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
# setting up the title and icon
pygame.display.set_caption("Asteroids")
icon = pygame.image.load("asteroid1.png")
pygame.display.set_icon(icon)

# setting up all the possible spawn points outside the screen
spawn_points = []
for i in range(200//10):
    for j in range(600//10):
        spawn_points.append((800+i*10, j*10))
        spawn_points.append((-800+i*10, j*10))
        spawn_points.append((i*10, 600+j*10))
        spawn_points.append((i*10, -600+j*10))

print("spawn points set up")


# creating the player
player_image = pygame.image.load("spaceship.png")
resized_player_image = pygame.transform.scale(player_image, (64, 64))
player = Player(400, 300, resized_player_image, 64)
speed = 0.5

# setting up the bullets
bullet_image = pygame.image.load("laser.png")
resized_bullet_image = pygame.transform.scale(bullet_image, (32, 32))

# creating the bullets group
bullets = pygame.sprite.Group()

# setting up the asteroids
asteroid_images = [pygame.image.load("asteroid1.png"), pygame.image.load("asteroid2.png"), pygame.image.load("asteroid3.png"), pygame.image.load("asteroid4.png")]
resized_asteroid_images = []
for asteroid_image in asteroid_images:
    resized_asteroid_image = pygame.transform.scale(asteroid_image, (64, 64))
    resized_asteroid_images.append(resized_asteroid_image)

# creating the asteroids group
asteroids = pygame.sprite.Group()

# setting up a thread for asteroids
asteroid_thread = threading.Thread(target=asteroid_loop)

# setting up the ufos
ufo_image = pygame.image.load("ufo.png")
resized_ufo_image = pygame.transform.scale(ufo_image, (64, 64))

# creating the ufos group
ufos = pygame.sprite.Group()

# main loop
running = True
clock = pygame.time.Clock()
while running:

    # starting the asteroid thread
    if not asteroid_thread.is_alive():
        asteroid_thread.start()

    # setting the background color
    screen.fill((0, 0, 0))

    # checking for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.change_direction("left")
            elif event.key == pygame.K_d:
                player.change_direction("right")
            elif event.key == pygame.K_w:
                player.change_direction("up")
            elif event.key == pygame.K_s:
                player.change_direction("down")
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(player.x, player.y, player.angle, resized_bullet_image)
                bullets.add(bullet)
            elif event.key == pygame.K_l:
                asteroid = Asteroid()
                asteroids.add(asteroid)
            elif event.key == pygame.K_k:
                ufo = Ufo()
                ufos.add(ufo)
            elif event.key == pygame.K_q:
                print("q key pressed")
                player.angle += 45
                player.per_angle += 45
                print(player.angle)
                print(player.per_angle)
                if player.angle == 360 or player.angle == -360:
                    player.angle = 0
            elif event.key == pygame.K_e:
                print("e key pressed")
                player.angle -= 45
                player.per_angle -= 45
                if player.angle == 360 or player.angle == -360:
                    player.angle = 0

    # moving the player in the directions
    player.move(speed)

    # moving the bullets
    for bullet in bullets:
        bullet.move(8)

    # moving the ufos
    for ufo in ufos:
        ufo.move()

    # checking if player has it the outer walls of the screen
    if player.x <= 0 + player.image.get_width() / 2:
        player.x = 0 + player.image.get_width() / 2
        player.horizontal_speed = 0
    elif player.x >= 800 - player.image.get_width() / 2:
        player.x = 800 - player.image.get_width() / 2
        player.horizontal_speed = 0
    if player.y <= player.image.get_height() / 2:
        player.y = player.image.get_height() / 2
        player.vertical_speed = 0
    elif player.y >= 600 - player.image.get_height() / 2:
        player.y = 600 - player.image.get_height() / 2
        player.vertical_speed = 0
    player.rect = player.image.get_rect(center=(player.x, player.y))

    # checking if the bullets have hit the outer walls of the screen
    for bullet in bullets:
        if bullet.x <= 0 + bullet.image.get_width() / 2 or bullet.x >= 800 - bullet.image.get_width() / 2 or bullet.y <= 0 + bullet.image.get_height() / 2 or bullet.y >= 600 - bullet.image.get_height() / 2:
            bullets.remove(bullet)

    # checking if the bullets have hit the asteroids or the ufos
    for bullet in bullets:
        for asteroid in asteroids:
            if bullet.rect.colliderect(asteroid.rect):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
        for ufo in ufos:
            if bullet.rect.colliderect(ufo.rect):
                bullets.remove(bullet)
                ufos.remove(ufo)
    
    #print(player.angle)

    # drawing the player
    player.draw()

    # drawing the bullets
    bullets.draw(screen)

    # drawing the asteroids, asteroids have to be drawn in the main loop, to keep them sync
    asteroids.draw(screen)
    #print(len(asteroids))

    # drawing the ufos
    ufos.draw(screen)

    # updating the display
    clock.tick(60)
    pygame.display.update()

# quiting the game
pygame.quit()