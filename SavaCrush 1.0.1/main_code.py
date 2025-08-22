import pygame as pg
from random import choice, shuffle
from functionality import *
from assets import *
from game_objects import firework, bomb, lightning

pg.init()

numbers_to_images |= {9: firework, 10: bomb, 11: lightning}

running: bool = True
while running:
    #pg.time.delay(100) # for debugging
    SCREEN.fill(colors["bg"])

    draw_board()
    draw_gems(gems_scheme, coords)

    if None not in gems_scheme:
        destroy_gems(gems_scheme, coords)
    else:
        generate_gems(gems_scheme)
        gravity(gems_scheme)

    if mode == "Swapping":
        if x_pos in range(GAPS * GEM_SCALE + 1) and y_pos in range(GAPS * GEM_SCALE + 1):
            pg.draw.rect(SCREEN, colors["selection"], pg.Rect(x_pos // GEM_SCALE * GEM_SCALE,
                                                      y_pos // GEM_SCALE * GEM_SCALE, 
                                                      GEM_SCALE, GEM_SCALE), 
                                                      3, 4)
        else:
            mode = "Selection"
            pg.mixer.Sound.play(choice((forbidden, forbidden2)))
        
    # shuffles the board if no matches are possible
    if all(gems_scheme) and not check_matches(gems_scheme, coords):
        shuffle(gems_scheme)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            x_pos, y_pos = pg.mouse.get_pos()
            cursor_onboard: bool = x_pos <= GAPS * GEM_SCALE \
                                   and y_pos <= GAPS * GEM_SCALE
            
            # select the first gem
            if cursor_onboard and mode == "Selection":
                gem_idx = coords.index((y_pos // GEM_SCALE, 
                                        x_pos // GEM_SCALE))
                mode = "Swapping"

            # select the second gem
            elif cursor_onboard and mode == "Swapping":
                swap_idx = coords.index((y_pos // GEM_SCALE, 
                                        x_pos // GEM_SCALE))

                if legit_swap(gems_scheme, gem_idx, swap_idx, coords): # successful move
                    destroy_gems(gems_scheme, coords)
                    gems_scheme[gem_idx], gems_scheme[swap_idx] = \
                    gems_scheme[swap_idx], gems_scheme[gem_idx]
                    if gems_scheme[gem_idx] in {9, 10, 11}:
                        numbers_to_images[gems_scheme[gem_idx]].explode(gem_idx, swap_idx)
                    elif gems_scheme[swap_idx] in {9, 10, 11}:
                        numbers_to_images[gems_scheme[swap_idx]].explode(swap_idx, gem_idx)
                    pg.mixer.Sound.play(choice((pop, pop2, pop3, pop4)))
                    mode = "Selection"

                else:                             # unsuccessful move
                    mode = "Swapping"
                    gem_idx = coords.index((y_pos // GEM_SCALE,
                                            x_pos // GEM_SCALE))

    pg.display.flip()
    clock.tick(60)

pg.quit()