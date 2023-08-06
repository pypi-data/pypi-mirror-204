# JUtils
JUtils is a package containing various utility functions i needed now and then, summarized into a single package
and released, in case someone finds the need to use something.

**Disclaimer: Please note that the contained functions are very specific and maybe no one will find a use in them.**

# Table of Contents
## 1. [JArr](#JUtils.JArr)
## 2. [JColors](#JUtils.JColors)
## 3. [JConst](#JUtils.JConst)
## 4. [JConv](#JUtils.JConv)
## 5. [JNum](#JUtils.JNum)
## 6. [JOut](#JUtils.JOut)
## 7. [JStr](#JUtils.JStr)

# JArr
Functions for array analysing and modification.
```py
from JUtils.JArr import *
```

- **IterComp**
```
    Check if 2 iterables of the same length have the same elements, regardless of type.

    Args:
        a: An iterable object.
        b: An iterable object.

    Returns:
        - True if every element in `a` is equal to the corresponding element in `b`.
        - False if there is at least one pair of non-equal elements in `a` and `b`.
        - None if the length of `a` and `b` differ.

    Examples:
        >>> IterComp([1, 2, 3], [1, 2, 3])
        True
        >>> IterComp([1, 2, 3], [1, 2, 4])
        False
        >>> IterComp([1, 2, 3], [1, 2])
        None
    .
```
- **flt2d**
```
    Flatten a list of lists into a single list. Only for 2d lists, because the inner items should not be flattened.
    
    Parameters:
        arr (list): The list of lists to be flattened.
        
    Returns:
        list: The resulting flattened list.
        
    Example:
        >>> flt([[(), ()], [(), ()]])
        [(), (), (), (), (), ()]
    .
```
- **overlp**
```
    Checks if elements in l1 and l2 share any same elements

    Parameters:
        l1 (list): a list of elements
        l2 (list): a list of elements

    Returns:
        bool: if there are any overlaps between l1 and l2
    .
```
- **segm**
```
    Divide a list into sublists of a specified size.
    
    Parameters:
        arr (list): The list to be divided into sublists.
        n (int): The size of each sublist.
        
    Returns:
        list: A list of sublists, where each sublist contains 'n' elements.
        
    Example:
        >>> segm([1, 1, 1, 1, 1, 1], 2)
        [[1, 1], [1, 1], [1, 1]]
    .
```
# JColors
Color constants importable by name.
```py
from JUtils.JColors import *
```

- **randColor**
```Returns a random color
    
    Returns:
        tuple: A 3-tuple of integers representing the red, green, and blue components of the color.
    .
```
# JConst
Constants for keeping code clean.
```py
from JUtils.JConst import *
```

# JConv
Functions for converting values.
```py
from JUtils.JConv import *
```

