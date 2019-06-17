from arcade import *

"""
An arcade platforming game

- Stephen Lee, Sean Xie

"""

# GLOBAL VARIABLES ------------------------------------------------------------
# Screen variables
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Laser & Platforms"

# The center x-value of the play area
PLAY_AREA_CENTER = 2700

# "Floating" title Textures
title_y = 680
title_speed = 0.2

# Button variables
button_transparency = [255, 255, 255, 255]
button_pos = [
    [300, 200],
    [3900, 200],
    [300, 100],
    [500, 1650]
]
# The mouse click positions are different from the draw positions.
# The mouse "lives" inside 0 <= x <= 600 and 0 <= y <= 800
mouse_button_pos = [
    [300, 200],
    [300, 200],
    [300, 100],
    [500, 750]
]

# Variables for transition from menu into game
transition_state = False
screen_tracker = 300
transition_speed = 20
instruction_press = -1
in_instruct_screen = False

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
acceleration = 1.75
airTime = 0
score = 0
life = 490

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

# Laser variables
laser_x = 2400
laser_speed = 2
laser_frequency = 101
laser_state = False
laser_fire_timer = 0
laser_wait_timer = 0
currentlyFiring = False


# UPDATE ----------------------------------------------------------------------
def update_everything(delta_time):
    global upProgress, upSpeed, frameCount_gameStart, score
    screens()
    transition()

    if screen_tracker == PLAY_AREA_CENTER:
        move_platform()

    ground()
    player()
    player_score()
    player_life()

    if timerCount == 60:
        score += 1
        laser()

        if frameCount_gameStart % 500 == 0:
            upSpeed += 2

        upProgress += upSpeed

    frameCount_gameStart += 1


# SCREENS ---------------------------------------------------------------------
def screens():
    global button_pos, button_transparency, title_y, title_speed
    global screen_tracker, transition_state, instruction_press

    start_render()
    # Loading the textures for screen
    background = load_texture("Textures/background.png", 0, 0, 2053, 1366)
    title = load_texture("Textures/title_text.png", 0, 0, 1225, 459)
    button = load_texture("Textures/label.png", 0, 36, 48, 12)
    game_over = load_texture("Textures/game_over.png", 0, 0, 1074, 144)
    game_over_back = load_texture("Textures/game_over_back.png", 0, 0, 320,
                                  256)

    # Instructions
    instruct_back = load_texture("Textures/space.jpg", 0, 0, 320, 480)
    draw_texture_rectangle(300, 1300, 600, 800, instruct_back)
    draw_text("1. Press W to jump.", 50, 1600, color.WHITE, 25,
              font_name="calibri")
    draw_text("2. Press A to go left, D to go right.", 50, 1450,
              color.WHITE, 25, font_name="calibri")
    draw_text("3. You can jump through the platforms.", 50, 1300,
              color.WHITE, 25, font_name="calibri")
    draw_text("4. Stay in the screen and dodge the lasers", 50, 1150,
              color.WHITE, 25, font_name="calibri")
    draw_text("to survive!", 50, 1115, color.WHITE, 25,
              font_name="calibri")
    draw_text("5. Keep playing to improve your score!", 50, 975, color.WHITE,
              25, font_name="calibri")


    # Putting textures onto screen
    draw_texture_rectangle(300, 450, 600, 900, background)
    draw_texture_rectangle(3900, 450, 600, 900, game_over_back)

    # Looping background textures during game play
    for multi in range(1, 5):
        draw_texture_rectangle(300 + 600 * multi, 450, 600, 900, background)

    for multi2 in range(1, 10):
        draw_texture_rectangle(2700, 800 * multi2 + 400, 600, 900, background)

    # The "hovering" effect for the title and game over text
    draw_texture_rectangle(315, title_y, 400, 180, title)
    draw_texture_rectangle(3900, title_y, 400, 75, game_over)

    title_y += title_speed

    if title_y >= 690:
        title_speed = -title_speed

    elif title_y <= 670:
        title_speed = -title_speed

    # Drawing the buttons. Can't use a "for" loop. It won't work
    draw_texture_rectangle(button_pos[0][0],
                           button_pos[0][1], 200, 100, button, 0,
                           button_transparency[0])
    draw_texture_rectangle(button_pos[1][0],
                           button_pos[1][1], 200, 100, button, 0,
                           button_transparency[1])
    draw_texture_rectangle(button_pos[2][0],
                           button_pos[2][1], 200, 100, button, 0,
                           button_transparency[2])
    draw_texture_rectangle(button_pos[3][0],
                           button_pos[3][1], 200, 100, button, 0,
                           button_transparency[3])

    draw_text("Play", 280, 192, color.WHITE, 20, font_name="calibri",
              bold=True, italic=True)
    draw_text("Instructions", 237, 92, color.WHITE, 20,
              font_name="calibri",
              bold=True, italic=True)
    draw_text("Restart", 3860, 192, color.WHITE, 20, font_name="calibri",
              bold=True, italic=True)
    draw_text("Back", 478, 1640, color.WHITE, 20, font_name="calibri",
              bold=True, italic=True)

    # Final Score
    draw_text(f"FINAL SCORE: {score}", 3800, 300, color.WHITE, 25,
              font_name="calibri")


