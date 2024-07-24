# necesery imports
import pygame
import random
import math
import threading
import tkinter
# debuging imports
import cProfile

    # Classes
# player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image, size, state, lives):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.lives = lives
        self.state = state
        self.vertical_speed = 0
        self.horizontal_speed = 0
        self.direction = ""
        self.angle = 0
        self.image = image
        self.real_image = image
        self.size = size
        self.speed = 2
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        # rotating the player image according to the angle
        if self.state == "protected":
            self.image = pygame.transform.rotate(self.image, self.angle)
        else:
            self.image = self.real_image
            self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
        # drawing the player
        screen.blit(self.image, self.rect)

    def change_direction(self, direction):
        self.direction = direction

    def move(self):
        # new movement code
        # based on the direction the player will move, player can move only forward or backward(it is easier to program)
        if self.direction == "forward":
            self.image = thrust_spaceship
            self.horizontal_speed -= math.sin(math.radians(self.angle)) * self.speed
            self.vertical_speed -= math.cos(math.radians(self.angle)) * self.speed
        elif self.direction == "back":
            self.horizontal_speed += math.sin(math.radians(self.angle)) * self.speed
            self.vertical_speed += math.cos(math.radians(self.angle)) * self.speed
        # if the player is not moving the player will slow down
        elif self.direction == "":
            if self.horizontal_speed > 0:
                self.horizontal_speed -= resistance
            elif self.horizontal_speed < 0:
                self.horizontal_speed += resistance
            if self.vertical_speed > 0:
                self.vertical_speed -= resistance
            elif self.vertical_speed < 0:
                self.vertical_speed += resistance
        # if the speeds are near 0 they will be set to 0
        if self.horizontal_speed < 0.3 and self.horizontal_speed > -0.3:
            self.horizontal_speed = 0
        if self.vertical_speed < 0.3 and self.vertical_speed > -0.3:
            self.vertical_speed = 0
        # moving the player
        self.x += self.horizontal_speed
        self.y += self.vertical_speed
        
        self.rect = self.image.get_rect(center=(self.x, self.y))

# bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle, image):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.angle = angle + 180
        self.horizontal_speed = 0
        self.vertical_speed = 0
        self.speed = bullet_speed
        # based on the direction of the player the bullet will move in that direction
        self.horizontal_speed = math.sin(math.radians(self.angle)) * self.speed
        self.vertical_speed = math.cos(math.radians(self.angle)) * self.speed
        #based on the angle the bullet image will be rotated
        self.image = pygame.transform.rotate(image, self.angle)

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self):
        self.x += self.horizontal_speed
        self.y += self.vertical_speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

# asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spawn_point = random.choice(spawn_points)
        self.x = self.spawn_point[0]
        self.y = self.spawn_point[1]
        self.angle = random.randint(0, 359)
        self.image = random.choice(resized_asteroid_images)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self, speed):
        self.x += math.cos(math.radians(self.angle)) * speed
        self.y += math.sin(math.radians(self.angle)) * speed
        self.x = round(self.x, 2)
        self.y = round(self.y, 2)
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

