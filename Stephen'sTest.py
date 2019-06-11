from arcade import *

SCH = 800
SCW = 800
SCT = "Vector Testing"

playerPos = [SCH / 2, SCH / 2]
playerSpeed = 5

W = False
A = False
S = False
D = False


def update(delta_time):
    draw_player(playerPos[0], playerPos[1])
    if W:
        playerPos[1] += playerSpeed

    if S:
        playerPos[1] -= playerSpeed

    if A:
        playerPos[0] -= playerSpeed

    if D:
        playerPos[0] += playerSpeed

    if playerPos[1] - 25 <= 0:
        playerPos[1] = 25


def draw_player(x, y):
    start_render()
    draw_rectangle_filled(x, y, 50, 50, color.RED)


def keypress(sym, mod):
    global W, A, S, D
    if sym == key.W:
        W = True

    if sym == key.S:
        S = True

    if sym == key.A:
        A = True

    if sym == key.D:
        D = True


def keyrelease(sym, mod):
    global W, A, S, D
    if sym == key.W:
        W = False

    if sym == key.S:
        S = False

    if sym == key.A:
        A = False

    if sym == key.D:
        D = False


def setup():
    open_window(SCW, SCH, SCT)
    set_background_color(color.WHITE)
    schedule(update, 1 / 60)
    window = get_window()
    window.on_key_press = keypress
    window.on_key_release = keyrelease
    run()


setup()