# Instructions Screen
def instruction_screen():
    global in_instruct_screen
    set_viewport(0, 600, 900, 1700)
    in_instruct_screen = True


# Countdown timer in game
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
def transition():
    global transition_speed, screen_tracker, frameCount_playStart
    if transition_state:
        set_viewport(screen_tracker - 300, screen_tracker + 300, 0, 800)

        screen_tracker += transition_speed

        if screen_tracker == PLAY_AREA_CENTER:
            frameCount_playStart += 1
            transition_speed = 0
            timer()
            if timerCount == 60:
                level_progression()


# Making the viewport move up as game progresses
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
    # Only left and right key presses are required as jumping only ends
    # (w is released) when floor is touched
    global A, D

    if symbol == key.D or symbol == key.RIGHT:
        D = False

    elif symbol == key.A or symbol == key.LEFT:
        A = False


def mouse_detection(x, y, dx, dy):
    global button_pos, button_transparency, Player_pos, button_area_list

    # Detects when mouse is over the button.
    # Can't use a "for" loop. Mouse detection won't work
    start_button_area = (
            mouse_button_pos[0][0] - 100 <= x <=
            mouse_button_pos[0][0] + 100 and
            mouse_button_pos[0][1] - 50 <= y <=
            mouse_button_pos[0][1] + 50
    )

    restart_button_area = (
            mouse_button_pos[1][0] - 100 <= x <=
            mouse_button_pos[1][0] + 100 and
            mouse_button_pos[1][1] - 50 <= y <=
            mouse_button_pos[1][1] + 50
    )

    instruct_button_area = (
            mouse_button_pos[2][0] - 100 <= x <=
            mouse_button_pos[2][0] + 100 and
            mouse_button_pos[2][1] - 50 <= y <=
            mouse_button_pos[2][1] + 50
    )

    back_button_area = (
            mouse_button_pos[3][0] - 100 <= x <=
            mouse_button_pos[3][0] + 100 and
            mouse_button_pos[3][1] - 50 <= y <=
            mouse_button_pos[3][1] + 50
    )

    # For easier reference to button areas
    button_area_list = [
        start_button_area,
        restart_button_area,
        instruct_button_area,
        back_button_area
    ]

    # Change to 50% transparency when moused over
    if button_area_list[0]:
        button_transparency[0] = 127.5
    else:
        button_transparency[0] = 255

    if button_area_list[1]:
        button_transparency[1] = 127.5
    else:
        button_transparency[1] = 255

    if button_area_list[2]:
        button_transparency[2] = 127.5
    else:
        button_transparency[2] = 255

    if button_area_list[3]:
        button_transparency[3] = 127.5
    else:
        button_transparency[3] = 255


# Detect when a button is clicked
def button_click(x, y, button, modifiers):
    global button_area_list, instruction_press, transition_state, \
        in_instruct_screen

    # Start button clicked
    if button_area_list[0] and button == MOUSE_BUTTON_LEFT \
            and screen_tracker == 300 and not in_instruct_screen:
        transition_state = True

    # Reset button clicked
    elif button_area_list[1] and button == MOUSE_BUTTON_LEFT \
            and screen_tracker == 3300:
        reset()

    # Instruction pressed
    elif button_area_list[2] and button == MOUSE_BUTTON_LEFT \
            and screen_tracker == 300:
        instruction_screen()

    # Back button pressed
    elif button_area_list[3] and button == MOUSE_BUTTON_LEFT \
            and screen_tracker == 300:
        in_instruct_screen = False
        reset()


# PLAYER ----------------------------------------------------------------------
def player():
    global W, A, S, D
    global screen_tracker, jumpDuration, onPlatform, onGround, airTime, \
        acceleration

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

    # The amount of time not spent on platform our ground
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
                W = False

            if Player_pos[0] <= 2425:
                Player_pos[0] = 2425

            if Player_pos[0] >= 2975:
                Player_pos[0] = 2975

            # The range of a platform that a player can "touch"
            platform_x = (
                    plat_list_x[i] - 90 <
                    Player_pos[0]
                    < plat_list_x[i] + 90
            )

            platform_y_top = (
                    plat_list_y[i] <=
                    Player_pos[1]
                    <= plat_list_y[i] + 38
            )

            platform_y_bottom = (
                    plat_list_y[i] >=
                    Player_pos[1]
                    >= plat_list_y[i] - 38
            )

            # When player is on a platform,
            # they gain the x-value of the platform
            # "W" is also released to complete a full jump
            if platform_x and platform_y_top:
                Player_pos[1] = plat_list_y[i] + 38
                Player_pos[0] += plat_speed_list[i]
                onPlatform = True
                W = False

            # Hitting bottom of platform
            elif platform_x and platform_y_bottom:
                Player_pos[1] = plat_list_y[i] - 50
    # GRAVITY
    # Modified displacement equation to fit game
    displacement = 0.5 * acceleration * airTime

    # Player falls onto platform and ground
    if not onPlatform or not onGround:
        Player_pos[1] -= displacement

    if Player_pos[1] - displacement <= 125:
        Player_pos[1] = 125