# powerup class
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randint(0, width)
        self.y = random.randint(50, height//2)
        self.y = self.y * -1
        self.speed = random.randint(1, 3)
        self.type = random.choice(powerup_types)
        if self.type == "shield":
            self.image = resized_powerup_image
        elif self.type == "lives":
            self.image = resized_lives_powerup_image
        elif self.type == "pulse":
            self.image = resized_pulse_powerup_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
    def draw(self):
        screen.blit(self.image, self.rect)
    def move(self):
        self.y += self.speed
        self.rect = self.image.get_rect(center=(self.x, self.y))

    # Functions

# function to create end screen
def end_screen():
    end = True
    global running

    # end screen loop
    while end:
        screen.fill((0, 0, 0))
        font = pygame.font.Font("freesansbold.ttf", width//25)
        text = font.render("Game Over", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width//2, height//2))
        screen.blit(text, text_rect)
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width//2, height//2 + 50))
        screen.blit(text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    end = False
                    reset()
        pygame.display.update()

# function to apply settings
def apply_settings(window, asteroids_entry, powerups_entry, ufo_entry, playersize, player_speed, bulletspeed):
    global settings, number_of_asteroids
    if int(asteroids_entry) <= 0 or int(powerups_entry) < 0 or int(ufo_entry) < 0:
        return
    else:
        # unpausing the movement of the asteroids and destroying the settings window
        settings = False
        window.destroy()
        # changing the number of asteroids
        number_of_asteroids = int(asteroids_entry)
        # changing the number of powerups
        global number_of_powerups
        number_of_powerups = int(powerups_entry)
        # changing the chance of a ufo spawning
        global chance_of_ufo
        chance_of_ufo = int(ufo_entry)
        # changing the size of the player
        global player_size
        player_size = playersize
        # changing the speed of the player
        global playerspeed
        playerspeed = player_speed
        # changing the speed of the bullets
        global bullet_speed, bullet_speed_mode
        if bulletspeed == "Slow":
            bullet_speed_mode = "Slow"
            bullet_speed = 3
        elif bulletspeed == "Normal":
            bullet_speed_mode = "Normal"
            bullet_speed = 5
        elif bulletspeed == "Fast":
            bullet_speed_mode = "Fast"
            bullet_speed = 7

    # resetting the game to apply the settings
    reset()
        
# function to create settings window
def settings_window():
    # pausing the movement of the asteroids
    global settings,bullet_speed, playerspeed, player_size, bullet_speed_mode
    settings = True

    # creating the window
    window = tkinter.Tk()
    window.title("Settings")
    window.geometry("400x400")
    window.resizable(False, False)
    window.iconbitmap("settings_icon.ico")
    # creating a main label
    main_label = tkinter.Label(window, text="Settings", font=("Arial", 20))
    main_label.pack()
    # creating a frame for the settings
    settings_frame = tkinter.Frame(window)
    settings_frame.pack()
    # creating a label for the number of asteroids
    asteroids_label = tkinter.Label(settings_frame, text="Number of asteroids")
    asteroids_label.grid(row=0, column=0)
    # creating entry for the number of asteroids
    e1 = tkinter.StringVar()
    e1.set(str(number_of_asteroids))
    asteroids_entry = tkinter.Entry(settings_frame, textvariable=e1)
    asteroids_entry.grid(row=0, column=1)
    # creating a label for the number of powerups
    powerups_label = tkinter.Label(settings_frame, text="Number of powerups")
    powerups_label.grid(row=1, column=0)
    # creating entry for the number of powerups
    e2 = tkinter.StringVar()
    e2.set(str(number_of_powerups))
    powerups_entry = tkinter.Entry(settings_frame, textvariable=e2)
    powerups_entry.grid(row=1, column=1)
    # creating a label for the chance of a ufo spawning
    ufo_label = tkinter.Label(settings_frame, text="Chance of a ufo spawning")
    ufo_label.grid(row=2, column=0)
    # creating entry for the chance of a ufo spawning
    e3 = tkinter.StringVar()
    e3.set(str(chance_of_ufo))
    ufo_entry = tkinter.Entry(settings_frame, textvariable=e3)
    ufo_entry.grid(row=2, column=1)
    # creating a option menu for the size of the player
    playersize_label = tkinter.Label(settings_frame, text="Size of the player")
    playersize_label.grid(row=3, column=0)
    playersize = tkinter.StringVar()
    playersize.set(str(player_size))
    playersize_menu = tkinter.OptionMenu(settings_frame, playersize, "Small", "Normal", "Big")
    playersize_menu.grid(row=3, column=1)
    # creating a option menu for the speed of the player
    player_speed_label = tkinter.Label(settings_frame, text="Speed of the player")
    player_speed_label.grid(row=4, column=0)
    player_speed = tkinter.StringVar()
    player_speed.set(str(playerspeed))
    player_speed_menu = tkinter.OptionMenu(settings_frame, player_speed, "Slow", "Normal", "Fast")
    player_speed_menu.grid(row=4, column=1)
    # creating option menu for the bullet speed
    bulletspeed_label = tkinter.Label(settings_frame, text="Speed of the bullets")
    bulletspeed_label.grid(row=5, column=0)
    bulletspeed = tkinter.StringVar()
    bulletspeed.set(str(bullet_speed_mode))
    bulletspeed_menu = tkinter.OptionMenu(settings_frame, bulletspeed, "Slow", "Normal", "Fast")
    bulletspeed_menu.grid(row=5, column=1)
        # more settings will be added

    # creating apply button
    apply_button = tkinter.Button(window, text="Apply", command=lambda: apply_settings(window, asteroids_entry.get(), powerups_entry.get(), ufo_entry.get(), playersize.get(), player_speed.get(), bulletspeed.get()), font=("Arial", 15))
    apply_button.pack(side="bottom")
    window.mainloop()

# function to reset the game
def reset():
    # getting new width and height of the screen
    global width, height
    width = screen.get_width()
    height = screen.get_height()
    # resetting the game
    global reset_on, player, asteroids, bullets, ufos, powerups, score, all_sprites, angle
    reset_on = True
    score = 0
    angle = 0
    # resetting the player
    player.x = width//2
    player.y = height//2
    player.angle = 0
    player.vertical_speed = 0
    player.horizontal_speed = 0
    player.state = "normal"
    player.lives = 3
    player.direction = ""
    # resetting the asteroids
    asteroids.empty()
    # resetting the bullets
    bullets.empty()
    # resetting the ufos
    ufos.empty()
    # resetting the powerups
    powerups.empty()
    # resetting everything
    all_sprites.empty()

    # resizing everything, asteroids, ufos, powerups, player, etc.
    global resized_player_image, resized_asteroid_images, resized_ufo_image, resized_powerup_image, resized_lives_powerup_image, resized_bullet_image, resized_settings_button, resized_pulse_powerup_image
    # resizing the player based on the size selected in the settings
    global player_size, playerspeed, protected_player, thrust_spaceship
    #print(player_size)
    if player_size == "Small":
        resized_player_image = pygame.transform.scale(player_image, (height//15, height//15))
        player.size = width//15
        player.image = resized_player_image
        player.real_image = resized_player_image
        player.rect = player.image.get_rect(center=(player.x, player.y))
    elif player_size == "Normal":
        resized_player_image = pygame.transform.scale(player_image, (height//12, height//10))
        player.size = width//12
        player.image = resized_player_image
        player.real_image = resized_player_image
        player.rect = player.image.get_rect(center=(player.x, player.y))
        #print("normal")
    elif player_size == "Big":
        resized_player_image = pygame.transform.scale(player_image, (height//10, height//8))
        player.size = width//10
        player.image = resized_player_image
        player.real_image = resized_player_image
        player.rect = player.image.get_rect(center=(player.x, player.y))
    protected_player = pygame.transform.scale(protected_player, (resized_player_image.get_width(), resized_player_image.get_height()))
    thrust_spaceship = pygame.transform.scale(thrust_spaceship, (resized_player_image.get_width(), resized_player_image.get_height()))
    # changing the speed of the player based on the speed selected in the settings
    global playerspeed
    if playerspeed == "Slow":
        player.speed = 1
    elif playerspeed == "Normal":
        player.speed = 2
    elif playerspeed == "Fast":
        player.speed = 3
    
    # resizing the asteroids and the ufos and the powerups and the bullets
    resized_asteroid_images.clear()
    for asteroid_image in asteroid_images:
        resized_asteroid_image = pygame.transform.scale(asteroid_image, (height//12, height//12))
        resized_asteroid_images.append(resized_asteroid_image)
    resized_ufo_image = pygame.transform.scale(ufo_image, (height//12, height//12))
    resized_powerup_image = pygame.transform.scale(powerup_image, (height//25, height//25))
    resized_lives_powerup_image = pygame.transform.scale(lives_powerup_image, (height//25, height//25))
    resized_bullet_image = pygame.transform.scale(bullet_image, (height//25, height//25))
    resized_settings_button = pygame.transform.scale(settings_button, (height//10, height//10))
    resized_pulse_powerup_image = pygame.transform.scale(pulse_powerup_image, (height//25, height//25))

    # resizing the background
    global resized_background
    resized_background = pygame.transform.scale(background, (width, height))

    # getting new spawn points for the asteroids
    global spawn_points
    spawn_points.clear()
    for i in range((width//4)//10):
        for j in range(height//10):
            spawn_points.append((width+i*10, j*10))
            spawn_points.append((-width+i*10, j*10))
            spawn_points.append((i*10, height+j*10))
            spawn_points.append((i*10, -height+j*10))

    # ending the reset
    reset_on = False

# function to handle the asteroids and the powerups
def asteroid_loop():
    global running, asteroids, clock, powerups, number_of_asteroids
    # checking if the game is running
    while running:
        global settings, reset_on, asteroids, powerups, number_of_asteroids, width, height, resized_powerup_image, chance_of_ufo, ufos
        # checking if the settings window is open, if it is, the asteroids will stop moving
        while settings:
            pass
        # checking if reset function is doing some changes to the game
        while reset_on:
            pass
        # checking if there is a right amount of asteroids and powerups
        if len(asteroids)< number_of_asteroids:
            asteroid = Asteroid()
            asteroids.add(asteroid)
        if len(powerups) < number_of_powerups:
            powerup = Powerup()
            powerups.add(powerup)
        if random.randint(0, 100) < chance_of_ufo:
            ufo = Ufo()
            ufos.add(ufo)
        # checking if the asteroids have hit the outer walls of the screen
        for asteroid in asteroids:
            if asteroid.x <= 0 - height//2 + asteroid.image.get_width() / 2 or asteroid.x >= width + height//2 - asteroid.image.get_width() / 2 or asteroid.y <= 0 - height//2 + asteroid.image.get_height() / 2 or asteroid.y >= height + height//2 - asteroid.image.get_height() / 2:
                asteroids.remove(asteroid)
        # checking if the powerups have hit the outer walls of the screen
        for powerup in powerups:
            if powerup.y >= height + height//2 - powerup.image.get_height() / 2:
                powerups.remove(powerup)
    
        # moving the asteroids
        for asteroid in asteroids:
            asteroid.move(random.randint(1, 3))
        # moving the powerups
        for powerup in powerups:
            powerup.move()

        clock.tick(60)

# initialize pygame
pygame.init()
# setting up the screen
width = 800
height = 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
reset_on = False
score = 0
# setting up the title and icon
pygame.display.set_caption("Asteroids")
icon = pygame.image.load("asteroid1.png")
pygame.display.set_icon(icon)

# setting up all the possible spawn points outside the screen
spawn_points = []
for i in range((width//4)//10):
    for j in range(height//10):
        spawn_points.append((width+i*10, j*10))
        spawn_points.append((-width+i*10, j*10))
        spawn_points.append((i*10, height+j*10))
        spawn_points.append((i*10, -height+j*10))

# creating the player
player_image = pygame.image.load("spaceship.png")
resized_player_image = pygame.transform.scale(player_image, (height//12, height//10))
player = Player(width//2, height//2, resized_player_image, width//12, "normal", 3)
resistance = 0.7
protected_player = pygame.image.load("protected_player.png")
protected_player = pygame.transform.scale(protected_player, (resized_player_image.get_width(), resized_player_image.get_height()))
thrust_spaceship = pygame.image.load("spaceship_thrust.png")
resized_thrust_spaceship = pygame.transform.scale(thrust_spaceship, (resized_player_image.get_width(), resized_player_image.get_height()))
angle = 0
player_size = "Normal"
playerspeed = "Normal"

# setting up the bullets
bullet_image = pygame.image.load("laser.png")
resized_bullet_image = pygame.transform.scale(bullet_image, (width//25, height//25))
bullet_speed = 5
bullet_speed_mode = "Normal"

# setting up the powerups
# setting up the shield powerup
powerup_image = pygame.image.load("powerup.png")
resized_powerup_image = pygame.transform.scale(powerup_image, (height//25, height//25))
powerups = pygame.sprite.Group()
#setting up the lives adding powerup
lives_powerup_image = pygame.image.load("powerup_health.png")
resized_lives_powerup_image = pygame.transform.scale(lives_powerup_image, (height//25, height//25))
# setting the pulse powerup
pulse_powerup_image = pygame.image.load("powerup_pulse.png")
resized_pulse_powerup_image = pygame.transform.scale(pulse_powerup_image, (height//25, height//25))

number_of_powerups = 1

# list of all the powerup types
powerup_types = ["shield", "lives", "pulse"]

# creating the bullets group
bullets = pygame.sprite.Group()

# setting up the asteroids
asteroid_images = [pygame.image.load("asteroid1.png"), pygame.image.load("asteroid2.png"), pygame.image.load("asteroid3.png"), pygame.image.load("asteroid4.png")]
resized_asteroid_images = []
for asteroid_image in asteroid_images:
    resized_asteroid_image = pygame.transform.scale(asteroid_image, (width//12, height//12))
    resized_asteroid_images.append(resized_asteroid_image)
number_of_asteroids = 10

# creating the asteroids group
asteroids = pygame.sprite.Group()

# setting up a thread for asteroids
asteroid_thread = threading.Thread(target=asteroid_loop)

# setting up the ufos
ufo_image = pygame.image.load("ufo.png")
resized_ufo_image = pygame.transform.scale(ufo_image, (width//12, height//12))
chance_of_ufo = 0

# creating the ufos group
ufos = pygame.sprite.Group()

# setting up settings button
settings_button = pygame.image.load("settings.png")
resized_settings_button = pygame.transform.scale(settings_button, (height//10, height//10))
settings = False

# setting up the background image
background = pygame.image.load("background.jpeg")
resized_background = pygame.transform.scale(background, (width, height))

# setting up the score and lives font
font = pygame.font.Font("freesansbold.ttf", width//25)

# main loop
running = True
#one_second = 0
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
def main():
    global running, player, bullets, asteroids, score, asteroid_thread, ufos, powerups, settings, resized_settings_button, width, height, resized_background, reset_on
    global clock, text, all_sprites, angle
    while running:

        # starting the asteroid thread
        if asteroid_thread.is_alive() == False:
            asteroid_thread.start()

        # setting the background image
        screen.blit(resized_background, (0, 0))

        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_a:
                    angle = 5
                elif event.key == pygame.K_e or event.key == pygame.K_d:
                    angle = -5
                # new movement code
                elif event.key == pygame.K_w:
                    player.change_direction("forward")
                    
                elif event.key == pygame.K_s:
                    player.change_direction("back")

                # other non movement key events
                elif event.key == pygame.K_SPACE:
                    bullet = Bullet(player.x, player.y, player.angle, resized_bullet_image)
                    bullets.add(bullet)
                elif event.key == pygame.K_r:
                    reset()
            # checking if the settings button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if pos[0] >= width - resized_settings_button.get_width() and pos[1] >= height - resized_settings_button.get_height():
                        settings = True
                        settings_window()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player.change_direction("")
                if event.key == pygame.K_q or event.key == pygame.K_e or event.key == pygame.K_a or event.key == pygame.K_d:
                    angle = 0

        # changing the angle of the player
        player.angle += angle

        # moving the player in the directions
        player.move()

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
        elif player.x >= width - player.image.get_width() / 2:
            player.x = width - player.image.get_width() / 2
            player.horizontal_speed = 0
        if player.y <= player.image.get_height() / 2:
            player.y = player.image.get_height() / 2
            player.vertical_speed = 0
        elif player.y >= height - player.image.get_height() / 2:
            player.y = height - player.image.get_height() / 2
            player.vertical_speed = 0
        player.rect = player.image.get_rect(center=(player.x, player.y))

        # checking if the bullets have hit the outer walls of the screen
        for bullet in bullets:
            if bullet.x <= 0 + bullet.image.get_width() / 2 or bullet.x >= width - bullet.image.get_width() / 2 or bullet.y <= 0 + bullet.image.get_height() / 2 or bullet.y >= height - bullet.image.get_height() / 2:
                bullets.remove(bullet)
                all_sprites.remove(bullet)

        # checking if the bullets have hit the asteroids or the ufos
        for bullet in bullets:
            for asteroid in asteroids:
                if bullet.rect.colliderect(asteroid.rect):
                    bullets.remove(bullet)
                    all_sprites.remove(bullet)
                    asteroids.remove(asteroid)
                    all_sprites.remove(asteroid)
                    score += 1
            for ufo in ufos:
                if bullet.rect.colliderect(ufo.rect):
                    bullets.remove(bullet)
                    ufos.remove(ufo)
                    all_sprites.remove(ufo)
                    all_sprites.remove(bullet)
                    score += 5

        # checking if player has hit the powerup
        for powerup in powerups:
            if player.rect.colliderect(powerup.rect):
                powerups.remove(powerup)
                all_sprites.remove(powerup)
                if powerup.type == "shield":
                    player.state = "protected"
                elif powerup.type == "lives":
                    player.lives += 1
                elif powerup.type == "pulse":
                    # creating a pulse of bullets, these bullets will shoot in all angles
                    for i in range(0, 360, 45):
                        bullet = Bullet(player.x, player.y, i, resized_bullet_image)
                        bullets.add(bullet)
                        all_sprites.add(bullet)

        # checking if the player has hit the asteroids
        for asteroid in asteroids:
            if player.rect.colliderect(asteroid.rect):
                asteroids.remove(asteroid)
                all_sprites.remove(asteroid)
                if player.state == "protected":
                    player.state = "normal"
                    score += 1
                elif player.lives > 1:
                    player.lives -= 1
                else:
                    end_screen()

        # drawing the score to the top right corner
        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (width - text.get_width(), 0))
        # drawing the lives to the top left corner
        lives = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
        screen.blit(lives, (0, 0))

        # reseting the direction of the player, if no key is pressed
        player.draw()

        # adding all the sprites to the all_sprites group
        all_sprites.add(bullets)
        all_sprites.add(asteroids)
        all_sprites.add(ufos)
        all_sprites.add(powerups)

        # drawing everything
        all_sprites.draw(screen)

        # drawing the settings button
        screen.blit(resized_settings_button, (width- resized_settings_button.get_width(), height - resized_settings_button.get_height()))

        # if the code reaches this part than the settings window must be closed
        settings = False

        # updating the display
        pygame.display.flip()
        clock.tick(60)

cProfile.run("main()")

# quiting the game
pygame.quit()