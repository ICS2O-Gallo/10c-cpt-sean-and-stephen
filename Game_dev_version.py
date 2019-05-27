import arcade as arc
import random

# Implement realistic gravity
# Fix bug that makes player able to jump for extended periods of time using the platforms
# Add "death" feature when player leaves viewport

# GLOBAL VARIABLES -----------------------------------------------------------------------------------------------------
# Screen variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Laser Platform"

# The center x-value of the play area
PLAY_AREA_CENTER = 2700

# "Floating" title text
title_y = 680
title_speed = 0.2

# Button variables
button_transparency = 1
button_pos = [300, 200]

# Variables for transition from menu into game
x_transition = 0
transition_state = False
screen_tracker = 300
transition_speed = 20

# Platform variables
plat_speed_list = []
plat_list_x = []
plat_list_y = []
plat_quantity = 20

# Player variables
Player_pos = [2700, 100]
Player_speed = 5
jumpDuration = 0
jumpCap = 15
jumpSpeed = 45
acceleration = 1
airTime = 0

# Variables for ground/platform collision
onPlatform = False
onGround = False

# Keypress variables
W = False
A = False
S = False
D = False

view_mode = input("Viewmode: play, title, full > ")


# UPDATE ---------------------------------------------------------------------------------------------------------------
def update_everything(delta_time):
    title_screen()
    # transition(transition_state)
    create_platform()
    ground()
    player()

    if view_mode == "full":
        arc.set_viewport(0, 3000, 0, 3000)

    elif view_mode == "play":
        arc.set_viewport(2400, 3000, 0, 800)

    elif view_mode == "title":
        arc.set_viewport(0, 600, 0, 800)


# TITLE SCREEN LOGIC ---------------------------------------------------------------------------------------------------
def title_screen():
    global button_pos, button_transparency, title_y, title_speed, x_transition, screen_tracker, transition_state

    arc.start_render()
    # Loading the textures for screen
    background = arc.load_texture("background.png", 0, 0, 320, 256)
    title = arc.load_texture("title_text.png", 0, 0, 1225, 459)
    button = arc.load_texture("label.png", 0, 36, 48, 12)

    # Putting textures onto screen
    arc.draw_texture_rectangle(300, 450, 600, 900, background)

    for multi in range(1, 5):
        arc.draw_texture_rectangle(300 + 600 * multi, 450, 600, 900, background)

    for multi2 in range(1, 10):
        arc.draw_texture_rectangle(2700, 800 * multi2 + 400, 600, 900, background)

    arc.draw_texture_rectangle(315, title_y, 400, 180, title)
    title_y += title_speed

    if title_y >= 690:
        title_speed = -title_speed

    elif title_y <= 670:
        title_speed = -title_speed

    arc.draw_texture_rectangle(button_pos[0], button_pos[1], 200, 100, button, 0, button_transparency)
    arc.draw_text("Play", 280, 192, arc.color.WHITE, 20, font_name="Calibri", bold=True, italic=True)


# TRANSITION -----------------------------------------------------------------------------------------------------------
'''def transition(state):
    global transition_speed, screen_tracker
    if state:
        arc.set_viewport(screen_tracker - 300, screen_tracker + 300, 0, 800)
        screen_tracker += transition_speed

        if screen_tracker == PLAY_AREA_CENTER:
            transition_speed = 0

    # When transition reaches center of play area,
    # Viewport tracks player
    if screen_tracker == PLAY_AREA_CENTER:
        arc.set_viewport(2400, 3000, Player_pos[1] - 115, Player_pos[1] + 670)'''


# KEY/MOUSE PRESS/RELEASE ----------------------------------------------------------------------------------------------
def player_press(symbol, modifiers):
    global W, A, D

    if symbol == arc.key.D:
        D = True

    elif symbol == arc.key.A:
        A = True

    elif symbol == arc.key.W:
        W = True


def player_release(symbol, modifiers):
    global W, A, D

    if symbol == arc.key.D:
        D = False

    elif symbol == arc.key.A:
        A = False

    elif symbol == arc.key.W:
        W = False


def mouse_detection(x, y, dx, dy):
    global button_pos, button_transparency, button_area

    # Detects when mouse is over the button
    button_area = button_pos[0] - 100 <= x <= button_pos[0] + 100 and button_pos[1] - 50 <= y <= button_pos[1] + 50

    if button_area:
        button_transparency = 0.5
    else:
        button_transparency = 1


def button_click(x, y, button, modifiers):
    global button_area, transition_state

    # Initializing game
    if button_area and button == arc.MOUSE_BUTTON_LEFT and screen_tracker == 300:
        transition_state = True


# PLAYER ---------------------------------------------------------------------------------------------------------------
def player():
    global W, A, S, D
    global screen_tracker, jumpDuration, onPlatform, onGround, airTime

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
    cube = arc.load_texture("player.png", 0, 0, 64, 64)
    arc.draw_texture_rectangle(Player_pos[0], Player_pos[1], 50, 50, cube)

    # All collision (sides of screen, ground, platforms)
    for i in range(plat_quantity):
        if Player_pos[1] <= 125:
            Player_pos[1] = 125
            onGround = True

        if Player_pos[0] <= 2425:
            Player_pos[0] = 2425

        if Player_pos[0] >= 2975:
            Player_pos[0] = 2975

        # The range of a platform that a player can "land" on
        platform_x = plat_list_x[i] - 90 < Player_pos[0] < plat_list_x[i] + 90
        platform_y = plat_list_y[i] - 50 <= Player_pos[1] <= plat_list_y[i] + 37

        if platform_x and platform_y:
            Player_pos[1] = plat_list_y[i] + 37
            Player_pos[0] += plat_speed_list[i]
            onPlatform = True

    # GRAVITY
    displacement = ((1 / 2) * acceleration * (airTime * 10))
    if displacement > (Player_pos[1] - 125):
        displacement = (Player_pos[1] - 125)
    if onPlatform is False or onGround is False:
        Player_pos[1] = Player_pos[1] - displacement
    print("onPlat:", str(onPlatform), "|", "onGround:", str(onGround), "|", "displacement:", displacement, "|",
          "airTime:", airTime)


# PLATFORM / GROUND ----------------------------------------------------------------------------------------------------
def create_platform():
    platform = arc.load_texture("platform.png", 0, 0, 28, 11)

    for i in range(plat_quantity):
        plat_list_y.append(i * 300 + 400)
        plat_list_x.append(random.randint(2500, 2900))
        plat_speed_list.append(random.choice([-2, 2, -3, 3]))
        arc.draw_texture_rectangle(plat_list_x[i], plat_list_y[i], 150, 30, platform)

        plat_list_x[i] += plat_speed_list[i]

        if plat_list_x[i] > 2925:
            plat_speed_list[i] = -plat_speed_list[i]

        elif plat_list_x[i] < 2475:
            plat_speed_list[i] = -plat_speed_list[i]

        arc.draw_texture_rectangle(plat_list_x[i], plat_list_y[i], 150, 30, platform)


def ground():
    # Drawing ground
    floor = arc.load_texture("floor.jpg", 0, 0, 1920, 480)
    arc.draw_texture_rectangle(2700, 50, 600, 100, floor)


# SCREEN ---------------------------------------------------------------------------------------------------------------
def screen_setup():
    arc.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arc.set_background_color(arc.color.SKY_BLUE)

    arc.schedule(update_everything, 1 / 60)

    window = arc.get_window()
    window.on_mouse_motion = mouse_detection
    window.on_mouse_press = button_click
    window.on_key_press = player_press
    window.on_key_release = player_release

    title_screen()
    arc.run()


screen_setup()