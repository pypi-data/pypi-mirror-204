# JUtils
JUtils is a package containing various utility functions i needed now and then, summarized into a single package
and released, in case someone finds the need to use something.

**Disclaimer: Please note that the contained functions are very specific and maybe no one will find a use in them.**

## Table of contents
# 1. [JArr](#JUtils.JArr)
# 2. [Jcolors](#JUtils.JColors)
# 3. [JConv](#JUtils.JConv)
# 4. [JNum](#JUtils.Num)
# 5. [JOut](#JUtils.JOut)
# 6. [JStr](#JUtils.JStr)

## JUtils.JArr
Functions for array analysing and modification.
```py
from JUtils.JArr import *
```

- **segm**
Divide a list into sublists of a specified size.
    ```py
    segm(list, int)
    ```
- **flt2d**
Flatten a list of lists into a single list. Only for 2d lists, because the inner items should not be flattened.
    ```py
    flt2d(list[list])
    ```
- **overlp**
Checks if elements in l1 and l2 share any same elements
    ```py
    overlp(list, list)
    ```

## JUtils.JColors
Color constants importable by name
```py
from JUtils.JColors import *
```

- **randColor**
Returns a random Color
    ```py
    randColor()
    ```

- **Color Constants**
Importable by name, also available in hex representation, via ```HEX_RED``` for example.
    ```py
    RGB_RED              = (255, 0, 0)
    RGB_RED_DARK         = (139, 0, 0)
    RGB_CRIMSON          = (220, 20, 60)
    RGB_SALMON           = (250, 128, 114)
    RGB_SALMON_LIGHT     = (255, 160, 122)
    RGB_SALMON_DARK      = (233, 150, 122)
    RGB_MAROON           = (128, 0, 0)
    
    RGB_ROSE             = (255, 105, 180)
    RGB_ROSE_LIGHT       = (255, 192, 203)
    RGB_ROSE_DARK        = (219, 112, 147)
    RGB_PINK             = (255, 20, 147)
    RGB_PINK_DARK        = (199, 21, 133)
    
    RGB_ORANGE           = (255, 140, 0)
    RGB_ORANGE_LIGHT     = (255, 165, 0)
    RGB_ORANGE_DARK      = (255, 69, 0)
    RGB_TOMATO           = (255, 99, 71)
    RGB_CORAL            = (255, 127, 80)
    
    RGB_YELLOW           = (255, 255, 0)
    RGB_YELLOW_LIGHT     = (255, 255, 224)
    RGB_GOLD             = (255, 215, 0)
    RGB_MOCCASIN         = (255, 228, 181)
    RGB_KHAKI            = (240, 230, 140)
    RGB_KHAKI_LIGHT      = (238, 232, 170)
    RGB_KHAKI_DARK       = (189, 183, 107)
    
    RGB_PURPLE           = (128, 0, 128)
    RGB_INDIGO           = (75, 0, 130)
    RGB_MAGENTA          = (255, 0, 255)
    RGB_MAGENTA_DARK     = (139, 0, 139)
    RGB_FUCHSIA          = (255, 0, 255)
    RGB_VIOLET           = (238, 130, 238)
    RGB_VIOLET_DARK      = (148, 0, 211)
    RGB_LAVENDER         = (230, 230, 250)
    RGB_SLATEBLUE        = (106, 90, 205)
    RGB_SLATEBLUE_DARK   = (72, 61, 139)
    
    RGB_GREEN            = (0, 128, 0)
    RGB_GREEN_LIGHT      = (144, 238, 144)
    RGB_GREEN_DARK       = (0, 100, 0)
    RGB_LIME             = (0, 255, 0)
    RGB_LIMEGREEN        = (50, 205, 50)
    RGB_LAWNGREEN        = (124, 252, 0)
    RGB_GREENYELLOW      = (173, 255, 47)
    RGB_PALEGREEN        = (152, 251, 152)
    RGB_SPRINGGREEN      = (0, 255, 127)
    RGB_SEAGREEN         = (46, 139, 87)
    RGB_SEAGREEN_LIGHT   = (32, 178, 170)
    RGB_SEAGREEN_DARK    = (143, 188, 139)
    RGB_OLIVE            = (128, 128, 0)
    RGB_OLIVE_DARK       = (85, 107, 47)
    RGB_OLIVEDRAB        = (107, 142, 35)
    
    RGB_BLUE             = (0, 0, 255)
    RGB_BLUE_LIGHT       = (173, 216, 230)
    RGB_NAVY             = (0, 0, 128)
    RGB_MIDNIGHTBLUE     = (25, 25, 112)
    RGB_ROYALBLUE        = (65, 105, 225)
    RGB_CORNFLOWERBLUE   = (100, 149, 237)
    RGB_DODGERBLUE       = (30, 144, 255)
    RGB_AQUA             = (0, 255, 255)
    RGB_CYAN             = (0, 255, 255)
    RGB_CYAN_LIGHT       = (224, 255, 255)
    RGB_CYAN_DARK        = (0, 139, 139)
    RGB_TEAL             = (0, 128, 128)
    RGB_TURQUOISE        = (64, 224, 208)
    RGB_TURQUOISE_DARK   = (0, 206, 209)
    RGB_AQUAMARINE       = (127, 255, 238)
    RGB_CADETBLUE        = (95, 158, 160)
    RGB_STEELBLUE        = (70, 130, 180)
    RGB_STEELBLUE_LIGHT  = (176, 196, 222)
    RGB_POWDERBLUE       = (176, 224, 230)
    RGB_SKYBLUE          = (135, 206, 235)
    RGB_SKYBLUE_LIGHT    = (135, 206, 250)
    RGB_SKYBLUE_DARK     = (0, 191, 255)
    
    RGB_BROWN            = (139, 69, 19)
    RGB_BROWN_LIGHT      = (160, 82, 45)
    RGB_BROWNRED         = (165, 42, 42)
    RGB_CHOCOLATE        = (210, 105, 30)
    RGB_PERU             = (205, 133, 63)
    RGB_SANDYBROWN       = (244, 164, 96)
    RGB_ROSYBROWN        = (188, 143, 143)
    RGB_GOLDENBROWN      = (218, 165, 32)
    RGB_GOLDENBROWN_DARK = (184, 134, 11)
    RGB_TAN              = (210, 180, 140)
    RGB_CORNSLIK         = (255, 248, 220)
    RGB_BLANCHEDALMOND   = (255, 235, 205)
    RGB_BISQUE           = (255, 228, 196)
    RGB_WHEAT            = (245, 222, 179)
    
    RGB_WHITE            = (255, 255, 255)
    RGB_SNOW             = (255, 255, 250)
    RGB_HONEYDEW         = (240, 255, 240)
    RGB_MINTCREAM        = (245, 255, 250)
    RGB_AZURE            = (240, 255, 255)
    RGB_ALICEBLUE        = (240, 248, 255)
    RGB_GHOSTWHITE       = (248, 248, 255)
    RGB_WHITESMOKE       = (245, 245, 245)
    RGB_SEASHELL         = (255, 245, 238)
    RGB_BEIGE            = (245, 245, 220)
    RGB_OLDLACE          = (253, 245, 230)
    RGB_FLORALWHITE      = (255, 250, 240)
    RGB_IVORY            = (255, 255, 240)
    RGB_ANTIQUEWHITE     = (250, 245, 215)
    RGB_LINEN            = (250, 240, 230)
    RGB_LAVENDERBUSH     = (255, 240, 245)
    RGB_MISTYROSE        = (255, 228, 225)
    
    RGB_BLACK            = (0, 0, 0)
    RGB_GRAY             = (128, 128, 128)
    RGB_GRAY_LIGHT       = (211, 211, 211)
    RGB_GRAY_DARK        = (169, 169, 169)
    RGB_SILVER           = (192, 192, 192)
    RGB_DIMGRAY          = (105, 105, 105)
    RGB_SLATEGRAY        = (112, 128, 144)
    RGB_SLATEGRAY_LIGHT  = (119, 136, 153)
    RGB_SLATEGRAY_DARK   = (47, 79, 79)
    RGB_GAINSBORO        = (220, 220, 220)
    ```

