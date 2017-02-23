
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

################################################################################
# 
#  Copyright (C) 2008 Scott D. Peckham <Scott.Peckham@colorado.edu>
# 
#  This file is part of i2py.
# 
#  i2py is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
# 
#  i2py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with i2py; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#--------------------------------------------------------------------
#  Notes: Arguments to map_var, map_pro and map_func are explained
#         in map.py, in the SubroutineMapping class definition.

#         lambda forms may not contain statements, but starting
#         with Python 2.5 can contain conditional expressions.
#         These are used for functions like ATAN and TOTAL below.

#         IDL's KEYWORD_SET function is handled at the bottom of
#         the file "map.py". (SDP)

#         Modules to be imported (use "extracode" argument):
#         numpy.linalg, numpy, os, random, time, etc.
#--------------------------------------------------------------------

"""
Defines Python mappings for some many IDL functions and procedures
"""

#----------------------------------------------------
# Need next line for things like "eval('int16(5)')",
# which occurs in "idl_make_array_callfunc"
#----------------------------------------------------
from numpy import *
import numpy

from map import map_var, map_pro, map_func
import error  # (part of i2py)
import re
import user_lib   ##########

################################################################################
#
#  Convenience functions, used below.
#
################################################################################

def print_error_message(idl_command, err_str):
    msg  = "\n   >>>>  ERROR in converting call to %s." % idl_command
    msg += "\n   >>>>  (%s)\n" % err_str
    error.conversion_error(msg, 0)    
    # print msg
    # error.conversion_error(msg, self.lineno)
    
#--------------------------------------------------------------------        
def arrgen(typename):
    "Returns an array-generation callfunc for type typename"
    return (lambda i,o: "zeros([%s], dtype='%s')" %
           (reverse_arg_str(i), typename) if not(idl_key_set('nozero',i))
           else "empty([%s], dtype='%s')" % (reverse_arg_str(i), typename) )

#--------------------------------------------------------------------
def rampgen(typename):
    "Returns a 'ramp-generation' callfunc for type typename (SDP)"
    return (lambda i,o: "arange(%s, dtype='%s')" % (arg_product_str(i), typename)
            if (len(i)==1) else "reshape(arange(%s, dtype='%s'), [%s])" %
            ( arg_product_str(i), typename, reverse_arg_str(i) ) )

#--------------------------------------------------------------------
def typeconv(typename):
    "Returns a type-conversion callfunc for type typename"
    return (lambda i,o: '%s(%s)' % (typename.lower(), i[0]))

#  This may be more general, and can handle string argument like '123'
##def typeconv(typename):
##   "Returns a type-conversion callfunc for type typename"
##   return (lambda i,o: "array(%s, copy=0).astype('%s')" % (i[0], typename))

#--------------------------------------------------------------------
def idl_key_set(key_str, inpars):
    
    #----------------------------------------------------------------
    # NB! i2py converts IDL keywords to upper case, full names.
    #     The idl_*_callfunc routines treat keywords as lower case,
    #     so we need to use upper() method in next 3 functions.
    #     Also see notes in "util.py".
    #----------------------------------------------------------------
    s1 = key_str.upper() + '=True'
    s2 = key_str.upper() + '=1'    
    # s1 = key_str.lower() + '=True'  ########## (11/06/08)
    # s2 = key_str.lower() + '=1'
    return ((s1 in inpars) or (s2 in inpars))

#--------------------------------------------------------------------
def idl_arg_list(inpars):
    
    #-------------------------------------------------------
    # NB!  An inpar with an equals sign could be a keyword
    #      that returns a value.  However, an argument can
    #      also contain an equals sign, as in:
    #         w = where(a eq 10)   (since eq -> ==)
    #         w = where(a le 10)   (since le -> <=)
    #      This routine must take this into account.
    #-------------------------------------------------------
    args = []
    for s in inpars:
        #-----------------------------------
        # Note: "==" can occur in argument
        #       but not in a keyword
        #-----------------------------------
        p1 = s.find('=')
        EQ = (s.find('==') != -1)
        LE = (s.find('<=') != -1)
        GE = (s.find('>=') != -1)
        NE = (s.find('!=') != -1)
        COMPARISON = (EQ or LE or GE or NE)
        #----------------------------------------------
        # If "=" is inside a string, it's an argument
        #----------------------------------------------
        IN_QUOTES = re.search("'.*=.*'", s) or \
                    re.search('".*=.*"', s)
        
        if (p1 == -1) or COMPARISON or IN_QUOTES:
            args.append(s)
    return args

#--------------------------------------------------------------------
def idl_key_list(inpars):
    
    #-----------------------------------------------
    # Note: keys all have "=" now (vs. "/")
    # This isn't used anywhere now.
    # Need to change due to Notes in "idl_arg_list"
    #-----------------------------------------------
    keys = []
    for s in inpars:
        p = s.find('=')
        if (p != -1):
            name = s.split('=')[0]
            keys.append(name.upper()) #######
    return keys

#--------------------------------------------------------------------
def idl_key_index(key_str, inpars):
    
    #---------------------------------------------------
    # Note: This cannot yet distiguish between keyword
    #       names like "levels" and "nlevels".
    #---------------------------------------------------
    for k in xrange(len(inpars)):
        s = inpars[k]
        p = s.find( key_str.upper() + '=' )
        # p = s.find( key_str.lower() + '=' )  ########### (11/06/08)
        if (p == 0): return k
    return -1

#--------------------------------------------------------------------
##def idl_key_present(key_str, inpars):

##    k = key_str.lower()
##    keys = []
##    for s in inpars:
##        p = s.find('=')
##        if (p != -1):
##            w = s.split('=')
##            keys.append(w[0].lower())
##    return (k in keys)

#--------------------------------------------------------------------
def reverse_arg_str(i):
    a = idl_arg_list(i)
    return ', '.join([ a[n] for n in xrange(len(a)-1, -1, -1) ])

#--------------------------------------------------------------------
def arg_product_str(i):
    return '*'.join([ i[n] for n in xrange(len(i)) ])

#--------------------------------------------------------------------
def keyword_var(inpar):
    return inpar.split('=')[1]

#--------------------------------------------------------------------
def remove_chars(s, chars):
    for c in chars: s = s.replace(c,'')
    return s

#--------------------------------------------------------------------
def get_window_index_string(istr):
    # matplotlib window indices start at 1
    try:
        index_str = str(eval(istr) + 1)
    except:
        # Can't use eval because index argument is a variable
        index_str = (istr + '+1')

    return index_str

#--------------------------------------------------------------------
def numpy_type_name(code):
    type_map = {0:'UNDEFINED', 1:'UInt8', 2:'Int16', 3:'Int32',
                4:'Float32', 5:'Float64', 6:'Complex64', 7:'str',
                8:'STRUCTURE', 9:'Complex128', 10:'POINTER',
                11:'OBJREF', 12:'UInt16', 13:'UInt32', 14:'Int64',
                15:'UInt64'}
    dtype = type_map[code]
    return dtype

#--------------------------------------------------------------------
def idl_type_code(dtype):
    # Currently unused
    type_map = {'uint8':1, 'int16':2, 'int32':3, 'float32':4,
                'float64':5, 'complex64':6, 'str':7, 'complex128':9,
                'uint16':12, 'uint32':13, 'int64':14, 'uint64':15}
    return type_map[dtype]
        
################################################################################
#
#  IDL function and procedure maps, grouped by type
#
################################################################################

#---------------------------------------
#  Time-related routines (import time)
#---------------------------------------
map_func('SYSTIME', inpars=[1], callfunc=(lambda i,o: 'time.time()'),
          extracode='import time')
map_pro('WAIT', inpars=[1], callfunc=(lambda i,o: 'time.sleep(%s)' % i[0]),
        extracode='import time')

#----------------------------
#  Pointer-related routines
#----------------------------
# map_pro('PTRARR', ### Included with Array Init routines below.
map_pro('PTR_FREE', inpars=range(1,33), noptional=31,
        callfunc=(lambda i,o: idl_ptr_free_callfunc(i,o)) )
map_func('PTR_NEW', inpars=[1], noptional=1,
        inkeys=['ALLOCATE_HEAP','NO_COPY'],
        callfunc=(lambda i,o: idl_ptr_new_callfunc(i,o)) )
##map_func('PTR_VALID', inpars=[1], noptional=1,
##         # inkeys=['CAST','COUNT'],
##        callfunc=(lambda i,o: idl_ptr_valid_callfunc(i,o)) )

#---------------------------
#  Error handling routines
#----------------------------------------
#  Maybe use Python's RAISE statement ?
#  e.g. raise IOError
#----------------------------------------
#  http://python.about.com/od/pythonstandardlibrary/a/lib_exceptions.htm

map_pro('CATCH', inpars=[1],
        callfunc=(lambda i,o: '# CATCH, %s' % i[0] ))
map_pro('ON_ERROR', inpars=[1],
        callfunc=(lambda i,o: '# ON_ERROR, %s' % i[0] ))
# map_pro('ON_IOERROR', inpars=[1],
map_pro('MESSAGE', inpars=[1], inkeys=['INFORMATIONAL'],
        callfunc=(lambda i,o: idl_message_callfunc(i,o)),
        extracode='import sys')     
map_pro('STOP', inpars=range(1,33), noptional=32,
        callfunc=(lambda i,o: 'sys.exit()'), extracode='import sys')

#------------------------------------------------------
#  Operating system calls (import os, glob or shutil)
#------------------------------------------------------
#  Can use methods in os.path, e.g. abspath, dirname,
#  basename, exists, getsize(filename), isdir, split
#  Also check out os.stat (for filesize, etc.)
#------------------------------------------------------
map_pro('CD', inpars=[1], noptional=1, inkeys=['CURRENT'],    
        callfunc=(lambda i,o: idl_cd_callfunc(i,o)),
#       callfunc=idl_cd_callfunc(i,o),   ####  This doesn't work  #### 
        extracode='import os')
map_func('EOF', inpars=[1],
         callfunc=(lambda i,o: idl_eof_callfunc(i,o)),
         extracode='import os')
map_pro('FILE_CHMOD', inpars=[1,2], noptional=0,
        callfunc=(lambda i,o: 'os.chmod(%s,%s)' % (i[0],i[1]) ),
        extracode='import os')
map_pro('FILE_COPY', inpars=[1,2], noptional=0,
        callfunc=(lambda i,o: 'shutil.copyfile(%s,%s)' % (i[0],i[1]) ),
        extracode='import shutil')
map_pro('FILE_DELETE', inpars=range(1,33), noptional=31,
        callfunc=(lambda i,o: idl_file_delete_callfunc(i,o)),
        extracode='import idl_func, os')
# map_func('FILE_INFO',   inpars=[1],
# map_func('FILE_LINES',  inpars=[1],
map_func('FINDFILE', inpars=[1], inkeys=['COUNT'],
         callfunc=(lambda i,o: idl_file_search_callfunc(i,o)),
         extracode='import glob')          
map_func('FILE_SEARCH', inpars=[1], inkeys=['COUNT'],
         callfunc=(lambda i,o: idl_file_search_callfunc(i,o)),
         extracode='import glob') 
map_func('FILE_TEST', inpars=[1], inkeys=['DIRECTORY'],
         callfunc=(lambda i,o: 'os.path.exists(%s)' % i[0]),
         extracode='import os')
map_func('FSTAT', inpars=[1],
         callfunc=(lambda i,o: idl_fstat_callfunc(i,o)),
         extracode='import os')
map_func('PATH_SEP', callfunc=(lambda i,o: 'os.sep'),
          extracode='import os')
map_pro('SPAWN', inpars=[1], callfunc=(lambda i,o: 'os.system(%s)' % i[0]),
        extracode='import os')

#-------------------------------------
#  File manipulation procedures
#  For more info, try "help(file)"
#  Python "open" is alias to "file".
#-----------------------------------------------------------
#  NOTE:  In IDL, files are opened before we know whether
#         we will be reading text or binary, so how can we
#         convert properly?
#-----------------------------------------------------------
map_pro('CLOSE', inpars=range(1,11), noptional=10, inkeys=['ALL'],
        callfunc=(lambda i,o: idl_close_callfunc(i,o)),
        extracode='import os, idl_func')
map_pro('FREE_LUN', inpars=range(1,11), noptional=9,
        callfunc=(lambda i,o: idl_close_callfunc(i,o)),
        extracode='import os, idl_func')
map_pro('GET_LUN', inpars=[1],
        callfunc=(lambda i,o: idl_get_lun_callfunc(i,o)) )
map_pro('OPENR', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN'],
        callfunc=(lambda i,o: idl_openr_callfunc(i,o)) )
map_pro('OPENU', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN'],
        callfunc=(lambda i,o: idl_openu_callfunc(i,o)) )
map_pro('OPENW', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN'],
        callfunc=(lambda i,o: idl_openw_callfunc(i,o)) )
map_pro('POINT_LUN', inpars=[1,2],
        callfunc=(lambda i,o: idl_point_lun_callfunc(i,o)) )

map_pro('PRINT', inpars=range(1,101), noptional=99, inkeys=['FORMAT'],
        callfunc=(lambda i,o: idl_print_callfunc(i,o)) )
        ## extracode='import numpy')  NOT NEEDED
map_pro('PRINTF', inpars=range(1,102), noptional=99, inkeys=['FORMAT'],
        callfunc=(lambda i,o: idl_printf_callfunc(i,o)) )

##map_pro('READ', inpars=range(1,17), noptional=14,
##        callfunc=(lambda i,o: idl_read_callfunc(i,o)) )
map_pro('READF', inpars=range(1,17), noptional=14, inkeys=['FORMAT'],
         callfunc=(lambda i,o: idl_readf_callfunc(i,o)) )
map_pro('READS', inpars=range(1,17), noptional=14,
         callfunc=(lambda i,o: idl_reads_callfunc(i,o)) )
map_pro('READU', inpars=range(1,17), noptional=14,
        callfunc=(lambda i,o: idl_readu_callfunc(i,o)) )
map_pro('WRITEU', inpars=range(1,17), noptional=14, 
        callfunc=(lambda i,o: idl_writeu_callfunc(i,o)) )

#------------------------------
#  Type conversion functions
#-------------------------------------------------------
#  Note:  Numpy also supports 'Float96' = 'longdouble'
#-------------------------------------------------------
map_func('BYTE',   inpars=range(1,11), noptional=9,
         callfunc=(lambda i,o: idl_byte_callfunc(i,o)),
         extracode='import idl_func')
map_func('FIX',     inpars=[1], callfunc=typeconv('Int16'))
map_func('LONG',    inpars=[1], callfunc=typeconv('Int32'))
map_func('LONG64',  inpars=[1], callfunc=typeconv('Int64'))
map_func('FLOAT',   inpars=[1], callfunc=typeconv('Float32'))
map_func('DOUBLE',  inpars=[1], callfunc=typeconv('Float64'))
map_func('UINT',    inpars=[1], callfunc=typeconv('UInt16'))
map_func('ULONG',   inpars=[1], callfunc=typeconv('UInt32'))
map_func('ULONG64', inpars=[1], callfunc=typeconv('UInt64'))
map_func('REAL_PART', inpars=[1], callfunc=(lambda i,o: 'real(%s)' % i[0]),
         extracode='from numpy.lib.type_check import *')
map_func('IMAGINARY', inpars=[1], callfunc=(lambda i,o: 'imag(%s)' % i[0]),
         extracode='from numpy.lib.type_check import *')
#---------------------------------------------------------
# Note: 'Complex64' means two 32-bit floats.
#       IDL's COMPLEX and DCOMPLEX accept multiple args,
#       but this is not supported yet.
#---------------------------------------------------------
map_func('COMPLEX',  inpars=[1], callfunc=typeconv('Complex64') )
map_func('DCOMPLEX', inpars=[1], callfunc=typeconv('Complex128') )
# map_func('MACHAR', inpars=[1], callfunc= ### numpy.lib.machar  ###)

#-------------------------
#  Array initializations
#-------------------------
map_func('BYTARR',    inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('UInt8'))
map_func('INTARR',    inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('Int16'))
map_func('LONARR',    inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('Int32'))
map_func('LON64ARR',  inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('Int64'))
map_func('FLTARR',    inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('Float32'))
map_func('DBLARR',    inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('Float64'))
map_func('UINTARR',   inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('UInt16'))
map_func('ULONARR',   inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('UInt32'))
map_func('ULON64ARR', inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('UInt64'))
map_func('PTRARR', inpars=range(1,9), noptional=7,
         inkeys=['NOZERO','ALLOCATE_HEAP'],
         callfunc=(lambda i,o: idl_ptrarr_callfunc(i,o)) )

map_pro('STRARR', inpars=range(1,9), noptional=7, 
        callfunc=(lambda i,o: idl_strarr_callfunc(i,o)) )

##map_func('STRARR', inpars=range(1,9), noptional=7,
##         callfunc=arrgen('str'))
#---------------------------------------------------------------
map_func('COMPLEXARR', inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('Complex64') )
map_func('DCOMPLEXARR', inpars=range(1,9), noptional=7,
         inkeys=['NOZERO'], callfunc=arrgen('Complex128') )
#---------------------------------------------------------------
# Unsupported keywords: 'OBJ','PTR','DIMENSION','SIZE','VALUE'
#---------------------------------------------------------------
map_func('MAKE_ARRAY', inpars=range(1,9), noptional=7,
         inkeys=['BYTE','DOUBLE','FLOAT','INTEGER','L64','LONG',
                 'STRING','UINT','UL64','ULONG','NOZERO',
                 'INDEX','_TYPE','COMPLEX','DCOMPLEX'],
         callfunc=(lambda i,o: idl_make_array_callfunc(i,o)) )

#----------------------------------------
#  "Ramp functions" similar to "arange"
#-----------------------------------------------
#  Need to handle multiple dimension arguments
#-----------------------------------------------
map_func('BINDGEN',    inpars=range(1,9), noptional=7, callfunc=rampgen('UInt8'))
map_func('INDGEN',     inpars=range(1,9), noptional=7, callfunc=rampgen('Int16'))
map_func('LINDGEN',    inpars=range(1,9), noptional=7, callfunc=rampgen('Int32'))
map_func('FINDGEN',    inpars=range(1,9), noptional=7, callfunc=rampgen('Float32'))
map_func('DINDGEN',    inpars=range(1,9), noptional=7, callfunc=rampgen('Float64'))
map_func('UINDGEN',    inpars=range(1,9), noptional=7, callfunc=rampgen('UInt16'))
map_func('ULINDGEN',   inpars=range(1,9), noptional=7, callfunc=rampgen('UInt32'))
map_func('UL64INDGEN', inpars=range(1,9), noptional=7, callfunc=rampgen('UInt64'))
map_func('CINDGEN',    inpars=range(1,9), noptional=7, callfunc=rampgen('Complex64'))
map_func('DCINDGEN',   inpars=range(1,9), noptional=7, callfunc=rampgen('Complex128'))
map_func('SINDGEN',    inpars=range(1,9), noptional=7,
         callfunc=(lambda i,o: idl_sindgen_callfunc(i,o)) )
##         callfunc=(lambda i,o: 'idl_func.sindgen(%s)' % i[0]),
##         extracode='import idl_func')
         
