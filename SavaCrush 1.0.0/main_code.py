import pygame as pg
from itertools import product
from random import choice, shuffle
from typing import Generator, Any

pg.init()
pg.mixer.init()
pg.font.init()


colors: dict[str, tuple[int, ...]] = {"bg": (100, 200, 50), 
                                      "border": (100, 100, 100),
                                      "field": (224, 224, 224),
                                      "bg_red": (136, 8, 8),
                                      "selection": (20, 45, 50)}
# main game scales
WIN_SCALES: tuple[int, int] = (900, 700)
SCREEN: pg.surface.Surface = pg.display.set_mode(WIN_SCALES)
pg.display.set_caption("Sava Crush 1.0.0")
pg.display.set_icon(pg.image.load(r"Images\Icon.ico"))
GAPS: int = 9   # how many gems will there be in each row and column
FIELD_AREA: int = GAPS ** 2
GEM_SCALE: int = 50     # width and height of the gem images
clock: pg.time.Clock = pg.time.Clock()
mode: str = "Selection"     # if selection - player selects the first gem, if swapping - chooses the second one
x_pos: int | None = None
y_pos: int | None = None


# indexes for selection
gem_idx: int | None = None
swap_idx: int | None = None

# sounds of removing the gems
pop: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Gem_sound.wav")
pop2: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Gem_sound2.wav")
pop3: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Gem_sound3.mp3")
pop4: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Gem_sound4.wav")

# sounds of illegal move
forbidden: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Forbidden.mp3")
forbidden2: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Forbidden2.mp3")

# Explosives sounds
firework_sound: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Firework_sound.wav")
bomb_sound: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Bomb_sound.wav")
lightning_sound: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Lightning_sound.wav")

# gem coords
coords: tuple[tuple[int, int], ...] = tuple((i, j) for i, j in 
                                            product(range(GAPS), range(GAPS)))

# main board
gems_scheme: list[pg.Surface | None] = [None] * (GAPS ** 2)

# gems_images images
gems_images: list[pg.Surface] = [pg.transform.scale(image, 
                                                    (GEM_SCALE, GEM_SCALE))
                           for image in 
                           (pg.image.load(fr"Images\{color}_gem.png") 
                            for color in 
                            ("Bruise", "Green", "Magenta", "Blue",
                             "Red", "Orange", "Cyan"))] # removed Purple


def update_count() -> pg.surface.Surface:
    """updates the count value on the main screen"""
    return font.render(f"Gems destroyed: {count}", True, (0, 0, 0), 
                       colors["bg"])

count: int = 0
font: pg.font.Font = pg.font.SysFont("Calibri", 30)
text: pg.surface.Surface = update_count()
text_rect: pg.rect.Rect = text.get_rect()
text_rect.center: tuple[int, int] = (700, 100) # type: ignore

class Explosive(pg.Surface):
    def __init__(self, image: pg.Surface, 
                 sound: pg.mixer.Sound | None = None) -> None:
        super().__init__(size=(GEM_SCALE, GEM_SCALE))
        self.image = image
        self.sound = sound
        self.radius: int | None = 1


class Firework(Explosive):
    def __init__(self, image: pg.Surface, sound: pg.mixer.Sound | 
                 None = firework_sound) -> None:
        super().__init__(image=image, sound=sound)
        self.radius: int = 1
        self.sound = sound

    def explode(self, index: int, swapped_item_index: int) -> None:
        global count
        pg.mixer.Sound.play(self.sound)
        row: int = index // GAPS + 1 if index % GAPS > 0 else index // GAPS
        if coords[index][0] == coords[swapped_item_index][0]:
            whole_row_indices: Generator[int] = (i for i in 
                                                 range((row - 1) * GAPS, 
                                                       row * GAPS))
            for idx in whole_row_indices:
                gems_scheme[idx] = None
                if gems_scheme[idx] not in {bomb, firework, lightning}:
                    count += 1
        else:
            column: int = index - GAPS * (row - 1) + 1
            if column == 10:
                column = 1
            whole_column_indices: Generator = ((column - 1) + (GAPS * r) for
                                               r in range(GAPS))
            for idx in whole_column_indices:
                count += 1
                gems_scheme[idx] = None


