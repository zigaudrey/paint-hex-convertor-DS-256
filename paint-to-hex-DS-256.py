import os
from PIL import Image
from tkinter import filedialog
import struct
from math import floor

pal_file = ""
pal_file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Palette Image", filetype=(('PNG file', '*.png'),('BMP file', '*.bmp'),("ALL file",'*.*')))

if len(pal_file)!=0:
    list_colors = []
    openpal = Image.open(pal_file).convert("RGB")
    wp,hp = openpal.size

    BGR_pal = bytearray()
    
    if wp * hp == 256:
        R, G, B = 0, 0, 0
        for y in range(0,hp):
            for x in range (0,wp):
                R, G, B = openpal.getpixel((x,y))
                list_colors.append((R, G, B))
                R, G, B = floor(R // 8), floor(G // 8), floor(B // 8)
                BGR_pal += struct.pack("<L", (B * 32 * 32) + (G * 32) + R )[:2]

        if list_colors.count(list_colors[0]) != 512:

            bit_paint = bytearray()
            targ_file = ""
            targ_file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Picture", filetype=(('PNG file', '*.png'),('BMP file', '*.bmp'),("ALL file",'*.*')))
            new_bin_file = ""

            if len(targ_file) != 0 :

                openpic = Image.open(targ_file).convert("RGB")
                w,h = openpic.size

                if w % 8 == 0 and h % 8 == 0:

                    n=len(targ_file)-6
                    while n!= 0 and targ_file[n] != '/':
                        new_bin_file = targ_file[n] + new_bin_file
                        n -= 1

                    for y in range(0, h, 8):
                        for x in range (0, w, 8):
                            for iz in range(0, 8):
                                for ix in range(0, 8):
                                    RGB = openpic.getpixel((x+ix,y+iz))             
                                    bin_color = struct.pack("B", list_colors.index(RGB))
                                    bit_paint += bin_color
                    confirm = ""

                    while confirm == "":
                        confirm = str(input("Create Nitro Files? (y/n)")).lower()
                        if confirm != "y" and confirm != "n":
                            confirm = ""

                    if confirm == "y":
                        NCGR_size = struct.pack("<L", 64 + len(bit_paint))[:2]
                        NCGR_header = b'RGCN\xFF\xFE\x00\x01' + NCGR_size + b'\x00\x00\x10\x00\x01\x00RAHC\x20\x18\x00\x00' + struct.pack("<L", h // 8 )[:2] + struct.pack("<L", w // 8 )[:2] + b'\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + struct.pack("<L", w * h ) + b'\x18\x00\x00\x00'

                        out_file = open(new_bin_file + " Sprite.NCGR", "wb+")
                        out_file.write(NCGR_header + bit_paint)
                        out_file.close()

                        NCLR_header = b'RLCN\xFF\xFE\x00\x01' + struct.pack("<L", len(BGR_pal) + 40) + b'\x10\x00\x01\x00TTLP' + struct.pack("<L", len(BGR_pal) + 24) + b'\x04\x00\x00\x00\x00\x00\x00\x00' + struct.pack("<L", len(BGR_pal)) + b'\x10\x00\x00\x00'

                        out_file = open(new_bin_file + " DS Pal.NCLR", "wb+")
                        out_file.write(NCLR_header + BGR_pal)
                        out_file.close()

                        print("Pic and Pal Nitro files done!")
                        
                    else:
                        out_file = open(new_bin_file + " Sprite.bin", "wb+")
                        out_file.write(bit_paint)
                        out_file.close()

                        out_file = open(new_bin_file + " Pal.bin", "wb+")
                        out_file.write(BGR_pal)
                        out_file.close()
                    
                        print("Pic and Pal Bin files done!")

                else:

                    print("Both Image Dimensions isn't a divisible of 8")
        else:
             print("Palette File Empty")   

    else:
        if wp * hp > 16:
            print("The palette Picture exceed 256 colors")
        else:
            print("The palette Picture is too small")

else:
    print("No Palette Picture Selected")