# Score on death screen
def player_score():
    draw_text(f"Score: {score}", 2420, upProgress + 750, color.BLACK, 20)


# Logic for player life system
def player_life():
    draw_rectangle_outline(PLAY_AREA_CENTER,
                           upProgress + 10, 500, 10,
                           color.BLACK)

    draw_line(2455, upProgress + 10, 2455 + life, upProgress + 10, color.RED,
              5)

    # Death by laser
    if life <= 0:
        death()


# Function for dying in game
def death():
    global jumpSpeed, transition_state, screen_tracker, timerCount
    set_viewport(3600, 4200, 0, 800)
    # Disables jumping back into game
    jumpSpeed = 0
    transition_state = False
    screen_tracker += 600
    # Stop score increase
    timerCount = 0


# Resetting all game variables for new game
def reset():
    global screen_tracker, upProgress, upSpeed, frameCount_playStart
    global frameCount_gameStart, transition_speed, jumpSpeed, score, life

    # resetting
    screen_tracker = 300
    transition_speed = 20

    score = 0
    upSpeed = 0.5
    upProgress = 2
    frameCount_gameStart = 0
    frameCount_playStart = 0
    jumpSpeed = 25
    life = 490

    remove_platform()
    create_platform()
    set_viewport(0, 600, 0, 800)


# LASER -----------------------------------------------------------------------
warning = load_texture("Textures/warning.png", 0, 0, 400, 400)


def laser():
    global laser_x, laser_speed, laser_state, laser_fire_timer, \
        laser_wait_timer, currentlyFiring, life

    def fire_laser():
        global life
        draw_line(laser_x, upProgress, laser_x, upProgress + 800, color.RED, 4)

        # Collision with player
        if laser_x - 5 <= Player_pos[0] <= laser_x + 5:
            life -= 10

    # How long the laser has been firing
    laser_fire_timer += 1
    if laser_fire_timer <= laser_frequency:
        fire_laser()
        currentlyFiring = True

    else:
        # A pause timer to ensure that the laser is not constantly active
        laser_wait_timer += 1
        if laser_wait_timer == laser_frequency:
            laser_wait_timer = 0
            laser_fire_timer = 0
            currentlyFiring = False

    # Laser does not leave play area
    laser_x += laser_speed

    if laser_x >= 3000:
        laser_speed = -laser_speed

    if laser_x <= 2400:
        laser_speed = -laser_speed

    draw_texture_rectangle(laser_x, upProgress + 750,
                           50, 50, warning)


# PLATFORM / GROUND -----------------------------------------------------------
def create_platform():
    global upProgress

    for i in range(plat_quantity):
        # Creating and appending platforms coordinates and speeds to their
        # respective lists
        plat_list_y.append(i * 300)
        plat_list_x.append(random.randint(2500, 2900))
        plat_speed_list.append(random.choice([-2, 2, -3, 3]))


def move_platform():
    plat = load_texture("Textures/platform2.png", 0, 0, 195, 35)
    for i in range(plat_quantity):
        # Moving the platforms
        # They don't leave the play area
        plat_list_x[i] += plat_speed_list[i]

        if plat_list_x[i] > 2925:
            plat_speed_list[i] = -plat_speed_list[i]

        elif plat_list_x[i] < 2475:
            plat_speed_list[i] = -plat_speed_list[i]

        bot = upProgress
        top = 800 + upProgress

        # If a platform moves out of the screen, move it to the top
        # This method is used to avoid unneeded platforms
        if plat_list_y[i] < bot:
            plat_list_y[i] = top
            plat_list_x[i] = random.randint(2500, 2900)

        draw_texture_rectangle(plat_list_x[i], plat_list_y[i], 150, 30,
                               plat)


# When a player dies, the platforms are removed
# Later, they are created again through create_platform()
def remove_platform():
    for i in range(plat_quantity - 1, -1, -1):
        plat_list_y.pop(i)
        plat_list_x.pop(i)


def ground():
    # Drawing ground
    floor = load_texture("Textures/floor.jpg", 0, 0, 1920, 480)
    draw_texture_rectangle(2700, 50, 600, 100, floor)


# SCREEN ----------------------------------------------------------------------
# Setting up the window
def window_setup():
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


# Don't really know what this is for but it helps
if __name__ == '__main__':
    window_setup()
