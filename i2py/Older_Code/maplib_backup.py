# 
#  Copyright (C) 2005 Christopher J. Stawarz <chris@pseudogreen.org>
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


"""
Defines mappings for some builtin IDL variables, procedures, and functions
"""


from map import map_var, map_pro, map_func


################################################################################
#
# Variable maps
#
################################################################################


# pi is in Numeric/numarray
map_var('!DPI', 'pi')
map_var('!RADEG', '_radeg', '_radeg = 180.0 / pi')

# (SDP) Python reserved words that could be IDL variables
map_var('in', 'in1')
map_var('pow', 'p1')
map_var('systime(1)', 'time()', 'import time')

################################################################################
#
# Procedure maps
#
################################################################################


map_pro('ON_ERROR', inpars=[1],
        callfunc=(lambda i,o: '# ON_ERROR, %s' % i[0]))
map_pro('PRINT', inpars=range(1,101), noptional=99, inkeys=['FORMAT'],
        callfunc=(lambda i,o: 'print ' + ', '.join(i)))


################################################################################
#
# Function maps
#
################################################################################


def arrgen(typename):
   "Returns an array-generation callfunc for type typename"
   return (lambda i,o: 'zeros([%s], %s)' %
           (', '.join([ i[n] for n in xrange(len(i)-1, -1, -1) ]), typename))

def typeconv(typename):
   "Returns a type-conversion callfunc for type typename"
   return (lambda i,o: 'array(%s, copy=0).astype(%s)' % (i[0], typename))

#----------------------------------------------------
#  Modules to be imported (use "extracode" argument)
#----------------------------------------------------
#  Matrix (for invert, etc.), numpy, os, random, time

#--------------------------------------------------------------------
#  Note:  arguements to map_var, map_pro and map_func are explained
#         in map.py, in the SubroutineMapping class definition.
#--------------------------------------------------------------------

#----------------------------------
# (SDP) General utility functions
#----------------------------------
# map_func('N_ELEMENTS', inpars=[1],
#          callfunc=(lambda i,o: 'array(%s, copy=0).nelements()' % i[0]))
map_func('N_ELEMENTS', inpars=[1],
         callfunc=(lambda i,o: 'size(%s)' % i[0]))
map_func('REPLICATE', inpars=range(1,10), noptional=7,
         callfunc=(lambda i,o: '(%s)*ones([%s])' % (i[0],
	           ', '.join([ i[n] for n in xrange(len(i)-1, 0, -1) ]))))
# map_func('SIZE',      inpars=[1],
# map_func('TEMPORARY', inpars=[1],
map_func('WHERE', inpars=[1], noptional=1,
         callfunc=(lambda i,o: 'where(ravel(%s))[0]' % i[0]))
# Better to do this as a variable?  See above.
# map_func('SYSTIME', inpars=[0], callfunc=(lambda i,o: 'time()' % i[0]))

#----------------------------------
# (SDP) Type conversion functions
#----------------------------------
map_func('BYTE',   inpars=[1], callfunc=typeconv('Int8'))
map_func('FIX',    inpars=[1], callfunc=typeconv('Int32'))
map_func('LONG',   inpars=[1], callfunc=typeconv('Int32'))
map_func('LONG64', inpars=[1], callfunc=typeconv('Int64'))
map_func('FLOAT',  inpars=[1], callfunc=typeconv('Float32'))
map_func('DOUBLE', inpars=[1], callfunc=typeconv('Float64'))
# map_func('STRING', inpars=[1], callfunc= ######)
# map_func('UINT',   inpars=[1], callfunc= ######)
# map_func('ULONG',  inpars=[1], callfunc= ######)

#---------------------------------
# (SDP) Array initializations
# (what about NOZERO keyword ??)
#---------------------------------
map_func('BYTARR',    inpars=range(1,9), noptional=7, callfunc=arrgen('Int8'))
map_func('INTARR',    inpars=range(1,9), noptional=7, callfunc=arrgen('Int16'))
map_func('LONARR',    inpars=range(1,9), noptional=7, callfunc=arrgen('Int32'))
map_func('LON64ARR',  inpars=range(1,9), noptional=7, callfunc=arrgen('Int64'))
map_func('FLTARR',    inpars=range(1,9), noptional=7, callfunc=arrgen('Float32'))
map_func('DBLARR',    inpars=range(1,9), noptional=7, callfunc=arrgen('Float64'))
#map_func('ULON64ARR', inpars=range(1,9), noptional=7, callfunc=arrgen('Int64'))

#---------------------------------------------
# (SDP) "Ramp functions" similar to "arange"
#-----------------------------------------------
#  Need to handle multiple dimension arguments
#-----------------------------------------------
# map_func('BINDGEN', inpars=range(1,9), noptional=7, callfunc=(lambda i,o: 'arange(%s, dtype='Int8')' % i[0]))
# map_func('INDGEN',  inpars=range(1,9), noptional=7, callfunc=()
# map_func('LINDGEN', inpars=range(1,9), noptional=7, callfunc=()
# map_func('FINDGEN', inpars=range(1,9), noptional=7, callfunc=()
# map_func('DINDGEN', inpars=range(1,9), noptional=7, callfunc=()
# map_func('SINDGEN', inpars=range(1,9), noptional=7, callfunc=()

