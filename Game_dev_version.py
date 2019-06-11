import math
import random
from arcade import *

# Fix bug that makes player able to jump for extended periods of time using the
# platforms
# Add "death" feature when player leaves viewport

# GLOBAL VARIABLES ------------------------------------------------------------
# Screen variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Laser Platform"

# The center x-value of the play area
PLAY_AREA_CENTER = 2700

# "Floating" title Textures
title_y = 680
title_speed = 0.2

# Button variables
button_transparency = [1, 1, 1]
button_pos = [300, 200, 300, 200, 300, 100]

# Variables for transition from menu into game
x_transition = 0
transition_state = False
screen_tracker = 300
transition_speed = 20

# Platform variables
plat_speed_list = []
plat_list_x = []
plat_list_y = []
plat_quantity = 5

# Player variables
Player_pos = [2700, 100]
Player_speed = 5
Player_size = 50
Player_score = 0
jumpDuration = 0
jumpCap = 15
jumpSpeed = 25
acceleration = 1.5
airTime = 0
score = 0

# Variables for ground/platform collision
onPlatform = False
onGround = False

# Game progression variables
upProgress = 2
upSpeed = 0.5
frameCount_gameStart = 0
frameCount_playStart = 0
timerCount = 0

# Keypress variables
W = False
A = False
S = False
D = False

# Rocket variables
laserX = 3001
laser_speed = -5
launchState = -1
frequency = 100
rocket_y = 5
rocket_speed = 5


# UPDATE ----------------------------------------------------------------------
def update_everything(delta_time):
    global upProgress, upSpeed, frameCount_gameStart, score, rocket_y
    screens()
    transition(transition_state)
    if screen_tracker == PLAY_AREA_CENTER:
        move_platform()
    ground()
    player()
    player_score()

    if timerCount == 60:
        draw_laser()
        laser_movement()

        if launchState == 1:
            rocket_y += rocket_speed
            shoot_rocket(rocket_y)

        else:
            rocket_y = -10

        score += 1

        if frameCount_gameStart % 500 == 0:
            upSpeed *= 1.5

        upProgress += upSpeed

    frameCount_gameStart += 1


# SCREENS ---------------------------------------------------------------------
def screens():
    global button_pos, button_transparency, title_y, title_speed, x_transition \
        , screen_tracker, transition_state

    start_render()
    # Loading the textures for screen
    background = load_texture("Textures/background.png", 0, 0, 320, 256)
    title = load_texture("Textures/title_text.png", 0, 0, 1225, 459)
    button = load_texture("Textures/label.png", 0, 36, 48, 12)
    game_over = load_texture("Textures/game_over.png", 0, 0, 1074, 144)
    game_over_back = load_texture("Textures/game_over_back.png", 0, 0, 320,
                                  256)

    # Putting textures onto screen
    draw_texture_rectangle(300, 450, 600, 900, background)
    draw_texture_rectangle(3900, 450, 600, 900, game_over_back)

    for multi in range(1, 5):
        draw_texture_rectangle(300 + 600 * multi, 450, 600, 900, background)

    for multi2 in range(1, 10):
        draw_texture_rectangle(2700, 800 * multi2 + 400, 600, 900, background)

    draw_texture_rectangle(315, title_y, 400, 180, title)
    draw_texture_rectangle(3900, title_y, 400, 75, game_over)

    title_y += title_speed

    if title_y >= 690:
        title_speed = -title_speed

    elif title_y <= 670:
        title_speed = -title_speed

    draw_texture_rectangle(button_pos[0], button_pos[1], 200, 100, button, 0,
                           button_transparency[0])
    draw_texture_rectangle(button_pos[4], button_pos[5], 200, 100, button, 0,
                           button_transparency[2])
    draw_texture_rectangle(3900, 200, 200, 100, button, 0,
                           button_transparency[1])
    draw_text("Play", 280, 192, color.WHITE, 20, font_name="Calibri",
              bold=True, italic=True)
    draw_text("Instructions", 237, 92, color.WHITE, 20, font_name="Calibri",
              bold=True, italic=True)
    draw_text("Restart", 3860, 192, color.WHITE, 20, font_name="Calibri",
              bold=True, italic=True)


def timer():
    global timerCount
    one = load_texture("Textures/1.png", 0, 0, 382, 432)
    two = load_texture("Textures/2.png", 0, 0, 377, 425)
    three = load_texture("Textures/3.png", 0, 0, 386, 435)

    if 60 <= frameCount_playStart < 120:
        draw_texture_rectangle(2700, 400, 50 * timerCount, 60 * timerCount,
                               three)
        if timerCount < 1:
            timerCount += 1

    elif 120 <= frameCount_playStart < 180:
        draw_texture_rectangle(2700, 400, 50 * timerCount, 60 * timerCount,
                               two)
        if timerCount < 2:
            timerCount += 1

    elif 180 <= frameCount_playStart < 240:
        draw_texture_rectangle(2700, 400, 50 * timerCount, 60 * timerCount,
                               one)
        if timerCount < 60:
            timerCount += 1


