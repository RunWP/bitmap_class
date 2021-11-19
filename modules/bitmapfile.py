
################################################################################
#                                  BitmapFile                                  #
################################################################################

"""Provide bitmap file (.bmp) management tools"""

################################################################################
#                                    IMPORTS                                   #
################################################################################

from math import ceil, floor
from os.path import abspath, isfile, basename, splitext, getsize, isdir, dirname


################################################################################
#                                   FUNCTIONS                                  #
################################################################################

def int_to_bytlst(intval, intlen):
    """Convert a integer (int) to little-endian byte list (list)"""
    # ------------------------------
    return list(intval.to_bytes(intlen, byteorder='little'))


################################################################################

def bytlst_to_int(bytlst):
    """Convert a little-endian byte list (list) to integer (int)"""
    # ------------------------------
    return int.from_bytes(bytes(bytlst), byteorder='little')


################################################################################
#                                     CLASS                                    #
################################################################################

class Bmpfile:
    """<class 'Bmpfile'> to open and create bitmap file (.bmp)"""
    # ******************************************************

    def __init__(self):
        """Construct a bitmap file structure"""
        # ------------------------------
        # Bitmap Header (hdr)
        self.fletype = 0x4D42              # FileType           W   {Chk} hdrlst[0:2]
        self.flesize = 58                  # FileSize           DW  {Cal} hdrlst[2:6]
        self.reservd = 0                   # Reserved           DW  {Uls} hdrlst[6:10]
        self.bmpofst = 54                  # BitmapOffset       DW  {Cal} hdrlst[10:14]
        self.hdrsize = 40                  # HeaderSize         DW  {Chk} hdrlst[14:18]
        self.bmpwdth = 1                   # BitmapWidth        DW  {Use} hdrlst[18:22]
        self.bmphght = 1                   # BitmapHeight       DW  {Use} hdrlst[22:26]
        self.plnecnt = 1                   # PlanesCount        W   {Chk} hdrlst[26:28]
        self.bitppxl = 24                  # BitsPerPixel       W   {Use} hdrlst[28:30]
        self.comprss = 0                   # Compression        DW  {Chk} hdrlst[30:34]
        self.bmpsize = 4                   # BitmapSize         DW  {Cal} hdrlst[34:38]
        self.hozreso = 0                   # H_Resolution       DW  {Uls} hdrlst[38:42]
        self.vrtreso = 0                   # V_Resolution       DW  {Uls} hdrlst[42:46]
        self.colruse = 0                   # ColorsUsed         DW  {Uls} hdrlst[46:50]
        self.colrimp = 0                   # ColorsImportant    DW  {Uls} hdrlst[50:54]

        # Bitmap Palette (pal)
        self.pal = []                      # PaletteColors      DWA {Use} pallst[0:palsize]

        # Bitmap Data (bmp)
        self.bmp = [255, 255, 255, 0]      # BitmapData         BA  {Use} bmplst[0:bmpsize]

        # Bitmap Useful Properties
        self.flepath = ""                  # FilePath           S   {Use}
        self.bytplne = 4                   # BytesPerLine       DW  {Cal}
        self.bytplnu = 3                   # BytesPerLineUsed   DW  {Cal}
        self.bytplna = 1                   # BytesPerLineAdded  DW  {Cal}
        self.bmpxmin = 0                   # BmpXmin            DW  {Cal}
        self.bmpxmax = 0                   # BmpXmax            DW  {Cal}
        self.bmpymin = 0                   # BmpYmin            DW  {Cal}
        self.bmpymax = 0                   # BmpYmax            DW  {Cal}
        self.palccnt = 0                   # PaletteColorsCount DW  {Cal}
        self.palofst = 54                  # PaletteOffset      DW  {Cal}
        self.palsize = 0                   # PaletteSize        DW  {Cal}

        # Bitmap Error Management
        self.err = []                      # ErrorList          SA  {Use}
        # ------------------------------

    def clean(self):
        """Set bitmap file structure with initial values (w1 h1 @24bpp)"""
        # ------------------------------
        self.__init__()
        # ------------------------------

    def hdr_lst(self):
        """Return bitmap header list format"""
        # ------------------------------
        hdrlst = []
        hdrlst += int_to_bytlst(self.fletype, 2)  # FileType         W   hdrlst[0:2]
        hdrlst += int_to_bytlst(self.flesize, 4)  # FileSize         DW  hdrlst[2:6]
        hdrlst += int_to_bytlst(self.reservd, 4)  # Reserved         DW  hdrlst[6:10]
        hdrlst += int_to_bytlst(self.bmpofst, 4)  # BitmapOffset     DW  hdrlst[10:14]
        hdrlst += int_to_bytlst(self.hdrsize, 4)  # HeaderSize       DW  hdrlst[14:18]
        hdrlst += int_to_bytlst(self.bmpwdth, 4)  # BitmapWidth      DW  hdrlst[18:22]
        hdrlst += int_to_bytlst(self.bmphght, 4)  # BitmapHeight     DW  hdrlst[22:26]
        hdrlst += int_to_bytlst(self.plnecnt, 2)  # PlanesCount      W   hdrlst[26:28]
        hdrlst += int_to_bytlst(self.bitppxl, 2)  # BitsPerPixel     W   hdrlst[28:30]
        hdrlst += int_to_bytlst(self.comprss, 4)  # Compression      DW  hdrlst[30:34]
        hdrlst += int_to_bytlst(self.bmpsize, 4)  # BitmapSize       DW  hdrlst[34:38]
        hdrlst += int_to_bytlst(self.hozreso, 4)  # H_Resolution     DW  hdrlst[38:42]
        hdrlst += int_to_bytlst(self.vrtreso, 4)  # V_Resolution     DW  hdrlst[42:46]
        hdrlst += int_to_bytlst(self.colruse, 4)  # ColorsUsed       DW  hdrlst[46:50]
        hdrlst += int_to_bytlst(self.colrimp, 4)  # ColorsImportant  DW  hdrlst[50:54]

        return hdrlst
        # ------------------------------

    def set_hdr(self, hdrlst):
        """Set bitmap header properties from bitmap header list format"""
        # ------------------------------
        self.fletype = bytlst_to_int(hdrlst[0:2])    # FileType         W
        self.flesize = bytlst_to_int(hdrlst[2:6])    # FileSize         DW
        self.reservd = bytlst_to_int(hdrlst[6:10])   # Reserved         DW
        self.bmpofst = bytlst_to_int(hdrlst[10:14])  # BitmapOffset     DW
        self.hdrsize = bytlst_to_int(hdrlst[14:18])  # HeaderSize       DW
        self.bmpwdth = bytlst_to_int(hdrlst[18:22])  # BitmapWidth      DW
        self.bmphght = bytlst_to_int(hdrlst[22:26])  # BitmapHeight     DW
        self.plnecnt = bytlst_to_int(hdrlst[26:28])  # PlanesCount      W
        self.bitppxl = bytlst_to_int(hdrlst[28:30])  # BitsPerPixel     W
        self.comprss = bytlst_to_int(hdrlst[30:34])  # Compression      DW
        self.bmpsize = bytlst_to_int(hdrlst[34:38])  # BitmapSize       DW
        self.hozreso = bytlst_to_int(hdrlst[38:42])  # H_Resolution     DW
        self.vrtreso = bytlst_to_int(hdrlst[42:46])  # V_Resolution     DW
        self.colruse = bytlst_to_int(hdrlst[46:50])  # ColorsUsed       DW
        self.colrimp = bytlst_to_int(hdrlst[50:54])  # ColorsImportant  DW
        # ------------------------------

    def pal_lst(self):
        """Return bitmap palette list format"""
        # ------------------------------
        pallst = []
        for color in self.pal:
            pallst += int_to_bytlst(color, 4)

        return pallst
        # ------------------------------

    def set_pal(self, pallst):
        """Set bitmap palette property from bitmap palette list format"""
        # ------------------------------
        self.pal = []
        for i in range(0, self.palccnt):
            idx = i * 4
            self.pal += [0xFFFFFF & bytlst_to_int(pallst[idx:idx + 4])]  # Mask Alpha channel (Delete)
        # ------------------------------

    def bmp_lst(self):
        """Return bitmap data list format"""
        # ------------------------------
        return self.bmp
        # ------------------------------

    def set_bmp(self, bmplst):
        """Set bitmap data property from bitmap data list format"""
        # ------------------------------
        self.bmp = bmplst
        # ------------------------------

    def info_dict(self):
        """Return bitmap file structure information dictionary"""
        # ------------------------------
        infodict = {
            'File': "Info",
            'FilePath': self.flepath,
            'Header': "Info",
            'FileType': self.fletype,
            'FileSize': self.flesize,
            'Reserved': self.reservd,
            'BitmapOffset': self.bmpofst,
            'HeaderSize': self.hdrsize,
            'BitmapWidth': self.bmpwdth,
            'BitmapHeight': self.bmphght,
            'PlanesCount': self.plnecnt,
            'BitsPerPixel': self.bitppxl,
            'Compression': self.comprss,
            'BitmapSize': self.bmpsize,
            'H_Resolution': self.hozreso,
            'V_Resolution': self.vrtreso,
            'ColorsUsed': self.colruse,
            'ColorsImportant': self.colrimp,
            'Useful': "Info",
            'BytesPerLine': self.bytplne,
            'BytesPerLineUsed': self.bytplnu,
            'BytesPerLineAdded': self.bytplna,
            'Bitmap': "Info",
            'BmpXmin': self.bmpxmin,
            'BmpXmax': self.bmpxmax,
            'BmpYmin': self.bmpymin,
            'BmpYmax': self.bmpymax,
            'Palette': "Info",
            'PaletteColorsCount': self.palccnt,
            'PaletteOffset': self.palofst,
            'PaletteSize': self.palsize,
            'Array': "Info",
            'PaletteLength': len(self.pal),
            'BitmapLength': len(self.bmp)
            }

        return infodict
        # ------------------------------

    def info_str(self):
        """Return bitmap file structure information string"""
        # ------------------------------
        infostr = ""
        dct = self.info_dict()
        for key, val in dct.items():
            if isinstance(val, int):
                infostr += f"{key}: {val} (0x{val:X})\n"
            elif val == "Info":
                sep = "-" * (38 - len(key + val))
                infostr += f"\n{sep} {key} {val}\n"
            else:
                infostr += f"{key}: {val}\n"

        return infostr
        # ------------------------------

    def pal_info(self):
        """Return bitmap palette information list"""
        # ------------------------------
        return self.pal
        # ------------------------------

    def pal_infostr(self):
        """Return bitmap palette information string"""
        # ------------------------------
        palinfostr = ""
        for i, c in enumerate(self.pal):
            palinfostr += f"({i:02X}) {i:03d}: #{c:06X}\n"

        return palinfostr
        # ------------------------------

    def pal_getcolor(self, index):
        """Return bitmap palette index color (0xRRGGBB) or (-1) if index is out of bounds"""
        # ------------------------------
        if 0 <= index < len(self.pal):
            color = self.pal[index]

        else:
            color = -1

        return color
        # ------------------------------

    def pal_setcolor(self, index, color):
        """Set bitmap palette index color (0xRRGGBB) if index isn't out of bounds"""
        # ------------------------------
        if 0 <= index < len(self.pal):
            self.pal[index] = 0xFFFFFF & color  # Mask Alpha channel (Delete)
        # ------------------------------

    def pal_stdinit(self):
        """Palette initialisation with standard colors (paint palette)"""
        # ------------------------------
        if self.bitppxl == 1:
            # 1 Bpp (2 colors)
            self.pal = [
                0x000000, 0xFFFFFF
                ]

        elif self.bitppxl == 4:
            # 4 Bpp (16 colors)
            self.pal = [
                0x000000, 0x800000, 0x008000, 0x808000, 0x000080, 0x800080, 0x008080, 0x808080,
                0xC0C0C0, 0xFF0000, 0x00FF00, 0xFFFF00, 0x0000FF, 0xFF00FF, 0x00FFFF, 0xFFFFFF
                ]

        elif self.bitppxl == 8:
            # 8 Bpp (256 colors)
            self.pal = [
                0x000000, 0x800000, 0x008000, 0x808000, 0x000080, 0x800080, 0x008080, 0xC0C0C0,
                0xC0DCC0, 0xA6CAF0, 0x402000, 0x602000, 0x802000, 0xA02000, 0xC02000, 0xE02000,
                0x004000, 0x204000, 0x404000, 0x604000, 0x804000, 0xA04000, 0xC04000, 0xE04000,
                0x006000, 0x206000, 0x406000, 0x606000, 0x806000, 0xA06000, 0xC06000, 0xE06000,
                0x008000, 0x208000, 0x408000, 0x608000, 0x808000, 0xA08000, 0xC08000, 0xE08000,
                0x00A000, 0x20A000, 0x40A000, 0x60A000, 0x80A000, 0xA0A000, 0xC0A000, 0xE0A000,
                0x00C000, 0x20C000, 0x40C000, 0x60C000, 0x80C000, 0xA0C000, 0xC0C000, 0xE0C000,
                0x00E000, 0x20E000, 0x40E000, 0x60E000, 0x80E000, 0xA0E000, 0xC0E000, 0xE0E000,
                0x000040, 0x200040, 0x400040, 0x600040, 0x800040, 0xA00040, 0xC00040, 0xE00040,
                0x002040, 0x202040, 0x402040, 0x602040, 0x802040, 0xA02040, 0xC02040, 0xE02040,
                0x004040, 0x204040, 0x404040, 0x604040, 0x804040, 0xA04040, 0xC04040, 0xE04040,
                0x006040, 0x206040, 0x406040, 0x606040, 0x806040, 0xA06040, 0xC06040, 0xE06040,
                0x008040, 0x208040, 0x408040, 0x608040, 0x808040, 0xA08040, 0xC08040, 0xE08040,
                0x00A040, 0x20A040, 0x40A040, 0x60A040, 0x80A040, 0xA0A040, 0xC0A040, 0xE0A040,
                0x00C040, 0x20C040, 0x40C040, 0x60C040, 0x80C040, 0xA0C040, 0xC0C040, 0xE0C040,
                0x00E040, 0x20E040, 0x40E040, 0x60E040, 0x80E040, 0xA0E040, 0xC0E040, 0xE0E040,
                0x000080, 0x200080, 0x400080, 0x600080, 0x800080, 0xA00080, 0xC00080, 0xE00080,
                0x002080, 0x202080, 0x402080, 0x602080, 0x802080, 0xA02080, 0xC02080, 0xE02080,
                0x004080, 0x204080, 0x404080, 0x604080, 0x804080, 0xA04080, 0xC04080, 0xE04080,
                0x006080, 0x206080, 0x406080, 0x606080, 0x806080, 0xA06080, 0xC06080, 0xE06080,
                0x008080, 0x208080, 0x408080, 0x608080, 0x808080, 0xA08080, 0xC08080, 0xE08080,
                0x00A080, 0x20A080, 0x40A080, 0x60A080, 0x80A080, 0xA0A080, 0xC0A080, 0xE0A080,
                0x00C080, 0x20C080, 0x40C080, 0x60C080, 0x80C080, 0xA0C080, 0xC0C080, 0xE0C080,
                0x00E080, 0x20E080, 0x40E080, 0x60E080, 0x80E080, 0xA0E080, 0xC0E080, 0xE0E080,
                0x0000C0, 0x2000C0, 0x4000C0, 0x6000C0, 0x8000C0, 0xA000C0, 0xC000C0, 0xE000C0,
                0x0020C0, 0x2020C0, 0x4020C0, 0x6020C0, 0x8020C0, 0xA020C0, 0xC020C0, 0xE020C0,
                0x0040C0, 0x2040C0, 0x4040C0, 0x6040C0, 0x8040C0, 0xA040C0, 0xC040C0, 0xE040C0,
                0x0060C0, 0x2060C0, 0x4060C0, 0x6060C0, 0x8060C0, 0xA060C0, 0xC060C0, 0xE060C0,
                0x0080C0, 0x2080C0, 0x4080C0, 0x6080C0, 0x8080C0, 0xA080C0, 0xC080C0, 0xE080C0,
                0x00A0C0, 0x20A0C0, 0x40A0C0, 0x60A0C0, 0x80A0C0, 0xA0A0C0, 0xC0A0C0, 0xE0A0C0,
                0x00C0C0, 0x20C0C0, 0x40C0C0, 0x60C0C0, 0x80C0C0, 0xA0C0C0, 0xFFFBF0, 0xA0A0A4,
                0x808080, 0xFF0000, 0x00FF00, 0xFFFF00, 0x0000FF, 0xFF00FF, 0x00FFFF, 0xFFFFFF
                ]

        else:
            # 24 Bpp (0 colors)
            self.pal = []
        # ------------------------------

    def bmp_stdinit(self):
        """Bitmap initialisation with standard background color (white)"""
        # ------------------------------
        bitused = self.bmpwdth * self.bitppxl
        rmngbit = bitused % 8  # Remaining Bits

        if rmngbit == 0:
            # No remaining bits
            self.bmp = (([255] * self.bytplnu) + ([0] * self.bytplna)) * self.bmphght

        else:
            # Some remaining bits
            bytfull = bitused // 8  # Fully Used Bytes (bytfull + 1 = self.bytplnu)
            lastbyt = 256 - (2 ** (8 - rmngbit))  # Contains Remaining Bits
            self.bmp = (([255] * bytfull) + [lastbyt] + ([0] * self.bytplna)) * self.bmphght
        # ------------------------------

    def check_hdr(self):
        """Check bitmap header for restricted and mandatory parameters"""
        # ------------------------------
        checkhdr = True

        # Check mandatory parameters

        # FileType
        if self.fletype != 0x4D42:
            checkhdr = False
            self.err += [("Invalid file type", "Check Header")]

        # HeaderSize
        if self.hdrsize != 40:
            checkhdr = False
            self.err += [("Unusual header size", "Check Header")]

        # PlanesCount
        if self.plnecnt != 1:
            checkhdr = False
            self.err += [("Unsupported plan count", "Check Header")]

        # Compression
        if self.comprss != 0:
            checkhdr = False
            self.err += [("Unsupported compressed file", "Check Header")]

        # Apply parameters restrictions

        # BitmapWidth
        if self.bmpwdth > 4096:
            checkhdr = False
            self.err += [("Bitmap width must be equal or less than 4096", "Check Header")]

        if self.bmpwdth < 1:
            checkhdr = False
            self.err += [("Bitmap width must be equal or greater than 1", "Check Header")]

        # BitmapHeight
        if self.bmphght > 4096:
            checkhdr = False
            self.err += [("Bitmap height must be equal or less than 4096", "Check Header")]

        if self.bmphght < 1:
            checkhdr = False
            self.err += [("Bitmap height must be equal or greater than 1", "Check Header")]

        # BitsPerPixel
        if self.bitppxl != 1 and self.bitppxl != 4 and self.bitppxl != 8 and self.bitppxl != 24:
            checkhdr = False
            self.err += [("Color depth must be 1, 4, 8, or 24 bpp", "Check Header")]

        return checkhdr
        # ------------------------------

    def calculate(self):
        """Bitmap file structure properties calculation"""
        # ------------------------------
        self.palccnt = 0
        if self.bitppxl <= 8:
            self.palccnt = 2 ** self.bitppxl

        self.palsize = self.palccnt * 4

        self.bytplne = 4 * ceil((self.bmpwdth * self.bitppxl) / 32)
        self.bytplnu = ceil((self.bmpwdth * self.bitppxl) / 8)
        self.bytplna = self.bytplne - self.bytplnu

        self.bmpsize = self.bytplne * self.bmphght
        self.palofst = 54  # 14 + self.hdrsize
        self.bmpofst = self.palofst + self.palsize
        self.flesize = self.bmpofst + self.bmpsize

        self.bmpxmin = 0
        self.bmpymin = 0
        self.bmpxmax = self.bmpwdth - 1
        self.bmpymax = self.bmphght - 1
        # ------------------------------

    def filebasename(self):
        """Return file base name only (Without extension)"""
        # ------------------------------
        name, _ext = splitext(basename(self.flepath))
        return name
        # ------------------------------

    def filelen(self):
        """Return file size or (-1) if file doesn't exists or is inaccessible"""
        # ------------------------------
        try:
            filesize = getsize(self.flepath)

        except OSError as e:
            self.err += [(e.strerror, "File Length")]
            filesize = -1

        return filesize
        # ------------------------------

    def is_openable(self):
        """Check file path and size"""
        # ------------------------------
        success = False

        if not isfile(self.flepath):
            # File doesn't exists
            self.err += [("File doesn't exists", "Is Openable")]

        else:
            # File does exists
            flen = self.filelen()
            if flen < 58:
                # Min w1 h1 @24bpp
                self.err += [(f"File too small, less than 58 bytes ({flen})", "Is Openable")]

            elif flen > 50331702:
                # Max w4096 h4096 @24bpp
                self.err += [(f"File too big, more than 50331702 bytes ({flen})", "Is Openable")]

            else:
                success = True

        return success
        # ------------------------------

    def is_savable(self, replace):
        """Check parent folder path and if existing file can be replaced"""
        # ------------------------------
        success = False

        if isfile(self.flepath):
            # File already exists
            if not replace:
                # File can't be replaced
                self.err += [("Unable to overwrite file with replace argument set to false", "Is Savable")]

            else:
                # File can be replaced
                success = True

        else:
            # File doesn't exists
            if isdir(self.flepath):
                # It's a folder
                self.err += [("A folder with this name already exists", "Is Savable")]

            else:
                # Check parent folder
                parentfld = dirname(self.flepath)
                if not isdir(parentfld):
                    # Parent folder doesn't exists
                    self.err += [("Parent folder doesn't exists", "Is Savable")]

                else:
                    # Parent folder does exists
                    success = True

        return success
        # ------------------------------

    def checksize(self):
        """Compare real file size with calculated size (theoretical size)"""
        # ------------------------------
        if self.filelen() < self.flesize:
            # Real size < Calculated size
            self.err += [("Unexpected file size", "Check Size")]
            success = False

        else:
            # Real size >= Calculated size
            success = True

        return success
        # ------------------------------

    def load_hdr(self):
        """Load bitmap header from file"""
        # ------------------------------
        try:
            with open(self.flepath, "rb") as f:
                f.seek(0)
                tmplst = list(f.read(54))
                # File is automatically close (End With)

        except OSError as e:
            self.err += [(e.strerror, "Load Header")]
            success = False

        else:
            self.set_hdr(tmplst)
            success = True

        return success
        # ------------------------------

    def load_pal(self):
        """Load bitmap palette from file"""
        # ------------------------------
        try:
            with open(self.flepath, "rb") as f:
                f.seek(self.palofst)
                tmplst = list(f.read(self.palsize))
                # File is automatically close (End With)

        except OSError as e:
            self.err += [(e.strerror, "Load Palette")]
            success = False

        else:
            self.set_pal(tmplst)
            success = True

        return success
        # ------------------------------

    def load_bmp(self):
        """Load bitmap data from file"""
        # ------------------------------
        try:
            with open(self.flepath, "rb") as f:
                f.seek(self.bmpofst)
                tmplst = list(f.read(self.bmpsize))
                # File is automatically close (End With)

        except OSError as e:
            self.err += [(e.strerror, "Load Bitmap")]
            success = False

        else:
            self.set_bmp(tmplst)
            success = True

        return success
        # ------------------------------

    def save(self):
        """Save bitmap file structure to file"""
        # ------------------------------
        tmparr = bytes(self.hdr_lst() + self.pal_lst() + self.bmp_lst())

        try:
            with open(self.flepath, "wb") as f:
                f.write(tmparr)
                # File is automatically close (End With)

        except OSError as e:
            self.err += [(e.strerror, "Save All")]
            success = False

        else:
            success = True

        return success
        # ------------------------------

    def err_lst(self):
        """Return current errors list"""
        # ------------------------------
        return self.err
        # ------------------------------

    def err_str(self):
        """Return current errors string"""
        # ------------------------------
        errstr = ""
        for e in self.err:
            error, fct = e
            errstr += f"{fct}: {error}\n"

        return errstr
        # ------------------------------

    def err_count(self):
        """Return current errors count"""
        # ------------------------------
        return len(self.err)
        # ------------------------------

    def err_clear(self):
        """Clear current errors list"""
        # ------------------------------
        self.err = []
        # ------------------------------

    def pixelcolor(self, x, y, truecolor):
        """If pixel (x, y) is in GFX area, returns its color, otherwise returns (-1) (Pixel doesn't exists)
           For 1, 4, 8 bpp: returns the palette color index or the true RGB color if (truecolor) is set to 'True'
           For 24 bpp: always returns the true RGB color (0xRRGGBB)"""
        # ------------------------------

        pxlcolr = -1

        if self.bmpxmin <= x <= self.bmpxmax and self.bmpymin <= y <= self.bmpymax:
            # Pixel (x, y) is in GFX area

            if self.bitppxl == 1:
                # 1 Bpp ----------------
                byte_idx = floor(x / 8)
                bit_idx = (byte_idx * 8) + 7 - x  # Bit shift count
                start_idx = byte_idx + ((self.bmpymax - y) * self.bytplne)

                pxlcolr = 0x01 & (self.bmp[start_idx] >> bit_idx)  # Palette color index (Mask 0x01)

                if truecolor:
                    pxlcolr = self.pal[pxlcolr]  # True RGB color

            elif self.bitppxl == 4:
                # 4 Bpp ----------------
                byte_idx = floor(x / 2)
                bit_idx = 4 * ((byte_idx * 2) + 1 - x)  # Bit shift count
                start_idx = byte_idx + ((self.bmpymax - y) * self.bytplne)

                pxlcolr = 0x0F & (self.bmp[start_idx] >> bit_idx)  # Palette color index (Mask 0x0F)

                if truecolor:
                    pxlcolr = self.pal[pxlcolr]  # True RGB color

            elif self.bitppxl == 8:
                # 8 Bpp ----------------
                byte_idx = x
                start_idx = byte_idx + ((self.bmpymax - y) * self.bytplne)

                pxlcolr = self.bmp[start_idx]  # Palette color index

                if truecolor:
                    pxlcolr = self.pal[pxlcolr]  # True RGB color

            elif self.bitppxl == 24:
                # 24 Bpp ---------------
                byte_idx = x * 3
                start_idx = byte_idx + ((self.bmpymax - y) * self.bytplne)

                pxlcolr = bytlst_to_int(self.bmp[start_idx:start_idx + 3])

            else:
                # Unexpected Bpp -------
                pass

        return pxlcolr
        # ------------------------------

    def drawpixel(self, x, y, c):
        """If pixel (x, y) is in GFX area, sets its color (c), otherwise does nothing
           For 1, 4, 8 bpp: (c) is the palette color index
           For 24 bpp: (c) is the true RGB color (0xRRGGBB)"""
        # ------------------------------

        if self.bmpxmin <= x <= self.bmpxmax and self.bmpymin <= y <= self.bmpymax:
            # Pixel (x, y) is in GFX area

            if self.bitppxl == 1:
                # 1 Bpp ----------------
                byte_idx = floor(x / 8)
                bit_idx = (byte_idx * 8) + 7 - x  # Bit shift count
                start_idx = byte_idx + ((self.bmpymax - y) * self.bytplne)

                msk_neg = 0xFF ^ (0x01 << bit_idx)           # 11011111
                old_msked = msk_neg & self.bmp[start_idx]    # RR0RRRRR
                new_msked = (c & 0x01) << bit_idx            # 00W00000
                self.bmp[start_idx] = old_msked | new_msked  # RRWRRRRR

            elif self.bitppxl == 4:
                # 4 Bpp ----------------
                byte_idx = floor(x / 2)
                bit_idx = 4 * ((byte_idx * 2) + 1 - x)  # Bit shift count
                start_idx = byte_idx + ((self.bmpymax - y) * self.bytplne)

                msk_neg = 0xFF ^ (0x0F << bit_idx)           # 00001111
                old_msked = msk_neg & self.bmp[start_idx]    # 0000RRRR
                new_msked = (c & 0x0F) << bit_idx            # WWWW0000
                self.bmp[start_idx] = old_msked | new_msked  # WWWWRRRR

            elif self.bitppxl == 8:
                # 8 Bpp ----------------
                byte_idx = x
                start_idx = byte_idx + ((self.bmpymax - y) * self.bytplne)

                self.bmp[start_idx] = c & 0xFF

            elif self.bitppxl == 24:
                # 24 Bpp ---------------
                byte_idx = x * 3
                start_idx = byte_idx + ((self.bmpymax - y) * self.bytplne)

                self.bmp[start_idx:start_idx + 3] = int_to_bytlst(c & 0xFFFFFF, 3)

            else:
                # Unexpected Bpp -------
                pass
        # ------------------------------

    def create(self, width, height, bpp):
        """Initialise a new bitmap file structure"""
        # ------------------------------
        success = False

        self.clean()
        self.bmpwdth = width
        self.bmphght = height
        self.bitppxl = bpp

        if self.check_hdr():
            # Structure initialisation
            self.calculate()
            self.pal_stdinit()
            self.bmp_stdinit()
            success = True

        return success
        # ------------------------------

    def open(self, spath):
        """Load bitmap file structure from file (.bmp)"""
        # ------------------------------
        success = False

        self.clean()
        self.flepath = abspath(spath)

        if self.is_openable():
            # Header loading
            if self.load_hdr():
                # Header successfully loaded
                if self.check_hdr():
                    # Header parameters successfully checked
                    self.calculate()

                    if self.checksize():
                        # File size successfully checked
                        if self.load_bmp():
                            # Bitmap successfully loaded
                            success = True

                            if self.palccnt > 0:
                                # Palette loading
                                success = self.load_pal()

        return success
        # ------------------------------

    def saveas(self, spath, replace):
        """Save bitmap file structure to file (.bmp)"""
        # ------------------------------
        success = False
        self.err_clear()

        self.flepath = abspath(spath)

        if self.is_savable(replace):
            # Save all
            success = self.save()

        return success
        # ------------------------------


################################################################################
#                                      EOF                                     #
################################################################################
