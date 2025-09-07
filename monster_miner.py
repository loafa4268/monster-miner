import pygame, random

TILE = 16
GW, GH = 32, 24
W, H = GW * TILE, GH * TILE
FPS = 60
GAME_TITLE = "Monster Miner"

EMPTY, DIRT, ROCK, ORE, BASE = 0, 1, 2, 3, 4

C_BG     = (13, 17, 23)
C_SKY    = (24, 29, 39)
C_GROUND = (40, 44, 52)
C_GRID   = (28, 33, 43)
C_TEXT   = (235, 235, 235)
C_DIRT   = (98, 77, 54)
C_ROCK   = (60, 60, 72)
C_ORE    = (240, 200, 80)
C_BASE   = (82, 185, 207)
C_BASE_OPEN = (120, 220, 240)
C_PLY    = (50, 220, 72)
C_DOT    = (200, 205, 220)

BAG_MAX = 10
ORE_VALUE = 5
MIN_ORE_TO_ENTER = 3

def tile_at(x, y):
    if x == 0 or x == GW - 1 or y == GH - 1:
        return ROCK
    if y < 3:
        return EMPTY
    if y == 3 and GW // 2 - 2 <= x <= GW // 2 + 2:
        return BASE
    p = 0.03 + (y / GH) * 0.07
    return ORE if random.random() < p * 0.65 else DIRT

def gen_world():
    return [[tile_at(x, y) for x in range(GW)] for y in range(GH)]

def can_walk(world, x, y, bag):
    # only allow walking into BASE if the player has enough ore to "enter" (sell)
    if not (0 <= x < GW and 0 <= y < GH):
        return False
    t = world[y][x]
    if t == BASE:
        return eligible_to_enter(bag)
    return t == EMPTY

def dig(world, x, y, bag):
    if 0 <= x < GW and 0 <= y < GH:
        t = world[y][x]
        if t == DIRT:
            world[y][x] = EMPTY
            return bag
        if t == ORE and bag < BAG_MAX:
            world[y][x] = EMPTY
            return bag + 1
    return bag

def eligible_to_enter(bag):
    return bag >= MIN_ORE_TO_ENTER

def try_sell_on_base(world, px, py, bag, cash):
    if world[py][px] != BASE:
        return bag, cash, "Not at base.", 0.8
    if eligible_to_enter(bag):
        gained = bag * ORE_VALUE
        cash += gained
        bag = 0
        return bag, cash, f"Sold! +${gained}", 1.2
    else:
        return bag, cash, f"Need ≥ {MIN_ORE_TO_ENTER} ore to enter", 1.2

def tile_color(t, bag):
    if t == DIRT:
        return C_DIRT
    if t == ROCK:
        return C_ROCK
    if t == ORE:
        return C_ORE
    if t == BASE:
        return C_BASE_OPEN if eligible_to_enter(bag) else C_BASE
    return C_BG

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(GAME_TITLE)
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont(None, 18)
    pygame.key.set_repeat(150, 60)

    acc, dt = 0.0, 1 / 60
    t_prev = pygame.time.get_ticks() / 1000

    world = gen_world()
    px, py = GW // 2, 2
    facing = (0, 1)
    bag, cash = 0, 0
    flash_msg, flash_time = "", 0.0

    running = True
    while running:
        t_now = pygame.time.get_ticks() / 1000
        acc += min(0.25, t_now - t_prev)
        t_prev = t_now

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key in (pygame.K_LEFT, pygame.K_a):
                    facing = (-1, 0)
                    nx, ny = px - 1, py
                    if 0 <= nx < GW and 0 <= ny < GH and world[ny][nx] == BASE and not eligible_to_enter(bag):
                        flash_msg, flash_time = f"Need ≥ {MIN_ORE_TO_ENTER} ore to enter", 1.2
                    elif can_walk(world, nx, ny, bag):
                        px -= 1
                elif e.key in (pygame.K_RIGHT, pygame.K_d):
                    facing = (1, 0)
                    nx, ny = px + 1, py
                    if 0 <= nx < GW and 0 <= ny < GH and world[ny][nx] == BASE and not eligible_to_enter(bag):
                        flash_msg, flash_time = f"Need ≥ {MIN_ORE_TO_ENTER} ore to enter", 1.2
                    elif can_walk(world, nx, ny, bag):
                        px += 1
                elif e.key in (pygame.K_UP, pygame.K_w):
                    facing = (0, -1)
                    nx, ny = px, py - 1
                    if 0 <= nx < GW and 0 <= ny < GH and world[ny][nx] == BASE and not eligible_to_enter(bag):
                        flash_msg, flash_time = f"Need ≥ {MIN_ORE_TO_ENTER} ore to enter", 1.2
                    elif can_walk(world, nx, ny, bag):
                        py -= 1
                elif e.key in (pygame.K_DOWN, pygame.K_s):
                    facing = (0, 1)
                    nx, ny = px, py + 1
                    if 0 <= nx < GW and 0 <= ny < GH and world[ny][nx] == BASE and not eligible_to_enter(bag):
                        flash_msg, flash_time = f"Need ≥ {MIN_ORE_TO_ENTER} ore to enter", 1.2
                    elif can_walk(world, nx, ny, bag):
                        py += 1
                elif e.key == pygame.K_SPACE:
                    if world[py][px] == BASE:
                        bag, cash, flash_msg, flash_time = try_sell_on_base(world, px, py, bag, cash)
                    else:
                        tx, ty = px + facing[0], py + facing[1]
                        bag = dig(world, tx, ty, bag)

        while acc >= dt:
            if flash_time > 0:
                flash_time = max(0.0, flash_time - dt)
            acc -= dt

        screen.fill(C_BG)
        pygame.draw.rect(screen, C_SKY,    (0, 0, W, 3 * TILE))
        pygame.draw.rect(screen, C_GROUND, (0, (GH - 1) * TILE, W, TILE))

        _ = [pygame.draw.rect(screen, tile_color(t, bag), (x * TILE, y * TILE, TILE, TILE))
             for y, row in enumerate(world) for x, t in enumerate(row) if t != EMPTY]

        pygame.draw.rect(screen, C_PLY, (px * TILE, py * TILE, TILE, TILE))
        fx = px * TILE + TILE // 2 + facing[0] * 5
        fy = py * TILE + TILE // 2 + facing[1] * 5
        pygame.draw.rect(screen, C_DOT, (fx - 2, fy - 2, 4, 4))

        _ = [pygame.draw.line(screen, C_GRID, (x, 0), (x, H)) for x in range(0, W, TILE)]
        _ = [pygame.draw.line(screen, C_GRID, (0, y), (W, y)) for y in range(0, H, TILE)]

        hud = f"Bag: {bag}/{BAG_MAX}   Cash: ${cash}   Enter needs ≥ {MIN_ORE_TO_ENTER} ore"
        screen.blit(font.render(hud, True, C_TEXT), (8, H - 24))
        tip = f"{GAME_TITLE} — Move: WASD/Arrows  Dig/Sell: SPACE  ESC: Quit"
        screen.blit(font.render(tip, True, C_TEXT), (8, 6))
        if flash_time > 0 and flash_msg:
            msg = font.render(flash_msg, True, C_TEXT)
            screen.blit(msg, (W // 2 - msg.get_width() // 2, 28))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
