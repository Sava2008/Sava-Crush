use crate::assets::{COORDS, FIELD_AREA, GAPS, GEM_SCALE, Rgbcolor, SIDE_LEN};
use crate::helper_funcs::{index_to_coords, swap_with};
use crate::objects::{
    Bomb, Firework,
    GameObject::{self, AnyGem, Explosive1, Explosive2, Explosive3, Null},
    Gem, Lightning, Void,
};
use ggez::{
    Context, GameResult,
    graphics::{self, Mesh},
    mint::Point2,
};
use rand::rngs::ThreadRng;
use rand::{Rng, rng};

pub fn background(context: &mut Context) -> GameResult<Mesh> {
    return Mesh::new_rectangle(
        context,
        graphics::DrawMode::fill(),
        graphics::Rect::new(0., 0., SIDE_LEN, SIDE_LEN),
        Rgbcolor::Field.ggez_color(),
    );
}

pub fn vertical_outline(context: &mut Context) -> GameResult<Mesh> {
    let mut vertical_points: Vec<Point2<f32>> = Vec::new();

    for i in 0..=GAPS {
        let pos: f32 = (GEM_SCALE * i) as f32;
        if i % 2 == 0 {
            vertical_points.extend_from_slice(&[
                Point2 { x: pos, y: 0. },
                Point2 {
                    x: pos,
                    y: SIDE_LEN,
                },
            ]);
        } else {
            vertical_points.extend_from_slice(&[
                Point2 {
                    x: pos,
                    y: SIDE_LEN,
                },
                Point2 { x: pos, y: 0. },
            ]);
        }
    }
    let vertical_mesh: Mesh =
        Mesh::new_line(context, &vertical_points, 2., Rgbcolor::Border.ggez_color())?;

    return Ok(vertical_mesh);
}

pub fn horizontal_outline(context: &mut Context) -> GameResult<Mesh> {
    let mut horizontal_points: Vec<Point2<f32>> = Vec::new();

    for i in 0..=GAPS {
        let pos: f32 = (GEM_SCALE * i) as f32;
        if i % 2 == 0 {
            horizontal_points.extend_from_slice(&[
                Point2 { x: 0., y: pos },
                Point2 {
                    x: SIDE_LEN,
                    y: pos,
                },
            ]);
        } else {
            horizontal_points.extend_from_slice(&[
                Point2 {
                    x: SIDE_LEN,
                    y: pos,
                },
                Point2 { x: 0., y: pos },
            ]);
        }
    }
    let horizontal_mesh: Mesh = Mesh::new_line(
        context,
        &horizontal_points,
        2.,
        Rgbcolor::Border.ggez_color(),
    )?;

    return Ok(horizontal_mesh);
}

pub fn selection(context: &mut Context, idx: Option<usize>) -> GameResult<Mesh> {
    let coordinates: (f32, f32) = index_to_coords(idx.unwrap());
    return graphics::Mesh::new_rectangle(
        context,
        graphics::DrawMode::stroke(3.),
        graphics::Rect::new(
            coordinates.0,
            coordinates.1,
            GEM_SCALE as f32,
            GEM_SCALE as f32,
        ),
        Rgbcolor::Selection.ggez_color(),
    );
}

pub fn gems_positions(board: &[GameObject; FIELD_AREA]) -> Vec<(usize, usize)> {
    let mut gem_indices: Vec<(usize, usize)> = Vec::new();
    for (index, gem) in board.iter().enumerate() {
        if !gem.is_void() {
            gem_indices.push((index, gem.get_placeholder()));
        }
    }
    return gem_indices;
}

pub fn generate_gems(board: &mut [GameObject; FIELD_AREA], thread_rng: &mut ThreadRng) -> () {
    for idx in 0..GAPS as usize {
        if board[idx].is_void() {
            board[idx] = AnyGem(Gem::new(thread_rng.random_range(0..=7), idx));
        }
    }
}

