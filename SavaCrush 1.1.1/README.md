# SavaCrush 1.1.1

## Installation instructions

The user is to ensure that every file is in the correct directory.
run the following command in the terminal:
```text
cd C:\Path\Where\You\Put\The\Project && cargo build --release
```
replace the path with what's true in your case

### Example of how files should be organized
SavaCrush/
├── Cargo.toml
├── assets/
  ├── Images/
    ├── Blue_gem.png
    ├── Bruise_gem.png
    ├── Cyan_gem.png
    ├── Magenta_gem.png
    ├── Orange_gem.png
    ├── Purple_gem.png
    ├── Red_gem.png
    ├── Green_gem.png
    ├── Icon.ico
    ├── Lightning.png
    ├── Firework.png
    └── Bomb.png
  ├── Sounds/
    ├── Forbidden.mp3
    ├── Forbidden2.mp3
    ├── Gem_sound.mp3
    ├── Gem_sound2.mp3
    ├── Gem_sound3.mp3
    ├── Gem_sound4.mp3
    ├── Bomb_sound.mp3
    └── Lightning_sound.mp3
├── Cargo.lock
└── src
  ├── assets.rs
  ├── functionality.rs
  ├── helper_funcs.rs
  ├── main.rs
  └── objects.rs

## System requirements

Hardware requirements threshold is low, thanks to the simplicity of SavaCrush. Tested on Windows, but should work on other operational systems as well, just make sure to recreate the executable from source.

## How to play this game

The SavaCrush game is similar to popular Candy Crush. It was called SavaCrush in honor of its developer (scroll down for further information). 
The game is pretty easy and play: just swap the objects. When gems get stacked together in a row or a column of 3 or more, they disintegrate, 
forming a special explosive according to their amount, with 4 in a row forming a firework, 4 in a column - a bomb and 5 in a row or column - 
a lightning (although this setup is temporary and can be changed at any given time). Fireworks destroy everything on the row or column that they're 
currently on right after swapping them with anything. Swapping them horizontally will result in destoying the row, whereas vertical swaps destroy 
the column. Bombs remove 3 by 3 grid after being triggered. Lightnings are the simplest: they break objects of the type they were merged with.

## For fellow programmers

The SavaCrush game is built in Rust 1.89.0, Dependencies used: ggez 0.7.1, rand 0.9.2. Rebuilding from source is possible with the following command:
```text
cd C:\Path\Where\You\Put\The\Project && cargo build --release
```

## New features for this version (1.1.0)

### Optimization
1. Removed redundant check for explosives in check_matches

### Game mechanics
1. Board shuffling now works as expected

### Other
1. Code is now formatted properly

## What is planned to be added?
1. Animations
2. Logging
3. Progress-save mechanics
4. More game objects
2. Your suggestions, if I find them sensible

## Credits

Developer - Sava2008
Designer - Sava2008
Images - AI generated
Sounds - Extracted from free sources

### Tools
Programming language - Rust 1.89.0
Dependencies - ggez 0.7.1, rand 0.9.2

