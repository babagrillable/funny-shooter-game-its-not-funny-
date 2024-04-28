
from pygame import *
from random import randint

# BACKGROUND MUSIC VERY COOL
# mixer.init()
# mixer.music.load('fire.ogg')
# mixer.music.play()
# fire_sound = mixer.Sound('fire.ogg')



# Font n Caption mah good man
font.init()
font1 = font.SysFont('Ariel',80)
win = font1.render('YOU WIN',True, (255,255,255))
lose = font1.render('FUCKING FAILURE', True, (180,0,0))

# WHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAT
img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_buoulet = 'bullet.png'
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'

# PARENT CLASS FOR OTHER SPRITES
class gameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# player class
class Player(gameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -88:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height -100:
            self.rect.y += self.speed
    def fire(self):
        boulet = Bullet("bullet.png",self.rect.centerx, self.rect.y,50,55,-30)
        boulets.add(boulet)

# everybody wanna be my enemy 🗣️🔥🔥
class Enemy(gameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if  self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost = lost + 1

# I NEED MORE BOULETS
class Bullet(gameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        

# CREATE WINDOW
life = 3
max_lost = 50
goal = 100
lost = 0
win_width = 1300
win_height = 650
display.set_caption("Shooting Shit")
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))



# Creating sprites
ship = Player(img_hero, 5, win_height - 100, 80,100, 20)
img_enemy = "ufo.png"
monsters = sprite.Group()
asteroids = sprite.Group()
asteroid = img_asteroid
for i in range(8):
    monster = Enemy(img_enemy, randint(80,win_width-80),-40,60,70,randint(3,10))
    monsters.add(monster)      
for i in range(8):
    asteroid = Enemy(img_asteroid, randint(80,win_width-80),-40,60,70,randint(3,6))
    asteroids.add(asteroid)         
score = 0
finish = False
boulets = sprite.Group()
# Main game loop:
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                ship.fire()
    
    if not finish:
        window.blit(background,(0,0))
        ship.update()
        ship.reset()
        boulets.update()
        boulets.draw(window)
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        collides1 = sprite.groupcollide(monsters,boulets,True,True)
        collides2 = sprite.groupcollide(asteroids,boulets,True,True)
        for c in collides1:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80),-40,60,70,randint(1,5))
            monsters.add(monster)
        for c in collides2:
            asteroid = Enemy(img_asteroid, randint(80, win_width - 80),-40,60,70,randint(1,5))
            asteroids.add(asteroid)
        if sprite.spritecollide(ship, monsters,False) or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monsters,True)
            sprite.spritecollide(ship,asteroids,True)
            life -=1

        
        # write text on DE screen
        text = font1.render("Score: " + str(score), 1, (255,255,255))
        window.blit(text, (10,20))
        
        text_lose = font1.render("Missed: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            finish = True
            window.blit(win,200,200)

        display.update()
    time.delay(50)



