![Paint Hex Convertor DS 256-Colors BANNER](https://github.com/zigaudrey/paint-hex-convertor-DS-256/assets/129554573/69e9857d-8435-48a3-8878-62009225af36)

# Paint-Hex Convertor DS-256 colors
Python Scripts that convert Picture into Bin file and vice-versa for DS 256-Colors Sprite Editing.

# Ressource
### DS
+ **Use [Tinker](https://www.romhacking.net/utilities/817/) to extract NCGR and NCLR.** The NCGR header has to show 04 00 00 00 like below:
![NCGR Header 4 Depth Showing](https://github.com/zigaudrey/paint-hex-convertor-DS-256/assets/129554573/294f6c04-cf5e-4192-b828-ae6b88f7d8e1)

# Setup
1. If you don't have PIL, open the command prompt and install it with PIP
1. Open one of the scripts in command prompt for PIL lib to work

# For Paint-to-hex Script
3. Choose a palette (image). **It have to have a total of 16 pixels**
4. Choose a sprite sheet (image). **Its dimensions should both be a divisible of 8**
+ You can choose to generate Nitro files or bin files
5. **Two bin/Nitro files will be created**, ready to replace data in DS Files

# For Hex-to-paint Script
3. Choose a palette (bin file). **Its lenght has to be 512.** If many, choose the right one that help with edit
+ If there is a duplicate colors, **you can choose to generate another palette image with only used colors**
4. Choose a sprite sheet (bin file). Its lenght has to be a divisble of 64 (one tile)
5. Choose the number of tiles for the width
6. Two (or three) images files will be created, ready to be edited in drawing tools

# Similar tools
+ [Paint - Hex Convertor Scripts (Sega Genesis / Megadrive)](https://github.com/zigaudrey/paint-hex-convertor-MSX)
+ [Paint - Hex Convertor (Gameboy Advance/DS 16-colors)](https://github.com/zigaudrey/paint-hex-convertor-GBA-DS)
