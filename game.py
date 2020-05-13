from time import sleep
import random
import time

import pygame
pygame.init()

#------------GAME EXIT--------------
def game_exit():
    pygame.quit()
    quit()
#------------COLORS-----------------

red = [200,0,0]
green= [0,200,0]
blue= [0,0,200]
bright_red = [255,0,0]
bright_green = [0,255,0]
white = [255,255,255]
black = [0,0,0]
light_gray = [166, 166, 166]
dark_gray = [102, 102, 102]
#------------game_display-----------

display_width = 800
display_height = 600
size = display_width,display_height

game_display = pygame.display.set_mode(size)
pygame.display.set_caption("Survive")
background_image = pygame.image.load("images/background.png").convert()


#------------CLOCK------------------

clock = pygame.time.Clock()


#------------CHARACTERS-------------

soldier_left_img = pygame.image.load("images/soldier_left.png")
soldier_right_img = pygame.image.load("images/soldier_right.png")

bullet_right = pygame.image.load("images/bullet_right.png")
bullet_left = pygame.image.load("images/bullet_left.png")

zombie_left = pygame.image.load("images/zombie_left.png")
zombie_right = pygame.image.load("images/zombie_right.png")

def soldier(x,y,direction):
    if direction.lower() == "r":
        game_display.blit(soldier_right_img,(x,y))
    else:
        game_display.blit(soldier_left_img,(x,y))

def fire(bullet_x,bullet_y,direction):
    if direction == "l":
        x = bullet_x-10
        y = bullet_y+15
        game_display.blit(bullet_left,(x,y))
    elif direction =="r":
        x = bullet_x+55
        y = bullet_y+13
        game_display.blit(bullet_right,(x,y))



    
def zombie(x,y,direction,hp,initial_hp):
    if direction.lower() == "r":
        game_display.blit(zombie_right,(x,y))
    else:
        game_display.blit(zombie_left,(x,y))
    
    

#------------TEXT AND OBJECTS------------------
def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()




def button(msg,x,y,w,h,d_c,l_c,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display,l_c,[x,y,w,h])
        if click[0] == 1 and action != None:
            if action == game_loop:
                action()
            else:
                action()
    else:
        pygame.draw.rect(game_display,d_c,[x,y,w,h])  
    
    small_text = pygame.font.Font('images/freesansbold.ttf',20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(text_surf, text_rect)


#------------MENU LOOP--------------
def menu():
    logo = pygame.image.load("images/logo.png").convert()
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit()
                
        game_display.fill(white)
        medium_text = pygame.font.Font('images/freesansbold.ttf',55)
        text_surf, text_rect = text_objects("game", medium_text)
        text_rect.center = ((display_width/2 + 30),(35))
        game_display.blit(logo,text_rect)
        button("Start",250,500,100,50,green,bright_green,game_loop)
        button("Quit",500,500,100,50,red,bright_red,game_exit)
        pygame.display.update()
        clock.tick(15)


#------------GAME LOOP--------------

highscore = 0
def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.74)
    soldier_width = 64
    x_change = 0
    kills = 0

    bullet_x = x
    bullet_y = y
    shoted = 0
    bullet_speed = 10
    last_position = "l"

    zombie_startx = random.choice([0,800])
    if zombie_startx == 0:
        z_last_position = "l"
    else:
        z_last_position = "r"
    zombie_starty = 440
    zombie_speed = 1

    zombie_count = 1
    kills = 0
    hp = 30
    initial_hp = hp
    game_exit = 0

    while not game_exit:
        if not shoted:
            bullet_x = x
        game_display.blit(background_image, [0, 0])

        small_text = pygame.font.Font('images/freesansbold.ttf',20)
        text_surf, text_rect = text_objects("score:{}".format(kills), small_text)
        text_rect.center = ( (35), (20) )
        game_display.blit(text_surf, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullet = fire(bullet_x,bullet_y,last_position)
                    bullet_speed = 10
                    shoted = 1
                else:
                    pass
        x += x_change
        if z_last_position == "l": 
            zombie_startx += zombie_speed

        else:
            zombie_startx -= zombie_speed
        zombie(zombie_startx,zombie_starty,z_last_position,hp,initial_hp)
        if shoted and z_last_position == last_position:
            shoted=0
            hp -=10
        if shoted:
            if last_position == "r":
                bullet_x = x+ bullet_speed
                pygame.display.update(bullet)
                fire(bullet_x,bullet_y,"r")
                bullet_speed += 50
                if bullet_x > display_width+150:
                    shoted=0
                
            else:
                bullet_x = x+ bullet_speed
                fire(bullet_x,y,"l")
                bullet_speed -= 50
                if bullet_x < -50:
                    shoted = 0
        if x > (display_width-soldier_width):
            x -= 5 
        if x < 0:
            x += 5
        if x_change < 0:
            soldier(x,y,"l")
            last_position = "l"
        elif x_change > 0:
            last_position = "r"
            soldier(x,y,"r")
        else:
            soldier(x,y,last_position)


        if hp == 0 or zombie_startx > 850 or zombie_startx < -50:
            hp = 30
            zombie_startx = random.choice([0,800])
            some_x = zombie_startx
            if some_x == 0:
                z_last_position = "l"
            else:
                z_last_position = "r"
            kills += 1
            zombie_speed +=1

        if z_last_position == "l":
            if zombie_startx >= x-40:
                break
        else:
            if zombie_startx <= x+40:
                break
        pygame.display.update()
        clock.tick(60)


menu()
pygame.quit()