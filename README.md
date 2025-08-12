# SavaCrush 1.0.0

## Installation instructions

Windows only instruction below. In case your operational system differs, I recommend you recreate the executable from the main_code.py file.

The user is to ensure that every file is in the correct directory.
The game folder should consist of 3 units: "Images" and "Sounds" folders (notice that all the names are case sensitive), and an executable, each located in the same directory. The "Images" folder should contain the following files: "Blue_gem.png", "Bruise_gem.png", "Cyan_gem.png", "Magenta_gem.png", "Orange_gem.png", "Purple_gem.png" (Not required in 1.0.0 version), "Red_gem.png", "Green_gem.png", "Icon.ico", "Lightning.png", "Firework.png", "Bomb.png". The "Sounds" folder must consist of "Forbidden.mp3", "Forbidden2.mp3", "Gem_sound.wav", "Gem_sound2.wav", "Gem_sound3.mp3", "Gem_sound4.wav", "Lightning_sound.wav", "Firework_sound.wav", "Bomb_sound.wav". In case you downloaded the zip file, everything should be organized for you. The order in each folder and the folders themselves doesn't matter. After reassuring yourself of integrity of the assets, run the executable and the game should start.

### Example of how files should be organized

SavaCrush/
├── Images/
│ ├── Blue_gem.png
│ ├── Bruise_gem.png
│ ├── Cyan_gem.png
│ ├── Magenta_gem.png
│ ├── Orange_gem.png
│ ├── Purple_gem.png
│ ├── Red_gem.png
│ ├── Green_gem.png
│ ├── Icon.ico
│ ├── Lightning.png
│ ├── Firework.png
│ └── Bomb.png
├── Sounds/
│ ├── Forbidden.mp3
│ ├── Forbidden2.mp3
│ ├── Gem_sound.wav
│ ├── Gem_sound2.wav
│ ├── Gem_sound3.mp3
│ └── Gem_sound4.wav
└── SavaCrush.exe

## System requirements

Hardware requirements threshold is low, thanks to the simplicity of SavaCrush. Tested on Windows, but should work on linux as well, just make sure to recreate the executable from source.

## How to play this game

The SavaCrush game is similar to popular Candy Crush. It was called SavaCrush in honor of its developer (scroll down for further information). The game is pretty easy to use and play: just swap the objects. When gems get stacked together in a row or column of 3 or more, they disintegrate, forming a special explosive according to their amount, with 4 in a column forming a firework, 4 in a row - a bomb and 5 in a row or column - a lightning (although this setup is temporary and can change at any given time). Fireworks destroy everything on the row or column that they're currently on right after swapping them with anything. Swapping them horizontally will result in destoying the row, whereas vertical swaps destroy the column. Bombs remove 3 by 3 grid after being triggered. Lightnings are the simplest: they break objects of the type they were merged with. For each destroyed gem, the player gets +1 point

## For fellow programmers

The SavaCrush game is built in python 3.13.5. Frameworks used: Pygame 2.6.1. Rebuilding from source is possible with special packages, such as pyinstaller.

```powershell
pyinstaller --onefile "C:\Users\user\Folder\main_code.py" --windowed --icon="C:\Users\user\Folder\Images\Icon.ico" --name "SavaCrush"
```

## New features for SavaCrush 1.0.0

1. Implemented explosives of three types: firework, bomb and lightning, each with unique mechanics.
2. Added boundary around selected slot during the game.
3. Purple gem was removed from spawning for balance and better chances of getting an ultimate explosive.
4. Slight optimization, where void is no longer deemed an objects for being destroyed.
5. The gems weren't getting destroyed sometimes, but now they do.

## What is planned to be added?

1. Variety to gameplay (Crates to break by destroying adjacent gems, blocked objects which have to be combined for some times to become accessible, etc.)
2. Optimizations with Rust programming language (python can't solve everything)
3. Animations
4. Rearranging the file structure for better sustainability
5. Your suggestions, if I find them sensible

## Credits

Developer - Sava2008
Designer - Sava2008
Images - AI generated
Sounds - Extracted from free sources