# SCREENS/VIEWPORTS -----------------------------------------------------------
def transition(state):
    global transition_speed, screen_tracker, frameCount_playStart
    if state:
        set_viewport(screen_tracker - 300, screen_tracker + 300, 0, 800)
        screen_tracker += transition_speed

        if screen_tracker == PLAY_AREA_CENTER:
            frameCount_playStart += 1
            transition_speed = 0
            timer()
            if timerCount == 60:
                level_progression()


def level_progression():
    global lower, upper
    lower = upProgress
    upper = 800 + upProgress
    set_viewport(2400, 3000, lower, upper)

    if Player_pos[1] <= lower:
        death()


# KEY/MOUSE PRESS/RELEASE -----------------------------------------------------
def player_press(symbol, modifiers):
    global W, A, D

    if symbol == key.D or symbol == key.RIGHT:
        D = True

    elif symbol == key.A or symbol == key.LEFT:
        A = True

    elif symbol == key.W or symbol == key.UP:
        W = True


def player_release(symbol, modifiers):
    global W, A, D

    if symbol == key.D or symbol == key.RIGHT:
        D = False

    elif symbol == key.A or symbol == key.LEFT:
        A = False

    elif symbol == key.W or symbol == key.UP:
        W = False


def mouse_detection(x, y, dx, dy):
    global button_pos, button_transparency, start_button_area, \
        restart_button_area, instruct_button_area, Player_pos

    # Detects when mouse is over the button
    start_button_area = button_pos[0] - 100 <= x <= button_pos[0] + 100 and \
                        button_pos[1] - 50 <= y <= button_pos[1] + 50
    restart_button_area = button_pos[2] - 100 <= x <= button_pos[2] + 100 and \
                          button_pos[3] - 50 <= y <= button_pos[3] + 50
    instruct_button_area = button_pos[4] - 100 <= x <= button_pos[4] + 100 \
                           and button_pos[5] - 50 <= y <= button_pos[5] + 50

    # List for "for" loop
    button_area_list = [start_button_area, restart_button_area,
                        instruct_button_area]

    for i in range(len(button_transparency)):
        if button_area_list[i]:
            button_transparency[i] = 0.5

        else:
            button_transparency[i] = 1


def button_click(x, y, button, modifiers):
    global start_button_area, restart_button_area, instruct_button_area, transition_state, \
        screen_tracker

    if not transition_state:
        # Initializing game
        if start_button_area and button == MOUSE_BUTTON_LEFT and \
                screen_tracker == 300:
            transition_state = True
        elif restart_button_area and button == MOUSE_BUTTON_LEFT:
            reset()
        elif instruct_button_area:
            pass
            # instruction_screen()


# PLAYER ----------------------------------------------------------------------
def player():
    global W, A, S, D
    global screen_tracker, jumpDuration, onPlatform, onGround, airTime, \
        displacement

    # MOVEMENT
    if D is True:
        Player_pos[0] += Player_speed

    if A is True:
        Player_pos[0] -= Player_speed

    # JUMP
    # player can only jump again if they touch the ground or platform
    if W is True and jumpDuration <= jumpCap:
        Player_pos[1] += jumpSpeed
        jumpDuration += 1

    if onPlatform or onGround:
        jumpDuration = 0
        onPlatform = False
        onGround = False
        airTime = -1

    airTime += 1

    # Drawing player
    cube = load_texture("Textures/player.png", 0, 0, 64, 64)
    draw_texture_rectangle(Player_pos[0], Player_pos[1], Player_size,
                           Player_size, cube)
    # All collision (sides of screen, ground, platforms)
    if screen_tracker == PLAY_AREA_CENTER:
        for i in range(plat_quantity):
            if Player_pos[1] <= 125:
                Player_pos[1] = 125
                onGround = True

            if Player_pos[0] <= 2425:
                Player_pos[0] = 2425

            if Player_pos[0] >= 2975:
                Player_pos[0] = 2975

            # The range of a platform that a player can "land" on
            platform_x = plat_list_x[i] - 90 < Player_pos[0] < plat_list_x[
                i] + 90
            platform_y_top = plat_list_y[i] <= Player_pos[1] \
                             <= plat_list_y[i] + 38

            platform_y_bottom = plat_list_y[i] >= Player_pos[1] \
                                >= plat_list_y[i] - 38

            if platform_x and platform_y_top:
                Player_pos[1] = plat_list_y[i] + 38
                Player_pos[0] += plat_speed_list[i]
                onPlatform = True

            elif platform_x and platform_y_bottom:
                Player_pos[1] = plat_list_y[i] - 38

    # GRAVITY
    displacement = ((1 / 2) * acceleration * airTime)

    if displacement > (Player_pos[1] - 125):
        displacement = (Player_pos[1] - 125)

    if onPlatform is False or onGround is False:
        Player_pos[1] = Player_pos[1] - displacement

    '''print("onPlat:", str(onPlatform), "|", "onGround:", str(onGround), "|",
          "displacement:", displacement, "|",
          "airTime:", airTime, "|", "Frame:", frameCount_playStart, "|",
          "upSpeed:", upSpeed, "|", "upProgress:",
          upProgress)'''


