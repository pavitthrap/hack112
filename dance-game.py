#!/usr/bin/env python

#Example of program in action can be found here http://www.youtube.com/watch?v=burYkYiI8vg

import sys, pygame, random, pygame.mixer, cv2
from PIL import Image
import PIL.ImageOps


#Setup
def setup():
    #Set resolution of camera
    global cam_h_rez
    global cam_v_rez
    global camera
    cam_h_rez = 640
    cam_v_rez = 480
    camera_port = 0
    #Opencv is used for video capture.  This ensures Windows compatibility as PyGame does not support a webcam in that OS.  
    camera = cv2.VideoCapture(camera_port)


    #Initiate pygame 
    pygame.init()


    #Program globals
    global black
    global size
    global screen
    global white
    global bass01
    global bass02
    global bass03
    global booo
    global applause

    size = width, height = cam_h_rez + (cam_h_rez / 2), cam_v_rez 
    black = 0,0,0
    white = 255,255,255
    screen = pygame.display.set_mode(size)
        
    #Set window title
    pygame.display.set_caption("RAVE 0.1")


    #Audio files for sound effects, use your own.
    bass01 = pygame.mixer.Sound('bass01.ogg')
    bass02 = pygame.mixer.Sound('clap01.ogg')
    bass03 = pygame.mixer.Sound('snare01.ogg')
    applause = pygame.mixer.Sound('Applause.wav')
    booo = pygame.mixer.Sound('booo.wav')


#Capture image
def get_image():
    retval, im = camera.read()
    return im


#title and options function
def title():

    #Threshholds (adjust to optimize for your lighting conditions)
    global rgb_thresh
    global movement_thresh
    rgb_thresh = 17 #camera sensitivity 
    movement_thresh = 2 #motion sensitvity
    screen.fill(black) 

    #Define menu text 
    font = pygame.font.Font(None, 45)
    text = font.render("Rave 0.1", True, (white))
    text2 = font.render("Select Difficulty (Press 1 - 4 on your keyboard)", True, (white))
    screen.blit(text, (((cam_h_rez/2) - 5), ((cam_v_rez/2) + 50)))
    screen.blit(text2, (((cam_h_rez/2) - 50), ((cam_v_rez/2) - 5)))
    pygame.display.flip()

    #Define keyboard inputs	
    exit = 1
    while exit == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:sys.exit()
            elif event.type == pygame.KEYDOWN:	
                if event.key == pygame.K_1:
                    exit = 0
                elif event.key == pygame.K_2:
                    exit = 0
                    movement_thresh = 8
                elif event.key == pygame.K_3:
                    exit = 0
                    movement_thresh = 16
                elif event.key == pygame.K_4:
                    exit = 0
                    movement_thresh = 32
    #Start main game function
    main_game()

                    


#calculate score, render messages
def score_board():

    final_score = movement_counter - lameness

    font = pygame.font.Font(None, 45)
    text = font.render("Final Score = " + str(final_score), True, (white))

    if movement_counter > lameness:
        text2 = font.render("Congrats!", True, (white))
        applause.play(loops=0, maxtime=0, fade_ms=0)
    else:
        text2 = font.render("Laaammmeee!", True, (white))
        booo.play(loops=0, maxtime=0, fade_ms=0)

    text3 = font.render("Press E to exit, T for title screen, A to try again", True, (white))	
                
    screen.blit(text, (((cam_h_rez/2) - 15), ((cam_v_rez/2) - 5)))
    screen.blit(text2, (((cam_h_rez/2) - 5), ((cam_v_rez/2) - 33)))
    screen.blit(text3, (((cam_h_rez/2) - 150), ((cam_v_rez/2) + 50)))
    pygame.display.flip()
        
    exit = 1
    while exit == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e: 
                    exit = 0
                    key_action = 1
                elif event.key == pygame.K_t:
                    exit = 0
                    key_action = 2
                elif event.key == pygame.K_a:
                    exit = 0
                    key_action = 3
                else:
                    sys.exit()

            
    if key_action == 1:
        sys.exit()
    elif key_action == 2:
        title()
    elif key_action == 3:
        main_game()
    else:
        sys.exit()
            

