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
        
        # drawing the player
        screen.blit(self.image, self.rect)

    def change_direction(self, direction):
        self.direction = direction

    def move(self, speed):
        #(player.angle)
        #print(speed)
        # new movement code
        if speed[0] != 0 or speed[1] != 0:
            #print("moving")
            if self.direction == "left":
                self.horizontal_speed -= speed[0]
            elif self.direction == "right":
                self.horizontal_speed += speed[0]
            elif self.direction == "up":
                self.vertical_speed -= speed[1]
            elif self.direction == "down":
                self.vertical_speed += speed[1]

        # slowing down the player, if a key managing the speed of the direction is not pressed
        if player.angle == 0 or player.angle == 180 or player.angle == -180:
            if self.horizontal_speed > 0 and speed[0] == 0:
                self.horizontal_speed -= resistance
            elif self.horizontal_speed < 0 and speed[0] == 0:
                self.horizontal_speed += resistance
            if self.vertical_speed > 0 and speed[1] == 0:
                self.vertical_speed -= resistance
            elif self.vertical_speed < 0 and speed[1] == 0:
                self.vertical_speed += resistance
        elif player.angle == 90 or player.angle == -90:
            if self.vertical_speed > 0 and speed[1] == 0:
                self.vertical_speed -= resistance
            elif self.vertical_speed < 0 and speed[1] == 0:
                self.vertical_speed += resistance
            if self.horizontal_speed > 0 and speed[0] == 0:
                self.horizontal_speed -= resistance
            elif self.horizontal_speed < 0 and speed[0] == 0:
                self.horizontal_speed += resistance
        elif player.angle == 270 or player.angle == -270:
            if self.vertical_speed > 0 and speed[1] == 0:
                self.vertical_speed -= resistance
            elif self.vertical_speed < 0 and speed[1] == 0:
                self.vertical_speed += resistance
            if self.horizontal_speed > 0 and speed[0] == 0:
                self.horizontal_speed -= resistance
            elif self.horizontal_speed < 0 and speed[0] == 0:
                self.horizontal_speed += resistance
        else:
            if self.horizontal_speed > 0 and speed[0] == 0:
                self.horizontal_speed -= resistance
            elif self.horizontal_speed < 0 and speed[0] == 0:
                self.horizontal_speed += resistance
            if self.vertical_speed > 0 and speed[1] == 0:
                self.vertical_speed -= resistance
            elif self.vertical_speed < 0 and speed[1] == 0:
                self.vertical_speed += resistance


                # failed attempt to slow down the player, caused unexpected movement
            #print("slowing down")
            #print(self.horizontal_speed, self.vertical_speed)
            #print(speed)
            #print("moving second")
            #if self.horizontal_speed > 0 and speed[0] == 0:
            #    self.horizontal_speed += resistance
            #    print("slowing down1")
            #elif self.horizontal_speed < 0 and speed[0] == 0:
            #    self.horizontal_speed += resistance
            #    print("slowing down2")
            #if self.vertical_speed > 0 and speed[1] == 0:
            #    self.vertical_speed += resistance
            #    print("slowing down3")
            #elif self.vertical_speed < 0 and speed[1] == 0:
            #    self.vertical_speed += resistance
            #    print("slowing down4")
        
        # rounding the speed to 2 decimal places
        self.horizontal_speed = round(self.horizontal_speed, 2)
        self.vertical_speed = round(self.vertical_speed, 2)

        #print(self.horizontal_speed, self.vertical_speed)
        self.y += self.vertical_speed
        self.x += self.horizontal_speed
        self.rect = self.image.get_rect(center=(self.x, self.y))
        #print(speed)

# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, image, speed=5):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.angle = angle + 180
        self.horizontal_speed = 0
        self.vertical_speed = 0
        # based on the direction of the player, the bullet will move in that direction and keep moving sideways, because player was moving sideways
        if player.angle == 0:
            self.horizontal_speed = 0
            self.vertical_speed =  speed
        elif player.angle == 90:
            self.horizontal_speed = speed
            self.vertical_speed = player.vertical_speed
        elif player.angle == 180:
            self.horizontal_speed = 0
            self.vertical_speed = speed
        elif player.angle == 270:
            self.horizontal_speed = speed
            self.vertical_speed = player.vertical_speed

        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self):
        #print(self.horizontal_speed, self.vertical_speed)
        self.x += math.sin(math.radians(self.angle)) * self.horizontal_speed
        self.y += math.cos(math.radians(self.angle)) * self.vertical_speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

# asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_point = random.choice(spawn_points)
        self.x = self.spawn_point[0]
        self.y = self.spawn_point[1]
        self.x = self.x
        self.y = self.y
        # depending on the spawn point, the angle options will be different
        if self.x <= 0:
            self.angle = random.randint(0, 180)
        elif self.x >= 800:
            self.angle = random.randint(180, 359)
        elif self.y <= 0:
            self.angle = random.randint(90, 270)
        elif self.y >= 600:
            self.angle = random.randint(-90, 90)

        self.rotation_speed = random.randint(-3,3)
        self.image = random.choice(resized_asteroid_images)
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def rotate(self):
        self.angle += self.rotation_speed
        self.image = pygame.transform.rotate(self.image, self.angle)
        if self.angle >= 360 or self.angle <= -360:
            self.angle = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))

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
        pos = random.choice(spawn_points)
        x = pos[0]
        y = pos[1]
        self.x = x
        self.y = y
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
    global running, asteroids, clock
    while running:
        if len(asteroids)< 3:
            asteroid = Asteroid()
            asteroids.add(asteroid)

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

# creating the player
player_image = pygame.image.load("spaceship.png")
resized_player_image = pygame.transform.scale(player_image, (64, 64))
player = Player(400, 300, resized_player_image, 64)
speed = [[],[]]
resistance = 0.2

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
        #print(player.angle)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # in case ship is pointing up
            if event.key == pygame.K_a and player.angle == 0:
                player.change_direction("left")
                speed[0] = 7
            elif event.key == pygame.K_d and player.angle == 0:
                player.change_direction("right")
                speed[0] = 7
            elif event.key == pygame.K_w and player.angle == 0:
                player.change_direction("up")
                speed[1] = 7
            elif event.key == pygame.K_s and player.angle == 0:
                player.change_direction("down")
                speed[1] = 7
            # in case ship is pointing right
            elif event.key == pygame.K_a and player.angle == -90 or player.angle == 90:
                player.change_direction("up")
                speed[1] = 7
            elif event.key == pygame.K_d and player.angle == -90 or player.angle == 90:
                player.change_direction("down")
                speed[1] = 7
            elif event.key == pygame.K_w and player.angle == -90 or player.angle == 90:
                player.change_direction("right")
                speed[0] = 7
            elif event.key == pygame.K_s and player.angle == -90 or player.angle == 90:
                player.change_direction("left")
                speed[0] = 7
            # in case ship is pointing down
            elif event.key == pygame.K_a and player.angle == -180 or player.angle == 180:
                player.change_direction("right")
                speed[0] = 7
            elif event.key == pygame.K_d and player.angle == -180 or player.angle == 180:
                player.change_direction("left")
                speed[0] = 7
            elif event.key == pygame.K_w and player.angle == -180 or player.angle == 180:
                player.change_direction("down")
                speed[1] = 7
            elif event.key == pygame.K_s and player.angle == -180 or player.angle == 180:
                player.change_direction("up")
                speed[1] = 7
            # in case ship is pointing left
            elif event.key == pygame.K_a and player.angle == -270 or player.angle == 270:
                player.change_direction("down")
                speed[1] = 7
            elif event.key == pygame.K_d and player.angle == -270 or player.angle == 270:
                player.change_direction("up")
                speed[1] = 7
            elif event.key == pygame.K_w and player.angle == -270 or player.angle == 270:
                player.change_direction("left")
                speed[0] = 7
            elif event.key == pygame.K_s and player.angle == -270 or player.angle == 270:
                player.change_direction("right")
                speed[0] = 7

            elif event.key == pygame.K_SPACE:
                bullet = Bullet(player.x, player.y, player.angle, resized_bullet_image)
                bullets.add(bullet)
            elif event.key == pygame.K_k:
                ufo = Ufo()
                ufos.add(ufo)
            elif event.key == pygame.K_q:
                player.angle += 90
                player.per_angle += 90
                if player.angle == 360 or player.angle == -360:
                    player.angle = 0
            elif event.key == pygame.K_e:
                player.angle -= 90
                player.per_angle -= 90
                if player.angle == 360 or player.angle == -360:
                    player.angle = 0
        if event.type == pygame.KEYUP:
            if player.angle == 0 or player.angle == 180 or player.angle == -180:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.change_direction("")
                    speed[0] = 0
                    #print("key up")
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    player.change_direction("")
                    speed[1] = 0
                    #print("key up")
            else:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.change_direction("")
                    speed[0] = 0
                    #print("key up")
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    player.change_direction("")
                    speed[1] = 0
                    #print("key up")
        

    # moving the player in the directions
    player.move(speed)

    # moving the bullets
    for bullet in bullets:
        bullet.move()

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

    # checking if the player has hit the asteroids
    for asteroid in asteroids:
        if player.rect.colliderect(asteroid.rect):
            asteroids.remove(asteroid)
            print("hit")

    # drawing the player
    player.draw()
    player.change_direction("")

    # drawing the bullets
    bullets.draw(screen)

    # drawing the asteroids, asteroids have to be drawn in the main loop, to keep them sync
    asteroids.draw(screen)

    # drawing the ufos
    ufos.draw(screen)

    # updating the display
    clock.tick(60)
    pygame.display.update()

# quiting the game
pygame.quit()