#-------------------------------
# (SDP) Mathematical functions
#--------------------------------------------------
#  Ones with same names include: ceil, cos, cosh,
#  exp, floor, sin, sinh, sqrt, tan, tanh
#--------------------------------------------------
map_func('ABS',    inpars=[1], callfunc=(lambda i,o: 'absolute(%s)' % i[0]))
map_func('ACOS',   inpars=[1], callfunc=(lambda i,o: 'arccos(%s)'   % i[0]))
map_func('ALOG',   inpars=[1], callfunc=(lambda i,o: 'log(%s)'      % i[0]))
map_func('ALOG10', inpars=[1], callfunc=(lambda i,o: 'log10(%s)'    % i[0]))
map_func('ASIN',   inpars=[1], callfunc=(lambda i,o: 'arcsin(%s)'   % i[0]))
# map_func('ATAN',   inpars=[1], noptional=1,
# map_func('FFT',    inpars=[1],
# map_func('FINITE', inpars=[1],
map_func('MIN', inpars=[1],
         callfunc=(lambda i,o: 'array(%s, copy=0).min()' % i[0]))
map_func('MAX', inpars=[1],
         callfunc=(lambda i,o: 'array(%s, copy=0).max()' % i[0]))
map_func('RANDOMN',  inpars=[1], callfunc=(lambda i,o: 'random.standard_normal(%s)' % i[0]))
map_func('RANDOMU',  inpars=[1], callfunc=(lambda i,o: 'random.random(%s)' % i[0]))
# map_func('REGRESS',  inpars=[1],
# map_func('ROUND',    inpars=[1],

### Note:  Can use numpy's "cumsum" for TOTAL's CUMULATIVE keyword
###        Can also use array.sum() and array.cumsum().
# map_func('TOTAL',    inpars=[1], callfunc=(lambda i,o: 'sum(%s)' % i[0]))
# map_func('TRIGRID',  inpars=[1],

#--------------------------------------
# (SDP) String manipulation functions
#--------------------------------------
map_func('STRLEN',     inpars=[1], callfunc=(lambda i,o: 'len(%s)'      % i[0]))
map_func('STRLOWCASE', inpars=[1], callfunc=(lambda i,o: '(%s).lower()' % i[0]))
# This may work but doesn't support optional 3rd argument
# map_func('STRMID',     inpars=[1,2,3], noptional=1,
#     callfunc=(lambda i,o: '(%s)[%s:%s]' % i[0], i[1], i[2]))

###  This may work to get all positions.
###  Notice need to use first "%s" twice.
###  But IDL version just gets first occurrence.
###  See:  http://mail.python.org/pipermail/python-list/2006-June/389388.html
###    map_func('STRPOS',     inpars=[1],  callfunc(lambda i,o:
###       '[j for j in xrange(len(%s)) if %s.startswith(%s,j)]' % i[0],i[0],i[1]
map_func('STRSPLIT',   inpars=[1], callfunc=(lambda i,o: '(%s).split()' % i[0]))
map_func('STRTRIM',    inpars=[1], callfunc=(lambda i,o: '(%s).strip()' % i[0]))
map_func('STRUPCASE',  inpars=[1], callfunc=(lambda i,o: '(%s).upper()' % i[0]))

#------------------------------------
# (SDP) File manipulation functions
#------------------------------------
# map_func('EOF',         inpars=[1],
# map_func('FILE_COPY',   inpars=[1],
# map_func('FILE_DELETE', inpars=[1],
# map_func('FILE_INFO',   inpars=[1],
# map_func('FILE_LINES',  inpars=[1],
# map_func('FILE_SEARCH', inpars=[1],
# map_func('FILE_TEST',   inpars=[1],
# map_func('FREE_LUN',    inpars=[1],
# map_func('FSTAT',       inpars=[1],
# map_func('GET_LUN',     inpars=[1],
# map_func('OPENR',       inpars=[1],
# map_func('OPENU',       inpars=[1],
# map_func('OPENW',       inpars=[1],
map_func('PATH_SEP',    inpars=[0], callfunc=(lambda i: 'os.sep' % i[0]))

#-------------------------------------
# (SDP) Array manipulation functions
#-------------------------------------
# map_func('ASSOC',     inpars=[1],
# map_func('CONGRID',   inpars=[1],
# map_func('CONVOLVE',  inpars=[1],
# map_func('HISTOGRAM',  inpars=[1],
#----- from LinearAlgebra import *, but inverse(a) doesn't work ?
#----- from Matrix import *, then invert(a) seems to work
# map_func('INVERT',     inpars=[1], callfunc=(lambda i,o: 'invert(%s)' % i[0]))
# map_func('MAKE_ARRAY', inpars=[1],
# map_func('REBIN',      inpars=[1],
# map_func('REFORM',     inpars=[1,2,3], noptional=1, callfunc=(lambda i: 'reshape(%s,###' % i[0]))
# map_func('REVERSE',    inpars=[1],
# map_func('ROTATE',     inpars=[1],
# map_func('SHIFT',      inpars=[1],
# map_func('SMOOTH',     inpars=[1],
map_func('SORT',  inpars=[1], callfunc=(lambda i,o: 'argsort(ravel(%s))' % i[0]))
# map_func('UNIQ',      inpars=[1],

#------------------------------------
# Native GUI dialogs (via wxPython)
#------------------------------------
# map_func('DIALOG_PICKFILE', inpars=[1],


