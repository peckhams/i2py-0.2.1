
#-----------------------
#  Things left to do:
#-----------------------

#  Use numpy's linspace() instead of arange().  See p. 133
#  in Langtangen's Python book.

#  Note that a[a < 0] = 0 works and could be used somewhere.

#  "convolve" routine from scipy.signal now works. That package
#  also includes many other routines.

#  Do we still need "array(var, copy=0)" in READU, WRITEU ?
#    Seems we no longer need this in MAX() and MIN().
#    What about a case like: "max([1,2,3])" ??

#  Add suppport for WHERE returning -1L ??

#  Add support for REBIN.
#  What to do about ASSOC ?
#  Test support for BYTE.

#  Test support for READF, READS, PRINTF, STRING & FORMAT keyword.

#  Avoid use of print_error_message() or rewrite this utility.

#  In ir.py, in "class WhileStatement", look for cases:
#     "while not(eof(" and convert to the Python way?

#  Finish support for TV and TVSCL.
#  Add support for OPLOT, SURFACE.
#  Add support for LOADCT (using cmaps like jet).
#  Add support for POLYFILL and POLYFILLV.
#  TVRD may not be needed due to matplotlib.pyplot.savefig.

#  Add support for HISTOGRAM's REVERSE_INDICES keyword
#      by using NumPy's DIGITIZE
#  Add support for INTERPOL, INTERPOLATE, SMOOTH,
#      CONVOL (need 1D and 2D), FFT
#  Add support for CONVERT_COORD

#  Finish support for UNIQ.
#  Is support for BYTSCL finished ?

#  Convert IDL code for library routines:
#      CURVEFIT, HIST_EQUAL, (INTERPOL ?)
#      Arrays:  CONGRID, ROT
#      Mapping:     MAP_*
#      Statistics:  MOMENT (& SKEWNESS), REGRESS

#  Add support for mapping routines: MAP_*
#  Add support for NetCDF format
#  Add support for shapefiles
#  Add support for image formats (READ_BMP, etc.) (via PIL ??)

#  Add support for STRCMP, STRCOMPRESS, STRJOIN, STRMATCH
#  Add support for color routines like: HLS, HSV, COLOR_CONVERT,
#      COLOR_QUAN, CMYK_CONVERT, LOADCT, REDUCE_COLORS

#  Finish support for FSTAT
#  Finish support for ONLINE_HELP procedure (via webbrowser)
#  Finish support for complex-number routines
#  Better approach to STRSPLIT ?  (maybe use "import re"?)

#  Done? Import multiple packages in 1 line e.g.: "import wx, os"

################################################################################
#
#  Comments regarding complex routines like READF, STRING, FSTAT, BYTE
#
################################################################################

#  Some IDL routines have "complex" behavior that cannot be reproduced
#  with a few simple Python commands.  For example, they may:
#     (1) test the types of the arguments and then branch (e.g. BYTE)
#     (2) return a structure (e.g. FSTAT, SIZE)
#     (3) be procedures that modify their arguments (e.g. READF, READS)
#     (4) have keywords that require many lines of code to handle
#         properly (e.g. FORMAT keyword in STRING, PRINTF, READF, READS)
#  For these types of IDL routines, it is simpler and cleaner to define
#  a new module called "idl_func.py" that contains simulated versions of
#  them.  They can then be called in a similar manner as they would be
#  in IDL.

################################################################################
#
#  Comments regarding support for boolean IDL keywords
#
################################################################################

#  Boolean IDL keywords can be set in various ways, including:
#       /KEYWORD, KEYWORD=1, KEYWORD=my_function(a)
#       (what about KEYWORD=1b ??)
#  I2PY maps the first 2 cases to KEYWORD=True, but more work is
#  required in the last case; basically the same procedure that is
#  needed for non-Boolean keywords where the key value must be
#  processed.  Right now, only OPENR, OPENU and OPENW support all
#  three Boolean keyword cases.  It might be a good idea to replace
#  the current utility functions idl_key_set() and idl_key_index()
#  with a new one called idl_key_value().  This new function would
#  return None if the keyword is not present, and would return True
#  or a more general key value otherwise.

#  If idl_key_index() returns a value other than -1, then we know
#  that the keyword has been set with an equals sign (vs. leading
#  "/".  The safest thing to do in this case is process the key
#  value.  If idl_key_index() returns -1, then we still need to
#  check whether idl_key_set() returns True (again, due to "/").

################################################################################
#
#  Comments regarding numpy.array() vs. numpy.concatenate()
#
################################################################################

#  Need robust approach to square brackets: array() vs. concatenate()

#  Now square brackets get translated to include "array", which has been
#  accounted for in several places.


################################################################################
#
#  Comments regarding bitwise vs. logical OR, AND and NOT.
#
################################################################################
#
#  In ir.py, the classes "LogicalExpression" and "BitwiseExpression"
#  determine how IDL's OR, AND and NOT are converted.  Recall that
#  "logical and/or/not" evaluates all args and returns 0 or 1, but
#  "bitwise and/or/not" does an AND operation on integers and
#  returns one of the 2 args for other types.

#  Most of the time, translating IDL's "and/or/not" to NumPy's
#  "logical_and/or/not" will give the desired result.  The latter
#  functions are ufuncs, but can also be applied to scalar arguments.
#  Instead of returning array elements of 0 or 1, they return array
#  elements of True or False.

#  I changed the BitwiseExpression class in ir.py accordingly.
#  However, it might be better for user to search and replace
#  occurrences of "and", "or" and "not" with &&, || and ~ and
#  leave ir.py as it was.

#  In IDL:
#     (1)  The 4 BITWISE operators are: AND, NOT, OR and XOR.
#     (2)  The 3 LOGICAL operators are:  "&&", "||" and "~".
#     (3)  When dealing with logical operators, non-zero numerical
#          values, non-null strings and non-null heap variables (pointers
#          and object references) are considered TRUE; all else is FALSE.
#     (4) false = 0b
#         true  = 1b
#         print, not(false)       (255)
#         print, not(true)        (254)
#         print, ~false           (1)
#         print, ~true            (0)

#  In Python:
#     (1) The and/or/not operators cannot operate on arrays, so for
#         arrays we must use NumPy ufuncs called "logical_and/or/not"
#         or "bitwise_and/or/not".
#     (2) false = numpy.uint8(0)
#         true  = numpy.uint8(1)
#         not(false)                       (True)
#         not(true)                        (False)
#         numpy.logical_not(false)         (True)
#         numpy.logical_not(true)          (False)
#         numpy.bitwise_not(false)         (255)
#         numpy.bitwise_not(true)          (254)
#         numpy.logical_or(false, true)    (True)
#         numpy.logical_and(false, true)   (False)
#         numpy.bitwise_or(false, true)    (1)
#         numpy.bitwise_and(false, true)   (0)
#         a = numpy.array([0,1,0])
#         b = numpy.array([1,1,0])
#         a and b                          (error)
#         a or  b                          (error)
#         numpy.logical_or(a,b)            [True, True, False]
#         numpy.logical_and(a,b)           [False, True, False]
#         numpy.logical_not(a,b)           [1, 0, 1]
#         numpy.bitwise_or(a,b)            [1, 1, 1]
#         numpy.bitwise_and(a,b)           [0, 0, 0]
#         numpy.bitwise_not(a,b)           [-1, -2, -1]
