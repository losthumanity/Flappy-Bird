import pygame, sys, random

def movefloor():
    screen.blit(floor_surface,(floor_x_pos,700))
    screen.blit(floor_surface,(floor_x_pos+450,700))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (650,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (650,random_pipe_pos - 250))
    return bottom_pipe,top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 4.5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
        
def check_collsion(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 750:
        can_score = True
        death_sound.play()
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
    return new_bird

def animate_bird():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect 

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render((str(int(score/4))),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (225, 90))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render((f'Score: {(int(score/4))}'),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (225, 90))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render((f'High Score: {(int(high_score/4))}'),True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (225, 650))
        screen.blit(high_score_surface,high_score_rect)

def check_score(score,high_score):
    if score > high_score:
        return score
    else:
        return high_score

def pipe_score_check():
    global score,can_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105:
                score += 1
                score_sound.play()
                can_score = False
            elif pipe.centerx < 0:
                can_score = True

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1,buffer = 512)
pygame.init()
screen = pygame.display.set_mode((450,800))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF',40)

# Game Variables
gravity = 0.20
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

bg_surface = pygame.image.load('assets/background-night.png').convert()
scaled_factor = 1.5625
bg_surface = pygame.transform.scale(bg_surface, (
    int(bg_surface.get_width() * scaled_factor),
    int(bg_surface.get_height() * scaled_factor)
))

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (
    int(floor_surface.get_width() * scaled_factor),
    int(floor_surface.get_height() * scaled_factor)
))
floor_x_pos = 0


bird_downflap = pygame.image.load('assets/bluebird-downflap.png')
bird_downflap = pygame.transform.scale(bird_downflap, (
    int(bird_downflap.get_width() * scaled_factor),
    int(bird_downflap.get_height() * scaled_factor)
))

bird_midflap = pygame.image.load('assets/bluebird-midflap.png')
bird_midflap = pygame.transform.scale(bird_midflap, (
    int(bird_midflap.get_width() * scaled_factor),
    int(bird_midflap.get_height() * scaled_factor)
))

bird_upflap = pygame.image.load('assets/bluebird-upflap.png')
bird_upflap = pygame.transform.scale(bird_upflap, (
    int(bird_upflap.get_width() * scaled_factor),
    int(bird_upflap.get_height() * scaled_factor)
))

bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (90,400))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale(bird_surface, (int(bird_surface.get_width() * scaled_factor),
#                                                      int(bird_surface.get_height() * scaled_factor)))
# bird_rect = bird_surface.get_rect(center = (90,400))

pipe_surface = pygame.image.load('assets/pipe-red.png')
pipe_surface = pygame.transform.scale(pipe_surface, (
    int(pipe_surface.get_width() * scaled_factor),
    int(pipe_surface.get_height() * scaled_factor)
))

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [350,450,550]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_surface = pygame.transform.scale(game_over_surface, (
    int(game_over_surface.get_width() * scaled_factor),
    int(game_over_surface.get_height() * scaled_factor)
))
game_over_rect = game_over_surface.get_rect(center = (225,400))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 142  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (90,400)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = animate_bird()

    screen.blit(bg_surface,(0,0))

    if game_active:
        
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collsion(pipe_list)

        # Pipes
        pipe_list = move_pipe(pipe_list)
        draw_pipes(pipe_list)
        
        pipe_score_check()
        high_score = check_score(score,high_score)
        score_display('main_game')
    else:
        screen.blit(game_over_surface,game_over_rect)
        # high_score = check_score(score,high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    movefloor()
    if floor_x_pos <= -450:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
