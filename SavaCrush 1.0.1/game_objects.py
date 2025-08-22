from assets import *
from typing import Generator
from random import choices

def row_column_from_index(index: int) -> tuple[int, int]:
        row: int = index // GAPS + 1
        return (row,
                1 if index % GAPS == 0 else index - GAPS * (row - 1) + 1)

class Explosive:
    def __init__(self, image: pg.Surface, 
                 sound: pg.mixer.Sound | None = None) -> None:
        self.image: pg.Surface = image
        self.sound: pg.mixer.Sound | None = sound

    def __eq__(self, other) -> bool:
        try:
            return self.image == other.image and self.sound == other.sound
        except AttributeError:
            return False
    
    def __hash__(self) -> int:
        return hash((self.image, self.sound))


class Firework(Explosive):
    def __init__(self, image: pg.Surface, sound: pg.mixer.Sound |
                 None=firework_sound) -> None:
        super().__init__(image=image, sound=sound)
        self.radius: int = 1
        self.sound: pg.mixer.Sound = sound

    def __eq__(self, other) -> bool:
        return super().__eq__(other=other)

    def __hash__(self) -> None:
        return super().__hash__()

    def explode(self, index: int, swapped_item_index: int) -> None:
        global count
        if gems_scheme[swapped_item_index] == 11:
            gems_scheme[swapped_item_index] = None
            substitute: list[int] = choices(range(FIELD_AREA), k=5)
            for idx in substitute:
                gems_scheme[idx] = gems_scheme[index]
            
            for idx in substitute:
                if gems_scheme[idx] is not None:
                    numbers_to_images[gems_scheme[idx]].explode(idx, idx)
            return

        pg.mixer.Sound.play(self.sound)
        row: int; column: int
        row, column = row_column_from_index(index)
        if coords[index][0] == coords[swapped_item_index][0]:
            whole_row_indices: Generator[int] = (i for i in 
                                                 range((row - 1) * GAPS, 
                                                       row * GAPS))
            for idx in whole_row_indices:
                if gems_scheme[idx] in {9, 10} and idx != index:
                    numbers_to_images[gems_scheme[idx]].explode(idx, idx)
                else:
                    gems_scheme[idx] = None
        else:
            whole_column_indices: Generator[int] = ((column - 1) + (GAPS * r)
                                                    for r in range(GAPS))
            for idx in whole_column_indices:
                if gems_scheme[idx] in {9, 10} and idx != index:
                    numbers_to_images[gems_scheme[idx]].explode(idx, idx)
                else:
                    gems_scheme[idx] = None


class Bomb(Explosive):
    def __init__(self, image: pg.Surface, 
                 sound: pg.mixer.Sound | None = bomb_sound) -> None:
        super().__init__(image=image, sound=sound)
        self.radius: int = 1
        self.sound: pg.mixer.Sound = sound

    def __eq__(self, other) -> bool:
        return super().__eq__(other=other)
    
    def __hash__(self) -> None:
        return super().__hash__()

    def explode(self, index: int, swapped_item_index: int) -> None:
        global count
        if gems_scheme[swapped_item_index] == 11:
            gems_scheme[swapped_item_index] = None
            substitute: list[int] = choices(range(FIELD_AREA), k=5)
            for idx in substitute:
                gems_scheme[idx] = gems_scheme[index]
            
            for idx in substitute:
                if gems_scheme[idx] is not None:
                    numbers_to_images[gems_scheme[idx]].explode(idx, idx)
            return

        pg.mixer.Sound.play(self.sound)
        row: int; column: int
        row, column = row_column_from_index(index)

        self.surrounding: set[int] = ({i for i in range(index - self.radius, 
        index + self.radius + 1) if row_column_from_index(i)[0] == row}
        .union(*[set([i for i in range(index - self.radius - GAPS * offset, 
        index + self.radius - GAPS * offset + 1) if row_column_from_index(i)[0] 
        == row - 1 and row_column_from_index(i)[1] in {column, column + offset,
        column - offset}] + [i for i in range(index - self.radius + GAPS * 
        offset, index + self.radius + GAPS * offset + 1) if 
        row_column_from_index(i)[0] == row + 1 and row_column_from_index(i)[1] 
        in {column, column + 1, column - 1}]) for offset in 
        range(self.radius + 1)]))

        for idx in self.surrounding:
            if idx in range(FIELD_AREA):
                if gems_scheme[idx] in \
                {9, 10} and idx != index:
                    numbers_to_images[gems_scheme[idx]].explode(idx, idx)
                else:
                    gems_scheme[idx] = None


class Lightning(Explosive):
    global count
    def __init__(self, image: pg.Surface,
                 sound: pg.mixer.Sound | None = lightning_sound) -> None:
        super().__init__(image=image, sound=sound)
        self.sound = sound

    def __eq__(self, other) -> bool:
        return super().__eq__(other=other)
    
    def __hash__(self) -> None:
        return super().__hash__()
    
    def explode(self, index: int, swapped_item_index: int) -> None:
        global gems_scheme
        pg.mixer.Sound.play(self.sound)
        if gems_scheme[swapped_item_index] == 11:
            for i, object in enumerate(gems_scheme):
                gems_scheme[i] = None
        elif gems_scheme[swapped_item_index] in {9, 10}:
            gems_scheme[index] = None
            substitute: list[int] = choices(range(FIELD_AREA), k=5)
            for idx in substitute:
                gems_scheme[idx] = gems_scheme[swapped_item_index]
                
            for idx in substitute:
                if gems_scheme[idx] is not None:
                    numbers_to_images[gems_scheme[idx]].explode(idx, idx)
            return
        gems_scheme[index] = None
        self.indices_to_remove: set[int] = {idx for idx, gem 
                                            in enumerate(gems_scheme) 
                                            if gem == 
                                            gems_scheme[swapped_item_index]}
            
        for idx in self.indices_to_remove:
            gems_scheme[idx] = None
                

firework: Firework = Firework(pg.transform.scale(
    pg.image.load(r"Images\Firework.png"), (GEM_SCALE, GEM_SCALE)))
bomb: Bomb = Bomb(pg.transform.scale(pg.image.load(r"Images\Bomb.png"), 
                                     (GEM_SCALE, GEM_SCALE)))
lightning: Lightning = Lightning(pg.transform.scale(pg.image.load\
                                                    (r"Images\Lightning.png"),
                                     (GEM_SCALE, GEM_SCALE)))