def player_score():
    draw_text(f"Score: {score}", 2420, upProgress + 750, color.BLACK, 20)


def death():
    global jumpSpeed, screen_tracker, laserAngles, transition_state
    set_viewport(3600, 4200, 0, 800)
    # Disables jumping back into game
    jumpSpeed = 0
    transition_state = False


def reset():
    global screen_tracker, upProgress, upSpeed, frameCount_playStart, \
        frameCount_gameStart, timerCount, x_transition, \
        transition_state, transition_speed, jumpSpeed, score

    # resetting many things ;)
    x_transition = 0
    transition_state = False
    screen_tracker = 300
    transition_speed = 20

    score = 0
    upSpeed = 0.5
    upProgress = 2
    frameCount_gameStart = 0
    frameCount_playStart = 0
    timerCount = 0

    jumpSpeed = 25
    # destroy_platforms()

    remove_platform()
    create_platform()
    set_viewport(0, 600, 0, 800)


# ROCKET ----------------------------------------------------------------------
def draw_laser():
    global lower, upper
    warning = load_texture("Textures/warning.png", 0, 0, 400, 400)

    draw_line(laserX, lower, laserX, upper, color.LASER_LEMON, 2)

    if launchState == 1 and frameCount_playStart % 7 != 0:
        draw_texture_rectangle(laserX, lower + 40, 100, 100, warning)


def shoot_rocket(rocket_y):
    global lower
    rocket = load_texture("Textures/missile.png", 0, 0, 253, 178)
    draw_texture_rectangle(laserX, rocket_y, 100, 50, rocket,
                           90)


def laser_movement():
    global laserX, laser_speed, launchState
    laserX += laser_speed
    if laserX >= PLAY_AREA_CENTER + 300:
        laser_speed = -laser_speed

    elif laserX <= PLAY_AREA_CENTER - 300:
        laser_speed = -laser_speed

    if frameCount_playStart % frequency == 0:
        launchState = -launchState


# PLATFORM / GROUND -----------------------------------------------------------
def create_platform():
    global upProgress

    for i in range(plat_quantity):
        # Creating and appending platforms coordinates and speeds to their
        # respective lists
        print("Creating...")
        print(i)
        plat_list_y.append(i * 300)
        plat_list_x.append(random.randint(2500, 2900))
        plat_speed_list.append(random.choice([-2, 2, -3, 3]))


def move_platform():
    platform = load_texture("Textures/platform2.png", 0, 0, 195, 35)
    for i in range(plat_quantity):
        # Moving the platforms
        plat_list_x[i] += plat_speed_list[i]

        if plat_list_x[i] > 2925:
            plat_speed_list[i] = -plat_speed_list[i]

        elif plat_list_x[i] < 2475:
            plat_speed_list[i] = -plat_speed_list[i]

        bot = upProgress
        top = 800 + upProgress

        if plat_list_y[i] < bot:
            plat_list_y[i] = top
            plat_list_x[i] = random.randint(2500, 2900)

        draw_texture_rectangle(plat_list_x[i], plat_list_y[i], 150, 30,
                               platform)


def remove_platform():
    for i in range(plat_quantity - 1, -1, -1):
        print("Removing...")
        print(i)
        plat_list_y.pop(i)
        plat_list_x.pop(i)


def ground():
    # Drawing ground
    floor = load_texture("Textures/floor.jpg", 0, 0, 1920, 480)
    draw_texture_rectangle(2700, 50, 600, 100, floor)


# SCREEN ----------------------------------------------------------------------
def screen_setup():
    open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    set_background_color(color.SKY_BLUE)

    schedule(update_everything, 1 / 60)
    create_platform()

    window = get_window()
    window.on_mouse_motion = mouse_detection
    window.on_mouse_press = button_click
    window.on_key_press = player_press
    window.on_key_release = player_release

    screens()
    run()


screen_setup()
