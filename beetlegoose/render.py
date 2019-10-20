import cv2
import numpy as np
import pygame

# global declares
NON_WHITE = (64,191,191)
WHITE = (255,255,255)
def draw_calib_rects(pygame, screen, calib_box_size, width, height, calib_frame_id):
    pygame.draw.rect(screen, WHITE,
            (0, 0, calib_box_size, calib_box_size))
    pygame.draw.rect(screen, WHITE,
            (width-calib_box_size, 0,
            calib_box_size, calib_box_size))
    pygame.draw.rect(screen, WHITE,
            (width-calib_box_size, height-calib_box_size,
            calib_box_size, calib_box_size))
    pygame.draw.rect(screen, WHITE,
            (0, height-calib_box_size,
            calib_box_size, calib_box_size))

    if (1 & calib_frame_id):
        pygame.draw.rect(screen, NON_WHITE,
                (0, 0, calib_box_size, calib_box_size))
    if (2 & calib_frame_id):
        pygame.draw.rect(screen, NON_WHITE,
                (width-calib_box_size, 0, calib_box_size, calib_box_size))
    if (4 & calib_frame_id):
        pygame.draw.rect(screen, NON_WHITE,
                (width-calib_box_size, height-calib_box_size,
                calib_box_size, calib_box_size))
    if (8 & calib_frame_id):
        pygame.draw.rect(screen, NON_WHITE,
                (0, height-calib_box_size, calib_box_size, calib_box_size))

def render():
    pygame.init()
    width, height = 1024, 768
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
    running = True
    screen.fill((0,0,0))
    pygame.display.flip()
    calib_frame_id = 0
    calib_frame_N = 16
    advance_frame_id = lambda x:(x+1)%calib_frame_N
    calib_box_size = 20
    while running:
        screen.fill(0)

        draw_calib_rects(pygame, screen, calib_box_size, width, height, calib_frame_id)

        pygame.display.flip()

        # post render procedures
        calib_frame_id = advance_frame_id(calib_frame_id)
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit(0)

