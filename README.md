# SavaCrush 1.0.1

## Installation instructions

Windows only instruction below. In case your operational system differs, I recommend you recreate the executable from the main_code.py file.

The user is to ensure that every file is in the correct directory.
The game folder should consist of 3 units: "Images" and "Sounds" folders (notice that all the names are case sensitive), and an executable, each located in the same directory. The "Images" folder should contain the following files: "Blue_gem.png", "Bruise_gem.png", "Cyan_gem.png", "Magenta_gem.png", "Orange_gem.png", "Purple_gem.png" (Not required in this version), "Red_gem.png", "Green_gem.png", "Icon.ico", "Lightning.png", "Firework.png", "Bomb.png". The "Sounds" folder must consist of "Forbidden.mp3", "Forbidden2.mp3", "Gem_sound.wav", "Gem_sound2.wav", "Gem_sound3.mp3", "Gem_sound4.wav", "Lightning_sound.wav", "Firework_sound.wav", "Bomb_sound.wav". In case you downloaded the zip file, everything should be organized for you. The order in each folder and the folders themselves doesn't matter. After reassuring yourself of integrity of the assets, run the executable and the game should start.

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
│ ├── Gem_sound.mp3
│ ├── Gem_sound2.mp3
│ ├── Gem_sound3.mp3
│ ├── Gem_sound4.mp3
│ ├── Firework_sound.mp3
│ ├── Bomb_sound.mp3
│ └── Lightning_sound.mp3
├── assets.py
├── functionality.py
├── game_objects.py
└── SavaCrush.exe

## System requirements

Hardware requirements threshold is low, thanks to the simplicity of SavaCrush. Tested on Windows, but should work on other operational systems as well, 
just make sure to recreate the executable from source.

## How to play this game

The SavaCrush game is similar to popular Candy Crush. It was called SavaCrush in honor of its developer (scroll down for further information). 
The game is pretty easy and play: just swap the objects. When gems get stacked together in a row or a column of 3 or more, they disintegrate, 
forming a special explosive according to their amount, with 4 in a row forming a firework, 4 in a column - a bomb and 5 in a row or column - 
a lightning (although this setup is temporary and can be changed at any given time). Fireworks destroy everything on the row or column that they're 
currently on right after swapping them with anything. Swapping them horizontally will result in destoying the row, whereas vertical swaps destroy 
the column. Bombs remove 3 by 3 grid after being triggered. Lightnings are the simplest: they break objects of the type they were merged with.

## For fellow programmers

The SavaCrush game is built in python 3.13.5. Frameworks used: Pygame 2.6.1. Rebuilding from source is possible with special packages, such as pyinstaller.

```powershell
pyinstaller --onefile "C:\Users\user\Folder\main_code.py" --windowed --icon="C:\Users\user\Folder\Images\Icon.ico" --name "SavaCrush"
```

## New features for this version (1.0.1)

### Optimization
1. The row checks got more optimized and now they skip the last items in each row
2. Switched from storing pygame Surfaces to storing integers and accounting them to references to images, which saves memory
3. Made bomb area lookup more robust

### Game mechanics
1. Added chain triggering to explosives
2. Added new combinations: Now lighting can interact with other explosives. It summons 5 of the explosive it was mingled with and activates them instantly
   Two lightnings destroy the whole field
3. Corrected the logic of destroying row matches. It used to skip the last 3 or for indices (lower right corner) which made the gems get stuck there

### Other
1. Temporarily removed the count
2. Split the code into 4 files for better sustainability
3. Corrected the TOML file
4. Converted all the WAVE into mp3 files

## What is planned to be added?

1. Optimizations with Rust programming language (python can't solve everything)
2. Animations
3. Your suggestions, if I find them sensible

## Credits

Developer - Sava2008
Designer - Sava2008
Images - AI generated
Sounds - Extracted from free sources

### Tools
Programming language - python 3.13.5
Dependencies - pygame 2.6.1