#-------------------------------
#  Mathematical functions
#--------------------------------------------------
#  Ones with same names include: ceil, cos, cosh,
#  exp, floor, sin, sinh, sqrt, tan, tanh
#--------------------------------------------------
map_func('ABS',    inpars=[1], callfunc=(lambda i,o: 'absolute(%s)' % i[0]))
map_func('ACOS',   inpars=[1], callfunc=(lambda i,o: 'arccos(%s)'   % i[0]))
map_func('ALOG',   inpars=[1], callfunc=(lambda i,o: 'log(%s)'      % i[0]))
map_func('ALOG10', inpars=[1], callfunc=(lambda i,o: 'log10(%s)'    % i[0]))
map_func('ASIN',   inpars=[1], callfunc=(lambda i,o: 'arcsin(%s)'   % i[0]))
map_func('ATAN',   inpars=[1,2], noptional=1,
         callfunc=(lambda i,o: 'arctan(%s)' % i[0] if (len(i)==1)
                   else 'arctan2(%s,%s)' % (i[1],i[0]) ))
map_func('CEIL',   inpars=[1],
         callfunc=(lambda i,o: "ceil(%s).astype('Int32')" % i[0]))
# map_func('FFT',    inpars=[1],
map_func('FINITE', inpars=[1,2,3], noptional=2, inkeys=['INFINITY','NAN'],
         callfunc=(lambda i,o: idl_finite_callfunc(i,o)) )
map_func('FLOOR',  inpars=[1],
         callfunc=(lambda i,o: "floor(%s).astype('Int32')" % i[0]))
map_func('MIN', inpars=[1,2,3,4,5], noptional=4,
         inkeys=['MAX','NAN','SUBSCRIPT_MAX'],
         callfunc=(lambda i,o: idl_min_callfunc(i,o)) )
map_func('MAX', inpars=[1,2,3,4,5], noptional=4,
         inkeys=['MIN','NAN','SUBSCRIPT_MIN'],
         callfunc=(lambda i,o: idl_max_callfunc(i,o)) )
map_func('RANDOMN', inpars=range(1,10), noptional=9,
         inkeys=['BINOMIAL','DOUBLE','GAMMA','LONG','NORMAL','POISSON','UNIFORM'],
         callfunc=(lambda i,o: idl_random_callfunc(i,'RANDOMN') ))
map_func('RANDOMU', inpars=range(1,10), noptional=9,
         inkeys=['BINOMIAL','DOUBLE','GAMMA','LONG','NORMAL','POISSON','UNIFORM'],
         callfunc=(lambda i,o: idl_random_callfunc(i,'RANDOMU') ))

# May be able to use numpy.linalg.lstsq(x,y) ##################
# map_func('REGRESS',  inpars=[1],

map_func('ROUND',    inpars=[1], callfunc=(lambda i,o: "around(%s).astype('Int32')" % i[0]))
map_func('TOTAL', inpars=[1,2,3,4], noptional=3,
         inkeys=['CUMULATIVE','DOUBLE','NAN'],
         callfunc=(lambda i,o: idl_total_callfunc(i,o) ))
# map_pro('TRIANGULATE', inpars=[1],
# map_func('TRIGRID',  inpars=[1],

#--------------------------------------
#  String manipulation functions
#-----------------------------------------------------------
#  In IDL, we have "a = execute(<string>)", but in Python
#  we just have "exec(<string>)".  So here we just set the
#  IDL variable (e.g. "a") to 1 (for success) and then call
#  "exec" on the next line.
#-----------------------------------------------------------
map_func('EXECUTE', inpars=[1,2,3], noptional=2,
         callfunc=(lambda i,o: '1  # (EXEC has no return value)\nexec(%s)'
         % i[0].replace('&',';')) )
# map_func('READS', inpars=[1],
map_func('STRING', inpars=range(1,101), noptional=99, inkeys=['FORMAT'],
         callfunc=(lambda i,o: idl_string_callfunc(i,o)) )
         ## extracode='import numpy')  NOT NEEDED
map_func('STRLEN',     inpars=[1], callfunc=(lambda i,o: 'len(%s)' % i[0]))
map_func('STRLOWCASE', inpars=[1], callfunc=(lambda i,o: '%s.lower()' % i[0]))
# STRMID also has a REVERSE_OFFSET keyword and accepts array arguments
map_func('STRMID',     inpars=[1,2,3], noptional=1,
         callfunc=(lambda i,o: '%s[%s:]' % (i[0],i[1])
                   if (len(i)==2) else '%s[%s:%s]' %
                   (i[0], i[1], (i[1] + '+' + i[2])) ))
                   # Can't evaluate if i[1] or i[2] is a variable
                   #(i[0], i[1], str(eval(i[1]) + eval(i[2]))) ))

# Returns index or -1 if substring is not found, just like IDL
map_func('STRPOS', inpars=[1,2], callfunc=(lambda i,o: '%s.find(%s)' % (i[0],i[1]) ))
# Note that length of destination string should not change.
map_pro('STRPUT', inpars=[1,2,3], noptional=1,
        callfunc=(lambda i,o: '%s = (%s[:%s] + %s + %s[%s+len(%s):])[:len(%s)]' %
                  (i[0], i[0], i[2], i[1], i[0], i[2],i[1],i[0]) if (len(i)==3)
                  else '%s = (%s + %s[len(%s):])[:len(%s)]' %
                  (i[0], i[1], i[0], i[1], i[0]) ))
map_func('STRSPLIT',   inpars=[1,2,3], noptional=2,
         inkeys=['EXTRACT','COUNT','LENGTH'],
         callfunc=(lambda i,o: idl_strsplit_callfunc(i,o) ))
map_func('STRTRIM', inpars=[1,2], noptional=1,
         callfunc=(lambda i,o: idl_strtrim_callfunc(i,o) ))
map_func('STRUPCASE',  inpars=[1], callfunc=(lambda i,o: '%s.upper()' % i[0]))

#-------------------------------------
#  Image manipulation functions
#-------------------------------------------------------------
#  Check out imageop module, esp. imageop.scale (like rebin)
#  Check out colorsys, imghdr, jpeg,  modules.
#-------------------------------------------------------------
# Not fully supported yet.
map_func('BYTSCL', inpars=[1], inkeys=['MAX','MIN','TOP'],
         callfunc=(lambda i,o: idl_bytscl_callfunc(i,o) ))

# map_func('CONGRID', inpars=[1],
# map_func('HIST_EQUAL', inpars=[1],

##  Could maybe use:
##    imageop.scale(image, psize, width, height, newwidth, newheight)
##  but need image to be "8 or 32 bit pixels stored in python strings"
##
map_func('REBIN', inpars=range(1,10), noptional=7, inkeys=['SAMPLE'],
         callfunc=(lambda i,o: idl_rebin_callfunc(i,o)) )

#-------------------------------------
#  Array manipulation functions
#-------------------------------------
# map_func('ASSOC', inpars=[1],

## See IDL help pages for the formula that is used.
# map_func('BILINEAR',

# CONJ and CONJUGATE are synonyms in NumPy, and work the same.
# map_func('CONJ', inpars=[1], callfunc=(lambda i,o: 'conj(%s)' % i[0]))

# NumPy's CONVOLVE only works for two 1D arrays.
# But scipy.signal.convolve, or convolve2d should work.  ###############
# What about numpy.numarray.convolve.convolve2d ?? ##############

# map_func('CONVOL', inpars=[1],

map_func('DETERM', inpars=[1], callfunc=(lambda i,o: 'linalg.det(%s)' % i[0]))
#-------------------------------------------------
#  Need to support keyword options to HIST_2D.
#-------------------------------------------------
map_func('HIST_2D', inpars=[1,2], callfunc=(lambda i,o: 'histogram2d(%s,%s)[0]' % (i[0],i[1])))
#---------------------------------------------------
#  Need to support keyword options to HISTOGRAM.
#  The 2nd return value from NumPy's HISTOGRAM
#  is "lower_edges of bins (float)".  Can perhaps
#  use this in a call to NumPy's DIGITIZE to get
#  same thing as IDL's "REVERSE_INDICES" keyword.
#---------------------------------------------------
map_func('HISTOGRAM',  inpars=[1], noptional=0,
         inkeys=['BINSIZE','INPUT','MAX','MIN','NAN','NBINS',
                 'OMAX','OMIN','REVERSE_INDICES'],
         callfunc=(lambda i,o: idl_histogram_callfunc(i,o) ))

# map_func('INTERPOL', inpars=[1],   ##### maybe use numpy.interp

#----- from Matrix import *, then invert(a) also seems to work
map_func('INVERT', inpars=[1], callfunc=(lambda i,o: 'linalg.inv(%s)' % i[0]))
# map_func('ISHFT', inpars=[1],  ### goes to right_shift(), left_shift
# map_func('LUSOL',  ###########

map_func('N_ELEMENTS', inpars=[1],
         callfunc=(lambda i,o: idl_n_elements_callfunc(i,o)) )

map_func('NORM', inpars=[1], callfunc=(lambda i,o: 'linalg.norm(%s)' % i[0]))
## REFORM's OVERWRITE keyword is not supported yet.
map_func('REFORM', inpars=range(1,9), noptional=7, 
         callfunc=(lambda i,o: idl_reform_callfunc(i,o) ))
#---------------------------------------------------
#  Use NumPy's REPEAT function, which can do
#  strings, numbers and structures, similar to IDL.
#  Only supports 1D arrays as written.
#---------------------------------------------------
map_func('REPLICATE', inpars=[1,2],
         callfunc=(lambda i,o: 'repeat(%s,%s)' % (i[0],i[1]) ) )
##map_func('REPLICATE', inpars=range(1,10), noptional=7,
##         callfunc=(lambda i,o: '(%s)*ones([%s])' % (i[0],
##	           ', '.join([ i[n] for n in xrange(len(i)-1, 0, -1) ]))))
map_func('REVERSE', inpars=[1], callfunc=(lambda i,o: idl_reverse_callfunc(i,o)) )
map_func('ROTATE', inpars=[1,2], callfunc=(lambda i,o: idl_rotate_callfunc(i,o)) )
map_func('SHIFT', inpars=[1,2,3,4], noptional=2,
         callfunc=(lambda i,o: idl_shift_callfunc(i,o)) )
map_func('SIZE', inpars=[1],
         inkeys=['DIMENSIONS','N_DIMENSIONS','N_ELEMENTS','_TYPE'],
         callfunc=(lambda i,o: idl_size_callfunc(i,o) ))

# map_func('SMOOTH',     inpars=[1],
map_func('SORT',  inpars=[1], callfunc=(lambda i,o: 'argsort(ravel(%s))' % i[0]))

#  TEMPORARY capability is also available in Numpy because ufuncs
#  can take an optional output argument.
# map_func('TEMPORARY', inpars=[1],

## TRANSPOSE command is same in IDL and NumPy
## map_func('TRANSPOSE', inpars=[1], callfunc=(lambda i,o: 'transpose(%s)' % i[0]))

# map_func('TRISOL',  ###########

map_func('UNIQ',  inpars=[1,2], noptional=1,
         callfunc=(lambda i,o: idl_uniq_callfunc(i,o)) )
map_func('WHERE', inpars=[1,2], noptional=1,
         inkeys=['COMPLEMENT','NCOMPLEMENT'],
         callfunc=(lambda i,o: idl_where_callfunc(i,o)) )

#---------------------------------------------
#  Device and Window manipulation procedures
#---------------------------------------------
#  Use the Device Context (DC) in wxPython
#  IDL's DEVICE has _lots_ of keywords.
#------------------------------------------------------
#  The standard usage of "set_plot" and "device" is
#  largely replaced by savefig in matplotlib.pyplot.
#  e.g.
#     IDL> set_plot, 'ps'
#     IDL> device, file='foo.eps', /land
#     IDL> plot, x, y
#     IDL> device, /close
#     IDL> set_plot, 'win'
#  gets replaced by: "savefig('foo.eps')" and
#  can get other image formats with:
#     savefig('foo.pdf'), savefig('foo.png'), etc.
#------------------------------------------------------
#  IDL's DEVICE is also often used as in:
#     IDL> device, decomposed=0  ;(decomposed colors)
#------------------------------------------------------
map_pro('DEVICE', inkeys=['CLOSE','DECOMPOSED','FILENAME',
                          'GET_VISUAL_DEPTH', 'GET_SCREEN_SIZE'],
        callfunc=(lambda i,o: idl_device_callfunc(i,o)) )
# ERASE has an optional background color arg
map_pro('ERASE', inpars=[1], noptional=1,
        callfunc=(lambda i,o: 'matplotlib.pyplot.clf()'),
        extracode='import matplotlib.pyplot')
# map_pro('SET_PLOT', inpars=[1],
#         callfunc=
map_pro('WDELETE', inpars=range(1,101), noptional=100,
        callfunc=(lambda i,o: idl_wdelete_callfunc(i,o)),
        extracode='import matplotlib.pyplot')
map_pro('WINDOW',  inpars=[1], noptional=1,
        inkeys=['FREE','XSIZE','YSIZE','TITLE','XPOS','YPOS'],
        # inkeys=['FREE','PIXMAP','RETAIN','TITLE','XPOS','YPOS','XSIZE','YSIZE'],
        callfunc=(lambda i,o: idl_window_callfunc(i,o)),
        extracode='import matplotlib.pyplot')
map_pro('WSET', inpars=[1], noptional=1,
        callfunc=(lambda i,o: idl_wset_callfunc(i,o)),
        extracode='import matplotlib.pyplot')

#-----------------------------------------------
#  Plotting procedures (via matplotlib.pyplot)
#-----------------------------------------------------------------
#  The complete set of IDL Graphics Keywords are:
#     BACKGROUND, CHANNEL, CHARSIZE, CHARTHICK, CLIP, COLOR,
#     DATA, DEVICE, FONT, LINESTYLE, NOCLIP, NODATA, NOERASE,
#     NORMAL, ORIENTATION, POSITION, PSYM, SUBTITLE, SYMSIZE,
#     T3D, THICK, TICKLEN, TITLE, [XYZ]CHARSIZE, [XYZ]GRIDSTYLE,
#     [XYZ]MARGIN, [XYZ]MINOR, [XYZ]RANGE, [XYZ]STYLE,
#     [XYZ]THICK, [XYZ]TICK_GET, [XYZ]TICKFORMAT,
#     [XYZ]TICKINTERVAL, [XYZ]TICKLAYOUT, [XYZ]TICKLEN,
#     [XYZ]TICKNAME, [XYZ]TICKS, [XYZ]TICKUNITS, [XYZ]TICKV,
#     [XYZ]TITLE, Z, ZVALUE
#-----------------------------------------------------------------
# Use "contour" and "contourf" in matplotlib.
map_pro('CONTOUR', inpars=[1,2,3], noptional=2,
        inkeys=['BACKGROUND','C_COLORS','C_LABELS','C_LINESTYLE',
                'C_THICK',
                'CELL_FILL', 'CLOSED','DEVICE','DOWHILL','FILL',
                'FOLLOW','IRREGULAR','ISOTROPIC','LEVELS',
                'MAX_VALUE','MIN_VALUE','NLEVELS','NOERASE',
                'OVERPLOT','POSITION','XSTYLE','YSTYLE'],
        ## Unsupported: BACKGROUND, C_COLORS, C_LABELS, C_LINESTYLE,
        ##    C_THICK, CLOSED DEVICE, 
        ##    NOERASE, POSITION, XSTYLE, YSTYLE
        callfunc=(lambda i,o: idl_contour_callfunc(i,o)),
        extracode='import matplotlib.pyplot')

#         inkeys=['C_ANNOTATION','C_CHARSIZE','C_CHARTHICK','C_COLORS',
#                 'C_LABELS','C_LINESTYLE','CELL_FILL','FILL',
#                 'C_ORIENTATION','C_SPACING','C_THICK',
#                 'DOWNHILL','FOLLOW','IRREGULAR','ISOTROPIC','LEVELS',
#                 'NLEVELS','MAX_VALUE','MIN_VALUE','OVERPLOT',
#                 'PATH_DATA_COORDS','PATH_FILENAME','PATH_INFO',
#                 'PATH_XY','TRIANGULATION','PATH_DOUBLE','XLOG','YLOG',
#                 'ZAXIS'],

# map_pro('OPLOT',   (use "hold" or "over" in matplotlib ??)

# Compare "plot" and "scatter" in matplotlib.
map_pro('PLOT', inpars=[1,2], noptional=1,
        inkeys=['BACKGROUND','COLOR','ISOTROPIC','LINESTYLE',
                'POLAR','POSITION','PSYM','SYMSIZE','THICK','TITLE',
                'XLOG','XMARGIN','XRANGE','XSTYLE','XTICKS','XTITLE',
                'YLOG','YMARGIN','YRANGE','YSTYLE','YTICKS','YTITLE',
                'YNOZERO'],
        callfunc=(lambda i,o: idl_plot_callfunc(i,o)),
        extracode='import matplotlib.pyplot')

map_pro('PLOT_FIELD', inpars=[1,2], noptional=0,
        inkeys=['LENGTH','TITLE'],
        callfunc=(lambda i,o: idl_plot_field_callfunc(i,o)),
        extracode='import matplotlib.pyplot')
#       inkeys=['ASPECT','LENGTH','N','TITLE'],

# map_pro('PLOTS',

# map_pro('SURFACE', inpars=[1,2,3], noptional=2,
#         inkeys=['.....'],
#         callfunc=(lambda i,o: idl_surface_callfunc(i,o)),
#         extracode='import matplotlib.pyplot')

map_pro('TV', inpars=range(1,5), noptional=3,
        inkeys=['CENTIMETERS','INCHES','ORDER','TRUE','WORDS'
                'XSIZE','YSIZE'],
        callfunc=(lambda i,o: idl_tv_callfunc(i,o)),
        extracode='import matplotlib.pyplot')

map_pro('TVSCL', inpars=range(1,5), noptional=3,
        inkeys=['CENTIMETERS','INCHES','ORDER','TRUE','WORDS'
                'XSIZE','YSIZE'],
        callfunc=(lambda i,o: idl_tvscl_callfunc(i,o)),
        extracode='import matplotlib.pyplot')

map_pro('XYOUTS', inpars=[1,2,3], noptional=2,
        inkeys=['COLOR','NORMAL'],
        callfunc=(lambda i,o: idl_xyouts_callfunc(i,o)),
        extracode='import matplotlib.pyplot')
##        inkeys=['ALIGNMENT','CHARSIZE','CHARTHICK','TEXT_AXES',
##                'WIDTH','CLIP','COLOR','DATA','DEVICE','NORMAL',
##                'FONT','ORIENTATION','NOCLIP','T3D','Z']

#------------------------------------
#  Native GUI dialogs (via wxPython)
#------------------------------------
map_func('DIALOG_PICKFILE',
         # inkeys = ['DIRECTORY', 'GET_PATH', .... (not ready yet)
         inkeys=['DIALOG_PARENT','_FILE','FILTER','MULTIPLE_FILES',
                 'MUST_EXIST','OVERWRITE_PROMPT','PATH','READ',
                 'TITLE','WRITE'],
         callfunc=(lambda i,o: idl_dialog_pickfile_callfunc(i,o)),
         extracode='import wx, os')

#------------------------------
#  Additional procedures
#------------------------------
map_pro('ONLINE_HELP', inpars=[1], noptional=1,
        inkeys=['BOOK','FULL_PATH','QUIT'],
        callfunc=(lambda i,o: idl_online_help_callfunc(i,o)),
        extracode='import webbrowser')