pub fn gravity(board: &mut [GameObject; FIELD_AREA]) -> () {
    for idx in (0..FIELD_AREA - GAPS).rev() {
        if !board[idx].is_void() && board[idx + GAPS].is_void() {
            swap_with(board, idx, idx + GAPS);
        }
    }
}

pub fn destroy_gems(board: &mut [GameObject; FIELD_AREA]) -> () {
    for m in (3..=5).rev() {
        let row_check_generator: Vec<usize> = (0..board.len())
            .filter(|num: &usize| {
                let modulus: usize = (*num + 1) % GAPS;
                match m {
                    5 => ![0, GAPS - 1, GAPS - 2, GAPS - 3].contains(&modulus),
                    4 => ![0, GAPS - 1, GAPS - 2].contains(&modulus),
                    _ => ![0, GAPS - 1].contains(&modulus),
                }
            })
            .map(|num: usize| num as usize)
            .collect();
        for idx in row_check_generator {
            // row checks
            if !board[idx].is_void()
                && ((1..m).all(|x: usize| board[idx] == board[idx + x]))
                && ((1..m).all(|x: usize| COORDS[idx].y == COORDS[idx + x].y))
            {
                for i in 0..m {
                    board[idx + i] = Null(Void::new(idx + i));
                }
                match m {
                    4 => board[idx + 1] = Explosive1(Firework::new(idx + 1)),
                    5 => board[idx + 2] = Explosive3(Lightning::new(idx + 2)),
                    _ => (),
                }
            }
        }

        let col_check_generator: Vec<usize> = (0..(board.len() - GAPS * (m - 1))).collect();
        for idx in col_check_generator {
            // column check
            if !board[idx].is_void() && (1..m).all(|x: usize| board[idx] == board[idx + GAPS * x]) {
                for i in 0..m {
                    board[idx + GAPS * i] = Null(Void::new(idx + GAPS * i));
                }
                match m {
                    4 => board[idx + GAPS] = Explosive2(Bomb::new(idx + GAPS)),
                    5 => board[idx + GAPS * 2] = Explosive3(Lightning::new(idx + GAPS * 2)),
                    _ => (),
                }
            }
        }
    }
}

pub fn check_matches(mut board: [GameObject; FIELD_AREA]) -> bool {
    for idx in 0..board.len() - 1 {
        if board[idx].is_explosive() {
            return true;
        }
        if COORDS[idx].x == COORDS[idx + 1].x {
            swap_with(&mut board, idx, idx + 1);
            destroy_gems(&mut board);
            if board.iter().any(|gem: &GameObject| gem.is_void()) {
                return true;
            }
            swap_with(&mut board, idx, idx + 1);
        }
    }
    for idx in 0..board.len() - GAPS {
        swap_with(&mut board, idx, idx + GAPS);
        destroy_gems(&mut board);
        if board.iter().any(|gem: &GameObject| gem.is_void()) {
            return true;
        }
        swap_with(&mut board, idx, idx + GAPS);
    }
    return false;
}

pub fn legit_swap(mut board: [GameObject; FIELD_AREA], idx1: usize, idx2: usize) -> bool {
    let (row1, col1, row2, col2) = (
        idx1 % GAPS + 1,
        idx1 / GAPS + 1,
        idx2 % GAPS + 1,
        idx2 / GAPS + 1,
    );
    if (row1 == row2 && col1 == col2 - 1)
        || (row1 == row2 && col1 == col2 + 1)
        || (row1 == row2 - 1 && col1 == col2)
        || (row1 == row2 + 1 && col1 == col2)
    {
        if board[idx1].is_explosive() || board[idx2].is_explosive() {
            return true;
        }
        swap_with(&mut board, idx1, idx2);
        destroy_gems(&mut board);
        if board.iter().any(|el: &GameObject| el.is_void()) {
            return true;
        }
    }

    return false;
}

pub fn shuffle(array: &mut [GameObject; FIELD_AREA]) -> () {
    let mut thread: rand::prelude::ThreadRng = rng();
    for i in (1..FIELD_AREA).rev() {
        swap_with(array, i, thread.random_range(0..i + 1));
    }
}