## JUtils.JConv 
Functions for converting values
```py
from JUtils.JConv import *
```

- **rgb2hex**
Convert an RGB tuple to a hexadecimal string representation.
    ```py
    rgb2hex(tuple)
    ```
- **hex2rgb*
Convert a hexadecimal string representation to an RGB tuple.
    ```py
    hex2rgb(str)
    ```
- **hex2asc**
Convert a string of hexadecimal characters to a string of ASCII characters.
    ```py
    hex2asc(str)
    ```
- **deg2rad**
Converts an angle in degrees to radians.
    ```py
    deg2rad(float)
    ```
- **rad2deg**
Converts an angle in radians to degrees.
    ```py
    rad2deg(float)
    ```
- **pol2cart**
Converts polar coordinates (angle, radius) to Cartesian coordinates (x, y).
    ```py
    pol2cart(float, float)
    ```
- **cart2pol**
Converts Cartesian coordinates (x, y) to polar coordinates (angle, radius).
    ```py
    cart2pol(float, float)
    ```

## JUtils.JNum
Functions for handling numbers
```py
from JUtils.JNum import *
```

- **sgn**
return the sign of a number (```-1``` / ```0``` / ```1```)
    ```py
    sgn(float)
    ```
- **contain**
Clamps a number within a given range.
    ```py
    contain(number, lower_limit, upper_limit)
    ```

## JUtils.JOut
Functions for handling console output
```py
from JUtils.JOut import *
```

- **printn**
Prints the given argument, with newlines before and after (works with multiple args like print)
    ```py
    printn(any)
    ```

## JUtils.JStr
Functions for string analysing and modification
```py
from JUtils.JStr import *
```

- **locBrac**
Finds the index of the closing bracket that matches the opening bracket at the given index in the given string.
allowed brackets are ```(``` / ```[``` / ```{``` / ```<```
    ```py
    locBrac(string, bracket_character, opening_index)
    ```
- **nl**
Newline constant to keep code clean
    ```py
    nl = "\n"

\
\
\
This Package is not under active development, i will update it every now and then if i find a new function to add.
Please consider emailing me at: [jan@seifert-online.de](mailto:jan@seifert-online.de) if you got any suggestions for improvement.