# map_pro('RESTORE', inpars=[1],
# map_pro('SAVE', inpars=[1],

################################################################################
#
#  A few utilities used by the "callfuncs" below, alphabetical order
#
################################################################################

def idl_appended_graphics_keywords(i):
   
    #------------------------------------------------------
    #  This function supports idl_plot_callfunc as well
    #  as idl_contour_callfunc.  See more comments below.
    #------------------------------------------------------
    cmds = ''

    #---------------------------
    # Handle the COLOR keyword
    #---------------------------
    k = idl_key_index('color', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += ", color='%s'" % idl_color_mapping(kv)
    
    #-------------------------------
    # Handle the LINESTYLE keyword
    #--------------------------------------------
    #  The IDL linestyles are:
    #  0=solid, 1=dotted, 2=dashed, 3=dash dot,
    #  4=dash dot dot, 5=long dashes
    #--------------------------------------------
    #  The matplotlib linestyles are:
    #  '-'=solid, '--'=dashed, '-.'=dash dot,
    #  ':'=dotted, 'steps'=?, 'steps-pre'=?,
    #  'steps-mid'=?, 'steps-post'=?.
    #  "steps" linestyles are like histograms.
    #--------------------------------------------
    linestyle_map = {0:'-', 1:':', 2:'--', 3:'-.',
                     4:'-.', 5:'-'}
    k = idl_key_index('linestyle', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += ", linestyle='%s'" % linestyle_map[eval(kv)]

    #--------------------------
    # Handle the PSYM keyword
    #---------------------------------------------------------
    #  The IDL plotting symbols are:
    #     0=None, 1=+, 2=*, 3=., 4=diamond, 5=triangle,
    #     6=square, 7=X, 8=user-defined (via USERSYM),
    #     9=undefined, 10="histogram mode".
    #     Negative values means connect symbols with lines.
    #---------------------------------------------------------
    #  The matplotlib (and MatLab ?) plotting symbols are:
    #     's'=square, 'o'=circle, '^'=triangle up,
    #     'v'=triangle down, '<'=triangle left,
    #     'd'=diamond, 'p'=pentagram, 'h'=hexagon,
    #     '8'=octagon.  (from help(scatter))
    #     Can also use (?): ',' '1','2','3','4' (help(plot))
    #     Seems that 'x' is allowed, but not '*' or 'X'.
    #     Default linestyle is '-'.  To get no lines, must
    #     set "linestyle='None'.
    #---------------------------------------------------------  
    symbol_map = {0:'None', 1:'+', 2:'p', 3:'.', 4:'d',
                  5:'^', 6:'s', 7:'x', 8:'None', 9:'None'}
    k = idl_key_index('psym', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += ", marker='%s'" % symbol_map[abs(eval(kv))]        
        p  = kv.find('-')  # check for minus sign
        if (p == -1):
           cmds += ", linestyle='None'"

    #-----------------------------
    # Handle the SYMSIZE keyword
    #-----------------------------
    k = idl_key_index('symsize', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += ', markersize=%s' % kv

    #---------------------------
    # Handle the THICK keyword
    #---------------------------
    k = idl_key_index('thick', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += ', linewidth=%s' % kv

    return cmds

#--------------------------------------------------------------------------
def idl_color_mapping(color_str):

    cstr = color_str.lower()
    
    #---------------------------------------------------
    #  If the color index in the IDL code was set to
    #  one of these names, we might find a match here.
    #---------------------------------------------------
    if (cstr == 'blue'):    return 'b'
    if (cstr == 'green'):   return 'g'
    if (cstr == 'red'):     return 'r'
    if (cstr == 'cyan'):    return 'c'
    if (cstr == 'magenta'): return 'm'
    if (cstr == 'yellow'):  return 'y'
    if (cstr == 'black'):   return 'k'
    if (cstr == 'white'):   return 'w'

    #----------------------------------------------------------
    #  Otherwise, the color index is applied to the currently
    #  active IDL color table.  So here, we just map numbers
    #  to semi-arbitrary colors, for now.
    #----------------------------------------------------------
    if (cstr == '0'):   return 'k'
    if (cstr == '255'): return 'w'
    if (cstr == '100'): return 'r'

    return 'k'   # (black)

#--------------------------------------------------------------------------
def idl_graphics_keyword_commands(i):
   
    #------------------------------------------------------------------
    #  Notes: Graphics keywords that are also implemented with
    #         keyword in matplotlib can be found in the routine above
    #         called idl_appended_graphics_keywords.  Those that are
    #         implemented as a separate command on a separate line
    #         can be found here.
    
    #         This function supports idl_plot_callfunc as well as the
    #         idl_contour_callfunc routine.
    #------------------------------------------------------------------
    #  The complete set of IDL Graphics Keywords are:
    #     BACKGROUND, CHANNEL, CHARSIZE, CHARTHICK, CLIP, COLOR,
    #     DATA, DEVICE, FONT, LINESTYLE, NOCLIP, NODATA, NOERASE,
    #     NORMAL, ORIENTATION, POSITION, PSYM, SUBTITLE, SYMSIZE,
    #     T3D, THICK, TICKLEN, TITLE, [XYZ]CHARSIZE, [XYZ]GRIDSTYLE,
    #     [XYZ]MARGIN, [XYZ]MINOR, [XYZ]RANGE, [XYZ]STYLE,
    #     [XYZ]THICK, [XYZ]TICK_GET, [XYZ]TICKFORMAT,
    #     [XYZ]TICKINTERVAL, [XYZ]TICKLAYOUT, [XYZ]TICKLEN,
    #     [XYZ]TICKNAME, [XYZ]TICKS, [XYZ]TICKUNITS, [XYZ]TICKV,
    #     [XYZ]TITLE, Z, ZVALUE

    #  The ISOTROPIC keyword gets used by PLOT and CONTOUR and has
    #  been added here as well.
    #------------------------------------------------------------------
    prefix = 'matplotlib.pyplot.'
    cmds = ''

    k1 = idl_key_index('xticks', i)
    k2 = idl_key_index('yticks', i)
    if (k1 != -1) or (k2 != -1):
        a = idl_arg_list(i)
        n_args = len(a)

    #--------------------------------
    # Handle the BACKGROUND keyword
    #--------------------------------
    k = idl_key_index('background', i)
    if (k != -1):
        kv  = keyword_var(i[k])
        cstr = idl_color_mapping(kv)
        cmds += "\n" + prefix + "axes(axisbg='%s')" % cstr

    #-------------------------------
    # Handle the ISOTROPIC keyword
    #-------------------------------
    if (idl_key_set('isotropic', i)):
        cmds += "\n" + prefix + "axis('equal')"

    #------------------------------
    # Handle the POSITION keyword
    #----------------------------------------------------
    # In IDL, arg = [x0,y0,x1,y1], where (x0,y0) and
    # (x1,y1) are normalized coords of lower-left and
    # upper-right corner.  In matplotlib, we have
    # arg = (x0, y0, xsize, ysize), where (x0,y0) is
    # as before, but normalized rectangle size is given.
    # Note that xsize=(x1-x0), ysize=(y1-y0).
    #----------------------------------------------------
    k = idl_key_index('position', i)
    if (k != -1):
        kv = keyword_var(i[k])
        kv = kv.replace('concatenate','')
        kv = kv.replace('array','')
        kv = kv.replace('([','')
        kv = kv.replace('])','')
        kv = kv.replace(' ','')
        vals = kv.split(',')
        ## print 'vals =', vals
        
        x0_str = vals[0]
        y0_str = vals[1]
        x1_str = vals[2]
        y1_str = vals[3]
        xL_str = str(eval(x1_str) - eval(x0_str))
        yL_str = str(eval(y1_str) - eval(y0_str))
        kv  = x0_str + ', ' + y0_str + ', '
        kv += xL_str + ', ' + yL_str
        cmds += ('\n' + prefix + 'axes((%s))' % kv)
     
    #---------------------------
    # Handle the TITLE keyword
    #---------------------------
    k = idl_key_index('title', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += '\n' + prefix + 'title(%s)' % kv

    #----------------------------
    # Handle the XMARGIN keyword
    #----------------------------
    k = idl_key_index('xmargin', i)
    if (k != -1):
        msg = 'Warning: XMARGIN keyword to PLOT not supported yet.'
        print msg
        # print_error_message('PLOT', msg)
        
    #----------------------------
    # Handle the XRANGE keyword
    #----------------------------    
    k = idl_key_index('xrange', i)
    if (k != -1):
        kv = keyword_var(i[k])
        kv = kv.replace('[','')
        kv = kv.replace(']','')
        cmds += '\n' + prefix + 'xlim(%s)' % kv

    #----------------------------
    # Handle the XSTYLE keyword
    #----------------------------
    #  e.g. force exact range or
    #  suppress entire axis
    #----------------------------
    k = idl_key_index('xstyle', i)
    if (k != -1):
        kv = keyword_var(i[k])
        code = eval(kv)
        bstr = numpy.binary_repr(code) + '00000'
        if (bstr[0] == '1'):
            cmds += "\n" + prefix + "axis('image')"
        if (bstr[2] == '1'):
            cmds += "\n" + prefix + "axis('off')"

    #----------------------------
    # Handle the XTHICK keyword
    #----------------------------
    
    #---------------------------------
    # Handle the XTICKS keyword
    # = number of equal-spaced ticks
    #---------------------------------
    k = idl_key_index('xticks', i)
    if (k != -1):
        kv = keyword_var(i[k])
        s  = 'numpy.linspace(%s.min(), %s.max(), %s)' % (a[0],a[0],kv)
        cmds += '\n' + prefix + 'xticks(%s)' % s
        
    #----------------------------
    # Handle the XTICKV keyword
    #----------------------------
    k = idl_key_index('xtickv', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += '\n' + prefix + 'xticks(%s)' % kv

    #----------------------------
    # Handle the XTITLE keyword
    #----------------------------    
    k = idl_key_index('xtitle', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += '\n' + prefix + 'xlabel(%s)' % kv

    #----------------------------
    # Handle the YMARGIN keyword
    #----------------------------
    k = idl_key_index('ymargin', i)
    if (k != -1):
        msg = 'Warning: YMARGIN keyword to PLOT not supported yet.'
        print msg
        # print_error_message('PLOT', msg)
        
    #----------------------------
    # Handle the YRANGE keyword
    #----------------------------    
    k = idl_key_index('yrange', i)
    if (k != -1):
        kv = keyword_var(i[k])
        kv = kv.replace('[','')
        kv = kv.replace(']','')
        cmds += '\n' + prefix + 'ylim(%s)' % kv

    #----------------------------
    # Handle the YSTYLE keyword
    #----------------------------
    #  e.g. force exact range or
    #  suppress entire axis
    #----------------------------
    #  So far, both axes same.
    #----------------------------
    k = idl_key_index('ystyle', i)
    if (k != -1):
        kv = keyword_var(i[k])
        code = eval(kv)
        bstr = numpy.binary_repr(code) + '00000'
        if (bstr[0] == '1'):
            cmds += "\n" + prefix + "axis('image')"
        if (bstr[2] == '1'):
            cmds += "\n" + prefix + "axis('off')"

    #----------------------------
    # Handle the YTHICK keyword
    #----------------------------
    
    #----------------------------
    # Handle the YTICKS keyword
    # = number of equal-spaced ticks
    #---------------------------------
    k = idl_key_index('yticks', i)
    if (k != -1):
        kv = keyword_var(i[k])
        if (n_args == 2): c = a[1]
        else: c = a[0]
        s  = 'numpy.linspace(%s.min(), %s.max(), %s)' % (c,c,kv)
        cmds += '\n' + prefix + 'yticks(%s)' % s    

    #----------------------------
    # Handle the YTICKV keyword
    #----------------------------
    k = idl_key_index('ytickv', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += '\n' + prefix + 'yticks(%s)' % kv
        
    #----------------------------
    # Handle the YTITLE keyword
    #----------------------------
    k = idl_key_index('ytitle', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += '\n' + prefix + 'ylabel(%s)' % kv

    return cmds

################################################################################
#
#  IDL function and procedure "callfuncs", alphabetical order
#
#  These show one way to handle keywords to a function that are used
#  in IDL to return values.  They must be included with inpars since
#  a function isn't allowed to have outpars.  The undefined variables
#  are set to expressions in separate function calls on subsequent lines.
#
################################################################################


#--------------------------------------------------------------------------
def idl_byte_callfunc(i,o):
    #---------------------------------------------------------------
    # Note: IDL's BYTE function is sometimes used to test the byte
    #       order of the current machine.  This is done as:
    #          big_endian = (byte(1,0,2))[0] eq 0b
    #       The 3 args are:  an integer, an offset in bytes and
    #          the number of dimensions of the result.

    #       In Python, we can just use "sys.byteorder", which is
    #       either "little" or "big".
    #---------------------------------------------------------------
    cmd = 'idl_func.byte(%s)' % i[0]
    return cmd
    
##    a = idl_arg_list(i)
##    n_args = len(a)
##    if (n_args == 1):
##        cmd = 'idl_func.byte(%s)' % i[0]
##        return cmd
##    elif (n_args == 3):
##        if (a[0]=='1') and (a[1]=='0') and (a[2]=='2'):
##            bmap = {'big':0,'little':1}
##            cmd = '[%s]' % bmap
##        elif:
##            print 'ERROR: I2PY only supports 1 argument to BYTE.'
##            
##    else:
##        print 'ERROR: I2PY only supports 1 argument to BYTE.'
##
##    return ''

#--------------------------------------------------------------------------
def idl_byte_callfunc2(i,o):
    #---------------------------------------------------------
    # Note:  IDL's BYTE function is overloaded.
    #        If arg is a string, then a byte array of ASCII
    #           ordinal values is returned.
    #        Otherwise, if arg is scalar or array, type
    #           is converted to (unsigned) byte.
    #--------------------------------------------------------- 
    #        If called with more than 1 arg, then it can
    #        be used to extract 1 byte of data from 1st arg.
    #        This is not supported yet.
    #---------------------------------------------------------    
    if (len(i) == 1):
        cmd  = "if (type(%s) == type('abc')):\n" % i[0]
        cmd += "    array(map(ord, %s), copy=0)\n" % i[0]
        cmd += "else:\n"
        cmd += "    array(%s, copy=0).astype('UInt8')" % i[0] 
    else:
        print 'Error: I2PY only supports 1 argument to BYTE.'
        cmd = ''
    return cmd

#--------------------------------------------------------------------------
def idl_bytscl_callfunc(i,o):

    #----------------------------------------------------------
    # Notes:  This doesn't yet test the argument to determine
    #         whether it is INTEGER or FLOAT (int assumed).
    #         Can use a.dtype  (if a is numpy.ndarray)
    #         if (str(a.dtype)[0] in ['i','u']) then INTEGER.
    
    #         The NAN keyword is not yet supported.
    #----------------------------------------------------------
    a = idl_arg_list(i)
    
    #---------------------
    # Handle MAX keyword
    #---------------------
    k = idl_key_index('max', i)
    if (k != -1):
        max_str = keyword_var(i[k])
    else:
        max_str = ('%s.max()' % a[0])
        
    #---------------------
    # Handle MIN keyword
    #---------------------
    k = idl_key_index('min', i)
    if (k != -1):
        min_str = keyword_var(i[k])
    else:
        min_str = ('%s.min()' % a[0])

    #---------------------
    # Handle TOP keyword
    #---------------------
    k = idl_key_index('top', i)
    if (k != -1):
        top_str = keyword_var(i[k])
    else:
        top_str = '255'

    #-----------------------
    # For integer argument
    #-------------------------------------------------
    # b = ((top + 1) * (x - xmin) - 1)/(xmax - xmin)
    #-------------------------------------------------
    s = '((%s + 1) * (%s - %s) - 1) / (%s - %s)'

    #-----------------------
    # For floating argument
    #-------------------------------------------------
    # b = (top + 0.9999) * (x - xmin)/(xmax - xmin)
    #-------------------------------------------------
    # s = '(%s + 0.9999) * (%s - %s)/(%s - %s)'

    
    return (s % (top_str, a[0], min_str, max_str, min_str))

#--------------------------------------------------------------------------
def idl_cd_callfunc(i,o):
    a = idl_arg_list(i)

    if (len(a) == 1):
        cmd = ('os.chdir(%s)' % a[0])
    else:
        cmd = ''
    
    #-------------------------
    # Handle CURRENT keyword
    #-------------------------------------------------
    # Both IDL and Python return the current working
    # directory without a final filepath separator.
    #-------------------------------------------------
    k = idl_key_index('current', i)
    if (k != -1):
        kv = keyword_var(i[k])
        if (len(cmd) > 0): cmd += '\n'
        cmd += ('%s = os.getcwd()' % kv)

    return cmd

#--------------------------------------------------------------------------
def idl_close_callfunc(i,o):
    #------------------------------------------------
    # See IDL's help pages for OPENR and GET_LUN.
    # OPEN routines use LUNs from 1 to 99, while
    # GET_LUN uses LUNs from 100 to 128.
    #------------------------------------------------    
    # Can use the following to find out the maximum
    # number of files that can be open:
    #    >>> import posix
    #    >>> posix.sysconf('SC_OPEN_MAX')
    # Then loop over this many file indices & close?
    #------------------------------------------------
    if idl_key_set('all', i):
        #------------------
        # Close all files
        #------------------
##        print 'Warning: ALL keyword to CLOSE is not supported yet.'
##        cmd = '## I2PY does not support "close, /all" yet.'
##        return cmd

        cmd = 'idl_func.close_all_files()'
        return cmd
    
    #-----------------------------------------------
    # Replace "." with "_" in suffix.  This takes
    # care of cases where a unit number is a field
    # in a structure, e.g:   iv.q_profile_unit
    #-----------------------------------------------
    suffix = i[0].replace('.','_')
    cmd = ('file_%s.close()' % suffix)
    for k in range(1,len(i)):
        suffix = i[k].replace('.','_')
        cmd += ('\nfile_%s.close()' % suffix)
    return cmd
   
#--------------------------------------------------------------------------
def idl_contour_callfunc(i,o):

    #----------------------------------------------------------------
    # Notes: In IDL, X and Y can be 1D vectors (while Z is 2D).
    #        In matplotlib, X,Y and Z must all have same dimensions.
    #        Not all keywords to CONTOUR are supported.
    #----------------------------------------------------------------
    
#     inkeys=['C_ANNOTATION','C_CHARSIZE','C_CHARTHICK','C_COLORS',
#             'C_LABELS','C_LINESTYLE','CELL_FILL','FILL',
#             'C_ORIENTATION','C_SPACING','C_THICK','CLOSED',
#             'DOWNHILL','FOLLOW','IRREGULAR','ISOTROPIC','LEVELS',
#             'NLEVELS','MAX_VALUE','MIN_VALUE','OVERPLOT',
#             'PATH_DATA_COORDS','PATH_FILENAME','PATH_INFO',
#             'PATH_XY','TRIANGULATION','PATH_DOUBLE','XLOG','YLOG',
#             'ZAXIS']

    a = idl_arg_list(i)
    n_args = len(a)
    prefix = 'matplotlib.pyplot.'
    
    #-----------------------------------------------------
    #  This is used for PLOT, but not as important here.
    #-----------------------------------------------------
    #  This is a "quick fix" to a problem that occurs
    #  if the x or y argument to CONTOUR is a set of
    #  values enclosed/joined with square brackets.
    #-----------------------------------------------------
    for j in range(n_args):
        a[j] = a[j].replace('concatenate', '')
        a[j] = a[j].replace('array','')
        a[j] = a[j].replace('(','')
        a[j] = a[j].replace(')','')
        # a[j] = a[j].replace('concatenate', 'array')
        
    cmds = (prefix + 'contour')
    
    #--------------------------
    # Handle the FILL keyword
    #--------------------------
    if idl_key_set('fill', i): cmds += 'f'

    #----------------------
    # Get 1 or 3 arguments
    #-------------------------------------------
    # IDL uses Z,X,Y but matplotlib uses X,Y,Z
    #-------------------------------------------
    if (len(a) == 1):
        cmds += '(%s' % a[0]
    else:
        cmds += '(%s, %s, %s' % (a[1], a[2], a[0])

    #-----------------------------
    # Handle the NLEVELS keyword
    #-----------------------------
    k = idl_key_index('nlevels', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += ', %s' % kv
    else:
        #-----------------------------
        # Handle the LEVELS keyword
        #--------------------------------------------------
        # NB! "idl_key_index" routine cannot distinguish
        #     between 'levels' and 'nlevels', but it's not
        #     a problem here because both cannot be used.
        #     Notice that each of them uses a 4th argument
        #     (scalar or vector) to matplotlib's CONTOUR.
        #--------------------------------------------------
        k = idl_key_index('levels', i)
        if (k != -1):
            kv = keyword_var(i[k])
            cmds += ', %s' % kv
         
    #--------------------------------
    # Handle the CELL_FILL keywword
    #--------------------------------
    if idl_key_set('cell_fill', i):
        print 'Warning: CELL_FILL keyword to CONTOUR not supported yet.'

    #-----------------------------
    # Handle the CLOSED keywword
    #-----------------------------
    if idl_key_set('closed', i):
        print 'Warning: CLOSED keyword to CONTOUR not supported yet.'

    #-----------------------------
    # Handle the DEVICE keywword
    #-----------------------------------
    # This is an IDL Graphics Keyword,
    # handled separately below.
    #-----------------------------------
##    if idl_key_set('device', i):
##        print 'Warning: DEVICE keyword to CONTOUR not supported yet.'
        
    #------------------------------
    # Handle the DOWNHILL keyword
    #------------------------------
    if idl_key_set('downhill', i):
        print 'Warning: DOWHILL keyword to CONTOUR not supported yet.'

    #----------------------------
    # Handle the FOLLOW keyword
    #----------------------------
    if idl_key_set('follow', i):
        print 'Warning: FOLLOW keyword to CONTOUR not supported yet.'
        
    #-------------------------------
    # Handle the IRREGULAR keyword
    #-------------------------------
    if idl_key_set('irregular', i):
        print 'Warning: IRREGULAR keyword to CONTOUR not supported yet.'
    
    #-------------------------------
    # Handle the MAX_VALUE keyword
    #-------------------------------
    k = idl_key_index('max_value', i)
    if (k != -1):
        print 'Warning: MAX_VALUE keyword to CONTOUR not supported yet.'
    
    #-------------------------------
    # Handle the MIN_VALUE keyword
    #-------------------------------
    k = idl_key_index('min_value', i)
    if (k != -1):
        print 'Warning: MIN_VALUE keyword to CONTOUR not supported yet.'
    
    #------------------------------
    # Handle the OVERPLOT keyword
    #------------------------------
    if idl_key_set('overplot', i):
        print 'Warning: OVERPLOT keyword to CONTOUR not supported yet.'
        
    #-----------------------------------------
    # These keywords get appended as keywords
    # to the matplotlib plotting command.
    #-----------------------------------------
    cmds += idl_appended_graphics_keywords(i)
    cmds += ')'

    #------------------------------------------------
    # Handle IDL Graphics Keywords that correspond
    # to matplotlib commands that are separate from
    # the main plotting command.  Insert these on
    # separate lines *after* the plotting command.
    # Note that some of them don't work unless they
    # come after the plotting command, such as
    # xstyle=1 -> axis('image').
    #------------------------------------------------
    cmds += idl_graphics_keyword_commands(i)
    
    #----------------------------------------
    # Add "show()" command and return
    # (How is "show" different from "draw" ?
    #----------------------------------------
    cmds += '\n' + prefix + 'show()'
    return cmds

#--------------------------------------------------------------------------
def idl_device_callfunc(i,o):

    #------------------------------------------------------
    # Note:   This is unfinished.
    #------------------------------------------------------
    # return '# Note: Removed unneeded DEVICE call from here.'
    
    #---------------------------
    # Handle the CLOSE keyword
    #---------------------------
    k = idl_key_index('close', i)
    if (k != -1):
        print 'Error: Unsupported CLOSE keyword to DEVICE.'

    #--------------------------------
    # Handle the DECOMPOSED keyword
    #--------------------------------
    k = idl_key_index('decomposed', i)
    if (k != -1):
        print 'Error: Unsupported DECOMPOSED keyword to DEVICE.'
        
    #------------------------------
    # Handle the FILENAME keyword
    #------------------------------
    k = idl_key_index('filename', i)
    if (k != -1):
        print 'Error: Unsupported FILENAME keyword to DEVICE.'

    #--------------------------------------
    # Handle the GET_VISUAL_DEPTH keyword
    #--------------------------------------
    k = idl_key_index('get_visual_depth', i)
    if (k != -1):
        print 'Error: Unsupported GET_VISUAL_DEPTH keyword to DEVICE.'

    #-------------------------------------
    # Handle the GET_SCREEN_SIZE keyword
    #-------------------------------------
    k = idl_key_index('get_screen_size', i)
    if (k != -1):
        print 'Error: Unsupported GET_SCREEN_SIZE keyword to DEVICE.'

    args = ', '.join(i)
    cmd  = 'idl_func.device(%s)' % args
    return cmd

#--------------------------------------------------------------------------
def idl_dialog_pickfile_callfunc(i,o):

    #--------------------------------------------------------
    # Notes:  DIRECTORY and GET_PATH keywords are not yet
    #         supported.  (Tested with wx_tests.pro.)
    #---------------------------------------------------------
    #         In first line, we need to use a list object
    #         in order for I2PY_filepath to be another
    #         name for the one on LHS of the assignment
    #         that we don't have access to.
    #---------------------------------------------------------
    #         MULTIPLE_FILES option is not yet working but
    #         could be supported via loop and "append".
    #---------------------------------------------------------
    # cmds  = "I2PY_filepath = ['']\n"  # null string default
    cmds  = "I2PY_filepath = []\n"  # empty list
    cmds += "app = wx.PySimpleApp()\n"
    cmds += "I2PY_dialog = wx.FileDialog("

    #-----------------------------------
    # Handle the DIALOG_PARENT keyword
    #-----------------------------------
    k = idl_key_index('dialog_parent', i)
    if (k != -1):
        parent_ID = keyword_var(i[k])
        cmds += "parent=%s" % parent_ID
    else:
        cmds += "parent=None"

    #--------------------------------
    # Handle the MUST_EXIST keyword
    #--------------------------------
    k = idl_key_index('must_exist', i)
    if (k != -1):
        print 'Error: Unsupported MUST_EXIST keyword to DIALOG_PICKFILE.'

    #--------------------------
    # Handle the PATH keyword
    #--------------------------
    k = idl_key_index('path', i)
    if (k != -1):
        default_dir = keyword_var(i[k])
        cmds += ", defaultDir=%s" % default_dir
    else:
        cmds += ", defaultDir=os.getcwd()"

    #--------------------------
    # Handle the FILE keyword
    #--------------------------
    k = idl_key_index('_file', i)
    if (k != -1):
        default_file = keyword_var(i[k])
        cmds += ", defaultFile=%s" % default_file
 
    #------------------------------------
    # Handle the MULTIPLE_FILES keyword
    #------------------------------------
    if idl_key_set('multiple_files', i):
        cmds += ", style=wx.OPEN | wx.MULTIPLE"
        OPEN_MODE = True
    else:
        OPEN_MODE = False
 
    #--------------------------------------
    # Handle the OVERWRITE_PROMPT keyword
    #--------------------------------------
    if idl_key_set('overwrite_prompt', i):
        cmds += ", style=wx.SAVE | wx.OVERWRITE_PROMPT"
        SAVE_MODE = True
    else:
        SAVE_MODE = False

    #-----------------------------------------------
    # Is the basic style OPEN/READ or SAVE/WRITE ?
    #-----------------------------------------------
    if not(OPEN_MODE or SAVE_MODE):
        if idl_key_set('read', i):
            cmds += ", style=wx.OPEN"
        elif idl_key_set('write', i):
            cmds += ", style=wx.SAVE"
        else:
            cmds += ", style=wx.SAVE"

    #---------------------------
    # Handle the TITLE keyword
    #---------------------------
    k = idl_key_index('title', i)
    if (k != -1):
        title = keyword_var(i[k])
        cmds += ", message=%s" % title

    #----------------------------
    # Handle the FILTER keyword
    #----------------------------
    k = idl_key_index('filter', i)
    if (k != -1):
        wildcard = keyword_var(i[k])
        wildcard = wildcard.replace("'",'')
        wildcard = wildcard.replace('"','')
        cmds += ", wildcard='(%s)|%s'" % (wildcard, wildcard)
    
    cmds += ")\n"
    cmds += "if (I2PY_dialog.ShowModal() == wx.ID_OK):\n"
    cmds += "    I2PY_filepath.append(I2PY_dialog.GetPath())\n"
    cmds += "I2PY_dialog.Destroy()"
    
    # cmds += "    I2PY_pathlist = I2PY_dialog.GetPath()\n"
    # cmds += "    for I2PY_path in I2PY_pathlist: I2PY_filepath.append(I2PY_path)\n"
    # cmds += "    I2PY_filepath[0] = I2PY_dialog.GetPath()\n"
    # cmds += "app.MainLoop()\n"   #### (not needed)
    # cmds += "I2PY_dialog.Destroy()"

    return cmds

#--------------------------------------------------------------------------
def idl_eof_callfunc(i,o):

    #---------------------------------------------------------
    # Note:  This version adds less clutter to the converted
    #        code than the version below.
    #---------------------------------------------------------    
    # Note:  This works, but is not the "Python way".  Most
    #        Python programmers do something like this:
    #
    #         b = zeros([10], dtype='Int32')
    #         file_unit = open(data_file, 'rb')
    #         while (True):
    #             b = numpy.fromfile(file_unit, count=size(b),
    #                                dtype=str(b.dtype))
    #             if (len(b)==0): break
    #             print b
    #         file_unit.close()
    #---------------------------------------------------------
    print "Warning: IDL's EOF() not converted to Python way."
    print "         Search for os.path.getsize, then use:"
    print '         "while (True):" and something like'
    print '              "if (len(data)==0): break" in loop.'
    #---------------------------------------------------------
    cmd = 'idl_func.eof(file_%s)' % i[0]
    return cmd

#--------------------------------------------------------------------------
def idl_eof_callfunc2(i,o):
    #---------------------------------------------------------
    # Note:  This works, but is not the "Python way".  Most
    #        Python programmers do something like this:
    #
    #         b = zeros([10], dtype='Int32')
    #         file_unit = open(data_file, 'rb')
    #         while (True):
    #             b = numpy.fromfile(file_unit, count=size(b),
    #                                dtype=str(b.dtype))
    #             if (len(b)==0): break
    #             print b
    #         file_unit.close()
    #---------------------------------------------------------
    print "Warning: IDL's EOF() not converted to Python way."
    print "         Search for os.path.getsize, then use:"
    print '         "while (True):" and something like'
    print '              "if (len(data)==0): break" in loop.'
    #---------------------------------------------------------
    cmd = ('file_%s.tell() == os.path.getsize(file_%s.name)'
           % (i[0],i[0]) )

##    cmd  = '(True):\n'
##    cmd += '    if (len(DATA) == 0): break'
    
    return cmd

#--------------------------------------------------------------------------
def idl_file_delete_callfunc(i,o):

    a = idl_arg_list(i)
    files = ', '.join(a)
    cmd = ('idl_func.file_delete(%s)' % files)
    return cmd

##    cmd = ('idl_func.file_delete(%s)' % i[0])
##    for k in range(1,len(i)):
##        cmd += ('\nidl_func.file_delete(%s)' % i[k])
##    return cmd

#--------------------------------------------------------------------------
def idl_file_search_callfunc(i,o):
    #------------------------------------------------------------
    # Note:  IDL's FILE_SEARCH has numerous optional keywords
    #        and a recursion option which are not yet supported.
    #        Could also make use of os.path.walk.
    #------------------------------------------------------------
    # Note:  It is possible to use IDL's FILE_SEARCH like this:
    #            IDL> files = file_search('*.bin')
    #            IDL> if (files[0] ne '') then ...
    #        This usage is not (yet) supported, so usage should
    #        be changed to:
    #            IDL> files = file_search('*.bin', count=count)
    #            IDL> if (count ne 0) then ...
    #------------------------------------------------------------ 
    a = idl_arg_list(i)
    if (len(a) > 1):
        print 'ERROR: I2PY only supports 1 argument to FILE_SEARCH.'
        return ''
    
    #---------------------------
    # Handle the COUNT keyword
    #---------------------------
    k = idl_key_index('count', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds  = ('I2PY_file_list = glob.glob(%s)' % a[0])
        cmds += '\n%s = len(I2PY_file_list)' % kv
    else:
        cmds  = ('glob.glob(%s)' % a[0])
        
    return cmds

#--------------------------------------------------------------------------
def idl_finite_callfunc(i,o):
    if idl_key_set('infinity', i):
        return ('isinf(%s)' % i[0])
    if idl_key_set('nan', i):
        return ('isnan(%s)' % i[0])
    return ('isfinite(%s)' % i[0])

#--------------------------------------------------------------------------
def idl_fstat_callfunc(i,o):
    #---------------------------------------------------------
    # Note:  This version adds less clutter to the converted
    #        code than the version below.
    #-------------------------------------------------------
    # Note:  IDL's FSTAT function returns a structure, but
    #        is commonly used to get the size of a file.
    #        e.g. temp     = fstat(unit)
    #             filesize = temp.size
    #        Could add remaining fields for FSTAT in the
    #        call to "bunch".
    #-------------------------------------------------------
    cmd = 'idl_func.fstat(file_%s)' % i[0]
    return cmd

#--------------------------------------------------------------------------
def idl_fstat_callfunc2(i,o):
    #-------------------------------------------------------
    # Note:  IDL's FSTAT function returns a structure, but
    #        is commonly used to get the size of a file.
    #        e.g. temp     = fstat(unit)
    #             filesize = temp.size
    #        Could add remaining fields for FSTAT in the
    #        call to "bunch".
    #-------------------------------------------------------
    s  = 'I2PY_temp = bunch(size=numpy.int32(0))\n'
    s += 'I2PY_temp.size = os.path.getsize(file_%s.name)\n' % i[0]
    return (s % i[0])

#--------------------------------------------------------------------------
def idl_get_lun_callfunc(i,o):

    #--------------------------------------------------------
    # Note:  We don't actually need to get unit numbers due
    #        to the way Python's file objects work.  So we
    #        can just return a comment line.
    #--------------------------------------------------------
    return '# Note: Removed unneeded GET_LUN call from here.'

#--------------------------------------------------------------------------
##  def idl_hist_equal_callfunc(i,o):
    
#--------------------------------------------------------------------------
def idl_histogram_callfunc(i,o):
    a = idl_arg_list(i)
    cmd = 'histogram(%s)[0]' % a[0]

    #-----------------------------------------------------------------
    # bins (if int: number of equal-width bins in given range
    #       if sequence of floats: lower bounds of bins)
    # range: (float, float)  if not given, a.min() and a.max() used.
    # normed: True (to get pdf) or False
    #-----------------------------------------------------------------

    #-----------------------------
    # Handle the BINSIZE keyword
    #-----------------------------
    
    #---------------------------
    # Handle the INPUT keyword
    #---------------------------

    #-------------------------
    # Handle the MAX keyword
    #-------------------------

    #-------------------------
    # Handle the MIN keyword
    #-------------------------

    #-------------------------
    # Handle the NAN keyword
    #-------------------------

    #---------------------------
    # Handle the NBINS keyword
    #---------------------------

    #--------------------------
    # Handle the OMAX keyword
    #--------------------------

    #--------------------------
    # Handle the OMAX keyword
    #--------------------------

    #-------------------------------------
    # Handle the REVERSE_INDICES keyword
    #-------------------------------------
    #  Use digitize() ??
    
    return cmd

#--------------------------------------------------------------------------
def idl_make_array_callfunc(i,o):

    a = idl_arg_list(i)

    #--------------------------
    # Handle the TYPE keyword
    #--------------------------
    k = idl_key_index('_type', i)
    if (k != -1):
        idl_type_code_str = keyword_var(i[k])
        #--------------------------------------------------
        # Need numpy.int here, because idl_type_code_str
        # may equal something like "int16(5)" and regular
        # int can't handle cases like this.
        #--------------------------------------------------
        idl_type_code = int(eval(idl_type_code_str))
        typename = numpy_type_name(idl_type_code)
    else:
        #-------------------------------------------------
        # Use keywords to determine data type (typename)
        #-------------------------------------------------
        if   idl_key_set('byte', i):     typename = 'UInt8'
        elif idl_key_set('uint', i):     typename = 'UInt16'
        elif idl_key_set('ulong', i):    typename = 'UInt32'
        elif idl_key_set('ul64', i):     typename = 'UInt64'
        elif idl_key_set('integer', i):  typename = 'Int16'
        elif idl_key_set('long', i):     typename = 'Int32'
        elif idl_key_set('l64', i):      typename = 'Int64'
        elif idl_key_set('float', i):    typename = 'Float32'
        elif idl_key_set('double', i):   typename = 'Float64'
        elif idl_key_set('complex', i):  typename = 'Complex64'
        elif idl_key_set('dcomplex', i): typename = 'Complex128'
        elif idl_key_set('string', i):   typename = 'str'

    #---------------------------
    # Handle the INDEX keyword
    #---------------------------
    if not(idl_key_set('index', i)):
        #----------------------------
        # Handle the NOZERO keyword
        #----------------------------
        if idl_key_set('nozero', i):
            cmd = "empty([%s], dtype='%s')" % (reverse_arg_str(a), typename)  
        else:
            cmd = "zeros([%s], dtype='%s')" % (reverse_arg_str(a), typename)      
    else:
        if (len(a)==1):
            cmd = "arange(%s, dtype='%s')" % (arg_product_str(a), typename)
        else:
            cmd = "reshape(arange(%s, dtype='%s'), [%s])" %  \
                  ( arg_product_str(a), typename, reverse_arg_str(a) )

    #---------------------------
    # Handle the VALUE keyword
    #---------------------------
    k = idl_key_index('value', i)
    if (k != -1):
        value_str = keyword_var(i[k])
        cmd += ' + %s' % value_str

    return cmd

#--------------------------------------------------------------------------
def idl_max_callfunc(i,o):

    #------------------------------------------------------------
    # Note: The array() function here is numpy.array().
    #       But Python's built-in array() also has max()/min().
    #-----------------------------------------------------------------------   
    # Note:  Next line won't work if argument is a list vs. an array
    # map_func('MAX', inpars=[1], callfunc=(lambda i,o: '%s.max()' % i[0]))
    #-----------------------------------------------------------------------
    a = idl_arg_list(i)

    if (idl_key_set('nan',i)):
        s = 'nanmax(%s)' % i[0]
        if (len(a) > 1):
            s = s + '\n%s = nanargmax(%s)' % (a[1],a[0])
        k1 = idl_key_index('min', i)
        if (k1 != -1):
            kv1 = keyword_var(i[k1])
            s = s + '\n%s = nanmin(%s)' % (kv1, i[0])
        k2 = idl_key_index('subscript_min', i)
        if (k2 != -1):
            kv2 = keyword_var(i[k2])
            s = s + '\n%s = nanargmin(%s)' % (kv2, i[0])
    else:
        s = '%s.max()' % i[0]
        if (len(a) > 1):
            s = s + '\n%s = %s.argmax()' % (a[1],a[0])
        k1 = idl_key_index('min', i)
        if (k1 != -1):
            kv1 = keyword_var(i[k1])
            s = s + '\n%s = %s.min()' % (kv1, i[0])
        k2 = idl_key_index('subscript_min', i)
        if (k2 != -1):
            kv2 = keyword_var(i[k2])
            s = s + '\n%s = %s.argmin()' % (kv2, i[0])
            
    return s

#--------------------------------------------------------------------------
def idl_max_callfunc2(i,o):

    #------------------------------------------------------------
    # Note: This version uses: array( var, copy=0).max(), which
    #       should no longer be needed.
    #------------------------------------------------------------    
    # Note: The array() function here is numpy.array().
    #       But Python's built-in array() also has max()/min().
    #-----------------------------------------------------------------------   
    # Note:  Next line won't work if argument is a list vs. an array
    # map_func('MAX', inpars=[1], callfunc=(lambda i,o: '%s.max()' % i[0]))
    #-----------------------------------------------------------------------
    a = idl_arg_list(i)

    if (idl_key_set('nan',i)):
        s = 'nanmax(array(%s, copy=0))' % i[0]
        if (len(a) > 1):
            s = s + '\n%s = nanargmax(array(%s, copy=0))' % (a[1],a[0])
        k1 = idl_key_index('min', i)
        if (k1 != -1):
            kv1 = keyword_var(i[k1])
            s = s + '\n%s = nanmin(array(%s, copy=0))' % (kv1, i[0])
        k2 = idl_key_index('subscript_min', i)
        if (k2 != -1):
            kv2 = keyword_var(i[k2])
            s = s + '\n%s = nanargmin(array(%s, copy=0))' % (kv2, i[0])
    else:
        s = 'array(%s, copy=0).max()' % i[0]
        if (len(a) > 1):
            s = s + '\n%s = array(%s, copy=0).argmax()' % (a[1],a[0])
        k1 = idl_key_index('min', i)
        if (k1 != -1):
            kv1 = keyword_var(i[k1])
            s = s + '\n%s = array(%s, copy=0).min()' % (kv1, i[0])
        k2 = idl_key_index('subscript_min', i)
        if (k2 != -1):
            kv2 = keyword_var(i[k2])
            s = s + '\n%s = array(%s, copy=0).argmin()' % (kv2, i[0])

    return s

#--------------------------------------------------------------------------
def idl_message_callfunc(i,o):

    #--------------------------------
    # Handle INFORMATIONAL keyword
    #  (not important here ??)
    #--------------------------------
    
    cmd  = ('print %s' % i[0])
    cmd += '\nsys.exit()'
    return cmd

#--------------------------------------------------------------------------
def idl_min_callfunc(i,o):

    #------------------------------------------------------------
    # Note: The array() function here is numpy.array().
    #       But Python's built-in array() also has max()/min().
    #-----------------------------------------------------------------------   
    # Note:  Next line won't work if argument is a list vs. an array
    # map_func('MAX', inpars=[1], callfunc=(lambda i,o: '%s.max()' % i[0]))
    #----------------------------------------------------------------------- 
    a = idl_arg_list(i)

    if (idl_key_set('nan',i)):
        s = 'nanmin(%s)' % i[0]
        if (len(a) > 1):
            s = s + '\n%s = nanargmin(%s)' % (a[1],a[0])
        k1 = idl_key_index('max', i)
        if (k1 != -1):
            kv1 = keyword_var(i[k1])
            s = s + '\n%s = nanmax(%s)' % (kv1, i[0])
        k2 = idl_key_index('subscript_max', i)
        if (k2 != -1):
            kv2 = keyword_var(i[k2])
            s = s + '\n%s = nanargmax(%s)' % (kv2, i[0])
    else:
        s = '%s.min()' % i[0]
        if (len(a) > 1):
            s = s + '\n%s = %s.argmin()' % (a[1],a[0])
        k1 = idl_key_index('max', i)
        if (k1 != -1):
            kv1 = keyword_var(i[k1])
            s = s + '\n%s = %s.max()' % (kv1, i[0])
        k2 = idl_key_index('subscript_max', i)
        if (k2 != -1):
            kv2 = keyword_var(i[k2])
            s = s + '\n%s = %s.argmax()' % (kv2, i[0])

    return s

#--------------------------------------------------------------------------
def idl_min_callfunc2(i,o):

    #------------------------------------------------------------
    # Note: This version uses: array( var, copy=0).max(), which
    #       should no longer be needed.
    #------------------------------------------------------------    
    # Note: The array() function here is numpy.array().
    #       But Python's built-in array() also has max()/min().
    #-----------------------------------------------------------------------   
    # Note:  Next line won't work if argument is a list vs. an array
    # map_func('MIN', inpars=[1], callfunc=(lambda i,o: '%s.min()' % i[0]))
    #-----------------------------------------------------------------------
    
    a = idl_arg_list(i)

    if (idl_key_set('nan',i)):
        s = 'nanmin(array(%s, copy=0))' % i[0]
        if (len(a) > 1):
            s = s + '\n%s = nanargmin(array(%s, copy=0))' % (a[1],a[0])
        k1 = idl_key_index('max', i)
        if (k1 != -1):
            kv1 = keyword_var(i[k1])
            s = s + '\n%s = nanmax(array(%s, copy=0))' % (kv1, i[0])
        k2 = idl_key_index('subscript_max', i)
        if (k2 != -1):
            kv2 = keyword_var(i[k2])
            s = s + '\n%s = nanargmax(array(%s, copy=0))' % (kv2, i[0])
    else:
        s = 'array(%s, copy=0).min()' % i[0]
        if (len(a) > 1):
            s = s + '\n%s = array(%s, copy=0).argmin()' % (a[1],a[0])
        k1 = idl_key_index('max', i)
        if (k1 != -1):
            kv1 = keyword_var(i[k1])
            s = s + '\n%s = array(%s, copy=0).max()' % (kv1, i[0])
        k2 = idl_key_index('subscript_max', i)
        if (k2 != -1):
            kv2 = keyword_var(i[k2])
            s = s + '\n%s = array(%s, copy=0).argmax()' % (kv2, i[0])

    return s

#--------------------------------------------------------------------------
def idl_n_elements_callfunc(i,o):
    
    #------------------------------------------------------------
    # Note:  Use numpy.size() to compute the number of elements
    #        (in an array) if the array name is defined.
    #        However, IDL's N_ELEMENTS also returns 0 in the
    #        case where its argument is undefined.  See notes
    #        in "idl_func.py".
    #-----------------------------------------------------------
    #        The case "if (n_elements(g) eq 0)" is handled by
    #        code in ir.py.
    #-----------------------------------------------------------
    cmd = "idl_func.n_elements(%s)" % i[0]
    return cmd

#--------------------------------------------------------------------------
def idl_n_elements_callfunc2(i,o):
    
    #------------------------------------------------------------
    # Note:  Use numpy.size() to compute the number of elements
    #        (in an array) if the array name is defined.
    #        However, IDL's N_ELEMENTS also returns 0 in the
    #        case where its argument is undefined.  In order to
    #        reproduce this behavior, we use the following
    #        conditional expression and Python's built-in
    #        globals() or locals() method.
    #-----------------------------------------------------------
    #        The case "if (n_elements(g) eq 0)" is handled by
    #        code in ir.py.
    #-----------------------------------------------------------
    cmd = "(size(%s) if ('%s' in locals()) else 0)" % (i[0], i[0])
    #cmd = "(size(%s) if ('%s' in globals()) else 0)" % (i[0], i[0])

    return cmd

#--------------------------------------------------------------------------
def idl_online_help_callfunc(i,o):
    
    #--------------------------------------------------------------
    # Notes: IDL's ONLINE_HELP function has one optional argument
    #        as well as the keywords: BOOK, FULL_PATH and QUIT.
    #        There is another, Windows only keyword, CONTEXT.
    
    #        The "webbrowser" module in Python has methods like:
    #        open, open_new, open_new_tab, but not "close".
    #        So not sure how to support the QUIT keyword.
    #        The user's default browser is the one opened.
    #--------------------------------------------------------------
    if idl_key_set('quit', i):
        msg = 'Error: QUIT keyword for ONLINE_HELP not supported.'
        print msg
##        msg = 'QUIT keyword is not yet supported.'
##        print_error_message('ONLINE_HELP', msg)
        return 'online_help(%s)' % i[0]

    k = idl_key_index('book', i)
    if (k != -1):
        if (idl_key_set('full_path', i)):
            path = keyword_var(i[k])
            cmd  = "result = webbrowser.open('file://' + %s)" % path
            return cmd
        else:
            # IDL would now search the directories listed
            # in !help_path.  This is not yet supported.
            msg = 'Error: I2PY requires FULL_PATH keyword for ONLINE_HELP.'
            print msg
##            msg = 'I2PY requires FULL_PATH keyword to be set.'
##            print_error_message('ONLINE_HELP', msg)
        return 'online_help(%s)' % i[0]
    else:
        msg = 'Error: I2PY requires BOOK keyword for ONLINE_HELP.'
        print msg
##        msg = 'I2PY requires BOOK keyword to be set.'
##        print_error_message('ONLINE_HELP', msg)
        return 'online_help(%s)' % i[0]

#--------------------------------------------------------------------------
def idl_openr_callfunc(i,o):
    
    #----------------------------------------------------------    
    # Notes: If the SWAP_ENDIAN keyword is set, we know that
    #        we are supposed to read BINARY data and add 'b'.
    #        Otherwise, the situation is unclear so we assume
    #        ASCII data but issue a warning.
    #----------------------------------------------------------
    a = idl_arg_list(i)

    #---------------------------------
    # Handle the SWAP_ENDIAN keyword
    #---------------------------------
    if idl_key_set('swap_endian', i):
        #---------------------------------------
        # Keyword must be set to "1" or "True"
        #---------------------------------------
        cmd  = "file_%s = open(%s, 'rb')" % (a[0], a[1])
        cmd += '\nI2PY_SWAP_ENDIAN = True'
    else:
        k = idl_key_index('swap_endian', i)
        if (k != -1):
            #----------------------------------------------
            # The presence of this keyword indicates that
            # the we must be reading binary data.
            #----------------------------------------------
            value = keyword_var(i[k])
            cmd  = "file_%s = open(%s, 'rb')"  % (a[0], a[1])
            cmd += '\nI2PY_SWAP_ENDIAN = %s' % value
        else:
            #-------------------------------------------
            # Assume that we're reading ASCII data but
            # issue a warning, just in case.
            #-------------------------------------------
            cmd  = "file_%s = open(%s, 'r')"  % (a[0], a[1])
            cmd += '\nI2PY_SWAP_ENDIAN = False'     
            print 'Warning: Is OPENR used for text or binary file?'
               
    #-----------------------------
    # Handle the GET_LUN keyword
    #-----------------------------------------------------
    # Can simply ignore GET_LUN keyword because of the
    # way that Python creates a file object and the way
    # that I2PY now uses the "unit" variable in the name
    # of the file object, as shown above.
    #-----------------------------------------------------
        
    return cmd

#--------------------------------------------------------------------------
def idl_openu_callfunc(i,o):
    #----------------------------------------------------------    
    # Notes: If the SWAP_ENDIAN keyword is set, we know that
    #        we are supposed to read BINARY data and add 'b'.
    #        Otherwise, the situation is unclear so we assume
    #        ASCII data but issue a warning.
    #----------------------------------------------------------
    a = idl_arg_list(i)

    #---------------------------------
    # Handle the SWAP_ENDIAN keyword
    #---------------------------------
    if idl_key_set('swap_endian', i):
        #---------------------------------------
        # Keyword must be set to "1" or "True"
        #---------------------------------------
        cmd  = "file_%s = open(%s, 'rb+')" % (a[0], a[1])
        cmd += '\nI2PY_SWAP_ENDIAN = True'
    else:
        k = idl_key_index('swap_endian', i)
        if (k != -1):
            #----------------------------------------------
            # The presence of this keyword indicates that
            # the we must be reading binary data.
            #----------------------------------------------
            value = keyword_var(i[k])
            cmd  = "file_%s = open(%s, 'rb+')"  % (a[0], a[1])
            cmd += '\nI2PY_SWAP_ENDIAN = %s' % value
        else:
            #-------------------------------------------
            # Assume that we're reading ASCII data but
            # issue a warning, just in case.
            #-------------------------------------------
            cmd  = "file_%s = open(%s, 'r+')"  % (a[0], a[1])
            cmd += '\nI2PY_SWAP_ENDIAN = False'     
            print 'Warning: Is OPENU used for text or binary file?'
                  
    #-----------------------------
    # Handle the GET_LUN keyword
    #-----------------------------------------------------
    # Can simply ignore GET_LUN keyword because of the
    # way that Python creates a file object and the way
    # that I2PY now uses the "unit" variable in the name
    # of the file object, as shown above.
    #-----------------------------------------------------
      
    return cmd

#--------------------------------------------------------------------------
def idl_openw_callfunc(i,o):
    #----------------------------------------------------------    
    # Notes: If the SWAP_ENDIAN keyword is set, we know that
    #        we are supposed to read BINARY data and add 'b'.
    #        Otherwise, the situation is unclear so we assume
    #        ASCII data but issue a warning.
    #----------------------------------------------------------
    a = idl_arg_list(i)

    #---------------------------------
    # Handle the SWAP_ENDIAN keyword
    #---------------------------------
    if idl_key_set('swap_endian', i):
        #---------------------------------------
        # Keyword must be set to "1" or "True"
        #---------------------------------------
        cmd  = "file_%s = open(%s, 'wb')" % (a[0], a[1])
        cmd += '\nI2PY_SWAP_ENDIAN = True'
    else:
        k = idl_key_index('swap_endian', i)
        if (k != -1):
            #----------------------------------------------
            # The presence of this keyword indicates that
            # the we must be reading binary data.
            #----------------------------------------------
            value = keyword_var(i[k])
            cmd  = "file_%s = open(%s, 'wb')"  % (a[0], a[1])
            cmd += '\nI2PY_SWAP_ENDIAN = %s' % value
        else:
            #-------------------------------------------
            # Assume that we're reading ASCII data but
            # issue a warning, just in case.
            #-------------------------------------------
            cmd  = "file_%s = open(%s, 'w')"  % (a[0], a[1])
            cmd += '\nI2PY_SWAP_ENDIAN = False'     
            print 'Warning: Is OPENW used for text or binary file?'
             
    #-----------------------------
    # Handle the GET_LUN keyword
    #-----------------------------------------------------
    # Can simply ignore GET_LUN keyword because of the
    # way that Python creates a file object and the way
    # that I2PY now uses the "unit" variable in the name
    # of the file object, as shown above.
    #-----------------------------------------------------
        
    return cmd

#--------------------------------------------------------------------------
def idl_plot_callfunc(i,o):

    #---------------------------------------------------------
    #  Notes:  Additional keywords that are not among the
    #          standard graphics keywords and are not yet
    #          supported are:
    #          'MAX_VALUE', 'MIN_VALUE', 'NSUM', 'YNOZERO'.
    #          However, "YNOZERO" is the default behavior for
    #          matplotlib.  Usually, YRANGE is used instead
    #          of MIN_VALUE and MAX_VALUE, although there may
    #          be differences in behavior.
    #---------------------------------------------------------
    a = idl_arg_list(i)
    n_args = len(a)
    prefix = 'matplotlib.pyplot.'
    
    #-----------------------------------------------------
    #  This is a "quick fix" to a problem that occurs
    #  if the x or y argument to PLOT is a set of values
    #  enclosed/joined with square brackets.
    #-----------------------------------------------------
    for j in range(n_args):
        a[j] = a[j].replace('concatenate', '')
        a[j] = a[j].replace('array','')
        a[j] = a[j].replace('(','')
        a[j] = a[j].replace(')','')
        # a[j] = a[j].replace('concatenate', 'array')
        
    cmds = ''

    #------------------------------------------------
    # Handle IDL Graphics Keywords that correspond
    # to matplotlib commands that are separate from
    # the main plotting command.  Insert these on
    # separate lines *before* the plotting command.
    #------------------------------------------------
    # SEE NOTES BELOW.  BEFORE DOESN'T ALWAYS WORK.
    #------------------------------------------------
##    cmds += idl_graphics_keyword_commands(i)
##    if (len(cmds) > 0):
##        if (cmds.startswith('\n')): cmds = cmds[1:]
##        cmds += '\n'
    
    #---------------------------------
    #  Get "toggle" keyword settings
    #---------------------------------
    XLOG    = idl_key_set('xlog', i)
    YLOG    = idl_key_set('ylog', i)
    POLAR   = idl_key_set('polar', i)
    YNOZERO = idl_key_set('ynozero', i)
    
    #---------------------------------------------------------
    # If there is only one argument, both IDL and matplotlib
    # take it as the y-values, with x-values taken to be an
    # array of integer indexes starting at 0.
    #--------------------------------------------------------- 
    if not(POLAR):
        if not(XLOG) and not(YLOG):
            cmds += (prefix + 'plot(%s' % a[0])
        elif YLOG and not(XLOG):
            cmds += (prefix + 'semilogy(%s' % a[0])
        elif XLOG and not(YLOG):
            cmds += (prefix + 'semilogx(%s' % a[0])
        else:
            cmds += (prefix + 'loglog(%s' % a[0])

        if (n_args == 2):
            cmds += (', %s' % a[1])
    else:
        #---------------------------------
        # Need to reverse arguments from
        #  (r,theta) to (theta, r)
        #---------------------------------
        cmds += (prefix + 'polar(%s, %s' % (a[1], a[0]) )
       
    #-----------------------------------------
    # These keywords get appended as keywords
    # to the matplotlib plotting command.
    #-----------------------------------------
    cmds += idl_appended_graphics_keywords(i)
    cmds += ')'

    #---------------------------------------
    # Handle the ISOTROPIC keyword to PLOT
    #---------------------------------------
    #  Now done in "idl_graphics_keyword_commands

    #------------------------------------------------
    # Handle IDL Graphics Keywords that correspond
    # to matplotlib commands that are separate from
    # the main plotting command.  Insert these on
    # separate lines *after* the plotting command.
    # Note that some of them don't work unless they
    # come after the plotting command, such as
    # xstyle=1 -> axis('image').
    #------------------------------------------------
    cmds += idl_graphics_keyword_commands(i)
    
    #----------------------------------------
    # Add "show()" command and return
    # (How is "show" different from "draw" ?
    #----------------------------------------
    cmds += '\n' + prefix + 'show()'
    return cmds

#--------------------------------------------------------------------------
def idl_plot_field_callfunc(i,o):
    #-----------------------------------------------
    #  Notes:  Both arguments (U,V) are 2D arrays.
    #  inkeys = ['ASPECT','LENGTH','N','TITLE']
    #-----------------------------------------------
    a = idl_arg_list(i)
    cmds = 'matplotlib.pyplot.quiver(%s, %s' % (a[0], a[1])

    #--------------------------------------
    # Handle the LENGTH keyword (sort of)
    #--------------------------------------
    k = idl_key_index('length', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmds += (', scale=%s' % kv)

    #-----------------------------------
    # Handle the N keyword (but how ?)
    #-----------------------------------
    
    #------------------------------------------------
    # This is only used for TITLE keyword ??
    #------------------------------------------------    
    # Handle IDL Graphics Keywords that correspond
    # to matplotlib commands that are separate from
    # the main plotting command.  Insert these on
    # separate lines *after* the plotting command.
    # Note that some of them don't work unless they
    # come after the plotting command, such as
    # xstyle=1 -> axis('image').
    #------------------------------------------------
    cmds += ')'
    cmds += idl_graphics_keyword_commands(i)
    return cmds

#--------------------------------------------------------------------------
def idl_point_lun_callfunc(i,o):
    #------------------------------------------------------------
    #  Notes: In IDL, if (unit < 0), then position is returned.
    #         In Python, you use "f.tell()" for this.

    #########   The "sign test" here won't work if the "unit"
    #########   argument is a variable.
    #------------------------------------------------------------
    if ('-' not in i[0]):
        cmd = ('file_%s.seek(%s)' % (i[0], i[1]))
    else:
        unit_name = remove_chars(i[0],' ()*-1')
        cmd = ('%s = file_%s.tell()' % (i[1], unit_name))
    return cmd

#--------------------------------------------------------------------------
def idl_print_callfunc(i,o):

    #---------------------------------------------------------   
    #  Notes:  This routine uses idl_func.string, since
    #          it also has a FORMAT keyword and behaves in a
    #          similar manner.  See additional notes there.

    #          Only the FORMAT keyword is supported so far.
    #          IDL's PRINT has the additional keywords:
    #          AM_PM, DAYS_OF_WEEK, MONTHS, STDIO_NON_FINITE

    #          See important Notes in idl_arg_list().
    #---------------------------------------------------------
    a = idl_arg_list(i)
    args = ', '.join(a)

##    print 'i    =', i
##    print 'a    =', a
##    print 'args =', args
##    print ' '
    
    #----------------------------
    # Handle the FORMAT keyword
    #----------------------------
    k = idl_key_index('format', i)
    if (k != -1):
        #------------------------------------------
        # Write string using specified formatting
        #------------------------------------------
        cmd = 'I2PY_out_str = idl_func.string(%s, format=%s)\n' % \
              (args, keyword_var(i[k]))
        cmd += 'print I2PY_out_str'
    else:
        #-------------------------------------------------
        # Write string using default (Python) formatting
        #-------------------------------------------------
        cmd = 'print %s' % args
    return cmd

#--------------------------------------------------------------------------
def idl_print_callfunc2(i,o):

    #---------------------------------------------------------
    #  Notes:  This is currently unused and may not work.
    #---------------------------------------------------------   
    #  Notes:  This routine uses idl_string_callfunc, since
    #          it also has a FORMAT keyword and behaves in a
    #          similar manner.  See additional notes there.

    #          Only the FORMAT keyword is supported so far.
    #          IDL's PRINT has the additional keywords:
    #          AM_PM, DAYS_OF_WEEK, MONTHS, STDIO_NON_FINITE
    #---------------------------------------------------------
    a = idl_arg_list(i)
    k = idl_key_index('format', i)
    if (k != -1):
        #------------------------------------------
        # Write string using specified formatting
        #------------------------------------------
        out_str = idl_string_callfunc(a,o)
    else:
        #----------------------------------------
        # Write string using default formatting
        #----------------------------------------
        out_str = ', '.join(a)
        
    cmd = 'print ' + out_str
    return cmd

#--------------------------------------------------------------------------
def idl_printf_callfunc(i,o):

    #----------------------------------------------------------   
    #  Notes:  This routine uses idl_func.string, since
    #          it also has a FORMAT keyword and behaves in a
    #          similar manner.  See additional notes there.

    #          Only the FORMAT keyword is supported so far.
    #          IDL's PRINTF has the additional keywords:
    #          AM_PM, DAYS_OF_WEEK, MONTHS, STDIO_NON_FINITE
    #----------------------------------------------------------
    #  NB!     file.write() does not add a newline character,
    #          but IDL's PRINTF procedure does, so we must
    #          add one to output string.
    #----------------------------------------------------------    
    a = idl_arg_list(i)
    unit_str = a[0]
    unit_str = unit_str.replace('.','_')
    a = a[1:]
    args = ', '.join(a)

    #----------------------------
    # Handle the FORMAT keyword
    #----------------------------
    k = idl_key_index('format', i)    
    if (k != -1):
        #------------------------------------------
        # Write string using specified formatting
        #------------------------------------------
        cmd  = 'I2PY_out_str = idl_func.string(%s, format=%s)\n' % \
               (args, keyword_var(i[k]))
        cmd += 'file_%s.write(I2PY_out_str + "\n")' % unit_str
    else:
        #-------------------------------------------------
        # Write string using default (Python) formatting
        #-------------------------------------------------
        cmd = 'file_%s.write(%s + "\n")' % (unit_str, args)
    return cmd

#--------------------------------------------------------------------------
def idl_printf_callfunc2(i,o):

    #---------------------------------------------------------
    #  Notes:  This is currently unused and may not work.
    #---------------------------------------------------------   
    #  Notes:  This routine uses idl_string_callfunc, since
    #          it also has a FORMAT keyword and behaves in a
    #          similar manner.  See additional notes there.

    #          Only the FORMAT keyword is supported so far.
    #          IDL's PRINTF has the additional keywords:
    #          AM_PM, DAYS_OF_WEEK, MONTHS, STDIO_NON_FINITE
    #---------------------------------------------------------
    a = idl_arg_list(i)
    unit_str = a[0]
    a = a[1:]
    
    k = idl_key_index('format', i)
    if (k != -1):
        #------------------------------------------
        # Write string using specified formatting
        #------------------------------------------
        out_str = idl_string_callfunc(a,o)
    else:
        #----------------------------------------
        # Write string using default formatting
        #----------------------------------------
        out_str = ', '.join(a)

    cmd = 'file_%s.write(%s)' % (unit_str, out_str)
    return cmd

#--------------------------------------------------------------------------
def idl_ptrarr_callfunc(i,o):

    #--------------------------------------------------------
    # Notes: In TopoFlow, IDL's PTRARR is only used with a
    #        data type of DOUBLE, so will use that for now
    #        and ignore keywords to PTRARR.
    #--------------------------------------------------------
    # print 'Error: I2PY does not support PTRARR yet.'
    # args = ', '.join(i)
    # cmd = 'idl_func.ptrarr(%s)' % args
    # return cmd

    print 'Warning: Data type of DOUBLE used to convert PTRARR.'
    a = idl_arg_list(i)
    cmd = "numpy.zeros(%s, dtype='Float64')" % a[0]
    return cmd

    #----------------------------
    # Handle the NOZERO keyword
    #----------------------------
##    if idl_key_set('nozero', i):
##        pass

    #-----------------------------------
    # Handle the ALLOCATE_HEAP keyword
    #----------------------------------- 
##    if idl_key_set('allocate_heap', i):
##        pass

#--------------------------------------------------------------------------
def idl_ptr_free_callfunc(i,o):

    #-----------------------------------------------------
    # Note:  We don't actually need to free pointers due
    #        to the way Python works.  So we can just
    #        return a comment line.
    #-----------------------------------------------------
    return 'pass  # Note: Removed unneeded PTR_FREE call from here.'

#--------------------------------------------------------------------------
def idl_ptr_new_callfunc(i,o):

    #-------------------------------------------------------
    # Note:  We don't actually need to create pointers due
    #        to the way Python works.  So we can just
    #        return the argument.

    # Note:  Conversion of "ptr_new(lonarr(1))" will not
    #        work at this point because the conversion of
    #        lonarr results in a "dtype=" part, and the
    #        idl_arg_list() function then thinks the
    #        argument is a keyword.
    #-------------------------------------------------------
    a = idl_arg_list(i)
    # print 'i =', i
    return a[0]

#--------------------------------------------------------------------------
def idl_random_callfunc(i, name):

    #  "name" is either "RANDOMN" or "RANDOMU".
    #  What should we do about 'DOUBLE' keyword ?

    #---------------------------------------------------
    #  If seed is defined in the IDL code, call
    #  "random.set_state", otherwise "random.get_state"
    #  But how do we check if it is defined?
    #---------------------------------------------------
    a = idl_arg_list(i)
    seed_str = a[0]
    s1 = 'random.set_state(%s)\n' % seed_str
    s2 = '\n### %s = random.get_state()' % seed_str
    
    #---------------------------------------
    #  Determine shape of the random array
    #---------------------------------------------
    #  Must remove required seed argument first.
    #  Note that 2nd argument could be an array.
    #---------------------------------------------
    if (len(a) > 1):
        shape = "(" + reverse_arg_str(a[1:]) + ")"
    else:
        shape = None

    #-------------------------------------- 
    #  Command to generate random numbers
    #--------------------------------------    
    k = idl_key_index('binomial', i)
    if (k != -1):
        kv = keyword_var(i[k])
        kv = kv.replace('concatenate','')
        kv = kv.replace('array','')
        kv = kv.replace('([','')
        kv = kv.replace('])','')
        cmd = 'random.binomial(%s, size=%s)' % (kv, shape)
        return (s1 + cmd + s2)
    #-------------------------------------------------------------
    k = idl_key_index('gamma', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmd = 'random.gamma(scale=%s, size=%s)' % (kv, shape)
        return (s1 + cmd + s2)
    #-------------------------------------------------------------
    k = idl_key_index('long', i)
    if (k != -1):
        kv = keyword_var(i[k])
        vmax = (2**31) - 2
        cmd = 'random.randint(low=0, high=vmax, size=%s)' % (kv, shape)
        return (s1 + cmd + s2)
    #-------------------------------------------------------------
    k = idl_key_index('normal', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmd = 'random.normal(loc=0.0, scale=1.0, size=%s)' % shape
        return (s1 + cmd + s2)
    #-------------------------------------------------------------
    k = idl_key_index('poisson', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmd = 'random.poisson(lam=%s, size=%s)' % (kv, shape)
        return (s1 + cmd + s2)
    #---------------------------------------------------------------
    k = idl_key_index('uniform', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmd = 'random.uniform(low=0.0, high=1.0, size=%s)' % shape
        return (s1 + cmd + s2)

    #-------------------------------------------
    # Can only get here if no keywords are set
    #-------------------------------------------
    if (name.upper() == 'RANDOMN'):
        cmd = 'random.normal(loc=0.0, scale=1.0, size=%s)' % shape
    else:
        cmd = 'random.uniform(low=0.0, high=1.0, size=%s)' % shape
    return (s1 + cmd + s2)

#--------------------------------------------------------------------------
def idl_read_callfunc(i,o):

    cmd = ''
    print 'ERROR: READ procedure is not yet supported.'
    return cmd

#--------------------------------------------------------------------------
def idl_readf_callfunc0(i,o):

    ######  This is unfinished and untested. ######
    
    #---------------------------------------------------------   
    #  Notes:  This routine uses idl_string_callfunc, since
    #          it also has a FORMAT keyword and behaves in a
    #          similar manner.  See additional notes there.

    #          Only the FORMAT keyword is supported so far.
    #          IDL's PRINTF has the additional keywords:
    #          AM_PM, DAYS_OF_WEEK, MONTHS, PROMPT
    #---------------------------------------------------------
    a = idl_arg_list(i)
    unit_str = a[0]
    a = a[1:]

    #-------------------------------------------------
    # Are we reading the entire line into a string ?
    #-------------------------------------------------
    if (len(a) == 1):
        cmds  = "if (type(%s) == type('abc')):\n"
        cmds += '    %s = file_%s.readline()\n' % (a[0], unit_str)
        cmds += 'else:\n'
        cmds += '    I2PY_s = file_%s.readline()\n' % unit_str
        # cmds += '    %s = 
        
    #-------------------------------------------------
    # Are we reading the entire line into a string ?
    #-------------------------------------------------
    if (len(a) == 1) and (type(a[0]) == type('abc')):
        cmd = '%s = file_%s.readline()' % (a[0], unit_str)
        return cmd
    
    #--------------------------------------------------
    # IDL's READF routine reads an entire line from a
    # text file and parses it into variables with the
    # indicated types.  An entire line is typically
    # read with:  line=''  &  readf, unit, line
    # Variables with specified types are typically
    # read with something like:
    #     a = 0L
    #     b = 0.0
    #     c = ''
    #     readf, unit, a, b, c
    #--------------------------------------------------
    cmd = 'I2PY_s = file_%s.readline()' % unit_str

    #--------------------------------------------------
    # Now how can we read values from this string ?
    # Note: eval('this') raises an exception.
    #--------------------------------------------------
    cmd += '\nI2PY_vals = I2PY_s.split()'
    for k in range(len(a)):
        #---------------------------------------------
        # This works for scalar numbers and strings,
        # but doesn't work for arrays yet.
        #---------------------------------------------
        cmd += "\n%s = array(I2PY_vals[%s]).astype(%s.dtype)" % (a[k],k,a[k])

        #-------------------------------------------------
        # This works for scalar numbers but not strings.
        #-------------------------------------------------
        # cmd += '\n%s = eval(I2PY_vals[%s])' % (a[k], k)

        #-----------------------------------------
        # How can we handle the FORMAT keyword ?
        # It may not be critical for READF.
        #-----------------------------------------
##    array(%s, copy=0).astype('%s')" % (i[0], typename))
 
##    k = idl_key_index('format', i)
##    if (k != -1):
##        #----------------------------------------------
##        # Read data string using specified formatting
##        #----------------------------------------------
##        out_str = idl_string_callfunc(a,o)
##    else:
##        #--------------------------------------------
##        # Read data string using default formatting
##        #---------------------------------------------
##        out_str = ', '.join(a)

    return cmd

#--------------------------------------------------------------------------
def idl_readf_callfunc(i,o):
    # print 'ERROR: READF procedure is not yet supported.'
    
    a = idl_arg_list(i)
    unit_str = a[0]
    a = a[1:]   # remove first argument
    args = ', '.join(a)
    cmd = '%s = idl_func.readf(file_%s, %s' % (args, unit_str, args)

    #----------------------------
    # Handle the FORMAT keyword
    #----------------------------
    k = idl_key_index('format', i)
    if (k != -1):
        cmd += ", format=%s)" % keyword_var(i[k])
    else:
        cmd += ')'   
    return cmd

#--------------------------------------------------------------------------
def idl_reads_callfunc(i,o):
    # print 'ERROR: READS procedure is not yet supported.'
    
    a = idl_arg_list(i)
    line = a[0]
    a = a[1:]   # remove first argument
    args = ', '.join(a)
    cmd = '%s = idl_func.reads(%s, %s' % (args, line, args)

    #----------------------------
    # Handle the FORMAT keyword
    #----------------------------
    k = idl_key_index('format', i)
    if (k != -1):
        cmd += ", format=%s)" % keyword_var(i[k])
    else:
        cmd += ')'   
    return cmd

#--------------------------------------------------------------------------
def idl_readu_callfunc(i,o):
    #----------------------------------------------------
    # Note: "eof_test.pro" provides a simple test case.
    #       Could we use "load" instead of "fromfile" ? ############
    #----------------------------------------------------
    a = idl_arg_list(i)
    #-------------------------------------------------
    # Read first data item & reshape (for 2D arrays)
    # Could also reshape in same "fromfile line" by
    # tacking ".reshape(I2PY_shape)" on the end.
    #-------------------------------------------------
    cmd  = "I2PY_shape = %s.shape\n" % a[1]
    cmd += "I2PY_dtype = str(%s.dtype)\n" % a[1]
    cmd += "%s = fromfile(file_%s, count=size(%s), dtype=I2PY_dtype)\n" \
            % (a[1], a[0], a[1])
    cmd += "%s = reshape(%s, I2PY_shape)" % (a[1], a[1])
    
    #-------------------------------
    # Read additional data items ?
    #-------------------------------
    for k in range(2,len(a)):
        cmd += "\n"
        cmd += "I2PY_shape = %s.shape\n" % a[k]
        cmd += "I2PY_dtype = str(%s.dtype)\n" % a[k]
        cmd += "%s = fromfile(file_%s, count=size(%s), dtype=I2PY_dtype)\n" \
               % (a[k],a[0],a[k])
        cmd += "%s = reshape(%s, I2PY_shape)" % (a[k], a[k])
    
    #---------------------------------------------
    # Swap the byte order of all the variables ?
    #------------------------------------------------------
    # Need "numpy.array" in case some vars are scalars, in
    # order for them to get access to "byteswap" method.
    # Use of "copy=0" and "True" does everything in place.
    # I2PY_SWAP_ENDIAN will have been defined earlier in
    # the same scope (routine) in call to OPENR or OPENU.
    #------------------------------------------------------
    # This does not yet handle data in a structure.
    #------------------------------------------------------    
    cmd += '\nif (I2PY_SWAP_ENDIAN):'
    for k in range(1,len(a)):
        cmd += '\n    array(%s, copy=0).byteswap(True)' % a[k]

    #-------------------------------------------------
    # May be able to use this version now, since all
    # variable assignments result in numpy objects.
    #-------------------------------------------------
##    for k in range(1,len(a)):
##        cmd += '\n    %s.byteswap(True)' % a[k]
        
    return cmd

#--------------------------------------------------------------------------
def idl_readu_callfunc2(i,o):
    #----------------------------------------------------
    # Note: "eof_test.pro" provides a simple test case.
    #       Could we use "load" instead of "fromfile" ? ############
    #----------------------------------------------------
    a = idl_arg_list(i)
    # Read first data item
    cmd = "%s = fromfile(file_%s, count=size(%s), dtype=str(%s.dtype))" \
          % (a[1],a[0],a[1],a[1])

    #-------------------------------
    # Read additional data items ?
    #-------------------------------
    for k in range(2,len(a)):
        cmd += "\n%s = fromfile(file_%s, count=size(%s), dtype=str(%s.dtype))" \
               % (a[k],a[0],a[k],a[k])

    #---------------------------------------------
    # Swap the byte order of all the variables ?
    #------------------------------------------------------
    # Need "numpy.array" in case some vars are scalars, in
    # order for them to get access to "byteswap" method.
    # Use of "copy=0" and "True" does everything in place.
    # I2PY_SWAP_ENDIAN will have been defined earlier in
    # the same scope (routine) in call to OPENR or OPENU.
    #------------------------------------------------------
    # This does not yet handle data in a structure.
    #------------------------------------------------------    
    cmd += '\nif (I2PY_SWAP_ENDIAN):'
    for k in range(1,len(a)):
        cmd += '\n    array(%s, copy=0).byteswap(True)' % a[k]

    #-------------------------------------------------
    # May be able to use this version now, since all
    # variable assignments result in numpy objects.
    #-------------------------------------------------
##    for k in range(1,len(a)):
##        cmd += '\n    %s.byteswap(True)' % a[k]
        
    return cmd

#--------------------------------------------------------------------------
def idl_rebin_callfunc(i,o):

    print 'Error: I2PY does not support REBIN yet.'
    # print 'ERROR: REBIN function is not supported yet.'
    args = ', '.join(i)
    cmd = 'idl_func.rebin(%s)' % args
    return cmd

#--------------------------------------------------------------------------
def idl_rebin_callfunc2(i,o):
    
    #-----------------------------------------------------------
    #  Notes:  A combination of numpy.repeat and numpy.reshape
    #          can be used for nearest-neighbor enlarging by
    #          an integer factor.
    #-----------------------------------------------------------
    cmd = ''
    print 'ERROR: REBIN function is not supported yet.'
    return cmd
    ######################################################

    a = idl_arg_list(i)
    cmd  = 'I2PY_binned_array\n'
    cmd += 'I2PY_M, I2PY_N = %s.shape\n' % a[0]
    cmd += ('I2PY_binned_array = reshape(%s, (I2PY_M/%s,%s,I2PY_N/%s,%s))\n' %
           (a[0], a[1], a[1], a[2], a[2]))
    
    return cmd

#--------------------------------------------------------------------------
def idl_reform_callfunc(i,o):
    a = idl_arg_list(i)
    a = a[1:]  # remove the array argument
    s = 'reshape(%s, [%s])' % (i[0], reverse_arg_str(a))
    return s

#--------------------------------------------------------------------------
def idl_reverse_callfunc(i,o):

    #---------------------------------------------------------
    # Note: rot90(y,-2) only works for 2D arrays, but flipud
    #       works on both 2D and 1D arrays.  IDL'S REVERSE
    #       is also intended for 1D arrays, but ROTATE works
    #       on both 1D and 2D.  The following Python code
    #       also works for 1D arrays, but may be slower.
    #           cmd = '%s[::-1]' % i[0]
    #---------------------------------------------------------
    cmd = 'flipud(%s)' % i[0]
    return cmd

#--------------------------------------------------------------------------
def idl_rotate_callfunc(i,o):

    #-------------------------------------------------------------    
    #  Note:  IDL's ROTATE command works with 1D and 2D arrays.
    #         As in IDL, the "rotation code" is modulo 8. 
    #         Each NumPy command here was checked for 2D arrays,
    #         but only TRANSPOSE and FLIPUD work for 1D arrays.
    #         FLIPUD reverses elements in a 1D array.
    #         Commented lines also work, but are expected to
    #         be slower.
    #         For 2D arrays, NumPy's SWAPAXES = TRANSPOSE.
    #-------------------------------------------------------------
    code = (eval(i[1]) % 8)
    if   (code == 0): cmd_str = '%s'
    elif (code == 1): cmd_str = 'rot90(%s, -1)'
    elif (code == 2): cmd_str = 'rot90(%s, -2)  ## Use FLIPUD to reverse 1D arrays'
    elif (code == 3): cmd_str = 'rot90(%s, -3)'
    elif (code == 4): cmd_str = 'transpose(%s)'
    elif (code == 5): cmd_str = 'fliplr(%s)'
    ## elif (code == 5): cmd_str = 'transpose(rot90(%s, 1))'
    elif (code == 6): cmd_str = 'transpose(rot90(%s, 2))'
    elif (code == 7): cmd_str = 'flipud(%s)'
    ## elif (code == 7): cmd_str = 'transpose(rot90(%s, 3))'
    else: cmd_str = '%s'
    return (cmd_str % i[0])

#--------------------------------------------------------------------------
def idl_shift_callfunc(i,o):
    #---------------------------------------------------
    #  Note:  Only supports shifts of 1D to 3D arrays.
    #  x-axis is 0 for 1D, 1 for 2D and 2 for 3D ?
    #---------------------------------------------------
    n_args = len(i)
    if (n_args == 2):
        #  Case of a 1D IDL array
        cmd = 'numpy.roll(%s, %s, axis=0)' % (i[0], i[1])
    elif (n_args == 3):
        #  Case of a 2D IDL array
        try:
            xshift = eval(i[1])
        except:
            xshift = i[1]
            print "Warning: Can't compute 1st argument to SHIFT."
        try:
            yshift = eval(i[2])
        except:
            yshift = i[2]
            print "Warning: Can't compute 2nd argument to SHIFT."    
            
        if (xshift != 0) and (yshift == 0):
            cmd = 'numpy.roll(%s, %s, axis=1)' % (i[0], i[1])
        if (yshift != 0) and (xshift == 0):
            cmd = 'numpy.roll(%s, %s, axis=0)' % (i[0], i[2])
        if (xshift != 0) and (yshift != 0):
            mid = 'numpy.roll(%s, %s, axis=0)' % (i[0], i[2])
            cmd = 'numpy.roll(%s, %s, axis=1)' % (mid,  i[1])
    elif (n_args == 4):
        #  Case of a 3D IDL array
        xshift = eval(i[1])
        yshift = eval(i[2])
        zshift = eval(i[3])
        if (xshift != 0) and (yshift == 0) and (zshift == 0):
            cmd = 'numpy.roll(%s, %s, axis=2)' % (i[0], i[1])
        elif (yshift != 0) and (xshift == 0) and (zshift == 0):
            cmd = 'numpy.roll(%s, %s, axis=1)' % (i[0], i[2])
        elif (zshift != 0) and (xshift == 0) and (yshift == 0):
            cmd = 'numpy.roll(%s, %s, axis=0)' % (i[0], i[3])
        #--------------------------------------------------------
        else:
            mid1 = 'numpy.roll(%s, %s, axis=0)' % (i[0], i[3])
            mid2 = 'numpy.roll(%s, %s, axis=1)' % (mid1, i[2])
            cmd  = 'numpy.roll(%s, %s, axis=2)' % (mid2, i[1])
            
    return cmd

#--------------------------------------------------------------------------
def idl_sindgen_callfunc(i,o):
    #--------------------------------------------------
    #  Note:  Only supports a single argument so far.
    #--------------------------------------------------
    a = idl_arg_list(i)
    n_args = len(a)
    if (n_args > 1):
        print "Error: I2PY only supports 1 argument to SINDGEN."
        cmd = ''
    else:
        cmd = "map(str, arange(%s, dtype='Int32'))" % a[0]
    return cmd

#--------------------------------------------------------------------------
def idl_size_callfunc(i,o):
    #---------------------------------------------------------
    #  By default, IDL's SIZE function returns a vector of
    #  values that describe an object's dimensions and type.
    #--------------------------------------------------------- 
    a = idl_arg_list(i)
    if idl_key_set('n_dimensions', i):
        return ('idl_func.size(%s, n_dimensions=True)' % a[0])
    if idl_key_set('n_elements', i):
        return ('idl_func.size(%s, n_elements=True)' % a[0])
    if idl_key_set('dimensions', i):
        return ('idl_func.size(%s, dimensions=True)' % a[0])
    if idl_key_set('_type', i):
        return ('idl_func.size(%s, _type=True)' % a[0])
        
    return ('idl_func.size(%s)' % a[0])

#--------------------------------------------------------------------------
def idl_size_callfunc2(i,o):
    #---------------------------------------------------------
    #  This version is unused and does not work as written.
    #---------------------------------------------------------
    #  By default, IDL's SIZE function returns a vector of
    #  values that describe an object's dimensions and type.
    #---------------------------------------------------------  
    if idl_key_set('n_dimensions', i): return ('ndim(%s)' % i[0])
    if idl_key_set('n_elements', i):   return ('size(%s)' % i[0])
    if idl_key_set('dimensions', i):
        #--------------------------------------------------------
        #  In Python code, first line will look something like
        #     s = I2PY_a = zeros(ndim( array )).
        #  When we set values in I2PY_a, they get set in s, too.
        #--------------------------------------------------------
        s  = "I2PY_a = zeros(ndim(%s), dtype='int32') \n"
        s += 'for I2PY_n in xrange(ndim(%s)-1,-1,-1): \n'
        s += '    I2PY_a[I2PY_n] = size(%s, I2PY_n)'
        return ( s % (i[0],i[0],i[0]) )
    if idl_key_set('_type', i):
        s  = "I2PY_a = numpy.array(5) \n"
        s += "I2PY_type_code = {'uint8':1, 'int16':2, 'int32':3, 'float32':4, "
        s += "'float64':5, 'complex32':6, 'str':7} \n"
        s += "I2PY_type_str  = str(%s.dtype)\n" % i[0]
        s += "if (I2PY_type_str[:2]=='|S'): I2PY_type_str='str'\n"
        s += "I2PY_a[0] = I2PY_type_code[I2PY_type_str]"
        return s
        
    #---------------------------------------------
    # Return an integer array like IDL does
    # IDL "type code" now hardwired to 5, DOUBLE
    #---------------------------------------------
    s  = "I2PY_a = zeros(ndim(%s)+3, dtype='int32') \n"
    s += 'I2PY_a[0] = ndim(%s) \n'
    s += 'for I2PY_n in xrange(ndim(%s)-1,-1,-1): \n'
    s += '    I2PY_a[I2PY_n + 1] = size(%s, I2PY_n) \n'
    s += "I2PY_type_map = {'uint8':1, 'int16':2, 'int32':3, 'float32':4, "
    s += "'float64':5, 'complex32':6, 'str':7} \n"
    s += 'I2PY_a[ndim(%s) + 1] = I2PY_type_map[str(%s.dtype)] \n'  
    # s += 'I2PY_a[ndim(%s) + 1] = 5 \n'
    s += 'I2PY_a[ndim(%s) + 2] = size(%s) \n'
    return ( s % (i[0],i[0],i[0],i[0],i[0],i[0],i[0],i[0]) )

    # msg = 'This function is not fully supported.'
    # print_error_message('SIZE', msg)
    # return ''

##  s = "array((" + "repeat('size(%s,%s)',
        
## ', '.join([ a[n] for n in xrange(len(a)-1, -1, -1) ])

##    a = idl_arg_list(i)
##    s = 'array( (ndim(%s), '
##    s = s + 'size(%s, n), size(%s, n-1), ...'
##    s = s + 'idl_type_code(%s), '
##    s = s + 'size(%s) )'
##    return (s % (i[0],i[0],i[0].....))

#--------------------------------------------------------------------------
def idl_strarr_callfunc(i,o):

    #--------------------------------------------------------
    # Note: If we use 'str' for dtype below, then elements
    #       in the resulting string array can only have one
    #       character each.  e.g.
    #            >>> a = zeros(3, dtype='str')
    #            >>> a[0] = 'this'
    #            >> print a[0]  (result is 't')
    #       However, if we use '|S100' for dtype, then we
    #       can store strings up to 100 characters each.
    #--------------------------------------------------------
    #       Addition operator doesn't work as in IDL.
    #       e.g. we can't do:   a = a + 'this'
    #--------------------------------------------------------    
    a = idl_arg_list(i)
    cmd = "zeros([%s], dtype='|S100')" % reverse_arg_str(a) 
    # cmd = "zeros([%s], dtype='str')" % reverse_arg_str(a) 
    return cmd

#--------------------------------------------------------------------------
def idl_string_callfunc(i,o):
    
    a = idl_arg_list(i)
    args = ', '.join(a)

    #----------------------------
    # Handle the FORMAT keyword
    #----------------------------
    k = idl_key_index('format', i)
    if (k != -1):
        kv  = keyword_var(i[k])
        cmd = "idl_func.string(%s, format=%s)" % (args, kv)
    else:
        if (len(a) == 1):
            cmd = "str(%s)" % a[0]
        else:
            cmd = "idl_func.string(%s)" % args
                                                  
    return cmd

#--------------------------------------------------------------------------
def idl_string_callfunc2(i,o):
    
    a = idl_arg_list(i)
    args = ', '.join(a)
    cmd = 'idl_func.string(%s' % args

    #----------------------------
    # Handle the FORMAT keyword
    #----------------------------
    k = idl_key_index('format', i)
    if (k != -1):
        cmd += ", format=%s)" % keyword_var(i[k])
    else:
        cmd += ')'   
    return cmd

#--------------------------------------------------------------------------
def idl_string_callfunc3(i,o):

    #---------------------------------------------------------
    #  NB!  This is UNFINISHED and currently UNUSED.
    #
    #---------------------------------------------------------   
    #  Notes:  An IDL formatting string looks like:
    #             '(F10.3, I6, 4x, d6.3, I5, A10)'
    #          A Python formatting string looks like:
    #             '%10.3f%6d    %6.3f%5d%10s'
    #          Note that 4 spaces are used for the "4x".

    #          IDL uses Fortran-style formatting strings,
    #          and only the most commonly used features
    #          are being supported here.
    
    #          If we use '%4s' for a string that has more
    #          than 4 characters, no truncation occurs.
    #          However, if we use '%10s' for a string with
    #          less than 10 characters, then padding spaces
    #          are added on the left-hand side.  Same idea
    #          applies to integers (e.g. %4d and %10d).
    
    #          Only the FORMAT keyword is supported so far.
    #          IDL's STRING has the following additional
    #          keywords:
    #          AM_PM, DAYS_OF_WEEK, MONTHS and PRINT

    #          This doesn't yet handle special behavior of
    #          IDL's STRING function when the argument is
    #          an array (like indgen(5)) or a byte array
    #          (like [72b, 101b, 108b, 108b, 111b]).  To
    #          handle this case we need to check the type
    #          of the argument first.  Could write a function
    #          idl_string() to put in idl_func.py.
    #---------------------------------------------------------
    k = idl_key_index('format', i)
    if (k == -1):
        s = ' '.join(i)
        s = s.replace("'",'')  # remove all quotes
        s = s.replace('"','')
        return ( "'" + s + "'")

    # Modify the formatting string
    cmds  = "parts = %s[1:-1].split(',')\n"
    cmds += "new_str = 'n"
    cmds += "fmap = {'F':'f', 'D':'f', 'I':'d', 'A':'s'}\n"
    cmds += "for p in parts:\n"
    
    
    kv = keyword_var(i[k])
    kv = kv.lower()            # go to lower case
    kv = kv.replace('(','')
    kv = kv.replace(')','')
    kv = kv.replace(' ', '')   # remove all spaces
    kv = kv.replace("'", '')   # remove all quotes
    kv = kv.replace('"', '')
     
    parts = kv.split(',')
    for m in xrange(len(parts)):

        s = parts[m]
        j = s.find('x')
        if (j == -1):
            if (s[0].isalpha()):
                #-----------------------------------------
                # Move "format letter" from start to end
                #-----------------------------------------
                parts[m] = s[1:len(s)] + s[0]
            else:
                #--------------------------------------               
                # Process a "repetition count" before
                # the "format letter".
                #--------------------------------------
                rep_str = ''
                len_str = ''
                FOUND = False
                for c in s:
                    if not(FOUND):
                        if c.isalpha():
                            code = c
                            FOUND = True
                        else:
                            rep_str += c
                    else:
                        len_str += c
                parts[m] = '%'.join(numpy.repeat(len_str + code, eval(rep_str)))
        else:      
            #-----------------------------------------
            # Insert "blank" strings into i to match
            # places with "<n>x" string formatting
            #-----------------------------------------
            nstr = s.replace('x','')
            nstr = nstr.replace(' ','')
            i.insert( m, "''.ljust(" + nstr + ")" )

    kv = "'%" + "%".join(parts) + "'"
    kv = kv.replace('d', 'f')  # for floats
    kv = kv.replace('i', 'd')  # for integers
    kv = kv.replace('a', 's')  # for strings
    kv = kv.replace('x', 's')  # see above

    a   = idl_arg_list(i)
    cmd = kv + ' % (' + ', '.join(a) + ')'
        
    return cmd

#--------------------------------------------------------------------------
def idl_string_callfunc1(i,o):
    #---------------------------------------------------------   
    #  Notes:  An IDL formatting string looks like:
    #             '(F10.3, I6, 4x, d6.3, I5, A10)'
    #          A Python formatting string looks like:
    #             '%10.3f%6d    %6.3f%5d%10s'
    #          Note that 4 spaces are used for the "4x".

    #          IDL uses Fortran-style formatting strings,
    #          and only the most commonly used features
    #          are being supported here.
    
    #          If we use '%4s' for a string that has more
    #          than 4 characters, no truncation occurs.
    #          However, if we use '%10s' for a string with
    #          less than 10 characters, then padding spaces
    #          are added on the left-hand side.  Same idea
    #          applies to integers (e.g. %4d and %10d).
    
    #          Only the FORMAT keyword is supported so far.
    #          IDL's STRING has the following additional
    #          keywords:
    #          AM_PM, DAYS_OF_WEEK, MONTHS and PRINT

    #          This doesn't yet handle special behavior of
    #          IDL's STRING function when the argument is
    #          an array (like indgen(5)) or a byte array
    #          (like [72b, 101b, 108b, 108b, 111b]).  To
    #          handle this case we need to check the type
    #          of the argument first.  Could write a function
    #          idl_string() to put in idl_func.py.
    #---------------------------------------------------------
    k = idl_key_index('format', i)
    if (k == -1):
        s = ' '.join(i)
        s = s.replace("'",'')  # remove all quotes
        s = s.replace('"','')
        return ( "'" + s + "'")

    # Modify the formatting string
    kv = keyword_var(i[k])
    kv = kv.lower()            # go to lower case
    kv = kv.replace('(','')
    kv = kv.replace(')','')
    kv = kv.replace(' ', '')   # remove all spaces
    kv = kv.replace("'", '')   # remove all quotes
    kv = kv.replace('"', '')
     
    parts = kv.split(',')
    for m in xrange(len(parts)):

        s = parts[m]
        j = s.find('x')
        if (j == -1):
            if (s[0].isalpha()):
                #-----------------------------------------
                # Move "format letter" from start to end
                #-----------------------------------------
                parts[m] = s[1:len(s)] + s[0]
            else:
                #--------------------------------------               
                # Process a "repetition count" before
                # the "format letter".
                #--------------------------------------
                rep_str = ''
                len_str = ''
                FOUND = False
                for c in s:
                    if not(FOUND):
                        if c.isalpha():
                            code = c
                            FOUND = True
                        else:
                            rep_str += c
                    else:
                        len_str += c
                parts[m] = '%'.join(numpy.repeat(len_str + code, eval(rep_str)))
        else:      
            #-----------------------------------------
            # Insert "blank" strings into i to match
            # places with "<n>x" string formatting
            #-----------------------------------------
            nstr = s.replace('x','')
            nstr = nstr.replace(' ','')
            i.insert( m, "''.ljust(" + nstr + ")" )

    kv = "'%" + "%".join(parts) + "'"
    kv = kv.replace('d', 'f')  # for floats
    kv = kv.replace('i', 'd')  # for integers
    kv = kv.replace('a', 's')  # for strings
    kv = kv.replace('x', 's')  # see above

    a   = idl_arg_list(i)
    cmd = kv + ' % (' + ', '.join(a) + ')'
        
    return cmd

#--------------------------------------------------------------------------
def idl_strsplit_callfunc(i,o):
    #--------------------------------------------------------
    #  Note: The currently supported keywords are: EXTRACT,
    #        COUNT and LENGTH.
    #        Other keywords are: ESCAPE, REGEX, FOLD_CASE,
    #        and PRESERVE_NULL.

    #        The 2nd, "pattern" argument to STRSPLIT can be
    #        a string with more than one "split" character.
    #        Similarly, the "startswith" string method can
    #        take a tuple argument, but "split" can't.

    #        The string method, split, returns null strings
    #        in the case where the delimeter is not white
    #        space (e.g. ";").
    #--------------------------------------------------------
    a = idl_arg_list(i)
    n_args = len(a)

    #-----------------------------                  
    # Handle the EXTRACT keyword
    #-----------------------------
    if idl_key_set('extract', i):
        # Return the substrings
        if (n_args == 1):
            cmd = ('%s.split()' % a[0] )
        else:
            # Does not handle 2nd arg like IDL does.
            cmd = ('%s.split(%s)' % (a[0], a[1]) )
    else:
        # Return positions of the substrings                
        if (n_args == 1):
            cmd = ('[j for j in xrange(len(%s)) if (ord(%s[j]) > 32) and ((j==0) or ((j>0) and (ord(%s[j-1]) < 33)))]' %
                   (a[0], a[0], a[0]) )
        else:
            cmd = ('[j for j in xrange(len(%s)) if (%s[j] not in %s) and ((j==0) or ((j>0) and (%s[j-1] in %s)))]' %
                   (a[0], a[0], a[1], a[0], a[1]) )

        #-----------------------------------------------------
        # This idea doesn't work for all types of whitespace
        # and has an offset, etc.
        #-----------------------------------------------------
##        if (n_args == 1):
##            cmd = ('[j for j in xrange(len(%s)) if %s.startswith(' ',j)] %
##                   (a[0], a[0])
##        else:
##            cmd = ('[j for j in xrange(len(%s)) if %s.startswith(tuple(%s),j)] %
##                   (a[0], a[0], a[1])
      
        #--------------------------------------------- 
        #  This idea doesn't work for strings like:
        # ' the the the the'
        #---------------------------------------------              
##        if (n_args == 1):
##            cmd = ('map(%s.find, %s.split())' % (a[0], a[0]) )
##        else:
##            cmd = ('map(%s.find, %s.split(%s))' % (a[0], a[0], a[1]) )

    #-----------------------------------------------------------
    # Note that COUNT and LENGTH keywords have not been set,
    # but are present and associated with undefined var names.
    #-----------------------------------------------------------
    k1 = idl_key_index('count', i)
    k2 = idl_key_index('length', i)
    if (k1 == -1) and (k2 == -1): return cmd
        
    if idl_key_set('extract', i):
        #----------------------------------------------------
        #  Create an alias called "I2PY_words" that can
        #  be used to compute COUNT and LENGTH.  However,
        #  it assumes that call to STRSPLIT is of the form:
        #  <words> = strsplit(<str>, [pattern])
        #----------------------------------------------------
        cmd = 'I2PY_words = ' + cmd
    else:
        if (n_args == 1):
            cmd += ('\nI2PY_words = %s.split()' % a[0] )
        else:
            cmd += ('\nI2PY_words = %s.split(%s)' % (a[0], a[1]) )

    #---------------------------                  
    # Handle the COUNT keyword
    #---------------------------
    k = idl_key_index('count', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmd += '\n%s = len(I2PY_words)' % kv

    #---------------------------
    # Handle the LENGTH keyword
    #---------------------------
    k = idl_key_index('length', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmd += '\n%s = map(len, I2PY_words)' % kv

    return cmd

#--------------------------------------------------------------------------
def idl_strtrim_callfunc(i,o):
    if (len(i)==1): return ('%s.rstrip()' % i[0])
    flag = eval(i[1])
    if (flag == 2):
        return ('%s.strip()' % i[0])
    elif (flag == 1):
        return ('%s.lstrip()'  % i[0])
    else: return ('%s.rstrip()' % i[0])

#--------------------------------------------------------------------------
def idl_surface_callfunc(i,o):
    pass

##    #-------------------------------------------------------
##    # Want to change the colormap (e.g. pylab.cm.prism),
##    # but can't figure out how to do it.
##    #-------------------------------------------------------    
##    # pylab.figure and ...Axes3D don't have a cmap keyword
##    # plot_surface accepts cmap keyword but doesn't use it?
##    #-------------------------------------------------------
##    # rstride and cstride keywords to plot_surface seem to
##    # change the mesh spacing.  Both default to 10 ?
##    #-------------------------------------------------------
##    fig = pylab.figure()
##    ax  = matplotlib.axes3d.Axes3DI(fig)
##    # ax = matplotlib.axes3d.Axes3DI(fig)# (I = interactive ?)
##
##    #------------------------------
##    # Rescale z-values to [0,1] ?
##    #------------------------------
##    #z2 = (z - z.min()) / (z.max() - z.min())
##
##    ## ax.plot_surface(xm, ym, z)
##
##    cs = maximum(1, self.nx/25)
##    rs = maximum(1, self.ny/25)
##    rs = minimum(cs, rs)
##    cs = rs.copy()
##    # print 'cs, rs, nx, ny = ', cs, rs, nx, ny
##
##    # ax.plot_surface(x, y, z)
##    ax.plot_surface(self.x, self.y, self.z, cstride=cs, rstride=rs)
##    
##    ## ax.plot_surface(xm, ym, z, cmap=pylab.cm.gray)
##    
##    ## ax.plot_surface(xm, ym, z, rstride=10, cstride=10)
##
##    ## ax.plot_wireframe(xm, ym, z, cmap=pylab.cm.gray)
##        
##    ax.set_xlabel('X')
##    ax.set_ylabel('Y')
##    ax.set_zlabel('Z')
##    pylab.show()
        
#--------------------------------------------------------------------------
def idl_total_callfunc(i,o):
    if (idl_key_set('nan', i)):
        if (idl_key_set('cumulative',i)):
            ##  There is no "nancumsum" function.
            cmd_str = 'cumsum(nan_to_num(%s))'
        else:
            cmd_str = 'nansum(%s)'
    else:
        if (idl_key_set('cumulative',i)):
            cmd_str = 'cumsum(%s)'
        else:
            cmd_str = 'sum(%s)'

    #-----------------------------------
    #  Convert array to double first ?
    #-----------------------------------
    if (idl_key_set('double',i)):
        a = 'double(' + i[0] + ')'
    else:
        a = i[0]
    return (cmd_str % a)

#--------------------------------------------------------------------------
def idl_tv_callfunc(i,o):
    #----------------------------------------------------------
    #  Notes: matplotlib's IMSHOW has other useful keywords
    #         such as: cmap, extent, interpolation, and norm.
    #----------------------------------------------------------
    #  From IMSHOW docs:
    
    #  Display the image in X to current axes.  X may be a
    #  float array, a uint8 array or a PIL image. If X is an
    #  array, X can have the following shapes:
    
    #      MxN    : luminance (grayscale, float array only)
    #      MxNx3  : RGB (float or uint8 array)
    #      MxNx4  : RGBA (float or uint8 array)
    
    #  The value for each component of MxNx3 and MxNx4 float
    #  arrays should be in the range 0.0 to 1.0; MxN float
    #  arrays may be normalised.
    #----------------------------------------------------------    
    a = idl_arg_list(i)
    prefix = 'matplotlib.pyplot.'
    
    #----------------------------------------------
    #  Could also use matplotlib's "pcolormesh" ?
    #----------------------------------------------
    cmds = (prefix + 'imshow(%s') % a[0]

    if (len(a) > 1):
        print 'Warning: Multiple arguments to TV not supported yet.'
        
    #---------------------------------
    # Handle the CENTIMETERS keyword
    #---------------------------------
    if idl_key_set('centimeters', i):
        print 'Warning: CENTIMETERS keyword to TV not supported yet.'
        
    #----------------------------
    # Handle the INCHES keyword
    #-----------------------=----
    if idl_key_set('inches', i):
        print 'Warning: INCHES keyword to TV not supported yet.'
        
    #---------------------------
    # Handle the ORDER keyword
    #---------------------------
    if idl_key_set('order', i):   
        cmds += ", origin='upper'"
##    else:
##        cmds += ", origin='lower'"
        
    #---------------------------
    # Handle the TRUE keyword
    #---------------------------
    k = idl_key_index('true', i)
    if (k != -1):
        print 'Warning: TRUE keyword to TV not supported yet.'
        
    #---------------------------
    # Handle the WORDS keyword
    #---------------------------
    if idl_key_set('words', i):
        print 'Warning: WORDS keyword to TV not supported yet.'
        
    #---------------------------
    # Handle the XSIZE keyword
    #---------------------------
    k = idl_key_index('xsize', i)
    if (k != -1):
        print 'Warning: XSIZE keyword to TV not supported yet.'
        
    #---------------------------
    # Handle the YSIZE keyword
    #---------------------------
    k = idl_key_index('ysize', i)
    if (k != -1):
        print 'Warning: YSIZE keyword to TV not supported yet.'
        
    #----------------------------------------
    # Add "show()" command and return
    # (How is "show" different from "draw" ?
    #----------------------------------------
    cmds += ')'
    cmds += '\n' + prefix + 'show()'
    return cmds

#--------------------------------------------------------------------------
def idl_tvscl_callfunc(i,o):
    a = idl_arg_list(i)
    prefix = 'matplotlib.pyplot.'
    
    #----------------------------------------------
    #  Could also use matplotlib's "pcolormesh" ?
    #----------------------------------------------
    cmds = (prefix + 'imshow(%s)') % a[0]
    print 'Warning: TVSCL procedure is not supported yet.'
    return cmds
    
#--------------------------------------------------------------------------
def idl_uniq_callfunc(i,o):
    #----------------------------------------------------------
    #  Notes:  This is not finished yet.
                   
    #  IDL's UNIQ returns the index of the *last* element
    #  in each set (or run) of non-unique elements.
                   
    #  UNIQUE1D flattens array argument if not already 1D,
    #  which is the same thing IDL does.
    #  It also returns position of *first* occurrence of
    #  each unique element in the original array vs. *last*.
    #----------------------------------------------------------
    #  This does not yet behave identically to IDL's UNIQ.
    #  As an example, let a = [2,2,2,3,3,4,4,1,2,3,4], then:
    #      i1 = uniq(a, sort(a)) = [7,2,4,6]
    #      i2 = unique1d(a, return_index=True)[0] = [7,0,3,5]
    #  However, a[i1] = a[i2] = [1,2,3,4]
    #----------------------------------------------------------
    if (len(i) == 2):
        # 2nd argument puts array in sorted order.
        cmd = ('unique1d(%s, return_index=True)[0]' % i[0])
    else:
        msg = 'This function is not fully supported.'
        print_error_message('UNIQ', msg)
        return ''
    return cmd

#--------------------------------------------------------------------------
def idl_wdelete_callfunc(i,o):
    a = idl_arg_list(i)
    if (len(a) == 0):
        return 'matplotlib.pyplot.close()'

    index_str = get_window_index_string(a[0])

    cmd = ('matplotlib.pyplot.close(%s)' % index_str)
    for k in range(1,len(a)):
        index_str = get_window_index_string(a[k])       
        cmd += ('\nmatplotlib.pyplot.close(%s)' % index_str)
    return cmd
    
#--------------------------------------------------------------------------
def idl_where_callfunc(i,o):
    #--------------------------------------------------------------
    #  Note:  IDL's WHERE function returns -1L if there are
    #         no matches.  Some code may use "if (w[0] ne -1L)"
    #         in subsequent lines, but it is better to get the
    #         count (say, nw) with the optional 2nd argument and
    #         use a test like: "if (nw ne 0)".
    
    #         If the COMPLEMENT keyword is used, IDL's WHERE is
    #         more efficient because it gets everything in 1 call.

    #         We must use "invert" vs. "not" for complement set.

    #         The "I2PY_w" trick makes use of 2 Python features
    #         and should not result in any performance hit.
    #--------------------------------------------------------------
    # NB!     An argument can contain an equals sign, as in:
    #             w = where(a eq 10)   (since eq -> ==)
    #             w = where(a le 10)   (since le -> <=)
    #         The "idl_arg_list" routine must take this into
    #         account.
    #--------------------------------------------------------------
    # NB!     Avoiding the use of "ravel()" allows us to use the
    #         the result of "where()" as a subscript to the orig-
    #         inal array, even if it is 2D or 3D.  This solves a
    #         number of problems but adds a few.  In particular,
    #         we need to use the [0] subscript when computing
    #         the size of the result, otherwise for 2D arrays it
    #         will be too big by a factor of 2, etc.
    #--------------------------------------------------------------
    a = idl_arg_list(i)

    if (len(a) == 1):
        s = 'where(%s)' % a[0]
        #### s = 'where(ravel(%s))[0]' % a[0]
    else:
        #  Optional second argument returns count.
        s  = 'I2PY_w = where(%s)\n' % a[0]
        #### s  = 'I2PY_w = where(ravel(%s))[0]\n' % a[0]
        s += ('%s = size(I2PY_w[0])' % a[1])
        
    k1 = idl_key_index('complement', i)
    if (k1 != -1):
        kv1 = keyword_var(i[k1])
        s += '\n%s = where(invert(%s))' % (kv1, a[0])
        #### s += '\n%s = where(ravel(invert(%s)))[0]' % (kv1, a[0])


    k2 = idl_key_index('ncomplement', i)
    if (k1 != -1) and (k2 != -1):
        kv2 = keyword_var(i[k2])
        s += '\n%s = size(%s[0])' % (kv2, kv1)
    return s

#--------------------------------------------------------------------------
def idl_window_callfunc(i,o):
##    if idl_key_set('free', i):
##        # Don't need to do anything?
##        pass

    a = idl_arg_list(i)      
    if (len(a) == 0):
        args = ''
    else:
        # matplotlib window indices start at 1
        args = get_window_index_string(a[0]) + ', '

    #--------------------------------------------------
    # Assume that monitor's dpi = 80.
    # Then, a window with (xsize, ysize) = (640, 480)
    # has a size in inches of (8.0, 6.0).
    #--------------------------------------------------
    dpi = 80.0
    
    #----------------------------------
    # Handle XSIZE and YSIZE keywords
    #----------------------------------
    k1 = idl_key_index('xsize', i)
    if (k1 != -1):
        kv1 = keyword_var(i[k1])
        kv1 = kv1 + '/' + str(dpi)
        # Can't evaluate if xsize is a variable name
        # kv1 = str(eval(kv1) / dpi)
    else:
        kv1 = '8'  # (npixels=640 if dpi=80)
    k2 = idl_key_index('ysize', i)
    if (k2 != -1):
        kv2 = keyword_var(i[k2])
        kv2 = kv2 + '/' + str(dpi)
        # Can't evaluate if xsize is a variable name
        # kv2 = str(eval(kv2) / dpi)
    else:
        kv2 = '6'  # (npixels=480 if dpi=80)

    #-----------------------------
    # These aren't supported yet
    # Not possible in matplotlib?
    # How about with wxPython?
    #-----------------------------
    k3 = idl_key_index('title', i)
    if (k3 != -1):
        msg = 'Warning: TITLE keyword to WINDOW not supported yet.'
        print msg
        # print_error_message('WINDOW', msg)       
    k4 = idl_key_index('xpos', i)
    if (k4 != -1):
        msg = 'Warning: XPOS keyword to WINDOW not supported yet.'
        print msg
        # print_error_message('WINDOW', msg)      
    k5 = idl_key_index('ypos', i)
    if (k5 != -1):
        msg = 'Warning: YPOS keyword to WINDOW not supported yet.'
        print msg
        # print_error_message('WINDOW', msg)

    args += 'figsize=(' + kv1 + ', ' + kv2 + '), dpi=80'
    cmd  = 'matplotlib.pyplot.figure(%s)' % (args)

    #------------------------------------------------
    # This "shows" all figures (it has no argument)
    #------------------------------------------------
    cmd += '\nmatplotlib.pyplot.show()'
    return cmd

#--------------------------------------------------------------------------
def idl_writeu_callfunc(i,o):
    #----------------------------------------------------
    # Note: "eof_test.pro" provides a simple test case.
    #----------------------------------------------------
    a = idl_arg_list(i)

    #---------------------------------------------
    # Swap the byte order of all the variables ?
    #------------------------------------------------------
    # Need "numpy.array" in case some vars are scalars, in
    # order for them to get access to "byteswap" method.
    # Use of "copy=0" and "True" does everything in place.
    # I2PY_SWAP_ENDIAN will have been defined earlier in
    # the same scope (routine) in call to OPENW.
    #------------------------------------------------------
    # This does not yet handle data in a structure.
    #------------------------------------------------------    
    cmd = 'if (I2PY_SWAP_ENDIAN):'
    for k in range(1,len(a)):
        cmd += '\n    array(%s, copy=0).byteswap(True)' % a[k]

    #--------------------------------
    # Write all of the data items ?
    #--------------------------------
    for k in range(1,len(a)):
        cmd += '\n%s.tofile(file_%s)' % (a[k], a[0])
    return cmd

#--------------------------------------------------------------------------
def idl_wset_callfunc(i,o):
    a = idl_arg_list(i) 
    if (len(a) == 0):
        args = ''
    else:
        # matplotlib window indices start at 1
        args = get_window_index_string(a[0])

    cmd  = 'matplotlib.pyplot.figure(%s)' % (args)
    return cmd

#--------------------------------------------------------------------------
def idl_xyouts_callfunc(i,o):

   #--------------------------------------------------------
   #  Notes:  matplotlib.pyplot.text uses DATA coordinates
   #          None of this has been tested yet.
   #--------------------------------------------------------
   
#  inkeys=['ALIGNMENT','CHARSIZE','CHARTHICK','TEXT_AXES',
#          'WIDTH','CLIP','COLOR','DATA','DEVICE','NORMAL',
#          'FONT','ORIENTATION','NOCLIP','T3D','Z']

    a = idl_arg_list(i)
    n_args = len(a)
    if (n_args == 1):
        msg = 'Single argument case is not supported.'
        print_error_message('XYOUTS', msg)
        return ''

    cmd = 'matplotlib.pyplot.text(%s, %s, %s' % (a[0], a[1], a[2])

    #-------------------------------
    # Handle the ALIGNMENT keyword
    #-------------------------------

    #------------------------------
    # Handle the CHARSIZE keyword
    #------------------------------

    #-------------------------------
    # Handle the CHARTHICK keyword
    #-------------------------------

    #---------------------------
    # Handle the COLOR keyword
    #---------------------------
    k = idl_key_index('color', i)
    if (k != -1):
        kv = keyword_var(i[k])
        cmd += ", color='%s'" % idl_color_mapping(kv)

    #--------------------------
    # Handle the FONT keyword
    #--------------------------

    #----------------------------
    # Handle the NORMAL keyword
    #----------------------------
    if idl_key_set('normal', i):
        cmd += ', transform=ax.transAxes'
    
    #---------------------------------
    # Handle the ORIENTATION keyword
    #---------------------------------
    
    return ( cmd + ')' )
    
#--------------------------------------------------------------------------

   
