# **BitmapClass v1.0.0**

### *Python (educational project)*

Provide bitmap file (.bmp) management tools

Supported bitmap file
- Color depth: 1, 4, 8, or 24 (bpp)
- Bitmap width: 1 ~ 4096 (pixels)
- Bitmap height: 1 ~ 4096 (pixels)
- File size: 58 ~ 50331702 (bytes)
- Plan count: 1 (only)
- Compressed file: Unsupported


## **Usages**

##### >  *Module import*
```py
from modules.bitmapfile import *
```

##### >  *Create bitmap object*
```py
pic = Bmpfile()
```


### **Object management**

##### >  *Create bitmap*
```py
boolean = pic.create(width, height, color_depth)
```
*Initialise a new bitmap file structure, return **True** if success or **False** if error*

##### >  *Load bitmap*
```py
boolean = pic.open(filepath)
```
*Load bitmap file structure from file (.bmp), return **True** if success or **False** if error*

##### >  *Save bitmap*
```py
boolean = pic.saveas(filepath, replace)
```
*Save bitmap file structure to file (.bmp), return **True** if success or **False** if error*

##### >  *Clean bitmap*
```py
pic.clean()
```
*Set bitmap file structure with initial values (w1 h1 @24bpp)*


### **Errors management**

##### >  *Get current errors list*
```py
array = pic.err_lst()
```

##### >  *Get current errors string*
```py
string = pic.err_str()
```

##### >  *Get current errors count*
```py
integer = pic.err_count()
```

##### >  *Clear current errors list*
```py
pic.err_clear()
```


### **Structure informations**

##### >  *Get bitmap file structure information dictionary*
```py
dictionary = pic.info_dict()
```

##### >  *Get bitmap file structure information string*
```py
string = pic.info_str()
```

##### >  *Get bitmap palette information list*
```py
array = pic.pal_info()
```

##### >  *Get bitmap palette information string*
```py
string = pic.pal_infostr()
```

##### >  *Get file base name (Without extension)*
```py
string = pic.filebasename()
```


### **Palette management**

##### >  *Palette initialisation with standard colors (paint palette)*
```py
pic.pal_stdinit()
```

##### >  *Get bitmap palette index color*
```py
integer = pic.pal_getcolor(index)
```
*Return bitmap palette index color (0xRRGGBB) or (-1) if index is out of bounds*

##### >  *Set bitmap palette index color*
```py
pic.pal_setcolor(index, color)
```
*Set bitmap palette index color (0xRRGGBB) if index isn't out of bounds*


### **Bitmap management**

##### >  *Bitmap initialisation with standard background color (white)*
```py
pic.bmp_stdinit()
```

##### >  *Get pixel color*
```py
color = pic.pixelcolor(x, y, truecolor)
```
*If pixel (x, y) is in GFX area, returns its color, otherwise returns (-1) (Pixel doesn't exists)*
*For 1, 4, 8 bpp: returns the palette color index or the true RGB color if (truecolor) is set to **True***
*For 24 bpp: always returns the true RGB color (0xRRGGBB)*

##### >  *Set pixel color*
```py
pic.drawpixel(x, y, color)
```
*If pixel (x, y) is in GFX area, sets its color (color), otherwise does nothing*
*# *For 1, 4, 8 bpp: (color) is the palette color index*
*# *For 24 bpp: (color) is the true RGB color (0xRRGGBB)*


## **Repository files**

| Path                               | Description                       |
|------------------------------------|-----------------------------------|
| ./modules/bitmapfile.py            | Bitmap Class Module               |
| ./Docs/Bmpfile Class Doc.txt       | Class description                 |
| ./Docs/Bitmap File Structure.pdf   | Bitmap File Structure description |
| ./BitmapClass_Usages.pyw           | Usage exemple                     |
| ./README.md                        | This file                         |
