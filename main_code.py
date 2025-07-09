import pygame as pg
from itertools import product
from random import choice, shuffle
from os import path

pg.init()
pg.mixer.init()
pg.font.init()

colors: dict[str, tuple[int, ...]] = {'bg': (100, 200, 50), 
                                      'border': (0, 0, 0),
                                      'field': (224, 224, 224),
                                      'bg_red': (136, 8, 8)}
# main game scales
WIN_SCALES: tuple[int, int] = (900, 700)
SCREEN: pg.surface.Surface = pg.display.set_mode(WIN_SCALES)
TITLE: None = pg.display.set_caption('Sava Crush beta')
gaps: int = 9   # how many gems will there be in a row and a column
gem_scale: int = 50     # width and height of the gem images
clock: pg.time.Clock = pg.time.Clock()
mode: str = 'Selection'     # if selection - player selects the first gem, if swapping - chooses the second one

# indexes for selection
gem_idx: int | None = None  
swap_idx: int | None = None

# sounds of removing the gems
pop: pg.mixer.Sound = pg.mixer.Sound(path.join(r'Sounds\Gem_sound.wav'))
pop2: pg.mixer.Sound = pg.mixer.Sound(path.join(r'Sounds\Gem_sound2.wav'))
pop3: pg.mixer.Sound = pg.mixer.Sound(path.join(r'Sounds\Gem_sound3.mp3'))
pop4: pg.mixer.Sound = pg.mixer.Sound(path.join(r'Sounds\Gem_sound4.wav'))

# sounds of illegal move
forbidden: pg.mixer.Sound = pg.mixer.Sound(path.join(r'Sounds\Forbidden.mp3'))
forbidden2: pg.mixer.Sound = pg.mixer.Sound(path.join(r'Sounds\Forbidden2.mp3'))
# gem coords
coords: tuple[tuple[int, int], ...] = tuple((i, j) for i, j in 
                                            product(range(gaps), range(gaps)))

# main board
gems_scheme: list[pg.Surface | None] = [None] * (gaps ** 2)

# gems_images images
gems_images: list[pg.Surface] = [pg.transform.scale(image, 
                                                    (gem_scale, gem_scale))
                           for image in 
                           (pg.image.load(fr'Images\{color}_gem.png') 
                            for color in 
                            ('Blue', 'Bruise', 'Green', 'Magenta',
                             'Red', 'Purple', 'Cyan', 'Orange'))]

def draw_board() -> None:
    '''draws the main board: background of the board and the outline'''
    pg.draw.rect(SCREEN, colors['field'], pg.Rect(0, 0, gem_scale * gaps,
                 gem_scale * gaps))
    for i in range(gaps + 1):
        pg.draw.line(SCREEN, colors['border'], (gem_scale * i, 0), 
                     (gem_scale * i, gaps * gem_scale))
        pg.draw.line(SCREEN, colors['border'], (0, gem_scale * i),
                     (gaps * gem_scale, gem_scale * i))
        
def generate_gems() -> None:
    '''spawns gems from the top row'''
    global gems_scheme
    for idx in range(gaps):
        if gems_scheme[idx] is None:
            gems_scheme[idx] = choice(gems_images)

def draw_gems() -> None:
    '''draws the gems + adds mechanics for 
    them to fall and fill the whole field'''
    global gems_scheme
    for coord, gem in zip(coords, gems_scheme):
        if gem is not None:
            SCREEN.blit(gem, (coord[1] * gem_scale, coord[0] * gem_scale))

    for idx, gem in enumerate(gems_scheme[:-gaps]):
        if gem is not None and gems_scheme[idx + gaps] is None:
            gems_scheme[idx], gems_scheme[idx + gaps] = \
                gems_scheme[idx + gaps], gems_scheme[idx]

def destroy_gems(board: list[pg.surface.Surface | None]=gems_scheme) -> None:
    '''check for matches and if there are any,
    removes the gems in the matches'''

    for match_lenght in range(5, 2, -1):        # rows check
        for idx in range(len(board) - match_lenght - 1):
            if (all(board[idx] is board[idx + i] for i in range(match_lenght)) and\
                all(coords[idx][0] is coords[idx + j][0] 
                    for j in range(match_lenght))):
                    for i in range(match_lenght):
                        board[idx + i] = None

    for match_lenght in range(5, 2, -1):        # columns check
        for idx in range(len(board) - gaps * (match_lenght - 1)):
            if all(board[idx] is board[idx + gaps * i] 
                   for i in range(match_lenght)):
               for i in range(match_lenght):
                        board[idx + gaps * i] = None


