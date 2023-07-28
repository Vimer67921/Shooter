from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN', True, (0,255,0))
lose = font1.render('YOU LOSE', True, (255,0,0))

lost = 0
score = 0

img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_asteroid = 'asteroid.png'


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image , self.rect)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= 5
        if keys[K_RIGHT]:
            self.rect.x += 5
        if keys[K_SPACE]:
            bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -10)
            bullets.add(bullet)
            fire_sound.play()

    def fire(self):
        pass

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = -50
            self.rect.x = randint(0, 700)
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

        
window = display.set_mode((700,500))
display.set_caption('Space')
background = transform.scale(image.load('galaxy.jpg'), (700,500))

ship = Player(img_hero, 5, 400, 80,100, 10)
pic = ['ufo.png', 'alien.png']
asteroids = sprite.Group()
monsters = sprite.Group()
bullets = sprite.Group()

fire_sound = mixer.Sound('fire.ogg')

for i in range(5):
    monster = Enemy(img_enemy, randint(80, 700-80), -40, 80, 50, randint(1, 7))
    monsters.add(monster)

for i in range(5):
    monster = Enemy(img_asteroid, randint(80, 700-80), -40, 80, 50, randint(1, 7))
    monsters.add(monster)

for k in pic:
    monster = Enemy(k, randint(80, 700-80), -40, 80, 50, randint(1, 7))
    monsters.add(monster)

life = 3
rel_time = False
num_fire = 0
    

run = True
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
                
    if not finish:
        window.blit(background, (0,0))

        text = font2.render(f"Счет: {score}", True, (255,255,255))
        window.blit(text, (10,20))
        text_lose = font2.render(f"Пропущено: {lost}", True, (255,255,255))
        window.blit(text_lose, (10,50))
    
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        bullets.draw(window)
        asteroids.draw(window)
        monsters.draw(window)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('Wait, reload...', True, (100, 100, 0))
                window.blit(reload, (250, 450))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, 700-80), -40, 80, 50, randint(1, 7))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, True) or sprite.spritecollide(ship, asteroids, True):
            life -= 1
        if life < 1:
            finish = True
            window.blit(lose, (200,200))
        if score > 9:
            finish = True
            window.blit(win, (200,200))
        
        if life == 3:
            life_color = (0,255,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (255,0,0)
        text_life = font1.render(str(life), True, life_color)
        window.blit(text_life, (650,10))
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        life = 3
        for a in asteroids:
            a.kill()
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.wait(1000)
        for i in range(5):
            monster = Enemy(img_enemy, randint(80, 700-80), -40, 80, 50, randint(1, 7))
            monsters.add(monster)
        for i in range(2):
            asteroid = Enemy(img_asteroid, randint(80, 700-80), -40, 80, 50, randint(1, 7))
            monsters.add(monster)



            
    display.update()
    time.delay(30)