class Bomb(Explosive):
    def __init__(self, image: pg.Surface, 
                 sound: pg.mixer.Sound | None = bomb_sound) -> None:
        super().__init__(image=image, sound=sound)
        self.radius: int = 2
        self.sound = sound

    def explode(self, index: int, swapped_item_index: int) -> None:
        global count
        pg.mixer.Sound.play(self.sound)
        #square_upper_left_corner: int = max(index - self.radius - GAPS, 0)
        #square_lower_right_corner: int = min(index + self.radius + GAPS, 
                                             #FIELD_AREA - 1)
        
        # raw implementation
        self.surrounding: tuple[int, ...] = (index, index - 1 - GAPS,
                                             index - GAPS, index + 1 - GAPS,
                                             index + 1 + GAPS, index + GAPS,
                                             index - 1 + GAPS,
                                             index - 1, index + 1)
        for idx in self.surrounding:
            if idx in range(0, FIELD_AREA - 1):
                count += 1
                gems_scheme[idx] = None


class Lightning(Explosive):
    def __init__(self, image: pg.Surface,
                 sound: pg.mixer.Sound | None = lightning_sound) -> None:
        super().__init__(image=image, sound=sound)
        self.sound = sound
    
    def explode(self, index: int, swapped_item_index: int) -> None:
        global count, gems_scheme
        gems_scheme[index] = None
        pg.mixer.Sound.play(self.sound)
        self.indices_to_remove: list[int] = [idx for idx, gem in enumerate(gems_scheme) 
                                        if gem == gems_scheme[swapped_item_index]]
        for idx in self.indices_to_remove:
            count += 1
            gems_scheme[idx] = None


firework: Firework = Firework(pg.transform.scale(
    pg.image.load(r"Images\Firework.png"), (GEM_SCALE, GEM_SCALE)))
bomb: Bomb = Bomb(pg.transform.scale(pg.image.load(r"Images\Bomb.png"), 
                                     (GEM_SCALE, GEM_SCALE)))
lightning = Lightning = Lightning(pg.transform.scale(pg.image.load(r"Images\Lightning.png"), 
                                     (GEM_SCALE, GEM_SCALE)))


def draw_board() -> None:
    """draws the main board: background of the board and the outline"""
    pg.draw.rect(SCREEN, colors["field"], pg.Rect(0, 0, GEM_SCALE * GAPS,
                 GEM_SCALE * GAPS))
    for i in range(GAPS + 1):
        pg.draw.line(SCREEN, colors["border"], (GEM_SCALE * i, 0), 
                     (GEM_SCALE * i, GAPS * GEM_SCALE))
        pg.draw.line(SCREEN, colors["border"], (0, GEM_SCALE * i),
                     (GAPS * GEM_SCALE, GEM_SCALE * i))
        
def generate_gems() -> None:
    """spawns gems from the top row"""
    global gems_scheme
    for idx in range(GAPS):
        if gems_scheme[idx] is None:
            gems_scheme[idx] = choice(gems_images)

def draw_gems() -> None:
    """draws the gems + adds mechanics for 
    them to fall and fill the whole field"""
    global gems_scheme
    for coord, gem in zip(coords, gems_scheme):
        if gem not in {bomb, firework, lightning} and gem is not None:
            SCREEN.blit(gem, (coord[1] * GEM_SCALE, coord[0] * GEM_SCALE))
        elif gem in {bomb, firework, lightning}:
            SCREEN.blit(gem.image, (coord[1] * GEM_SCALE, coord[0] * GEM_SCALE))

    for idx, gem in enumerate(gems_scheme[:-GAPS]):
        if gem is not None and gems_scheme[idx + GAPS] is None:
            gems_scheme[idx], gems_scheme[idx + GAPS] = \
                gems_scheme[idx + GAPS], gems_scheme[idx]

