import arcade as ac

"""
Air resistance does not exist in this simulation

"""

SCH = 800
SCW = 600
SCT = "Jumping with gravity - test"

object_radius = 10

# Object starts lower than "initial height" to ensure velocity is not 0
initial_y = 790
object_y = initial_y - 1
jumpCap = 700

# Acceleration of gravity
g = 1

# Up, down, left, right key states
U = False
D = False
L = False
R = False

# State of player location
inAir = False
onGround = False


def update(delta_time):
    # Updating functions

    global object_y, onGround, inAir, U
    draw_object(object_y)

    object_y -= instant_velocity()

    # Object does not fall through y = 0
    if object_y - object_radius <= 0:
        object_y = object_radius
        onGround = True
        inAir = False

    else:
        onGround = False
        inAir = True

    print("On ground: {0} | In air: {1}".format(onGround, inAir))

    if U:
        object_y += 2 * instant_velocity()

    if object_y >= initial_y - 5:
        U = False
        object_y -= instant_velocity()


def draw_object(y):
    # Drawing object with object_radius at y position
    ac.start_render()
    ac.draw_circle_filled(SCW / 2, y, object_radius, ac.color.GREEN)


def instant_velocity():
    # The distance is calculated every frame
    # in order to calculate instantaneous velocity
    def get_dist(current_y):
        return initial_y - current_y

    # Formula for instantaneous velocity after distance travelled
    return (2 * g * get_dist(object_y)) ** 0.5


def keypress(symbol, mod):
    global U, D, L, R
    if symbol == ac.key.UP and onGround:
        U = True


def setup():
    ac.open_window(SCW, SCH, SCT)
    ac.set_background_color(ac.color.WHITE)
    ac.schedule(update, 1 / 60)
    window = ac.get_window()
    window.on_key_press = keypress
    ac.run()


setup()
