use ggez::{ graphics::{ self, ImageGeneric, GlBackendSpec, Mesh }, mint::Point2, audio::{ Source, SoundSource }, 
    Context, GameResult };
use std::time::{ Duration, Instant };
use rand::{ rng, rngs::ThreadRng, Rng };
use crate::objects::GameObject;

pub const GAPS: usize = 9;
pub const FIELD_AREA: usize = (GAPS * GAPS) as usize;
pub const GEM_SCALE: usize = 50;
pub const SIDE_LEN: f32 = (GAPS * GEM_SCALE) as f32;
pub const WIN_SCALES: (f32, f32) = (900., 700.);
pub const COORDS: [Point2<f32>; FIELD_AREA] = generate_coords();

pub enum Rgbcolor {
    Bg,
    Border,
    Field,
    Selection,
}
impl Rgbcolor {
    pub fn ggez_color(&self) -> graphics::Color {
        return match self {
            Rgbcolor::Bg => graphics::Color { r: 0.39, g: 0.78, b: 0.2, a: 1. },
            Rgbcolor::Border => graphics::Color { r: 0.39, g: 0.39, b: 0.39, a: 1. },
            Rgbcolor::Field => graphics::Color { r: 0.88, g: 0.88, b: 0.88, a: 1. },
            Rgbcolor::Selection => graphics::Color { r: 0.08, g: 0.18, b: 0.2, a: 1. },
        };
    }
}

const fn generate_coords() -> [Point2<f32>; FIELD_AREA] {
    let mut coordinates: [Point2<f32>; FIELD_AREA] = [Point2 { x: 0., y: 0. }; FIELD_AREA];
    let mut index: usize = 0;
    while index < FIELD_AREA {
        coordinates[index] = Point2 { x: ((index % GAPS) * GEM_SCALE) as f32, 
            y: ((index / GAPS) * GEM_SCALE) as f32 };
        index += 1;
    }
    return coordinates;
}

#[derive(PartialEq, Eq)]
pub enum Mode {
    Selection,
    Swapping,
}

#[derive(PartialEq, Eq)]
pub enum Phase {
    Destruction,
    MatchCheck,
    Idle,
}

pub enum Swap {
    Horizontal,
    Vertical,
}

pub struct MainState {
	pub all_images: [ImageGeneric<GlBackendSpec>; 11],
	pub board: [GameObject; FIELD_AREA],
	pub mode: Mode,
	pub selection_index: Option<usize>,
	pub swapping_index: Option<usize>,
	pub mouse_down: bool,
	pub mouse_pressed: bool,
    pub phase: Phase,
    pub any_nones_on_board: bool,
    pub destroyed: bool,
	pub bg_mesh: Mesh,
	pub horizontal_outline_mesh: Mesh,
	pub vertical_outline_mesh: Mesh,
	pub last_update: Instant,
	pub update_interval: Duration,
    pub sounds: Sounds,
    pub mouse_pos: Point2<f32>,
}

pub struct Sounds {
    gem_sound1: Source,
    gem_sound2: Source,
    gem_sound3: Source,
    gem_sound4: Source,
    firework_sound: Source,
    bomb_sound: Source,
    lightning_sound: Source,
    out_of_bounds_click_sound1: Source,
    out_of_bounds_click_sound2: Source,
    thread_rng: ThreadRng,
}
impl Sounds {
    pub fn new(context: &mut Context) -> GameResult<Self> {
        return Ok(Sounds { gem_sound1: Source::new(context, "/Sounds/Gem_sound.mp3")?,
        gem_sound2: Source::new(context, "/Sounds/Gem_sound2.mp3")?,
        gem_sound3: Source::new(context, "/Sounds/Gem_sound3.mp3")?,
        gem_sound4: Source::new(context, "/Sounds/Gem_sound4.mp3")?,
        firework_sound: Source::new(context, "/Sounds/Firework_sound.mp3")?,
        bomb_sound: Source::new(context, "/Sounds/Bomb_sound.mp3")?,
        lightning_sound: Source::new(context, "/Sounds/Lightning_sound.mp3")?,
        out_of_bounds_click_sound1: Source::new(context, "/Sounds/Forbidden.mp3")?,
        out_of_bounds_click_sound2: Source::new(context, "/Sounds/Forbidden2.mp3")?,
        thread_rng: rng(), });
    }

    pub fn play_gem_sound(&mut self, context: &mut Context) -> GameResult {
        let sound: i8 = self.thread_rng.random_range(1..=4);
        match sound {
            1 => self.gem_sound1.play(context)?,
            2 => self.gem_sound2.play(context)?,
            3 => self.gem_sound3.play(context)?,
            4 => self.gem_sound4.play(context)?,
            _ => (),
        };
        return Ok(());
    }

    pub fn play_firework_sound(&mut self, context: &mut Context) -> GameResult {
        self.firework_sound.play(context)?;
        return Ok(());
    }

    pub fn play_bomb_sound(&mut self, context: &mut Context) -> GameResult {
        self.bomb_sound.play(context)?;
        return Ok(());
    }

    pub fn play_lightning_sound(&mut self, context: &mut Context) -> GameResult {
        self.lightning_sound.play(context)?;
        return Ok(());
    }

    pub fn play_oof_sound(&mut self, context: &mut Context) -> GameResult {
        let sound: i8 = self.thread_rng.random_range(1..=2);
        match sound {
            1 => self.out_of_bounds_click_sound1.play(context)?,
            2 => self.out_of_bounds_click_sound2.play(context)?,
            _ => (),
        };
        return Ok(());
    }
}