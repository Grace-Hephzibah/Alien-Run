import pygame
from sys import exit
from random import randint
import os

WIDTH, HEIGHT = 800, 400
FPS = 60
P_VEL = -20
GAME_COLOR = (64, 64, 64)
player_gravity = 0
LAST_SCORE = 0

LAST_GAME_SCORE = 0
ALL_SCORES = [0]
VEL = 6


def obstacle_movement(obstacle_list):  # obstacle_list = (obstacle, obs_code)
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle_rect = obstacle[0]
            obstacle_rect.x -= VEL
            obstacle_code = obstacle[1]

            if obstacle_code == SNAIL_CODE:
                screen.blit(snail_surface, obstacle_rect)
            elif obstacle_code == FLY_CODE:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle[0].x > -100]
        return obstacle_list
    else:
        return []


def display_score():
    current_time = pygame.time.get_ticks()
    game_score = current_time // FPS - LAST_SCORE
    score_surface = test_font.render(f'Score : {game_score}', False, GAME_COLOR)
    score_rect = score_surface.get_rect(topleft=(WIDTH - score_surface.get_width() - 20, 20))
    screen.blit(score_surface, (score_rect.x, score_rect.y))

    return game_score


def intro_scores():
    current_score_surface = test_font.render(f"Current Score : {LAST_GAME_SCORE}", False, GAME_COLOR)
    current_score_rect = current_score_surface.get_rect(
        topleft=(2 * WIDTH / 3, HEIGHT / 2 - 3 * current_score_surface.get_height()))

    max_score_surface = test_font.render(f"Maximum Score : {max(ALL_SCORES)}", False, GAME_COLOR)
    max_score_rect = max_score_surface.get_rect(
        topleft=(2 * WIDTH / 3, HEIGHT / 2 + current_score_surface.get_height()))

    screen.blit(current_score_surface, (current_score_rect.x, current_score_rect.y))
    screen.blit(max_score_surface, (max_score_rect.x, max_score_rect.y))


def collisions(player, obstacles, ALL_SCORES, LAST_GAME_SCORE):
    if obstacles:
        for obstacle in obstacles:
            obstacle_rec = obstacle[0]
            if player.colliderect(obstacle_rec):
                ALL_SCORES.append(LAST_GAME_SCORE)
                return False
    return True


def player_animation():
    global player_surface, player_index

    if player_rect.bottom < SKY_GROUND:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()  # Initiates the pygame module

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Creates a surface
pygame.display.set_caption("Alien Run 💨")

clock = pygame.time.Clock()

try:
    # Sounds
    x = 5/0
    jump_sound = pygame.mixer.Sound(os.path.join('Assets', 'audio', 'jump.mp3'))
    jump_sound.set_volume(0.4)  # Value ranges bw 0 to 1

    bg_sound = pygame.mixer.Sound(os.path.join('Assets', 'audio', 'music.wav'))
    bg_sound.set_volume(0.7)
    bg_sound.play(loops=-1)
except:
    jump_sound = None
    bg_sound = None

# Font
test_font = pygame.font.Font(os.path.join('Assets','font', 'Pixeltype.ttf'), 40)
big_font = pygame.font.Font(os.path.join('Assets','font', 'Pixeltype.ttf'), 60)
# Font type and font size

# State Management
game_active = False

'''
test_surface = pygame.Surface((100, 200))
test_surface.fill('Red') # This helps to fill a color 
'''

# Static Surfaces
# convert() helps for pygame to work with these images more easily
# convert_alpha() helps to better execute the bg of the image
sky_surface = pygame.image.load(os.path.join('Assets', 'graphics','Sky.png')).convert_alpha()
ground_surface = pygame.image.load(os.path.join('Assets', 'graphics', 'ground.png')).convert_alpha()

# Common Values
SKY_GROUND = sky_surface.get_height()
JUMP = 2  # Maximum Number of Jumps
current_jump = 0

# Start Button Like
start_surface = big_font.render("Play Now!", False, GAME_COLOR)
start_rect = start_surface.get_rect(
    topleft=(WIDTH / 2 - 2 * start_surface.get_width(), HEIGHT / 2 - start_surface.get_height()))

