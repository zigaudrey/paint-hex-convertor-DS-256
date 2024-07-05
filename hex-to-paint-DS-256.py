import os
import struct

from PIL import Image
from tkinter import filedialog

PAL_path = ""
PAL_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Palette/NCLR File", filetype=(('NCLR file', '*.nclr'),('Bin file', '*.bin'),("ALL file",'*.*')))

if len(PAL_path) != 0:
    PAL_open = open(PAL_path, 'rb')
    PAL_data = PAL_open.read()
    PAL_open.close()

    n=len(PAL_path) - 1
    SHORT_pal_name = ""
    while n!= 0 and PAL_path[n] != '.':
        n -= 1
    n -= 1
    while n!= 0 and PAL_path[n] != '/':
        SHORT_pal_name = PAL_path[n] + SHORT_pal_name
        n -= 1
    
    if len(PAL_data) >= 256:

        pal_END = 0
        if PAL_data[0:4] == b'RLCN':
            pal_START = 40
        elif PAL_data[0:4] == b'TTPL':
            pal_START = 24  
        else:
            pal_START = 0

        if b'PMCP' in PAL_data[-22:] :
            pal_END = 22
        else:
            pal_END = 0
        
        if (len(PAL_data) - pal_START - pal_END) % 512 == 0:

            PAL_List = []

            R, G, B = 0, 0, 0

            pal_NUM = 1

            if (len(PAL_data) - pal_START - pal_END) // 512 > 1:
                pal_NUM = 0
                while pal_NUM == 0:
                    print("Choose between palette 1 to", (len(PAL_data) - pal_START - pal_END) // 512 )
                    pal_NUM = int(input(""))
                    if pal_NUM < 1 and pal_NUM > (len(PAL_data) - pal_START - pal_END) // 512:
                        pal_NUM = 0

            pal_POINTER = pal_START + ((pal_NUM - 1) * 512)

            bin_hex = bytearray()
            for i in range(0,512,2):
                Dec_Color = struct.unpack("<L", PAL_data[pal_POINTER + i:pal_POINTER + i+2] + b'\x00\x00')[0]
                B = (Dec_Color // 32 // 32 % 32) * 8
                G = (Dec_Color // 32 % 32) * 8
                R = (Dec_Color % 32) * 8
                PAL_List.append((R, G, B))
                
            if PAL_List[0] in PAL_List[1:]:
                print("The first color is doubled. Change to (0, 224, 224).")
                PAL_List[0] = (0, 224, 224)

            duplicate_col = False
            for i in range(1, len(PAL_List)):
                if PAL_List[1:].count(PAL_List[i]) == 2:
                    duplicate_col = True

            user_color_OPT = ""

            if duplicate_col == True:
                while user_color_OPT == "":
                    user_color_OPT = str(input("Generate a palette with only used colors? (y/n)")).lower()
                    if user_color_OPT == "y" and user_color_OPT == "n" :
                            user_color_OPT = ""

                if user_color_OPT == "y":
                    used_pixel_LIST= []
                    used_colors_LIST = []
            
            BIN_name = ""
            BIN_name = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Sprite/NCGR File", filetype=(('NCGR file', '*.ncgr'),('Bin file', '*.bin'),("ALL file",'*.*')))

            if len(BIN_name) != 0:

                BIN_path = open(BIN_name, "rb")
                BIN_file = BIN_path.read()
                BIN_path.close()
                
                if BIN_file[0:4] == b'RGCN':
                    spr_POINTER = 48
                elif BIN_file[0:4] == b'RAHC':
                    spr_POINTER = 32   
                else:
                    spr_POINTER = 0

                if b'SOPC' in BIN_file[-16:] :
                    spr_END = 16
                else:
                    spr_END = 0

                lenght = len(BIN_file) - spr_POINTER - spr_END
                
                if lenght % 64 == 0:
                    
                    n=len(BIN_name) - 1
                    SHORT_name = ""
                    while n!= 0 and BIN_name[n] != '.':
                        n -= 1
                    n -= 1
                    while n!= 0 and BIN_name[n] != '/':
                        SHORT_name = BIN_name[n] + SHORT_name
                        n -= 1

                    tile_COUNT = 0

                    while tile_COUNT == 0:
                        tile_COUNT = int(input("Choose Tile Number (4 to 32)"))
                        if 4 > tile_COUNT or tile_COUNT > 32 :
                            tile_COUNT = 0
                    
                    BIN_len = lenght + (lenght % (tile_COUNT * 64))
                    w = 8 * tile_COUNT
                    h = BIN_len // (tile_COUNT * 64) * 8

                    OUTCOME= Image.new('RGB', (w , h))
       
                    for y in range(0, h, 8):
                        for x in range (0, w, 8):
                            for iz in range(0, 8):
                                for ix in range(0, 8):
                                    if spr_POINTER < len(BIN_file) - spr_END:
                                        Hex_Data = struct.pack("B", BIN_file[spr_POINTER])[0]
                                        if user_color_OPT == "y":
                                            if not Hex_Data in used_pixel_LIST:
                                                used_pixel_LIST.append(Hex_Data)
                                                used_colors_LIST.append(PAL_List[Hex_Data])
                                        OUTCOME.putpixel((x+ix,y+iz), PAL_List[Hex_Data])
                                        spr_POINTER += 1

                    OUTCOME.save(SHORT_name + " - " + str(tile_COUNT) + " Tiles - " + SHORT_pal_name + " Pal " + str(pal_NUM) + ".png")

                    PAL_OUTCOME= Image.new('RGB', (16 , 16))

                    if user_color_OPT == "y":
                        PAL_USED_COLOR_OUTCOME= Image.new('RGB', (16 , 16))
                        RA, GA, BA = 0, 0, 0
                        for x in range(len(used_colors_LIST)):
                            RA += used_colors_LIST[x][0] / len(used_colors_LIST)
                            GA += used_colors_LIST[x][1] / len(used_colors_LIST)
                            BA += used_colors_LIST[x][2] / len(used_colors_LIST)
                        RA, GA, BA = 256 - round(RA), 256 - round(GA), 256 - round(BA)

                    np = 0
                    for y in range(16):
                        for x in range(16):
                            PAL_OUTCOME.putpixel((x,y), PAL_List[np])
                            if user_color_OPT == "y":
                                if np in used_pixel_LIST:
                                    PAL_USED_COLOR_OUTCOME.putpixel((x,y), PAL_List[np])
                                else:
                                    PAL_USED_COLOR_OUTCOME.putpixel((x,y), (RA, GA, BA))
                            np += 1

                    PAL_OUTCOME.save(SHORT_pal_name + " Pal " + str(pal_NUM)+ ".png")

                    if user_color_OPT == "y":
                        PAL_USED_COLOR_OUTCOME.save(SHORT_pal_name + " - " + SHORT_name + " Used Colors Pal " + str(pal_NUM)+ " .png")                        

                    print("Image and Pal Datas Files Done!")
                            
                else:
                    print("The Sprite Bin File isn't a divisible of 64")

            else:
                print("No Sprite File Selected")

        else:
            print("All Palette doesn't have 256 colors.")

    else:
        print("The Palette Bin is too small")

else:
    print("No NCLR File Selected")