def destroy_gems(board: list[pg.surface.Surface | None]=gems_scheme) -> None:
    """check for matches and if there are any,
    removes the gems in the matches"""

    for match_lenght in range(5, 2, -1):        # rows check
        for idx in range(len(board) - match_lenght - 1):
            if (all(board[idx] is board[idx + i] for i in range(match_lenght))\
                and all(coords[idx][0] is coords[idx + j][0] 
                    for j in range(match_lenght))) and board[idx] is not None:
                    for i in range(match_lenght):
                        board[idx + i] = None
                    if match_lenght == 4:
                        board[idx + 1] = bomb
                    elif match_lenght == 5:
                        board[idx + 2] = lightning

    for match_lenght in range(5, 2, -1):        # columns check
        for idx in range(len(board) - GAPS * (match_lenght - 1)):
            if all(board[idx] is board[idx + GAPS * i] 
                   for i in range(match_lenght)) and board[idx] is not None:
               for i in range(match_lenght):
                        board[idx + GAPS * i] = None
               if match_lenght == 4:
                    board[idx + GAPS] = firework
               elif match_lenght == 5:
                    board[idx + 2] = lightning



def legit_swap(idx1: int, idx2: int) -> bool:
    """checks if the player swaps the gems legitimately"""
    global count

    if gems_scheme[idx1] in {bomb, firework, lightning} or gems_scheme[idx2] \
        in {bomb, firework, lightning}:
        return True
    
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
    if temp_board_scheme[idx1] not in {bomb, firework, lightning, None} and \
        temp_board_scheme[idx2] not in {bomb, firework, lightning, None}:
        return False
    
    return True

def check_matches() -> bool:
    """algorithm for checking the field for possible moves,
    if there are no such, the board is shuffled in the main loop"""
    temp_board_scheme: list[pg.Surface | None] = gems_scheme.copy()
    for idx in range(len(temp_board_scheme) - GAPS):
        temp_board_scheme[idx], temp_board_scheme[idx + GAPS] = \
        temp_board_scheme[idx + GAPS], temp_board_scheme[idx]
        destroy_gems(temp_board_scheme)
        if not all(temp_board_scheme):
            return True

        temp_board_scheme[idx], temp_board_scheme[idx + GAPS] = \
        temp_board_scheme[idx + GAPS], temp_board_scheme[idx]

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

running: bool = True
while running:
    #pg.time.delay(200) # for debugging
    SCREEN.fill(colors["bg"])
    SCREEN.blit(text, text_rect)

    draw_board()
    generate_gems()
    draw_gems()
    destroy_gems()

    if mode == "Swapping":
        pg.draw.rect(SCREEN, colors["selection"], pg.Rect(x_pos // GEM_SCALE * GEM_SCALE,
                                                      y_pos // GEM_SCALE * GEM_SCALE, 
                                                      GEM_SCALE, GEM_SCALE), 
                                                      3, 4)
        
    # shuffles the board if no matches are possible
    if all(gems_scheme) and not check_matches():
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

                if legit_swap(gem_idx, swap_idx): # successful move
                    text = update_count()
                    gems_scheme[gem_idx], gems_scheme[swap_idx] = \
                    gems_scheme[swap_idx], gems_scheme[gem_idx]
                    if gems_scheme[gem_idx] in {bomb, firework, lightning}:
                        gems_scheme[gem_idx].explode(gem_idx, swap_idx)
                    elif gems_scheme[swap_idx] in {bomb, firework, lightning}:
                        gems_scheme[swap_idx].explode(swap_idx, gem_idx)
                    pg.mixer.Sound.play(choice((pop, pop2, pop3, pop4)))

                else:                             # unsuccessful move
                    pg.mixer.Sound.play(choice((forbidden, forbidden2)))
                    
                mode = "Selection"

    pg.display.flip()
    clock.tick(60)

pg.quit()