#Main function
def main_game():

    global movement_counter
    global lameness
    movement_counter = 0
    movement_direction = 0
    lameness = 0
    rave_beat = 0
    screen.fill(black)

    #Main game loop
    while (movement_counter or lameness) < cam_v_rez:

        #Quit on window exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:sys.exit()

        #Capture and convert first frame	
        buffer_1 = get_image()
        buffer_1 = Image.fromstring('RGB', (cam_h_rez, cam_v_rez),  buffer_1)
        pixels = buffer_1.load()
        
        #Loop counters
        v_counter = 0
        h_counter = 0	
        past_image_value = []
        rgb_counter = 0

        #Capture and convert second frame
        buffer_2 = get_image()
        buffer_2 = Image.fromstring('RGB', (cam_h_rez, cam_v_rez),  buffer_2)
        pixels2 = buffer_2.load()

        #Generate random color values
        r_rand = random.randrange(50, 255)
        g_rand = random.randrange(50, 255)
        b_rand = random.randrange(50, 255)

        #Loop 2
        for v_counter in range(0, cam_v_rez):
            for h_counter in range(0, cam_h_rez):

                #Calculate average RGB values
                rgb_total1 = pixels[h_counter, v_counter]
                rgb_total2 = pixels2[h_counter, v_counter]
                rgb_1 = (rgb_total1[0] + rgb_total1[1] + rgb_total1[2]) / 3
                rgb_2 = (rgb_total2[0] + rgb_total2[1] + rgb_total2[2]) / 3

                #Compare RGB values of first and second frame vased on thresholds
                if (rgb_1 - rgb_2) > rgb_thresh or (rgb_2 - rgb_1) > rgb_thresh:
                #Gerate array to render as motion detection image
                #If motion detected add white pixel
                    past_image_value.append((r_rand,g_rand,b_rand))
                    rgb_counter += 255

                else:	

                #If motion not detected add black pixel
                    past_image_value.append((0,0,0))
                                                    
        #render image from array
        render_img = Image.new('RGB', (cam_h_rez, cam_v_rez))
        render_img.putdata(past_image_value)
        render = render_img.tostring()
        render = pygame.image.fromstring(render, (cam_h_rez, cam_v_rez), 'RGB')

        #if motion detected, increase motion bar and play audio	
        if (rgb_counter / (cam_h_rez * cam_v_rez)) > movement_thresh:
            movement_counter += 2
            movement_direction = 1
            rave_beat += 1
            if rave_beat == 4:
                bass02.play(loops = 0, maxtime = 0, fade_ms = 0)
            elif rave_beat == 8:
                bass03.play(loops = 0, maxtime = 0, fade_ms = 0)
                rave_beat = 0
            else:
                bass01.play(loops = 0, maxtime = 0, fade_ms = 0)

        else: 
                if movement_counter > 0:
                    pygame.draw.line(screen, black, [0, size[1] - movement_counter],[(size[0]/2), size[1] -movement_counter],2)
                    movement_counter -= 2 
                    movement_direction = 0
    


        #Pygame render
        if movement_direction == 1:
            pygame.draw.line(screen, ((movement_counter/2), (255 - (movement_counter/2)), 0), [0, size[1] -  movement_counter],[(size[0]/2), size[1] - movement_counter],2)

        else:
            pygame.draw.line(screen, ((lameness/2), 0, (255 - (lameness/2))), [(size[0]/2), size[1] -  lameness],[size[0], size[1] - lameness],2)
            lameness += 2
                
            screen.blit(render,(cam_v_rez / 3, 0))
            pygame.display.flip()

    #Call score board function  	
    score_board()


#Call functions on startup	


setup()


title()


main_game()