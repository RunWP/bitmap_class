
################################################################################
#                              Bitmap Class Usage                              #
################################################################################

# Usage of Bitmap class


################################################################################
#                                    IMPORTS                                   #
################################################################################

from tkinter import *

from modules.bitmapfile import *


################################################################################
#                                   FUNCTIONS                                  #
################################################################################

def show_pixel_info(pic, x, y):
    # Description
    # ------------------------------------------------------
        c = pic.pixelcolor(x, y, False)
        t = pic.pixelcolor(x, y, True)
        print(f"Pixel({x}, {y}), ColorIndex: 0x{c:02X}, TrueColor: 0x{t:06X}")


################################################################################

def button1_click():
    # Description
    # ------------------------------------------------------
    lst = [
        (32, 32, 1), (24, 24, 1), (16, 16, 1), (8, 8, 1),
        (8, 8, 4), (6, 6, 4), (4, 4, 4), (2, 2, 4),
        (4, 4, 8), (3, 3, 8), (2, 2, 8), (1, 1, 8),
        (4, 4, 24), (1, 1, 24), (2, 2, 24), (3, 3, 24)
        ]

    pic = Bmpfile()

    print("\ncreate, drawpixel, saveas")
    print("############################################################")

    print("Input List Length:", len(lst))

    for n, tpl in enumerate(lst, 1):
        w, h, bpp = tpl

        if pic.create(w, h, bpp):

            for i in range(0, w):
                pic.drawpixel(i, i, 0x00)

            p = f"Tst/Test_{bpp:02d}_{pic.bytplna}_{w}x{h}.bmp"
            if not pic.saveas(p, False):
                print(f"{n:02d} - {p} - Error: {pic.err_lst()[0][0]}")

            else:
                print(f"{n:02d} - {p} - Saved: {pic.filelen()}")

        else:
            print(f"{n:02d} - Create Error: {pic.err_lst()[0][0]}")


################################################################################

def button2_click():
    # Description
    # ------------------------------------------------------
    pic = Bmpfile()

    print("\nopen, info, pixelcolor")
    print("############################################################")

    p = f"Tst/Palette_08_16x16.bmp"
    if pic.open(p):

        print("info_str")
        print(pic.info_str())

        print("**************************************************")
        print("pal_infostr")
        print("   Index: #Color")
        print(pic.pal_infostr())

        print("**************************************************")
        print("pixelcolor")
        show_pixel_info(pic, 0, 0)
        show_pixel_info(pic, 15, 15)

    else:
        print(f"Open Error: {pic.err_lst()[0][0]}")


################################################################################
#                                     MAIN                                     #
################################################################################

# Create UserForm (Tkinter Window)
userform = Tk()
userform.title("Bitmap Class Usage")
userform.geometry("740x150")
userform.resizable(width=False, height=False)
userform.config(background='#404040')

# Create Frame in UserForm
frame = Frame(userform, bg='#404040')
frame.pack(expand=YES)

# Create Button in Frame
button1 = Button(frame, text="Create, Drawpixel, Saveas", font=("Arial", 20), bg='#808080', fg='#101010', command=button1_click)
button1.grid(row=0, column=0, padx=20)

# Create Button in Frame
button2 = Button(frame, text="Open, Info, Pixelcolor", font=("Arial", 20), bg='#808080', fg='#101010', command=button2_click)
button2.grid(row=0, column=1, padx=20)

# Display UserForm
userform.mainloop()


################################################################################
#                                      EOF                                     #
################################################################################
