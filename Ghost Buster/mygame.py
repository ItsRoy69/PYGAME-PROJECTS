import pygame
import random
from pygame.locals import *
pygame.init()
w=1000
h=500
red=(255,0,0)
col=(255,0,255)
col1=(255,255,0)
sec=8
pygame.time.set_timer(USEREVENT+1,1000)


# Time
def time(sec):
    font = pygame.font.SysFont(None,40)
    text=font.render('Time Left : '+str(sec),True,col)
    screen.blit(text,(w-200,0))


# Game Over
def over():
    while True:
        font = pygame.font.SysFont(None,40)
        text=font.render('GAME OVER !! ',True,col1)
        screen.blit(text,(w/2-40 ,h/2-40))
        pygame.display.update()
        quit()
    

# Images and Sounds of Background and Gun
screen = pygame.display.set_mode((w,h))
pic=pygame.image.load("assets/images/background.png")
tar=pygame.image.load("assets/images/aim_pointer.png")
gun=pygame.image.load("assets/images/gun.png")
gsound=pygame.mixer.Sound("assets/sounds/shot_sound.wav")
bsound=pygame.mixer.Sound("assets/sounds/background.wav")
bsound.play()

# Score Count
def score(counter):
    font = pygame.font.SysFont(None,40)
    text=font.render('Score : '+str(counter),True,red)
    screen.blit(text,(8,0))


# Images of Ghosts
def game():
    sec=20
    w=800
    h=500
    z1=pygame.image.load("assets/images/ghost_1.png")
    z2=pygame.image.load("assets/images/ghost_2.png")
    z3=pygame.image.load("assets/images/ghost_3.png")
    z4=pygame.image.load("assets/images/ghost_4.png")
    zlist=[z1,z2,z3,z4]
    zimg=random.choice(zlist)
    zx = random.randint(0,w - 200)
    zy = random.randint(0,h - 300)
    counter = 0

    # Game Loop
    while True:
        mx, my = pygame.mouse.get_pos()
        print(mx,my)
        zrec= pygame.Rect(zx,zy,zimg.get_width(),zimg.get_height())
        point= pygame.Rect(mx,my,tar.get_width(),tar.get_height())
        for event in pygame.event.get():
            print(event)
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        
            elif event.type==USEREVENT+1:
                sec-=1
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                gsound.play()
                if zrec.colliderect(point):
                    print("collission")
                    zx = random.randint(0,w - 200)
                    zy = random.randint(0,h - 300)
                    zimg=random.choice(zlist)
                    counter+=1
        if sec==0:
            over()
            break

        
        screen.blit(pic,(0,0))
        screen.blit(zimg,(zx,zy))
        screen.blit(tar,(mx-48,my-48))
        score(counter)
        time(sec)
        screen.blit(gun,(mx,h - 250))
        pygame.display.update()


game()