import arcade as ac

"""
Air resistance does not exist in this simulation

"""
# Window information
SCH = 800
SCW = 600
SCT = "Jumping with gravity - test"

object_radius = 10

# Object starts lower than "initial height" to ensure velocity is not 0
initial_y = 790
object_y = initial_y - 1
object_x = SCW / 2
object_speed = 5
jumpCap = initial_y - 5

# Acceleration of gravity
g = 1

# Up, left, right key states
U = False
L = False
R = False

# State of player location
inAir = False
onGround = False


def update(delta_time):
    # Updating functions
    draw_object(object_x, object_y)
    left_right_move()
    jump()


def draw_object(x, y):
    # Drawing object with object_radius at y position
    ac.start_render()
    ac.draw_circle_filled(x, y, object_radius, ac.color.GREEN)


def instant_velocity():
    # The distance is calculated every frame
    # in order to calculate instantaneous velocity
    def get_dist(current_y):
        return initial_y - current_y

    # Formula for instantaneous velocity after distance travelled
    return (2 * g * get_dist(object_y)) ** 0.5


def jump():
    global object_y, onGround, inAir, U
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

    # When a jump is called, the object moves up by twice the velocity in order
    # to counteract the "regular" gravity acting on it downwards.
    if U:
        object_y += 2 * instant_velocity()

    # Check if object has reached its maximum jump height.
    # If so, the jump is cancelled.
    if object_y >= jumpCap:
        U = False


def left_right_move():
    global object_x
    # Moving left and right
    if L:
        object_x -= object_speed

    if R:
        object_x += object_speed


# Key press / release functions
def keypress(symbol, mod):
    global U, L, R
    if symbol == ac.key.UP and onGround:
        U = True

    if symbol == ac.key.LEFT:
        L = True

    if symbol == ac.key.RIGHT:
        R = True


def keyrelease(symbol, mod):
    # Only left and right movement is detected as upwards control is
    # controlled in the jump() function
    global L, R
    if symbol == ac.key.LEFT:
        L = False

    if symbol == ac.key.RIGHT:
        R = False


# Setting up window.
def setup():
    ac.open_window(SCW, SCH, SCT)
    ac.set_background_color(ac.color.WHITE)
    ac.schedule(update, 1 / 60)
    window = ac.get_window()
    window.on_key_press = keypress
    window.on_key_release = keyrelease
    ac.run()


setup()
