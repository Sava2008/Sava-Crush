import pygame as pg
from itertools import product

pg.init()
pg.mixer.init()
pg.font.init()

colors: dict[str, tuple[int, int, int]] = {"bg": (100, 200, 50), 
                                      "border": (100, 100, 100),
                                      "field": (224, 224, 224),
                                      "bg_red": (136, 8, 8),
                                      "selection": (20, 45, 50)}
# main game scales
WIN_SCALES: tuple[int, int] = (900, 700)
GAPS: int = 9  # how many gems will there be in each row and column (minimum 5)
FIELD_AREA: int = GAPS ** 2
GEM_SCALE: int = 50

SCREEN: pg.Surface = pg.display.set_mode(WIN_SCALES)

# gems_images images
generation_subjects: tuple[int, ...] = tuple(range(1, 9))
numbers_to_images: dict[int, pg.Surface] = {num: pg.transform.scale(pg.image
                                            .load(fr"Images\{color}_gem.png"),
                                            (GEM_SCALE, GEM_SCALE)) for num, 
                                            color in zip(generation_subjects, 
                                            ("Bruise", "Blue", "Green", "Red",
                                            "Orange", "Purple", "Cyan", "Magenta"))}

# main game scales
pg.display.set_caption("Sava Crush 1.0.1")
pg.display.set_icon(pg.image.load(r"Images\Icon.ico"))
clock: pg.time.Clock = pg.time.Clock()
mode: str = "Selection"     # if selection - player selects the first gem, if swapping - chooses the second one
x_pos: int | None = None
y_pos: int | None = None


# indexes for selection
gem_idx: int | None = None
swap_idx: int | None = None

# sounds of removing the gems
pop: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Gem_sound.mp3")
pop2: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Gem_sound2.mp3")
pop3: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Gem_sound3.mp3")
pop4: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Gem_sound4.mp3")

# sounds of illegal move
forbidden: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Forbidden.mp3")
forbidden2: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Forbidden2.mp3")

# Explosives sounds
firework_sound: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Firework_sound.mp3")
bomb_sound: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Bomb_sound.mp3")
lightning_sound: pg.mixer.Sound = pg.mixer.Sound(r"Sounds\Lightning_sound.mp3")

# gem coords
coords: tuple[tuple[int, int], ...] = tuple((i, j) for i, j in 
                                            product(range(GAPS), range(GAPS)))

# main board
gems_scheme: list[int | None] = [None] * (GAPS ** 2)