#Создай собственный Шутер!
from pygame import *
from random import randint
from time import time as tm
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,play_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = play_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.centery,5)
        bullets.add(bullet)
        mixer.music.load('babax.ogg')
        mixer.music.play(-1)
class Enemy(GameSprite):
    def update(self):
        if self.rect.y + self.speed> 500:
            mixer.music.load('babax.ogg')
            mixer.music.play(-1)
            x = self.rect.x
            y = self.rect.y
            self.image = transform.scale(image.load(list_enemy_sprities[randint(0,1)]),(65,65))
            self.rect = self.image.get_rect()
            self.rect.y = 10
            self.rect.x = randint(10,600)
        else:
            self.rect.y += self.speed
class Bullet(GameSprite):
    def update(self):
        if self.rect.y < 10:
            self.kill()
        else:
            self.rect.y -= self.speed

list_enemy_sprities = ['ufo.png','asteroid.png']
window = display.set_mode((700,500))
counter = 0
font.init()
font1 = font.Font(None,33)
font_reload = font.Font(None,25)
reload_text= font_reload.render('ПЕРЕЗАРЯДКА',True,(255,0,0))
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
game = True
window.blit(background,(0,0))
finish = False
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
bullets = sprite.Group()
clock = time.Clock()
FPS = 144
round_end = False
is_reload = False
fire_num = 0
reload_start_time = None
player = Player('rocket.png',100,425,10)
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy('ufo.png', randint(100,600), 10, randint(1,7))
    enemies.add(enemy)
while game:
    text_counter = font1.render('Килы:'+str(counter),True,(123,123,123))

    clock.tick(FPS)
    if (counter > 10):
        round_end = True
    if round_end == False:
        window.blit(background,(0,0))
        window.blit(text_counter,(10,10))
        player.update()
        player.reset()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(enemies, bullets, True, True)
        for i in range(len(collides)):
            enemy = Enemy('ufo.png', randint(100,600), 10,3)
            enemies.add(enemy)
            counter +=1
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if fire_num >5:
                        time_now = tm()
                        print(time_now-reload_start_time)
                        if time_now - reload_start_time >1:
                            fire_num = 0
                        else:
                            
                            window.blit(reload_text,(player.rect.centerx,player.rect.centery))
                    else:
                        fire_num += 1
                        if fire_num>5:
                            reload_start_time = tm()
                        player.fire()

    else:
        for e in event.get():
            if e.type == QUIT:
                game = False
        if counter > 10:
            text_win = font1.render('Вы победили!', True,(0,255,0))
            window.blit(text_win, (300, 300))
    # enemy.reset()
    # enemy.update()   


    display.update()