def legit_swap(idx1: int, idx2: int) -> bool:
    '''checks if the player swaps the gems legitimately'''
    global count
    pos1: tuple[int, int] = coords[idx1]
    pos2: tuple[int, int] = coords[idx2]

    # temporary board for simulating swaps
    temp_board_scheme: list[pg.Surface | None] = gems_scheme.copy()

    if not ((pos1[0] - pos2[0] == 1 and pos1[1] == pos2[1]) or \
            (pos2[0] - pos1[0] == 1 and pos1[1] == pos2[1]) or \
                (pos1[1] - pos2[1] == 1 and pos1[0] == pos2[0]) \
                    or (pos2[1] - pos1[1] == 1 and pos1[0] == pos2[0])):
        return False
    temp_board_scheme[idx1], temp_board_scheme[idx2] = \
        temp_board_scheme[idx2], temp_board_scheme[idx1]
    destroy_gems(board=temp_board_scheme)
    count += temp_board_scheme.count(None)
    if temp_board_scheme[idx1] is not None and temp_board_scheme[idx2] \
    is not None:
        return False
        
    return True

def check_matches() -> bool:
    '''algorithm for checking the field for possible moves,
    if there are no such, the board is shuffled in the main loop'''
    temp_board_scheme: list[pg.Surface | None] = gems_scheme.copy()
    for idx in range(len(temp_board_scheme) - gaps):
        temp_board_scheme[idx], temp_board_scheme[idx + gaps] = \
        temp_board_scheme[idx + gaps], temp_board_scheme[idx]
        destroy_gems(temp_board_scheme)
        if not all(temp_board_scheme):
            return True

        temp_board_scheme[idx], temp_board_scheme[idx + gaps] = \
        temp_board_scheme[idx + gaps], temp_board_scheme[idx]

    for idx in range(len(temp_board_scheme) - 1):
        if coords[idx][0] == coords[idx + 1][0]:
            temp_board_scheme[idx], temp_board_scheme[idx + 1] = \
            temp_board_scheme[idx + 1], temp_board_scheme[idx]
            destroy_gems(temp_board_scheme)
            if not all(temp_board_scheme):
                return True

            temp_board_scheme[idx], temp_board_scheme[idx + 1] = \
            temp_board_scheme[idx + 1], temp_board_scheme[idx]
        
    return False


def update_count() -> pg.surface.Surface:
    '''updates the count value on the main screen'''
    return font.render(f'Gems destroyed: {count}', True, (0, 0, 0), 
                       colors['bg'])

count: int = 0
font: pg.font.Font = pg.font.SysFont('Calibri', 30)
text: pg.surface.Surface = update_count()
text_rect: pg.rect.Rect = text.get_rect()
text_rect.center: tuple[int, int] = (700, 100) # type: ignore

running: bool = True
while running:
    SCREEN.fill(colors['bg'])
    SCREEN.blit(text, text_rect)

    draw_board()
    generate_gems()
    draw_gems()
    destroy_gems()
        
    # shuffles the board if no matches are possible
    if all(gems_scheme) and not check_matches():
        shuffle(gems_scheme)

    for event in pg.event.get():

        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            x_pos, y_pos = pg.mouse.get_pos()
            cursor_onboard: bool = x_pos <= gaps * gem_scale \
                                   and y_pos <= gaps * gem_scale
            
            # select the first gem
            if cursor_onboard and mode == 'Selection':
                gem_idx = coords.index((y_pos // gem_scale, 
                                        x_pos // gem_scale))
                mode = 'Swapping'

            # select the second gem
            elif cursor_onboard and mode == 'Swapping':
                swap_idx = coords.index((y_pos // gem_scale, 
                                         x_pos // gem_scale))

                if legit_swap(gem_idx, swap_idx): # successful move
                    text = update_count()
                    gems_scheme[gem_idx], gems_scheme[swap_idx] = \
                    gems_scheme[swap_idx], gems_scheme[gem_idx]
                    pg.mixer.Sound.play(choice((pop, pop2, pop3, pop4)))

                else:                             # unsuccessful move
                    pg.mixer.Sound.play(choice((forbidden, forbidden2)))
                    
                mode = 'Selection'

    pg.display.flip()
    clock.tick(60)

pg.quit()