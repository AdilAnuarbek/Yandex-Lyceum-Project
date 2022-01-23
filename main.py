import pygame
import random
import sys


def draw_floor():
    screen.blit(floor, (floor_x_pos, 900))
    screen.blit(floor, (floor_x_pos + 576, 900))


def spawn_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(650, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(650, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            can_score = True
            return False
    if bird_rect.top < -100 or bird_rect.bottom > 900:
        can_score = True
        return False
    return True


def bird_anim():
    b = bird_frames[bird_pose]
    b_rect = b.get_rect(center=(100, bird_rect.centery))
    return b, b_rect


def show_score(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    p = []
    for pipe in pipes:
        if pipe.right > -50:
            p.append(pipe)
    return p


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def score_update(s, hs):
    if s > hs:
        hs = s
    return hs


def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                can_score = False
            if pipe.centerx < 0:
                can_score = True


pygame.init()

width = 576
height = 1024
screen = pygame.display.set_mode((width, height))

color = (255, 255, 255)
color_light = (170, 170, 170)
color_dark = (100, 100, 100)
selected_color = (230, 230, 230)

clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

smallfont = pygame.font.SysFont('Corbel', 20)

# select menu texts
night_bg_text = smallfont.render('Choose Night Theme', True, color)
day_bg_text = smallfont.render('Choose Day Theme', True, color)
bluebird_text = smallfont.render('Blue Bird', True, color)
redbird_text = smallfont.render('Red Bird', True, color)
yellowbird_text = smallfont.render('Yellow Bird', True, color)
exit_text = smallfont.render('Exit', True, color)
continue_text = smallfont.render('Continue', True, color)

bg_theme = 'Day Theme'
bird_color = 'Blue Bird'
blue_bird = False
red_bird = False
yellow_bird = False
day_theme = False
night_theme = False

game_active = True
settings_enabled = False
gravity = 0.2
bird_movement = 0
score = 0
high_score = 0
can_score = True
background = pygame.image.load('images/background_day.png').convert()
background = pygame.transform.scale2x(background)

floor = pygame.image.load('images/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# color of the bird by default
bird_down = pygame.transform.scale2x(pygame.image.load('images/bluebird_down.png').convert_alpha())
bird_mid = pygame.transform.scale2x(pygame.image.load('images/bluebird_mid.png').convert_alpha())
bird_up = pygame.transform.scale2x(pygame.image.load('images/bluebird_up.png').convert_alpha())
bird_frames = [bird_down, bird_mid, bird_up]
bird_pose = 0
bird_surface = bird_frames[bird_pose]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDPOSE = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDPOSE, 200)

pipe_surface = pygame.image.load('images/pipe.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

game_over_surface = pygame.transform.scale2x(pygame.image.load('images/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_height = [400, 500, 600, 700, 800]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and settings_enabled:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = -8
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE and settings_enabled:
            pipe_list.extend(spawn_pipe())

        if event.type == BIRDPOSE and settings_enabled:
            if bird_pose < 2:
                bird_pose += 1
            else:
                bird_pose = 0

            bird_surface, bird_rect = bird_anim()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if width / 2 <= mouse[0] <= width / 2 + 170 and height / 2 <= mouse[1] <= height / 2 + 40:
                bg_theme = 'Day Theme'
                day_theme = True
                night_theme = False
            elif width / 4 - 50 <= mouse[0] <= width / 4 + 120 and height / 2 <= mouse[1] <= height / 2 + 40:
                bg_theme = 'Night Theme'
                day_theme = False
                night_theme = True
            elif width / 10 <= mouse[0] <= width / 10 + 140 and height / 2 + 150 <= mouse[1] <= height / 2 + 190:
                bird_color = 'Blue Bird'
                blue_bird = True
                red_bird = False
                yellow_bird = False
            elif width / 10 + 160 <= mouse[0] <= width / 10 + 300 and height / 2 + 150 <= mouse[1] <= height / 2 + 190:
                bird_color = 'Red Bird'
                red_bird = True
                blue_bird = False
                yellow_bird = False
            elif width / 10 + 320 <= mouse[0] <= width / 10 + 460 and height / 2 + 150 <= mouse[1] <= height / 2 + 190:
                bird_color = 'Yellow Bird'
                yellow_bird = True
                blue_bird = False
                red_bird = False
            elif width / 2 <= mouse[0] <= width / 2 + 170 and height / 2 + 300 <= mouse[1] <= height / 2 + 340:
                settings_enabled = True
            elif width / 4 - 50 <= mouse[0] <= width / 4 + 120 and height / 2 + 300 <= mouse[1] <= height / 2 + 340:
                pygame.quit()

    mouse = pygame.mouse.get_pos()
    if not settings_enabled:
        if bg_theme == 'Day Theme':
            background = pygame.image.load('images/background_day.png').convert()
            background = pygame.transform.scale2x(background)
        elif bg_theme == 'Night Theme':
            background = pygame.image.load('images/background_night.png').convert()
            background = pygame.transform.scale2x(background)
        if bird_color == 'Blue Bird':
            bird_down = pygame.transform.scale2x(pygame.image.load('images/bluebird_down.png').convert_alpha())
            bird_mid = pygame.transform.scale2x(pygame.image.load('images/bluebird_mid.png').convert_alpha())
            bird_up = pygame.transform.scale2x(pygame.image.load('images/bluebird_up.png').convert_alpha())
            bird_frames = [bird_down, bird_mid, bird_up]
            bird = pygame.transform.scale2x(pygame.image.load('images/bluebird_mid.png').convert_alpha())
        elif bird_color == 'Red Bird':
            bird_down = pygame.transform.scale2x(pygame.image.load('images/redbird_down.png').convert_alpha())
            bird_mid = pygame.transform.scale2x(pygame.image.load('images/redbird_mid.png').convert_alpha())
            bird_up = pygame.transform.scale2x(pygame.image.load('images/redbird_up.png').convert_alpha())
            bird_frames = [bird_down, bird_mid, bird_up]
            bird = pygame.transform.scale2x(pygame.image.load('images/redbird_mid.png').convert_alpha())
        elif bird_color == 'Yellow Bird':
            bird_down = pygame.transform.scale2x(pygame.image.load('images/yellowbird_down.png').convert_alpha())
            bird_mid = pygame.transform.scale2x(pygame.image.load('images/yellowbird_mid.png').convert_alpha())
            bird_up = pygame.transform.scale2x(pygame.image.load('images/yellowbird_up.png').convert_alpha())
            bird_frames = [bird_down, bird_mid, bird_up]
            bird = pygame.transform.scale2x(pygame.image.load('images/yellowbird_mid.png').convert_alpha())
        screen.blit(background, (0, 0))
        screen.blit(bird, (width / 2 - 30, height / 4))

        pygame.draw.rect(screen, color_dark, [width / 2, height / 2, 170, 40])
        pygame.draw.rect(screen, color_dark, [width / 4 - 50, height / 2, 170, 40])
        pygame.draw.rect(screen, color_dark, [width / 10, height / 2 + 150, 140, 40])
        pygame.draw.rect(screen, color_dark, [width / 10 + 160, height / 2 + 150, 140, 40])
        pygame.draw.rect(screen, color_dark, [width / 10 + 320, height / 2 + 150, 140, 40])
        pygame.draw.rect(screen, color_dark, [width / 2, height / 2 + 300, 170, 40])
        pygame.draw.rect(screen, color_dark, [width / 4 - 50, height / 2 + 300, 170, 40])

        if day_theme:
            pygame.draw.rect(screen, selected_color, [width / 2, height / 2, 170, 40])
        elif night_theme:
            pygame.draw.rect(screen, selected_color, [width / 4 - 50, height / 2, 170, 40])
        if blue_bird:
            pygame.draw.rect(screen, selected_color, [width / 10, height / 2 + 150, 140, 40])
        elif red_bird:
            pygame.draw.rect(screen, selected_color, [width / 10 + 160, height / 2 + 150, 140, 40])
        elif yellow_bird:
            pygame.draw.rect(screen, selected_color, [width / 10 + 320, height / 2 + 150, 140, 40])
        if width / 2 <= mouse[0] <= width / 2 + 170 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 2, height / 2, 170, 40])
        elif width / 4 - 50 <= mouse[0] <= width / 4 + 120 and height / 2 <= mouse[1] <= height / 2 + 40:
            pygame.draw.rect(screen, color_light, [width / 4 - 50, height / 2, 170, 40])

        elif width / 10 <= mouse[0] <= width / 10 + 140 and height / 2 + 150 <= mouse[1] <= height / 2 + 190:
            pygame.draw.rect(screen, color_light, [width / 10, height / 2 + 150, 140, 40])
        elif width / 10 + 160 <= mouse[0] <= width / 10 + 300 and height / 2 + 150 <= mouse[1] <= height / 2 + 190:
            pygame.draw.rect(screen, color_light, [width / 10 + 160, height / 2 + 150, 140, 40])
        elif width / 10 + 320 <= mouse[0] <= width / 10 + 460 and height / 2 + 150 <= mouse[1] <= height / 2 + 190:
            pygame.draw.rect(screen, color_light, [width / 10 + 320, height / 2 + 150, 140, 40])

        elif width / 2 <= mouse[0] <= width / 2 + 170 and height / 2 + 300 <= mouse[1] <= height / 2 + 340:
            pygame.draw.rect(screen, color_light, [width / 2, height / 2 + 300, 170, 40])
        elif width / 4 - 50 <= mouse[0] <= width / 4 + 120 and height / 2 + 300 <= mouse[1] <= height / 2 + 340:
            pygame.draw.rect(screen, color_light, [width / 4 - 50, height / 2 + 300, 170, 40])

        screen.blit(day_bg_text, (width / 2 + 8, height / 2 + 10))
        screen.blit(night_bg_text, (width / 4 - 48, height / 2 + 10))
        screen.blit(bluebird_text, (width / 10 + 30, height / 2 + 160))
        screen.blit(redbird_text, (width / 10 + 195, height / 2 + 160))
        screen.blit(yellowbird_text, (width / 10 + 345, height / 2 + 160))
        screen.blit(exit_text, (width / 4 + 20, height / 2 + 310))
        screen.blit(continue_text, (width / 2 + 50, height / 2 + 310))

    if settings_enabled:
        screen.blit(background, (0, 0))
        if game_active:
            bird_movement += gravity
            bird_rect.centery += bird_movement
            screen.blit(bird_surface, bird_rect)
            game_active = check_collision(pipe_list)
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)
            pipe_score_check()
            show_score('main_game')
        else:
            screen.blit(game_over_surface, game_over_rect)
            high_score = score_update(score, high_score)
            show_score('game_over')
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -576:
            floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
