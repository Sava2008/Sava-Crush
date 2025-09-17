use ggez::GameResult;
use std::cmp::{ max, min };
use rand::{ rng, Rng };
use crate::assets::{ FIELD_AREA, GEM_SCALE, GAPS, Swap, Sounds };
use crate::helper_funcs::{ index_to_coords, indices_of_col, indices_of_row, 
    generate_board };

#[derive(Copy, Clone)]
pub struct Firework {
    placeholder: usize,
    index: usize
}
impl Firework {
    pub fn new(index: usize) -> Self {
        return Firework { placeholder: 8, index };
    }

    pub fn get_idx(&self) -> usize {
        return self.index;
    }

    pub fn set_idx(&mut self, new_index: usize) -> () {
        self.index = new_index;
    }

    pub fn get_placeholder(&self) -> usize {
        return self.placeholder;
    }

    pub fn explode(&self, swap: Swap, board: &mut [GameObject; FIELD_AREA],
        other: usize, sounds: &mut Sounds, context: &mut ggez::Context) -> GameResult {
        let coords: (f32, f32) = index_to_coords(self.index);
        match swap {
            Swap::Horizontal => {
                for x in indices_of_row(coords.1 as usize / GEM_SCALE) {
                    if board[x].is_explosive() && x != self.index {
                        GameObject::explode(x, Swap::Horizontal, board,
                            other, sounds, context)?;
                        sounds.play_firework_sound(context)?;
                    } else {
                        board[x] = GameObject::Null(Void::new(x));
                    }
                }
            },
            Swap::Vertical => {
                for x in indices_of_col(coords.0 as usize / GEM_SCALE) {
                    if board[x].is_explosive() && x != self.index {
                        GameObject::explode(x, Swap::Horizontal, board,
                            other, sounds, context)?;
                    } else {
                        board[x] = GameObject::Null(Void::new(x));
                    }
                }
            },
        }
        sounds.play_firework_sound(context)?;
        return Ok(());
    }
}

#[derive(Copy, Clone)]
pub struct Bomb {
    placeholder: usize,
    index: usize,
}
impl Bomb {
    pub fn new(index: usize) -> Self {
        return Bomb { placeholder: 9, index };
    }

    pub fn get_idx(&self) -> usize {
        return self.index;
    }

    pub fn set_idx(&mut self, new_index: usize) -> () {
        self.index = new_index;
    }

    pub fn get_placeholder(&self) -> usize {
        return self.placeholder;
    }

    pub fn explode(&self, _swap: Swap, board: &mut [GameObject; FIELD_AREA],
        other: usize, sounds: &mut Sounds, context: &mut ggez::Context) -> GameResult {
        for idx in self.bomb_surroundings() {
            if board[idx].is_explosive() && idx != self.get_idx() {
                GameObject::explode(idx, Swap::Horizontal, board, other,
                    sounds, context)?;
                sounds.play_bomb_sound(context)?;
            } else {
                board[idx] = GameObject::Null(Void::new(idx));
            }
        }
        sounds.play_bomb_sound(context)?;
        return Ok(());
    }

    pub fn bomb_surroundings(&self) -> Vec<usize> {
        let mut suroundings: Vec<usize> = Vec::new();
        let (row, col) = (self.index / GAPS, self.index % GAPS);
        let first_row: usize = max(row.saturating_sub(1), 0);
        let first_col: usize = max(col.saturating_sub(1), 0);
        let last_row: usize = min(GAPS - 1, row + 1);
        let last_col: usize = min(GAPS - 1, col + 1);

        for iteration in first_col..=last_col {
            for r in first_row..=last_row {
                suroundings.push(r * GAPS + iteration);
            }
        }

        return suroundings;
    }
}

#[derive(Copy, Clone)]
pub struct Lightning {
    placeholder: usize,
    index: usize,
}
impl Lightning {
    pub fn new(index: usize) -> Self {
        return Lightning { placeholder: 10, index };
    }

    pub fn get_idx(&self) -> usize {
        return  self.index;
    }

    pub fn set_idx(&mut self, new_index: usize) -> () {
        self.index = new_index;
    }

    pub fn get_placeholder(&self) -> usize {
        return self.placeholder;
    }

