import os
import pygame
import random
from pygame import *


pygame.init()

black = (0,0,0)
white = (255,255,255)
col = (255,255,255)
screen_size = (width,height) = (800,150)
FPS = 60
gravity = 0.6
HS = 0

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
pygame.display.set_caption("HDS(HipsterDinoSaur)")

jump_sound = pygame.mixer.Sound('sprites/jump.mp3')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')
BG_sound = pygame.mixer.Sound('sprites/BG_sound.mp3')
DK_sound = pygame.mixer.Sound('sprites/roar.wav')
Over_sound = pygame.mixer.Sound('sprites/growl.mp3')

###ฟังก์ชั่นโหลดรูป
def imp_image(
    name,
    scr_x=-1,
    scr_y=-1,
    CLK=None,
    ):

    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname).convert()
    if CLK != None:
        if CLK == 0:
            CLK = image.get_at((0, 0))
        image.set_colorkey(CLK)

    if scr_x != -1 or scr_y != -1:
        image = pygame.transform.scale(image, (scr_x, scr_y))

    return (image, image.get_rect()) ###returnค่าเป็นรูปและตำแหน่ง

###ฟังก์ชันโหลดตัวละคร
def sprite_sheet(
    sheetname,
    nx,
    ny,
	scalex = -1,
	scaley = -1,
	CLK = None,
        ):
    fullname = os.path.join('sprites',sheetname)
    sheet = pygame.image.load(fullname).convert() # Load the sprite sheet.

    sheet_rect = sheet.get_rect() 

    sprites = []

    scr_x = sheet_rect.width/nx
    scr_y = sheet_rect.height/ny

    for i in range(0,ny):
        for j in range(0,nx):
            rect = pygame.Rect((j*scr_x,i*scr_y,scr_x,scr_y))
            image = pygame.Surface(rect.size).convert()
            image.blit(sheet,(0,0),rect)

            if CLK != None:
                if CLK == -1:
                    CLK = image.get_at((0,0))
                image.set_colorkey(CLK)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image,(scalex,scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites,sprite_rect ### return ตัวละ และ ตำแหน่ง

### ฟังก์ชันแทรกตัวเลข
def extractDigits(number):
    if number >= 0:
        digits = []
        i = 0
        while(number%10 != 0):
            digits.append(number%10)
            number = int(number/10)

        digits.append(number%10)
        for i in range(len(digits),5):
            digits.append(0)
        digits.reverse()
        return digits


### ฟังก์ชันแสดงจอตอนเกมจบ
def disp_gameOver_msg(gameover_image):

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height*0.35

    screen.blit(gameover_image, gameover_rect)


### ตัวละครไดโนเสาร์
class Dino():
    def __init__(self,scr_x=-1,scr_y=-1):
        self.images,self.rect = sprite_sheet('55.png',5 ,1,scr_x,scr_y,-1)
        self.images1,self.rect1 = sprite_sheet('22.png',3,1,scr_x,scr_y,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping , self.isDead, self.isDucking, self.isBlinking  = False , False, False, False
        self.movement = [0,0]
        self.jumpSpeed = 12

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image,self.rect)
 
    def checkbounds(self): ### เช็คขอบเขตตอนโดด
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 5 == 0:
                    self.index = (self.index + 1)%5
            else:
                if self.counter % 80 == 19:
                    self.index = (self.index + 1)%5

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 +2

        if self.isDead:
           self.index = 1

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()


        self.counter = (self.counter + 1)

### ตัวละครกระบองเพชรกับหิน
class Cactus(pygame.sprite.Sprite):
    def __init__(self,speed=5,scr_x=-1,scr_y=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = sprite_sheet('mixe.png',3,1,50,scr_y,-1)
        self.rect.bottom = int(0.98*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed,0]

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

### ตัวละครนก
class Ptera(pygame.sprite.Sprite):
    def __init__(self,speed=5,scr_x=-1,scr_y=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = sprite_sheet('ptera.png',2,1,scr_x,scr_y,-1)
        self.ptera_height = [height*0.82,height*0.75,height*0.60]
        self.rect.centery = self.ptera_height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()

### ตัวละครลูกไฟ
class Fire(pygame.sprite.Sprite):
    def __init__(self,speed=5,scr_x=-1,scr_y=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images,self.rect = sprite_sheet('fire.png',8,1,25,25,-1)
        self.fire_height = [height*0.82,height*0.75,height*0.60]
        self.rect.centery = self.fire_height[random.randrange(0,3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed,0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1)%2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


### ตัวละครพื้น
class Ground():
    def __init__(self,speed=-5):
        self.image,self.rect = imp_image('ground.png',-1,-1,0)
        self.image1,self.rect1 = imp_image('ground.png',-1,-1,0)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image,self.rect)
        screen.blit(self.image1,self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


### สกอร์บอร์ด
class Scoreboard():
    def __init__(self,x=-1,y=-1):
        self.score = 0
        self.num_image,self.num_rec = sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
        self.image = pygame.Surface((55,int(11*6/5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width*0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height*0.1
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image,self.rect)

    def update(self,score):
        score_digits = extractDigits(score)
        self.image.fill(col)
        for s in score_digits:
            self.image.blit(self.num_image[s],self.num_rec)
            self.num_rec.left += self.num_rec.width
        self.num_rec.left = 0


### ฟังก์ชันแสดงหน้าเริ่ม
def introscreen():
    temp_dino = Dino(50 ,47)
    temp_dino.isBlinking = True
    gameStart = False



    temp_ground,temp_ground_rect = sprite_sheet('ground.png',1,1,-1,-1,-1)
    temp_ground_rect.left = 0
    temp_ground_rect.bottom = height

    logo,logo_rect = imp_image('logo.png',150,150,0)
    logo_rect.centerx = width/2
    logo_rect.centery = height/2
    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    temp_dino.isJumping = True
                    temp_dino.isBlinking = False
                    temp_dino.movement[1] = -1*temp_dino.jumpSpeed

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(black)
            screen.blit(temp_ground[0],temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo,logo_rect)

            temp_dino.draw()

            pygame.display.update()

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True


### เกมเพลย์
def gameplay():
    global HS
    gamespeed = 4
    gameOver = False
    gameQuit = False
    playerDino = Dino(44,47)
    new_ground = Ground(-1*gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width*0.78)
    counter = 0
    BG_sound.play()
    

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    fires = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Fire.containers = fires


    gameover_image,gameover_rect = imp_image('gov.png',138,70,0)
    temp_images,temp_rect = sprite_sheet('numbers.png',12,1,11,int(11*6/5),-1)
    HI_image = pygame.Surface((22,int(11*6/5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(col)
    HI_image.blit(temp_images[10],temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11],temp_rect)
    HI_rect.top = height*0.1
    HI_rect.left = width*0.73



    ### ลูปเกม
    while not gameQuit:
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if playerDino.rect.bottom == int(0.98*height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1*playerDino.jumpSpeed
                        if event.key == pygame.K_LSHIFT:
                        	gamespeed+=1
                        if event.key == pygame.K_DOWN:
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True
                                if pygame.mixer.get_init() != None :
                                	DK_sound.play()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False
                        if event.key == pygame.K_LSHIFT:
                        	gamespeed-=1
                  

            for c in cacti:
                c.movement[0] = -1*gamespeed
                if pygame.sprite.collide_mask(playerDino,c):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            for p in pteras:
                p.movement[0] = -1.5*gamespeed
                if pygame.sprite.collide_mask(playerDino,p):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            for f in fires:
                f.movement[0] = -2*gamespeed
                if pygame.sprite.collide_mask(playerDino,f):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()


            if len(cacti) < 5:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed,40,40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width*0.7 and random.randrange(0,25) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

            if len(pteras) == 0 and random.randrange(0,20) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Ptera(gamespeed, 46, 40))
            if len(fires) == 0 and random.randrange(0,200) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width*0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Fire(gamespeed, 46, 40))

            playerDino.update()
            cacti.update()
            pteras.update()
            fires.update() 
            new_ground.update()
            scb.update(playerDino.score)
            highsc.update(HS)

            if pygame.display.get_surface() != None:
                screen.fill(col)
                new_ground.draw()
                
                scb.draw()
                if HS != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                cacti.draw(screen)
                pteras.draw(screen)
                fires.draw(screen)
                playerDino.draw()

                pygame.display.update()
            clock.tick(FPS)
            ov = False
            if ov :
            	Over_sound.play()


            if playerDino.isDead:
                gameOver = True
                if playerDino.score > HS:
                    HS = playerDino.score
                
                pygame.mixer.pause()
                

            if counter%700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameplay()
            highsc.update(HS)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(gameover_image)
                if HS != 0:
                    highsc.draw()
                    screen.blit(HI_image,HI_rect)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


def main():
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()

main()