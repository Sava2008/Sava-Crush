use crate::assets::{FIELD_AREA, GAPS, GEM_SCALE, Swap};
use crate::objects::{
    GameObject::{self, Null},
    Void,
};
use ggez::{
    Context,
    graphics::{GlBackendSpec, Image, ImageGeneric},
    mint::Point2,
};

pub fn index_to_coords(index: usize) -> (f32, f32) {
    return (
        ((index % GAPS) * GEM_SCALE) as f32,
        ((index / GAPS) * GEM_SCALE) as f32,
    );
}

pub fn get_index_of(mouse_pos: &Point2<f32>) -> Option<usize> {
    let x_axis: usize = mouse_pos.x as usize / GEM_SCALE;
    let y_axis: usize = mouse_pos.y as usize / GEM_SCALE;
    return Some(x_axis + y_axis * GAPS);
}

pub fn load_images(context: &mut Context) -> [ImageGeneric<GlBackendSpec>; 11] {
    return [
        Image::new(context, "/Images/Blue_gem.png").unwrap(),
        Image::new(context, "/Images/Bruise_gem.png").unwrap(),
        Image::new(context, "/Images/Cyan_gem.png").unwrap(),
        Image::new(context, "/Images/Green_gem.png").unwrap(),
        Image::new(context, "/Images/Magenta_gem.png").unwrap(),
        Image::new(context, "/Images/Orange_gem.png").unwrap(),
        Image::new(context, "/Images/Purple_gem.png").unwrap(),
        Image::new(context, "/Images/Red_gem.png").unwrap(),
        Image::new(context, "/Images/Firework.png").unwrap(),
        Image::new(context, "/Images/Bomb.png").unwrap(),
        Image::new(context, "/Images/Lightning.png").unwrap(),
    ];
}

pub fn generate_board() -> [GameObject; FIELD_AREA] {
    return (0..FIELD_AREA)
        .map(|index: usize| Null(Void::new(index)))
        .collect();
}

pub fn swap_with(board: &mut [GameObject; FIELD_AREA], a: usize, b: usize) {
    if a == b {
        return;
    }
    let mut first: GameObject = std::mem::replace(&mut board[a], GameObject::Null(Void::new(a)));
    let mut second: GameObject = std::mem::replace(&mut board[b], GameObject::Null(Void::new(b)));
    first.set_idx(b);
    second.set_idx(a);
    board[a] = second;
    board[b] = first;
}

pub fn indices_of_row(row: usize) -> [usize; GAPS] {
    let mut row_indices: [usize; GAPS] = [0; GAPS];
    for idx in 0..GAPS {
        row_indices[idx] = idx + GAPS * row;
    }
    return row_indices;
}

pub fn indices_of_col(col: usize) -> [usize; GAPS] {
    let mut col_indices: [usize; GAPS] = [0; GAPS];
    for idx in 0..GAPS {
        col_indices[idx] = GAPS * idx + col;
    }
    return col_indices;
}

pub fn explosive_index(
    board: &[GameObject; FIELD_AREA],
    idx1: usize,
    idx2: usize,
) -> (Option<usize>, usize) {
    return match (board[idx1].is_explosive(), board[idx2].is_explosive()) {
        (false, false) => (None, idx2),
        (true, false) => (Some(idx1), idx2),
        (false, true) => (Some(idx2), idx1),
        (true, true) => (Some(idx1), idx2),
    };
}

pub fn define_swap_direction(idx1: isize, idx2: isize) -> Swap {
    let isize_gaps: isize = GAPS as isize;
    return match idx1 - idx2 {
        value if value == isize_gaps || value == -isize_gaps => Swap::Vertical,
        value if value == 1 || value == -1 => Swap::Horizontal,
        _ => Swap::Horizontal,
    };
}