- **cart2pol**
```Converts Cartesian coordinates to polar coordinates.

    Args:
        x (float): The x-coordinate.
        y (float): The y-coordinate.

    Returns:
        tuple: Polar coordinates (th, r), where r is the distance fromthe origin and th is the angle in degrees.
    .
```
- **deg2rad**
```Converts an angle in degrees to radians.

    Parameters:
        deg (float): An angle in degrees.

    Returns:
        float: The equivalent angle in radians.
    .
```
- **hex2asc**
```
    Convert a string of hexadecimal characters to a string of ASCII characters.
    
    Parameters:
        hx (str): The string of hexadecimal characters to be converted.
        
    Returns:
        str: The resulting string of ASCII characters.
    
    Example:
        >>> hex2asc('0000ff')
        '048048048048102102' #048 048 048 048 102 102
    .
```
- **hex2rgb**
```
    Convert a hexadecimal string representation to an RGB tuple.

    Parameters:
    hx (str): A hexadecimal string representation of an RGB color, in the form '#RRGGBB'.

    Returns:
    tuple: An RGB tuple with 3 integers between 0 and 255, inclusive, representing the red, green, and blue values.

    Example:
    >>> hex2rgb('#ff00ff')
    (255, 0, 255)
    .
```
- **pol2cart**
```Converts polar coordinates to Cartesian coordinates.

    Args:
        ang (float): An angle in degrees.
        r (float): The distance from the origin.

    Returns:
        tuple: A tuple of the Cartesian coordinates (x, y).
    .
```
- **rad2deg**
```Converts an angle in radians to degrees.

    Parameters:
        rad (float): An angle in radians.

    Returns:
        float: The equivalent angle in degrees.
    .
```
- **rgb2gray**
```
    Converts an RGB color tuple to a grayscale integer value using the luminosity method.
    
    Args:
        rgb (tuple): A tuple containing 3 integers representing the RGB color values. The values
                     should be in the range of 0-255, inclusive.
                     
    Returns:
        int: The grayscale integer value representing the given RGB color tuple.
    .
```
- **rgb2hex**
```
    Convert an RGB tuple to a hexadecimal string representation.

    Parameters:
    rgb (tuple): An RGB tuple with 3 integers between 0 and 255, inclusive, representing the red, green, and blue values.

    Returns:
    str: A hexadecimal string representation of the input RGB tuple, in the form '#RRGGBB'.

    Example:
    >>> rgb_to_hex((255, 0, 255))
    '#ff00ff'
    .
```
# JNum
Functions for handling numbers.
```py
from JUtils.JNum import *
```

- **contain**
```Clamps a number within a given range.

    Parameters:
        n (float): The number to be clamped.
        limDown (float): The lower bound of the range.
        limUp (float): The upper bound of the range.

    Returns:
        'n' if it is within the range, or the nearest bound if 'n' is outside
        the range.
    .
```
- **sTup2Tup**
```
    Turns the given string of a tuple to a tuple object.

    Parameters:
        s: A tuple in string form.

    Returns:
        The tuple as a tuple object.
    .
```
- **sgn**
```Returns the sign of a number.

    Parameters:
        n: An int/float number.

    Returns:
        An int representing the sign of 'n'. 1 if 'n' is positive, -1 if 'n'
        is negative, and 0 if 'n' is zero.
    .
```
# JOut
Functions for handling console output.
```py
from JUtils.JOut import *
```

- **delayPrint**
```Prints the given string with a slight delay after each character.

    Parameters:
        s: A string.
    .
```
- **printn**
```Prints the given arguments, with newlines before and after (works with multiple args like print)
    
    Parameters:
        *args: The arguments to print.
    .
```
# JStr
Functions for string analysing and modification.
```py
from JUtils.JStr import *
```

- **listPath**
```
    Just like os.listdir(), but with appended path.
    
    Args:
        d: The path to list.
        
    Returns:
        list: A list of paths of files and directories in the given path.
    .
```
- **locBrac**
```
    Finds the index of the closing bracket that matches the opening bracket at the given index in the given string.

    Parameters:
        string (str): The input string.
        brac (str): The bracket character | Possible are ( [ { <
        ix (int): The index of the opening bracket in the input string.

    Returns:
        int: The index of the closing bracket in the input string, or -1 if no matching closing bracket was found.

    Example:
        >>> locBrac('[hello[world]]', '[', 0)
        13
        >>> locBrac('<hello<world>>', '<', 6)
        12
        >>> locBrac('{hello}world}', '{', 0)
        -1
    .
```
- **multiCenter**
```
    Centers the text in a string by padding spaces on either side of each line.
    
    Args:
        s (str): The input string to center.
        l (int): The desired width of the centered string.
        
    Returns:
        str: The centered string. Each line is padded with spaces on either side to center the text. If
             a line already has an odd number of characters, the extra space is added to the right
             side of the line.
    .
```
\
\
\
This Package is not under active development, i will update it every now and then if i find a new function to add.
Please consider emailing me at: [jan@seifert-online.de](mailto:jan@seifert-online.de) if you got any suggestions for improvement.