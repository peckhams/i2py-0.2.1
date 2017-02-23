
#  Note: I2PY should recognize all built-in IDL routines and issue
#        a simple error message for those it can't yet translate.
#        It does this now for CONVOL, REBIN and SMOOTH, but for
#        most others the current behavior is to remain silent and
#        do nothing.

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

#         Modules to be imported (use "extracode" argument):
#         numpy.linalg, numpy, os, random, time, etc.
#--------------------------------------------------------------------

"""
Defines Python mappings for many IDL functions and procedures
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

from callfuncs      import *
from callfunc_utils import *
## import user_lib        ##########
from user_lib import *

################################################################################
#
#  IDL system variable maps
#
################################################################################

# pi is in Numeric/numarray/numpy
map_var('!DPI', 'numpy.pi')
map_var('!DTOR', '_dtor', '_dtor = numpy.pi / 180.0')
map_var('!PI',  'nympy.pi')
map_var('!RADEG', '_radeg', '_radeg = 180.0 / numpy.pi')

## map_var('!ORDER',
map_var('!PATH', 'sys.path', 'import sys')

#-----------------------------------------------------------
#  These next 2 ideas don't work.  See "PostfixExpression"
#  in "ir.py" for the current solution. (SDP)
#-----------------------------------------------------------
## map_var('!VALUES.F_INF', 'float32(numpy.Infinity)')
## map_var('!VALUES.F_NAN', 'float32(numpy.NaN)')
## map_var('!VALUES.D_INF', 'float64(numpy.Infinity)')
## map_var('!VALUES.D_NAN', 'float64(numpy.NaN)')

## map_var('!VALUES', 'float')
## map_var('.F_INF', '32(numpy.Infinity)')
## map_var('.F_NAN', '32(numpy.NaN)')
## map_var('.D_INF', '64(numpy.Infinity)')
## map_var('.D_NAN', '64(numpy.NaN)')

#-------------------------------------------
#  Don't do these here.  Deliberate typing
#  is now done in ir.py for "Number" node
#-------------------------------------------
# map_var('0b', '0')
# map_var('0d', 'double(0)')

################################################################################
#
#  Python reserved words that could be IDL variables
#
################################################################################
map_var('as',     '_as')
map_var('chr',    '_chr')
map_var('del',    '_del')
map_var('dir',    '_dir')
#------------------------------------------------------------
# Note: FILE is a keyword to DIALOG_PICKFILE and is often
# used as a keyword in user-written routines. Changing this
# mapping requires changes in "callfuncs.py", "idl_maps.py",
# and maybe "idl_func.py".
#------------------------------------------------------------
map_var('file',   'FILE')     ### or use "filename" ??
# map_var('file',   '_file')     # (before 6/25/09)
# map_var('file',   '_FILE')     ### or use "filename" ??
map_var('from',   '_from')
map_var('global', '_global')
map_var('in',     '_in')
map_var('is',     '_is')
map_var('lambda', '_lambda')
map_var('len',    '_len')
map_var('list',   '_list')
# map_var('map',    '_map')
map_var('map',    'MAP')
map_var('ord',    '_ord')
map_var('pass',   '_pass')
map_var('pow',    '_pow')
map_var('str',    '_str')
map_var('time',   '_time')     ## because of time package
#------------------------------------------------------------
# Note: TYPE is often used as a keyword that refers to data
#       type in user-written routines and in IDL routines
#       such as SIZE and MAKE_ARRRAY. Changing this mapping
#       requires changes in "callfuncs.py", "idl_maps.py",
#       and maybe "idl_func.py".
#------------------------------------------------------------
map_var('type',   'TYPE')
# map_var('type',   '_TYPE')  # (before 6/25/09)
# map_var('type',   '_type')
map_var('yield',  '_yield')

## map_var('local', '???')
## map_var('repr',  '???')
## map_var('vars',  '???')

# These don't work, probably due to parentheses.  See below.
# map_var('path_sep()', 'os.sep', 'import os')
# map_var('systime(1)', 'time()', 'import time')

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
map_pro('OPENR', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN','ERROR'],
        callfunc=(lambda i,o: idl_openr_callfunc(i,o)) )
map_pro('OPENU', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN','ERROR'],
        callfunc=(lambda i,o: idl_openu_callfunc(i,o)) )
map_pro('OPENW', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN','ERROR'],
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
                 'INDEX','TYPE','COMPLEX','DCOMPLEX'],
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
map_func('ASSOC', inpars=[1,2,3], noptional=1, inkeys=['PACKED'],
         callfunc=(lambda i,o: idl_assoc_callfunc(i,o)) )

## See IDL help pages for the formula that is used.
# map_func('BILINEAR',

# CONJ and CONJUGATE are synonyms in NumPy, and work the same.
# map_func('CONJ', inpars=[1], callfunc=(lambda i,o: 'conj(%s)' % i[0]))

map_func('CONVOL', inpars=[1,2,3], noptional=1,
         inkeys=['BIAS','CENTER','EDGE_TRUNCATE','EDGE_WRAP',
                 'EDGE_ZERO','INVALID','MISSING','NAN','NORMALIZE'],
         callfunc=(lambda i,o: idl_convol_callfunc(i,o)),
         extracode='import scipy.signal')

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
         inkeys=['DIMENSIONS','N_DIMENSIONS','N_ELEMENTS','TYPE'],
         callfunc=(lambda i,o: idl_size_callfunc(i,o) ))

# These two are not finished yet.
map_func('SMOOTH', inpars=[1], callfunc=(lambda i,o: idl_smooth_callfunc(i,o)) )
map_func('SORT', inpars=[1], callfunc=(lambda i,o: idl_sort_callfunc(i,o)) )

#  TEMPORARY capability is also available in Numpy because ufuncs
#  can take an optional output argument.
# map_func('TEMPORARY', inpars=[1],

## TRANSPOSE command is same in IDL and NumPy

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

map_pro('SHADE_SURF', inpars=[1,2,3], noptional=2,
        inkeys=['AX','AZ','BOTTOM','MAX_VALUE','MIN_VALUE',
                'SHADES','SKIRT','ZAXIS',
                'HORIZONTAL','LEGO','LOWER_ONLY','UPPER_ONLY',
                'SAVE','XLOG','YLOG','ZAXIS','ZLOG',
                'XTITLE','YTITLE','TITLE'],
        callfunc=(lambda i,o: idl_surface_callfunc(i,o, STYLE='shaded')),
        extracode='import matplotlib.axes3d')

map_pro('SURFACE', inpars=[1,2,3], noptional=2,
        inkeys=['AX','AZ','BOTTOM','MAX_VALUE','MIN_VALUE',
                'SHADES','SKIRT','ZAXIS',
                'HORIZONTAL','LEGO','LOWER_ONLY','UPPER_ONLY',
                'SAVE','XLOG','YLOG','ZAXIS','ZLOG',
                'XTITLE','YTITLE','TITLE'],
        callfunc=(lambda i,o: idl_surface_callfunc(i,o)),
        extracode='import matplotlib.axes3d')

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
         inkeys=['DIALOG_PARENT','FILE','FILTER','MULTIPLE_FILES',
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



