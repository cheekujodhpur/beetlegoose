import cv2
import numpy as np
import pygame

# global declares
NON_WHITE = (255,0,0)
WHITE = (255,255,255)
width, height = 1024, 768
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

class Monster:
    def __init__(self, path, size, pos, direction):
        self.path = path
        self.size = size
        self.pos = pos
        self.direction = direction
        self.n_frames = 8
        self.frame_id = 0
        self.frames = []
        self.active = True
        self.__init_frames()

    def __init_frames(self):
        # load all into memory
        for i in range(self.n_frames):
            img = pygame.image.load("{0}/frame-{1}.png".format(self.path,str(i+1)))
            img = pygame.transform.scale(img, self.size)
            self.frames.append(img)

    def __update_frame_id(self):
        self.frame_id = (self.frame_id + 1)%self.n_frames

    def update(self, update_f):
        if not self.active:
            return
        self.direction, self.pos = update_f(self.size, self.pos, self.direction)

    def draw(self,screen):
        if not self.active:
            return
        screen.blit(self.frames[self.frame_id], self.pos)
        self.__update_frame_id()

    def kill(self):
        self.active = False

    def is_hit(self,pt):
        if 0 <= pt[0]-self.pos[0] <= self.size[0] and \
        0 <= pt[1]-self.pos[1] <= self.size[1]:
            return True
        return False

class Air:
    def __init__(self, path, size):
        self.path = path
        self.size = size
        self.pos = (0,0)
        self.n_frames = 6
        self.frame_id = 0
        self.frames = []
        self.active = False
        self.__init_frames()

    def __init_frames(self):
        # load all into memory
        for i in range(self.n_frames):
            img = pygame.image.load("{0}/frame-{1}.png".format(self.path,str(i+1)))
            img = pygame.transform.scale(img, self.size)
            self.frames.append(img)

    def __update_frame_id(self):
        self.frame_id = self.frame_id + 1
        # kill after one animation
        if self.frame_id == self.n_frames:
            self.active = False

    def update(self):
        return

    def draw(self,screen):
        if not self.active:
            return
        screen.blit(self.frames[self.frame_id], self.pos)
        self.__update_frame_id()

    def activate(self, pos):
        self.pos = pos
        self.frame_id = 0
        self.active = True

def monster_random_motion(size, pos, direction):
    # determine a random motion
    speed = 4

    dx = speed*np.cos(direction)
    dy = speed*np.sin(direction) 
    updated = tuple(map(lambda x,y:x+y,pos,(dx,dy)))

    b1 = size[0]
    b3 = size[1]
    b2 = width-size[0]
    b4 = height-size[1]

    if b1 < pos[0] < b2 and b3 < pos[1] < b4:
        updated_direction = direction + (2*np.random.random()-1)
        while updated_direction >= 2*np.pi:
            updated_direction = updated_direction-2*np.pi
    else:
        updated_direction = direction

    # do nothing if trying to move out
    if (pos[0] < b2 and updated[0] > b2) or \
    (pos[0] > b1 and updated[0] < b1) or \
    (pos[1] > b3 and updated[1] < b3) or \
    (pos[1] < b4 and updated[1] > b4):
        updated = pos

    return updated_direction, updated

def pick_inactive(pool):
    for el in pool:
        if not el.active:
            return el

def render(queues={}):
    pygame.init()
    screen = pygame.display.set_mode((width, height),pygame.FULLSCREEN)
    background = pygame.image.load("res/images/bg.png")
    background = pygame.transform.scale(background,(width,height))

    running = True
    screen.fill((0,0,0))
    pygame.display.flip()
    calib_frame_id = 0
    calib_frame_N = 16
    advance_frame_id = lambda x:(x+1)%calib_frame_N
    calib_box_size = 20

    n_monsters = 4
    # declare monsters
    monster_size = (80,80)
    bat1 = Monster("res/images/08_bat_monster",monster_size,(-100,0), 0.35*np.pi)
    bat2 = Monster("res/images/08_bat_monster",monster_size,(1,height+100),-0.35*np.pi)
    pumpkin1 = Monster("res/images/07_flying_pumpkin",monster_size,(width,-100),0.8*np.pi)
    pumpkin2 = Monster("res/images/07_flying_pumpkin",monster_size,(width+100,height),1.3*np.pi)
    all_monsters = [bat1, bat2, pumpkin1, pumpkin2] 

    #declare air explosion
    airs = [Air("res/images/air_explode", monster_size) for i in range(n_monsters)]

    while running:
        screen.fill(0)

        screen.blit(background,(0,0))
        draw_calib_rects(pygame, screen, calib_box_size, width, height, calib_frame_id)
        for monster in all_monsters:
            monster.update(monster_random_motion)
            monster.draw(screen)

        for air in airs:
            air.update()
            air.draw(screen)

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pt = pygame.mouse.get_pos()
                # evaluate this
                for monster in all_monsters:
                    if monster.is_hit(pt):
                        monster.kill()
                        pick_inactive(airs).activate(monster.pos)

if __name__ == '__main__':
    render()
