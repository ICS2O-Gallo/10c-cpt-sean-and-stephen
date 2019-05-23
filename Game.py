import arcade as arc
import random

# Implement gravity / jumping

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Laser Platform"

GAME = False

button_transparency = 1
button_pos = [300, 200]

y_transition = 0
transition_state = False

plat_speed_list = []
plat_list_x = []
plat_list_y = []
plat_quantity = 20

Player_pos = [2700, 400]
Player_speed = 5
Gravity = 8

on_platform = False


W = False
A = False
S = False
D = False


def update_everything(delta_time):
    global y_transition, transition_state, screen_tracker
    global plat_list_x, plat_speed_list

    screen_tracker = 300
    screen_tracker += y_transition

    title_screen()

    # Transition logic
    if screen_tracker < 2700 and transition_state is True:
        y_transition += 20
        arc.set_viewport(0 + y_transition, 600 + y_transition, 0, 800)

    create_platform()
    ground()
    player()


def title_screen():
    global button_pos, button_transparency

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

    arc.draw_texture_rectangle(315, 680, 400, 180, title)
    arc.draw_texture_rectangle(button_pos[0], button_pos[1], 200, 100, button, 0, button_transparency)
    arc.draw_text("Play", 280, 192, arc.color.WHITE, 20, font_name="Calibri", bold=True, italic=True)


def mouse_detection(x, y, dx, dy):
    global button_pos, button_transparency, button_area

    # Detects when mouse is over the button
    button_area = button_pos[0] - 100 <= x <= button_pos[0] + 100 and button_pos[1] - 50 <= y <= button_pos[1] + 50

    if button_area:
        button_transparency = 0.5
    else:
        button_transparency = 1


def button_click(x, y, button, modifiers):
    global button_area, GAME, transition_state, screen_tracker

    # Initializing game
    if button_area and button == arc.MOUSE_BUTTON_LEFT and screen_tracker == 300:
        GAME = True
        transition_state = True


def create_platform():

    platform = arc.load_texture("platform.png", 0, 0, 28, 11)

    for i in range(plat_quantity):
        plat_list_y.append(i * 200 + 400)
        plat_list_x.append(random.randint(2500, 2900))
        plat_speed_list.append(random.choice([-2, 2, -3, 3]))
        arc.draw_texture_rectangle(plat_list_x[i], plat_list_y[i], 150, 30, platform)

        plat_list_x[i] += plat_speed_list[i]

        if plat_list_x[i] > 2925:
            plat_speed_list[i] = -plat_speed_list[i]

        elif plat_list_x[i] < 2475:
            plat_speed_list[i] = -plat_speed_list[i]

        arc.draw_texture_rectangle(plat_list_x[i], plat_list_y[i], 150, 30, platform)


def player_press(symbol, modifiers):
    global W, A, S, D
    global on_platform

    if symbol == arc.key.D:
        D = True

    elif symbol == arc.key.A:
        A = True

    elif symbol == arc.key.W:
        W = True

    elif symbol == arc.key.S:
        on_platform = True


def player_release(symbol, modifiers):
    global W, A, S, D
    global on_platform

    if symbol == arc.key.D:
        D = False

    elif symbol == arc.key.A:
        A = False

    elif symbol == arc.key.W:
        W = False

    elif symbol == arc.key.S:
        on_platform = False


def player():
    global W, A, S, D
    global screen_tracker

    # MOVEMENT
    if D is True:
        Player_pos[0] += Player_speed

    if A is True:
        Player_pos[0] -= Player_speed

    # JUMP
    if W is True:
        Player_pos[1] += 20

    cube = arc.load_texture("player.png", 0, 0, 64, 64)
    arc.draw_texture_rectangle(Player_pos[0], Player_pos[1], 50, 50, cube)

    for i in range(plat_quantity):
        if Player_pos[1] <= 125:
            Player_pos[1] = 125

        if Player_pos[0] <= 2425:
            Player_pos[0] = 2425

        if Player_pos[0] >= 2975:
            Player_pos[0] = 2975

        if plat_list_x[i] - 90 < Player_pos[0] < plat_list_x[i] + 90 and plat_list_y[i] + 10 <= Player_pos[1] <= \
                plat_list_y[i] + 48 and on_platform is False:
            
            Player_pos[1] = plat_list_y[i] + 48
            Player_pos[0] += plat_speed_list[i]

    # GRAVITY
    Player_pos[1] -= Gravity

    if screen_tracker == 2700:
        arc.set_viewport(2400, 3000, Player_pos[1] - 115, Player_pos[1] + 670)


def ground():
    floor = arc.load_texture("floor.jpg", 0, 0, 1920, 480)
    arc.draw_texture_rectangle(2700, 50, 600, 100, floor)


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
