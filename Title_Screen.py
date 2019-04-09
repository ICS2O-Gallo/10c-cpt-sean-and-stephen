import arcade as arc
import Main_Game

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Laser Platform"

GAME = False

button_transparency = 1
button_pos = [304, 200]


def update_everything(delta_time):
    title_screen()

    if GAME is True:
        Main_Game.change()


def title_screen():
    global button_pos, button_transparency

    arc.start_render()
    # Loading the textures for screen
    background = arc.load_texture("background.png", 0, 0, 320, 256)
    title = arc.load_texture("title.png", 0, 0, 1000, 97)
    button = arc.load_texture("label.png", 0, 36, 48, 12)

    # Putting textures onto screen
    arc.draw_texture_rectangle(300, 450, 600, 900, background)
    arc.draw_texture_rectangle(300, 675, 400, 50, title)
    arc.draw_texture_rectangle(button_pos[0], button_pos[1], 200, 100, button, 0, button_transparency)
    arc.draw_text("Play", 280, 192, arc.color.WHITE, 20, font_name="Calibri", bold=True, italic=True)


def mouse_detection(x, y, dx, dy):
    global button_pos, button_transparency, button_area

    # Detects when mouse is over the button
    button_area = button_pos[0] - 100 <= x <= button_pos[0] + 100 and button_pos[1] - 50 <= y <= button_pos[1] + 50

    if button_area:
        button_transparency = 0.6

    else:
        button_transparency = 1


def button_click(x, y, button, modifiers):
    global button_area, GAME

    # Initializing game
    if button_area and button == arc.MOUSE_BUTTON_LEFT:
        GAME = True


def screen_setup():
    arc.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arc.set_background_color(arc.color.BLACK)

    arc.schedule(update_everything, 1 / 60)

    window = arc.get_window()
    window.on_mouse_motion = mouse_detection
    window.on_mouse_press = button_click

    title_screen()

    arc.run()


screen_setup()
