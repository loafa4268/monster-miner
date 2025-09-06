# monster_miner.py — Monster Miner, Chunk 1: Boot & Render Loop (~80 LOC)
import pygame

# --- Config ---
TILE = 16
GW, GH = 32, 24                 # grid width/height in tiles
W, H = GW * TILE, GH * TILE     # window size in pixels
FPS = 60
GAME_TITLE = "Monster Miner"

# 8-bit-ish palette
C_BG     = (13, 17, 23)         # deep space
C_SKY    = (24, 29, 39)         # horizon
C_GROUND = (40, 44, 52)         # bedrock strip
C_GRID   = (28, 33, 43)         # subtle grid lines
C_TEXT   = (235, 235, 235)      # UI text

def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(f"{GAME_TITLE} — Chunk 1")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 18)

    # fixed-timestep scaffolding (stable physics later)
    acc, dt = 0.0, 1/60
    t_prev = pygame.time.get_ticks() / 1000

    running = True
    while running:
        # --- time ---
        t_now = pygame.time.get_ticks() / 1000
        acc += min(0.25, t_now - t_prev)  # clamp to avoid spiral of death
        t_prev = t_now

        # --- input ---
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.QUIT:
                running = False

        # --- update (none yet; structure ready for future) ---
        while acc >= dt:
            # physics update would go here
            acc -= dt

        # --- draw ---
        screen.fill(C_BG)    

        # sky band (3 tiles tall)
        pygame.draw.rect(screen, C_SKY, (0, 0, W, TILE * 3))
        pygame.draw.rect(screen, C_GROUND, (0, (GH - 1) * TILE, W, TILE))

        # grid for that cozy 8 bit tile vibe
        for x in range(0, W, TILE):
            pygame.draw.line(screen, C_GRID, (x, 0), (x, H))
        for y in range(0, H, TILE):
            pygame.draw.line(screen, C_GRID, (0, y), (W, y))

        #label
        tip = f"{GAME_TITLE} — Chunk 1: Boot & Render Loop - ESC to quit"
        screen.blit(font.render(tip, True, C_TEXT), (8, 6))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()