# Player Surface
player_walk1 = pygame.image.load(os.path.join('Assets', 'graphics', 'Player', 'player_walk_1.png')).convert_alpha()
player_walk2 = pygame.image.load(os.path.join('Assets', 'graphics', 'Player', 'player_walk_2.png')).convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load(os.path.join('Assets', 'graphics', 'Player', 'jump.png'))

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(topleft=(80, SKY_GROUND - player_surface.get_height()))

# Obstacles
# Snail Surface
snail_frame1 = pygame.image.load(os.path.join('Assets', 'graphics', 'snail', 'snail1.png')).convert_alpha()
snail_frame2 = pygame.image.load(os.path.join('Assets', 'graphics', 'snail', 'snail2.png')).convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_frame_index = 0
SNAIL_CODE = 1
snail_surface = snail_frames[snail_frame_index]

# Fly
fly_frame1 = pygame.image.load(os.path.join('Assets', 'graphics', 'Fly', 'Fly1.png')).convert_alpha()
fly_frame2 = pygame.image.load(os.path.join('Assets', 'graphics', 'Fly', 'Fly2.png')).convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
FLY_CODE = 2
fly_surface = fly_frames[fly_frame_index]

# Obstacle Work
obstacle_rect_list = []

# Timer
OBSTACLE_TIME = 1500
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, OBSTACLE_TIME)

SNAIL_TIME = 500
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, SNAIL_TIME)

FLY_TIME = 200
fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, FLY_TIME)

while True:  # Here the game runs continuously

    for event in pygame.event.get():  # Checks for the events
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # terminates the code and shuts down without further execution

        if game_active:  # Game Works
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and current_jump < JUMP:
                    player_gravity = P_VEL
                    current_jump += 1
                    try:
                        jump_sound.play()
                    except:
                        pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and current_jump < JUMP:
                    player_gravity = P_VEL
                    current_jump += 1
                    try:
                        jump_sound.play()
                    except:
                        pass

        else:  # Intro Page
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    game_active = 1
                    LAST_SCORE = pygame.time.get_ticks() // FPS

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = 1
                    LAST_SCORE = pygame.time.get_ticks() // FPS

        if game_active:
            if event.type == obstacle_timer:

                snail_rect = snail_surface.get_rect(
                    topleft=(randint(WIDTH + WIDTH // 4, WIDTH + WIDTH // 2), SKY_GROUND - snail_surface.get_height()))

                fly_rect = fly_surface.get_rect(
                    topleft=(
                        randint(WIDTH + WIDTH // 4, WIDTH + WIDTH // 2), SKY_GROUND - 2 * player_surface.get_height()))

                if event.type == obstacle_timer:
                    obstacle_code = randint(0, 2)

                    if obstacle_code == 1:
                        obstacle_rect_list.append((snail_rect, SNAIL_CODE))
                    else:
                        obstacle_rect_list.append((fly_rect, FLY_CODE))

            if event.type == snail_animation_timer:
                snail_frame_index = (snail_frame_index + 1) % len(snail_frames)
                snail_surface = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                fly_frame_index = (fly_frame_index + 1) % len(fly_frames)
                fly_surface = fly_frames[fly_frame_index]

    # Blit BG no matter what
    screen.blit(sky_surface, (0, 0))  # Block Image Transfer
    screen.blit(ground_surface, (0, SKY_GROUND))

    if game_active:  # Game Screen
        LAST_GAME_SCORE = display_score()

        # Player Movement
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= SKY_GROUND:
            player_rect.bottom = SKY_GROUND
            current_jump = 0

        player_animation()
        screen.blit(player_surface, player_rect)

        # Obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list, ALL_SCORES, LAST_GAME_SCORE)


    else:  # Intro Screen
        screen.blit(start_surface, (start_rect.x, start_rect.y))
        intro_scores()
        obstacle_rect_list.clear()
        player_rect.topleft = (80, SKY_GROUND - player_surface.get_height())
        player_gravity = 0

    # Display Update
    pygame.display.update()

    clock.tick(FPS)  # Controls the Frames Per Second
    # This is the maximum FPS
    # But to set the minimum FPS there is a bigger code
