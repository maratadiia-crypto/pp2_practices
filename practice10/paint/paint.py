import pygame  
pygame.init()  

# screen settings
screen = pygame.display.set_mode((900, 700)) 
screen.fill((255, 255, 255))  
pygame.display.set_caption('GFG Paint')  
draw_on = False  #drawing state
last_pos = (0, 0)  #last mouse position

radius = 5  #brush size

# colors
WHITE = (255 ,255, 255) 
RED = (255, 0, 0)  
YELLOW = (255, 255, 0)  
GREEN = (102, 204, 0) 
BLUE = (51, 51, 255)  
BLACK = (0, 0, 0)  
PINK = (255, 0, 255) 

# draw color palette
pygame.draw.rect(screen, RED, (0, 50, 20, 20))  
pygame.draw.rect(screen, YELLOW, (0, 70, 20, 20))  
pygame.draw.rect(screen, GREEN, (20, 50, 20, 20))  
pygame.draw.rect(screen, BLUE, (20, 70, 20, 20))  
pygame.draw.rect(screen, BLACK, (0, 90, 20, 20))  
pygame.draw.rect(screen, PINK, (20, 90, 20, 20))  

erasor = pygame.transform.scale(
    pygame.image.load('practice10/paint/eraser.png'), (40, 40)
)  # load and resize eraser
screen.blit(erasor, [0, 110])  # draw eraser icon


def roundline(canvas, color, start, end, radius=1):  #smooth line drawing
    Xaxis = end[0] - start[0]   #difference in x
    Yaxis = end[1] - start[1]   #difference in y
    dist = max(abs(Xaxis), abs(Yaxis))  #calculate distance

    for i in range(dist):  # draw small circles
        x = int(start[0] + float(i) / dist * Xaxis)  #x position
        y = int(start[1] + float(i) / dist * Yaxis)  #y position
        pygame.draw.circle(canvas, color, (x, y), radius)  #draw point


try:
    while True:  #main loop

        e = pygame.event.wait()  #wait for event

        if e.type == pygame.QUIT:  #close window
            raise StopIteration

        #mouse click
        if e.type == pygame.MOUSEBUTTONDOWN:

            spot = pygame.mouse.get_pos()  #get mouse position

            #color selection
            if spot[0] < 20 and spot[1] < 70 and spot[1] > 50:
                color = RED  
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 70 and spot[1] > 50:
                color = GREEN 
            elif spot[0] < 20 and spot[1] < 90 and spot[1] > 70:
                color = YELLOW  
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 90 and spot[1] > 70:
                color = BLUE  
            elif spot[0] < 20 and spot[1] < 110 and spot[1] > 90:
                color = BLACK  
            elif spot[0] < 40 and spot[0] > 20 and spot[1] < 110 and spot[1] > 90:
                color = PINK  
            elif spot[0] < 40 and spot[1] < 150 and spot[1] > 110:
                color = WHITE  # eraser color

            #start drawing
            if spot[0] > 60:
                pygame.draw.circle(screen, color, e.pos, radius)  # draw point

            draw_on = True  #enable drawing

        #stop drawing
        if e.type == pygame.MOUSEBUTTONUP:
            draw_on = False  #disable drawing

        #mouse movement
        if e.type == pygame.MOUSEMOTION:

            spot = pygame.mouse.get_pos()  #get position

            if draw_on and spot[0] > 60:  #draw only on canvas
                pygame.draw.circle(screen, color, e.pos, radius)  #draw point
                roundline(screen, color, e.pos, last_pos, radius)  #smooth line

            last_pos = e.pos  #save last position

        #keyboard control
        if e.type == pygame.KEYDOWN:

            spot = pygame.mouse.get_pos()  #get mouse position

            if e.key == pygame.K_r:  #draw rectangle
                rect_size = 100  #rectangle size
                pygame.draw.rect(
                    screen,
                    color,
                    (spot[0], spot[1], rect_size, rect_size + 100)
                )

            elif e.key == pygame.K_c:  #draw circle
                circle_radius = 50  #circle radius
                pygame.draw.circle(
                    screen,
                    color,
                    (spot[0], spot[1]),
                    circle_radius
                )

        pygame.display.flip()  #update screen
except StopIteration:
    pass
pygame.quit()  