    pub fn explode(&self, _swap: Swap, board: &mut [GameObject; FIELD_AREA], 
        other: usize, sounds: &mut Sounds, context: &mut ggez::Context) -> GameResult {
        match board[other].get_placeholder() {
            0..=7 => {
                for index in self.all_identical_objects(board, other) {
                    board[index] = GameObject::Null(Void::new(index));
                }
                board[self.index] = GameObject::Null(Void::new(self.index));
            },
            x if x == 8 || x == 9 => {
                let mut thread_rng: rand::prelude::ThreadRng = rng();
                for _ in 0..=4 {
                    let index: usize = thread_rng.random_range(0..FIELD_AREA);
                    board[index] = match x {
                        8 => GameObject::Explosive1(Firework::new(index)),
                        9 => GameObject::Explosive2(Bomb::new(index)),
                        _ => GameObject::Null(Void::new(index)),
                    };
                    GameObject::explode(index, Swap::Horizontal, board, other, sounds, context)?;
                    (board[self.index], board[other]) = (GameObject::Null(Void::new(self.index)), 
                    GameObject::Null(Void::new(other)));
                }
            },
            10 => { *board = generate_board(); },
            _ => (),
        }
        if board[other].get_placeholder() == 10 {
            
        }
        sounds.play_lightning_sound(context)?;
        return Ok(());
    }

    pub fn all_identical_objects(&self, board: &[GameObject; FIELD_AREA],
        other_index: usize) -> Vec<usize> {
        return (0..FIELD_AREA).filter(|index: &usize| board[*index] == board[other_index]).collect();
    }
}

#[derive(Copy, Clone)]
pub struct Gem {
    placeholder: usize,
    index: usize,
}
impl Gem {
    pub fn new(placeholder: usize, index: usize) -> Self {
        return Gem { placeholder, index };
    }

    pub fn get_idx(&self) -> usize {
        return self.index;
    }

    pub fn set_idx(&mut self, new_index: usize) -> () {
        self.index = new_index;
    }

    pub fn get_placeholder(&self) -> usize {
        return self.placeholder;
    }
}

#[derive(Copy, Clone)]
pub struct Void {
    pub index: usize,
}

impl Void {
    pub fn new(index: usize) -> Self {
        return Void { index };
    }

    pub fn get_idx(&self) -> usize {
        return  self.index;
    }

    pub fn set_idx(&mut self, new_index: usize) -> () {
        self.index = new_index;
    }

    pub fn get_placeholder(&self) -> usize {
        return 1000;
    }
}

#[derive(Copy, Clone)]
pub enum GameObject {
    Explosive1(Firework),
    Explosive2(Bomb),
    Explosive3(Lightning),
    AnyGem(Gem),
    Null(Void),
}

impl PartialEq for GameObject {
    fn eq(&self, other: &Self) -> bool {
        return match (self, other) {
            (GameObject::AnyGem(obj1), GameObject::AnyGem(obj2)) => { obj1.placeholder == obj2.placeholder },
            _ => false,
        };
    }
}

impl GameObject {
    pub fn is_void(&self) -> bool {
        matches!(self, GameObject::Null(_))
    }

    pub fn is_gem(&self) -> bool {
        matches!(self, GameObject::AnyGem(_))
    }

    pub fn is_explosive(&self) -> bool {
        return [8, 9, 10].iter().any(|n: &usize| n == &self.get_placeholder());
    }

    pub fn get_placeholder(&self) -> usize {
        return match self {
            GameObject::AnyGem(x) => x.placeholder,
            GameObject::Null(_x) => 1000,
            GameObject::Explosive1(x) => x.placeholder,
            GameObject::Explosive2(x) => x.placeholder,
            GameObject::Explosive3(x) => x.placeholder,
        };
    }

    pub fn get_idx(&self) -> usize {
        return match self {
            GameObject::AnyGem(x) => x.index,
            GameObject::Null(x) => x.index,
            GameObject::Explosive1(x) => x.index,
            GameObject::Explosive2(x) => x.index,
            GameObject::Explosive3(x) => x.index,
        };
    }

    pub fn set_idx(&mut self, new_index: usize) -> () {
        return match self {
            GameObject::AnyGem(x) => { x.index = new_index },
            GameObject::Null(x) => { x.index = new_index },
            GameObject::Explosive1(x) => { x.index = new_index },
            GameObject::Explosive2(x) => { x.index = new_index },
            GameObject::Explosive3(x) => { x.index = new_index },
        };
    }

    pub fn explode(idx: usize, swap: Swap,
        board: &mut [GameObject; FIELD_AREA], other: usize,
        sounds: &mut Sounds, context: &mut ggez::Context) -> GameResult {
        match board[idx] {
            GameObject::Explosive3(x) => x.explode(swap, board, 
                other, sounds, context)?,
            GameObject::Explosive1(x) => x.explode(swap, board, 
                other, sounds, context)?,
            GameObject::Explosive2(x) => x.explode(swap, board, 
                other, sounds, context)?,
            _ => (),
        };
        return Ok(());
    }
}

impl FromIterator<GameObject> for [GameObject; FIELD_AREA] {
    fn from_iter<T: IntoIterator<Item = GameObject>>(iter: T) -> Self {
        let mut iter: <T as IntoIterator>::IntoIter = iter.into_iter();
        return std::array::from_fn(|_| iter.next()
        .expect("Can't unwrap the FromIterator<GameObject> garbage"));
    }
}