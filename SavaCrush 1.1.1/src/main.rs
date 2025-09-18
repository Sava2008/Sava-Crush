#![windows_subsystem = "windows"]

use ggez::{
    self, Context, ContextBuilder, GameResult, conf, event,
    graphics::{self, Mesh},
    input::mouse::{self, button_pressed, position},
    mint::Point2,
};
use rand::rng;
use std::env::current_dir;
use std::time::{Duration, Instant};

mod assets;
mod functionality;
mod helper_funcs;
mod objects;
use assets::{COORDS, GAPS, MainState, Mode, Phase, Rgbcolor, SIDE_LEN, Sounds, Swap, WIN_SCALES};
use functionality::{
    background, check_matches, destroy_gems, gems_positions, generate_gems, gravity,
    horizontal_outline, legit_swap, selection, shuffle, vertical_outline,
};
use helper_funcs::{
    define_swap_direction, explosive_index, generate_board, get_index_of, load_images, swap_with,
};
use objects::GameObject;

impl MainState {
    fn new(context: &mut Context) -> GameResult<Self> {
        return Ok(MainState {
            all_images: load_images(context),
            board: generate_board(),
            mode: Mode::Selection,
            selection_index: None,
            swapping_index: None,
            mouse_down: false,
            mouse_pressed: false,
            phase: Phase::Destruction,
            any_nones_on_board: true,
            destroyed: true,
            checked_matches: true,
            bg_mesh: background(context)?,
            horizontal_outline_mesh: horizontal_outline(context)?,
            vertical_outline_mesh: vertical_outline(context)?,
            last_update: Instant::now(),
            update_interval: Duration::from_millis(1),
            sounds: Sounds::new(context)?,
            mouse_pos: Point2 { x: 0.0, y: 0.0 },
            random: rng(),
        });
    }

    fn perform_selection(&mut self) -> GameResult {
        self.selection_index = get_index_of(&self.mouse_pos);
        self.mode = Mode::Swapping;
        self.phase = Phase::Idle;
        return Ok(());
    }

    fn perform_swapping(&mut self, context: &mut Context) -> GameResult {
        self.swapping_index = get_index_of(&self.mouse_pos);
        let (idx1, idx2) = (self.selection_index.unwrap(), self.swapping_index.unwrap());

        if legit_swap(self.board, idx1, idx2) {
            swap_with(&mut self.board, idx1, idx2);
            let explosive_idx: (Option<usize>, usize) = explosive_index(&self.board, idx2, idx1);
            if let Some(i) = explosive_idx.0 {
                match self.board[i].get_placeholder() {
                    8 => {
                        GameObject::explode(
                            i,
                            define_swap_direction(idx1 as isize, idx2 as isize),
                            &mut self.board,
                            explosive_idx.1,
                            &mut self.sounds,
                            context,
                        )?;
                    }
                    9 => {
                        GameObject::explode(
                            i,
                            Swap::Horizontal,
                            &mut self.board,
                            explosive_idx.1,
                            &mut self.sounds,
                            context,
                        )?;
                    }
                    10 => {
                        GameObject::explode(
                            i,
                            Swap::Horizontal,
                            &mut self.board,
                            explosive_idx.1,
                            &mut self.sounds,
                            context,
                        )?;
                    }
                    _ => (),
                }
            } else {
                self.sounds.play_gem_sound(context)?;
            }
            (self.selection_index, self.swapping_index) = (None, None);
            self.destroyed = false;
            self.mode = Mode::Selection;
        } else {
            self.selection_index = get_index_of(&self.mouse_pos);
            self.mode = Mode::Swapping;
        }
        return Ok(());
    }

    fn handle_input(&mut self, context: &mut Context) -> GameResult {
        if self.mouse_pressed && !self.mouse_down {
            self.mouse_pos = position(context);

            if self.mouse_pos.x <= SIDE_LEN as f32 && self.mouse_pos.y <= SIDE_LEN as f32 {
                match self.mode {
                    Mode::Selection => {
                        self.perform_selection()?;
                    }
                    Mode::Swapping => {
                        self.perform_swapping(context)?;
                    }
                }
            } else {
                self.sounds.play_oof_sound(context)?;
                self.mode = Mode::Selection;
            }
        }
        self.mouse_down = self.mouse_pressed;
        return Ok(());
    }
    fn toggle_events(&mut self, _context: &mut Context) -> GameResult {
        if !self.any_nones_on_board {
            if self.checked_matches {
                self.phase = Phase::Destruction;
            }
            if self.mode == Mode::Selection {
                match self.phase {
                    Phase::Destruction if !self.destroyed => {
                        destroy_gems(&mut self.board);
                        self.destroyed = true;
                        self.phase = Phase::MatchCheck;
                        self.checked_matches = false;
                    }
                    Phase::MatchCheck => {
                        if !check_matches(self.board) {
                            shuffle(&mut self.board);
                        }
                        self.phase = Phase::Idle;
                        self.checked_matches = true;
                    }
                    _ => (),
                };
            }
        } else {
            gravity(&mut self.board);
            self.destroyed = false;
        }
        return Ok(());
    }
}

impl event::EventHandler for MainState {
    fn update(&mut self, context: &mut Context) -> GameResult {
        let current: Instant = Instant::now();
        self.any_nones_on_board = self.board.iter().any(|el: &GameObject| el.is_void());

        if !self.any_nones_on_board {
            self.mouse_pressed = button_pressed(context, mouse::MouseButton::Left);
        }
        if current - self.last_update >= self.update_interval {
            if self.board[0..GAPS]
                .iter()
                .any(|el: &GameObject| el.is_void())
            {
                generate_gems(&mut self.board, &mut self.random);
            }
            self.toggle_events(context)?;
            self.last_update = current;
            self.handle_input(context)?;
        }
        return Ok(());
    }

    fn draw(&mut self, context: &mut Context) -> GameResult {
        graphics::clear(context, Rgbcolor::Bg.ggez_color());
        let gem_indices: Vec<(usize, usize)> = gems_positions(&self.board);
        graphics::draw(context, &self.bg_mesh, graphics::DrawParam::default())?;
        graphics::draw(
            context,
            &self.horizontal_outline_mesh,
            graphics::DrawParam::default(),
        )?;
        graphics::draw(
            context,
            &self.vertical_outline_mesh,
            graphics::DrawParam::default(),
        )?;
        for (i, gem) in gem_indices {
            graphics::draw(
                context,
                &self.all_images[gem],
                graphics::DrawParam::default()
                    .dest(COORDS[i])
                    .scale([0.25, 0.25]),
            )?;
        }
        if self.mode == Mode::Swapping {
            let selection_mesh: Mesh = selection(context, self.selection_index)?;
            graphics::draw(context, &selection_mesh, graphics::DrawParam::default())?;
        }

        graphics::present(context)?;
        return Ok(());
    }
}

fn main() -> GameResult {
    let (mut context, mainloop) = ContextBuilder::new("SavaCrush", "Sava2008")
        .window_mode(conf::WindowMode::default().dimensions(WIN_SCALES.0, WIN_SCALES.1))
        .add_resource_path(current_dir()?.join("assets"))
        .build()?;
    let state: MainState = MainState::new(&mut context)?;
    graphics::set_window_title(&context, "SavaCrush 1.1.0");
    event::run(context, mainloop, state);
}
