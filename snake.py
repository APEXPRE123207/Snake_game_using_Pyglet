"""Tried to learn and make something new, ended up making a snake game from scratch. Used only online documentations available, as not many videos are available for this
package.Got frusatrated, cried a little bit maybe, but after few days finally completed this mini project of user playable, snake game, which consists all features, 
of a normal snake game. Hope you like it cause i like it very much, as I learnt from it a lot.
Thank you for going through my shit, have a good day"""

"""Open for suggestions, tips and etc"""

"""BUGS: Currently none, please inform if you find some, thank you"""

import pyglet as py
from pyglet.window import Window
from pyglet.window import key
from pyglet import graphics
from pyglet import image
from pyglet import resource
from pyglet import media
from pyglet import text
from itertools import cycle
from random import randint

window=py.window.Window(1500,760) #Window size

@window.event
def on_draw():
    window.clear()
    draw_square(snk_x,snk_y,cell_size) #draws head
    draw_square(fd_x,fd_y,cell_size,colour=(255,0,0,0)) #draws food
    for coors in tail:
        draw_square(coors[0],coors[1],cell_size,colour=(0,127,0,0)) #draws tail
    draw_square(snk_x,snk_y,cell_size) #draws head infront of tail 
    display_score()
    if game_over:
        draw_game_over()

def display_score():
    score=text.Label(f'Score: {len(tail)}', font_name='Times New Roman',
                     font_size=16,
                     x=10, y=window.height-20,
                     anchor_x='left', anchor_y='top')
    score.draw()

"""Creates new game after restart"""

def new_game():
    global snk_x,snk_y,snk_dx,snk_dy,game_over,tail
    if cell_size<1 or window.width%cell_size!=0 or window.height%cell_size!=0:
        print(window.width,window.height)
        print("Invalid cell size")
        exit()
    
    snk_x=window.width//cell_size//2*cell_size
    snk_y=window.height//cell_size//2*cell_size
    snk_dx,snk_dy=0,0
    tail=[]

    place_food()
    game_over=False

def draw_square(x,y,size,colour=(0,255,0,0)):
    img=image.create(size,size,py.image.SolidColorImagePattern(colour))
    img.blit(x,y)

def position():
    global tail
    fd_xx=randint(0,(window.width//cell_size)-1)*cell_size
    fd_yy=randint(0,(window.height//cell_size)-1)*cell_size
    if (fd_xx,fd_yy) in tail:
        return position()
    return fd_xx,fd_yy

def place_food():
    global fd_x,fd_y
    fd_x,fd_y=position()

def draw_game_over():
    game_screen=text.Label(f'Score: {len(tail)}\n (Press space to restart)',font_size=24,x=window.width//2,y=window.height//2,width=window.width,align='center',anchor_x='center',anchor_y='center',multiline=True)
    game_screen.draw()


"""Key bindings can be changed as per requirement eg. symbol==key.A, etc """
@window.event

def on_key_press(symbol,modifiers): 
    global snk_dx,snk_dy,game_over
    if not game_over:
        if symbol==key.LEFT: #Left arrow key
            if snk_dx==0:
                snk_dx=-cell_size #Left is negative in x axis
                snk_dy=0
        elif symbol==key.RIGHT: #Right arrow key
            if snk_dx==0:
                snk_dx=cell_size #Right is positive in x axis
                snk_dy=0
        elif symbol==key.UP: #Up arrow key
            if snk_dy==0:
                snk_dx=0
                snk_dy=cell_size #Up is positive in y axis
        elif symbol==key.DOWN: # Down arrow key
            if snk_dy==0:
                snk_dx=0
                snk_dy=-cell_size # Down is negative in y axis
    else:
        if symbol==key.SPACE: #Detects spacebar to restart the game
            new_game()

def update(dt):
    global snk_dx,snk_dy,snk_x,snk_y,game_over
    if game_over:
        return
    if game_over_condn():
        game_over=True
        return
    tail.append((snk_x,snk_y)) #It appends the coordinates to tail
    snk_x += snk_dx
    snk_y += snk_dy
    if snk_x==fd_x and snk_y==fd_y:
        place_food() #If food is eaten then the coordinate of the tail stays
    else:
        tail.pop(0) #Else it gets popped

def game_over_condn(): #Checks for gaem over conditions:- 1. Out of grid., 2. Head hitting the tail
    condn1=snk_x+snk_dx<0 or snk_x+snk_dx>window.width-cell_size or snk_y+snk_dy<0 or snk_y+snk_dy>window.height-cell_size
    condn2=(snk_x,snk_y) in tail
    return condn1 or condn2 



cell_size=20 #Size of the snake
fd_x,fd_y=0,0 #Initializaton of position of food
new_game()
py.clock.schedule_interval(update,1/15) # Schedules the update function to be called repeatedly at a fixed interval of time. Here, it is 1/15, 💀
#if you want to increase the spped of the snake, increase the value of the denominator (Try making it 1/10000000) 
py.app.run()