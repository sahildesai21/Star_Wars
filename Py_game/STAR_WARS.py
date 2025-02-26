import pygame
from pygame.locals import *
import random
from pygame import mixer 

pygame.mixer.pre_init(44100, -16, 2, 512)  # these pre_init values are predefined
mixer.init()
pygame.font.init()

# FPS
clock = pygame.time.Clock()
fps=60

screen_width=600
screen_height=800

# rows and coloums for aliens
rows = 5
cols = 5
alien_cooldown = 1000   # milliseconds
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0

#Font
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

# loading sounds
explosion_fx = pygame.mixer.Sound("C:\\Users\\ASUS\Documents\\Py_game\\explosion.wav")
explosion_fx.set_volume(0.25)

explosion2_fx = pygame.mixer.Sound("C:\\Users\\ASUS\\Documents\\Py_game\\explosion2.wav")
explosion2_fx.set_volume(0.25)

laser_fx = pygame.mixer.Sound("C:\\Users\\ASUS\\Documents\\Py_game\\laser.wav")
laser_fx.set_volume(0.25)

red = (255,0,0)
green = (0,255,0)
white = (255,255,255)

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("STAR WARS")

bg = pygame.image.load("C:\\Users\\ASUS\\Documents\\Py_game\\bg.png")

def draw_pg():
    screen.blit(bg, (0,0))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))


# creating class for spaceship
class spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\ASUS\\Documents\\Py_game\\spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.health_start = health
        self.health_remaining = health  
        self.last_shot = pygame.time.get_ticks()
    
    def update(self):
        # spaceship speed 
        speed = 8
        # cooldown variabe
        cooldown = 300  # milliseconds
        game_over = 0

        # get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed
        
        # record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            laser_fx.play()
            bullet = bullets(self.rect.centerx, self.rect.top)
            bullets_group.add(bullet)
            self.last_shot = time_now
        
        #image mask
        self.mask = pygame.mask.from_surface(self.image)    

        # health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom+10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom+10), int(self.rect.width*(self.health_remaining/self.health_start)), 15))
        elif self.health_remaining <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            Explosion_group.add(explosion)
            self.kill()
            game_over = 1
        return game_over
            

# creating class for bullets
class bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\ASUS\\Documents\\Py_game\\bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 45:
            self.kill()
        if pygame.sprite.spritecollide(self,  alien_group, True):    
            self.kill()
            explosion_fx.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            Explosion_group.add(explosion)  

# creating class for Aliens
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\ASUS\\Documents\\Py_game\\alien" + str(random.randint(1,5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.move_counter = 0
        self.move_direction = 1
    
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction    

# creating class for Explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"C:\\Users\\ASUS\\Documents\\Py_game\\exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20,20))
            if size == 2:
                img = pygame.transform.scale(img, (40,40))
            if size == 3:
                img = pygame.transform.scale(img, (160,160))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image= self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0


    def update(self):
        explosion_speed = 3
        #update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) -1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete then delete the explosion
        if self.index >= len(self.images) -1 and self.counter >= explosion_speed:
            self.kill()


# creating class for alien bullets
class alienbullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:\\Users\\ASUS\\Documents\\Py_game\\alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    
    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2_fx.play()
            #reduce health
            spaceship.health_remaining -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            Explosion_group.add(explosion)




# create sprite group
spaceship_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alienbullets_group = pygame.sprite.Group()
Explosion_group = pygame.sprite.Group()

# creating aliens
def create_aliens():
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100 , 100 + row * 70  )
            alien_group.add(alien)

create_aliens()

# creat player
spaceship = spaceship(int(screen_width/2), screen_height-100, 3)
spaceship_group.add(spaceship)

run = True
while run:

    clock.tick(fps)

    # draw background
    draw_pg()

    if countdown == 0:

        # crete random alien bullets and record the time 
        time_now = pygame.time.get_ticks()  
        if time_now - last_alien_shot > alien_cooldown and len(alienbullets_group) < 5 and len(alien_group) > 0: 
            attacking_alien = random.choice(alien_group.sprites())
            alienbullet = alienbullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alienbullets_group.add(alienbullet)
            last_alien_shot = time_now

        # check if all the aliens have been killed
        if len(alien_group) == 0:
            game_over = 1

        if game_over == 0:
            # update spaceship
            game_over = spaceship.update()

            # update sprites
            bullets_group.update()
            alien_group.update()
            alienbullets_group.update()
        else:
            if len(alien_group) == 0:
                draw_text("YOU WIN!", font40, white, int(screen_width/2 - 100), int(screen_height/2 + 50))  
            else:
                draw_text("GAME OVER!", font40, white, int(screen_width/2 - 100), int(screen_height/2 + 50))  

    
    if countdown > 0:
        draw_text('GET READY!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer

    Explosion_group.update()


    # draw sprit groups
    spaceship_group.draw(screen)
    bullets_group.draw(screen)
    alien_group.draw(screen)
    alienbullets_group.draw(screen)
    Explosion_group.draw(screen)

    # eventr handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
 
pygame.quit()
