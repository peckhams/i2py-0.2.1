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

#-------------------------------------------
# (SDP) Convenience functions, used below.
#-------------------------------------------
def idl_key_set(key_str, inpars):
    s1 = key_str.lower() + '=True'
    s2 = key_str.lower() + '=1'
    return ((s1 in inpars) or (s2 in inpars))

def idl_arg_list(inpars):
    args = []
    for s in inpars:
        p = s.find('=')
        if (p == -1): args.append(s)
    return args

def idl_key_list(inpars):
    # Note: keys all have "=" now (vs. "/")
    # This isn't used anywhere now.
    keys = []
    for s in inpars:
        p = s.find('=')
        if (p != -1):
            name = s.split('=')[0]
            keys.append(name)
    return keys

def idl_key_index(key_str, inpars):
    for k in xrange(len(inpars)):
        s = inpars[k]
        p = s.find( key_str.lower() + '=' )
        if (p == 0): return k
    return -1

##def idl_key_present(key_str, inpars):
##    k = key_str.lower()
##    keys = []
##    for s in inpars:
##        p = s.find('=')
##        if (p != -1):
##            w = s.split('=')
##            keys.append(w[0].lower())
##    return (k in keys)

def reverse_arg_str(i):
    a = idl_arg_list(i)
    return ', '.join([ a[n] for n in xrange(len(a)-1, -1, -1) ])

def arg_product_str(i):
    return '*'.join([ i[n] for n in xrange(len(i)) ])

def keyword_var(inpar):
    return inpar.split('=')[1]

def remove_chars(s, chars):
    for c in chars: s = s.replace(c,'')
    return s


################################################################################
#
# Variable maps
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
##map_var('!VALUES.F_INF', 'float32(numpy.Infinity)')
##map_var('!VALUES.F_NAN', 'float32(numpy.NaN)')
##map_var('!VALUES.D_INF', 'float64(numpy.Infinity)')
##map_var('!VALUES.D_NAN', 'float64(numpy.NaN)')

##map_var('!VALUES', 'float')
##map_var('.F_INF', '32(numpy.Infinity)')
##map_var('.F_NAN', '32(numpy.NaN)')
##map_var('.D_INF', '64(numpy.Infinity)')
##map_var('.D_NAN', '64(numpy.NaN)')

#-------------------------------------------
#  Don't do these here.  Deliberate typing
#  is now done in ir.py for "Number" node
#-------------------------------------------
# map_var('0b', '0')
# map_var('0d', 'double(0)')

#----------------------------------------------------------
# (SDP) Python reserved words that could be IDL variables
#----------------------------------------------------------
map_var('as',     '_as')
map_var('chr',    '_chr')
map_var('del',    '_del')
map_var('dir',    '_dir')
map_var('from',   '_from')
map_var('global', '_global')
map_var('in',     '_in')
map_var('is',     '_is')
map_var('lambda', '_lambda')
map_var('len',    '_len')
map_var('list',   '_list')
map_var('map',    '_map')
map_var('ord',    '_ord')
map_var('pass',   '_pass')
map_var('pow',    '_pow')
map_var('str',    '_str')
map_var('type',   '_type')
map_var('yield',  '_yield')

##map_var('vars', '???')
##map_var('repr', '???')

# These don't work, probably due to parentheses.  See below.
# map_var('path_sep()', 'os.sep', 'import os')
# map_var('systime(1)', 'time()', 'import time')

################################################################################
#
# Procedure maps
#
################################################################################

map_pro('CD', inpars=[1], callfunc=(lambda i,o: 'os.chdir(%s)' % i[0]),
        extracode='import os')
map_pro('ON_ERROR', inpars=[1],
        callfunc=(lambda i,o: '# ON_ERROR, %s' % i[0] ))
map_pro('PRINT', inpars=range(1,101), noptional=99, inkeys=['FORMAT'],
        callfunc=(lambda i,o: 'print ' + ', '.join(i)))
map_pro('WAIT', inpars=[1], callfunc=(lambda i,o: 'time.sleep(%s)' % i[0]),
        extracode='import time')

#--------------------------------------------------
# (SDP) Device and Window manipulation procedures
#--------------------------------------------------
#  Use the Device Context (DC) in wxPython
#  IDL's DEVICE has _lots_ of keywords.
#--------------------------------------------------
# map_pro('DEVICE', inpars=[1],
#         callfunc=
# map_pro('SET_PLOT', inpars=[1],
#         callfunc=
# map_pro('WDELETE', inpars=[1],
# map_pro('WINDOW',  inpars=[1],
# map_pro('WSET',    inpars=[1],

#-----------------------------------------------
# (SDP) Plotting procedures (via matplotlib ?)
#-----------------------------------------------
# map_pro('OPLOT',   inpars=[1],
# map_pro('PLOT',    inpars=[1],
# map_pro('PLOTS',   inpars=[1],

#--------------------------------------
#  (SDP) File manipulation procedures
#  For more info, try "help(file)"
#  Python "open" is alias to "file".
#-----------------------------------------------------------
#  NOTE:  In IDL, files are opened before we know whether
#         we will be reading text or binary, so how can we
#         convert properly?
#-----------------------------------------------------------
map_pro('CLOSE', inpars=range(1,11), noptional=9, inkeys=['ALL'],
        callfunc=(lambda i,o: idl_close_callfunc(i,o) ))
# map_pro('FILE_COPY',   inpars=[1],
map_pro('FILE_DELETE', inpars=range(1,33), noptional=31,
        callfunc=(lambda i,o: idl_file_delete_callfunc(i,o)),
        extracode='import idl_func')
map_pro('FREE_LUN', inpars=range(1,11), noptional=9,
        callfunc=(lambda i,o: idl_close_callfunc(i,o) ))
# map_pro('GET_LUN',     inpars=[1],
map_pro('OPENR', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN'],
        callfunc=(lambda i,o: "file_%s = open(%s, 'rb')" % (i[0],i[1]) ))
map_pro('OPENU', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN'],
        callfunc=(lambda i,o: "file_%s = open(%s, 'rb+')" % (i[0],i[1]) ))
map_pro('OPENW', inpars=[1,2], inkeys=['GET_LUN', 'SWAP_ENDIAN'],
        callfunc=(lambda i,o: "file_%s = open(%s, 'wb')" % (i[0],i[1]) ))
## In IDL, if (unit < 0), then position is returned (f.tell)
map_pro('POINT_LUN',  inpars=[1,2],
        callfunc=(lambda i,o: ('file_%s.seek(%s)' % (i[0],i[1]))
                  if ('-' not in i[0]) else ('%s = file_%s.tell()' %
                  (i[1], remove_chars(i[0],' ()*-1'))) ))
        
#  Problem:  How do I know if file was opened for binary or text I/O?
#  For more info:  help(numpy.ndarray.tofile).

map_pro('PRINTF', inpars=range(1,102), noptional=99, inkeys=['FORMAT'],
        callfunc=(lambda i,o: '%s.tofile(file_%s)' % (i[1],i[0]) ))
        # callfunc=(lambda i,o: 'print ' + ', '.join(i)))

# map_pro('READF',     inpars=[1],
map_pro('READU', inpars=[1,2], 
        callfunc=(lambda i,o: "%s = fromfile(file_%s, count=size(%s), dtype=str(%s.dtype))"
                  % (i[1],i[0],i[1],i[1]) ))
map_pro('WRITEU', inpars=[1,2], 
        callfunc=(lambda i,o: '%s.tofile(file_%s)' % (i[1],i[0]) ))

#------------------------------------------------------
#  Can use methods in os.path, e.g. abspath, dirname,
#  basename, exists, getsize(filename), isdir, split
#------------------------------------------------------


#------------------------------
# (SDP) Additional procedures
#------------------------------
# map_pro('MAKE_ARRAY', inpars=[1],
# map_pro('ON_IOERROR', inpars=[1],
# map_pro('ONLINE_HELP', inpars=[1],
# map_pro('RESTORE', inpars=[1],
# map_pro('SAVE', inpars=[1],
# map_pro('TRIANGULATE', inpars=[1],

################################################################################
#
# Function maps
#
################################################################################

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

def arrgen(typename):
   "Returns an array-generation callfunc for type typename"
   return (lambda i,o: "zeros([%s], dtype='%s')" %
           (reverse_arg_str(i), typename) if not(idl_key_set('nozero',i))
           else "empty([%s], dtype='%s')" % (reverse_arg_str(i), typename) )

def rampgen(typename):
   "Returns a 'ramp-generation' callfunc for type typename (SDP)"
   return (lambda i,o: "arange(%s, dtype='%s')" % (arg_product_str(i), typename)
           if (len(i)==1) else "reshape(arange(%s, dtype='%s'), [%s])" %
           ( arg_product_str(i), typename, reverse_arg_str(i) ) )

def typeconv(typename):
   "Returns a type-conversion callfunc for type typename"
   return (lambda i,o: '%s(%s)' % (typename.lower(), i[0]))

##def typeconv(typename):
##   "Returns a type-conversion callfunc for type typename"
##   return (lambda i,o: "array(%s, copy=0).astype('%s')" % (i[0], typename))

#--------------------------------------------------------------------------
#  This shows one way to handle keywords to a function that are used
#  in IDL to return values.  They must be included with inpars since
#  a function isn't allowed to have outpars.  The undefined variables
#  are set to expressions in separate function calls on subsequent lines.
#--------------------------------------------------------------------------
def idl_min_callfunc(i,o):
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
    # print 'i =', i
    # print 'idl_args = ', a
    # print 'keyword_var(i[k1]) =', kv1
    # print 'keyword_var(i[k2]) =', kv2
    return s
#--------------------------------------------------------------------------
def idl_max_callfunc(i,o):
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
    # print 'i =', i
    # print 'idl_args = ', a
    # print 'keyword_var(i[k1]) =', kv1
    # print 'keyword_var(i[k2]) =', kv2
    return s
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
    a = idl_arg_list(i)

    if (len(a)==1):
        s = 'where(ravel(%s))[0]' % i[0]
    else:
        #  Optional second argument returns count.
        s  = 'I2PY_w = where(ravel(%s))[0]' % i[0]
        s += '\n%s = size(I2PY_w)' % a[1]
        
    k1 = idl_key_index('complement', i)
    if (k1 != -1):
        kv1 = keyword_var(i[k1])
        s = s + '\n%s = where(ravel(invert(%s))[0]' % (kv1, i[0])

    k2 = idl_key_index('ncomplement', i)
    if (k1 != -1) and (k2 != -1):
        kv2 = keyword_var(i[k2])
        s = s + '\n%s = size(%s)' % (kv2, kv1)
    return s
#--------------------------------------------------------------------------
def idl_size_callfunc(i,o):
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
        s  = 'I2PY_a = zeros(ndim(%s)) \n'
        s += 'for I2PY_n in xrange(ndim(%s)-1,-1,-1): \n'
        s += '    I2PY_a[I2PY_n] = size(%s, I2PY_n)'
        return ( s % (i[0],i[0],i[0]) )
    
    return "##### IDL's SIZE function is not fully supported. #####"

##  s = "array((" + "repeat('size(%s,%s)',
        
## ', '.join([ a[n] for n in xrange(len(a)-1, -1, -1) ])

##    a = idl_arg_list(i)
##    s = 'array( (ndim(%s), '
##    s = s + 'size(%s, n), size(%s, n-1), ...'
##    s = s + 'idl_type_code(%s), '
##    s = s + 'size(%s) )'
##    return (s % (i[0],i[0],i[0].....))
#--------------------------------------------------------------------------
def idl_rotate_callfunc(i,o):
    #  Note:  IDL's ROTATE command works with 1D and 2D arrays.
    #         As in IDL, the "rotation code" is modulo 8. 
    #         Each NumPy command here was checked for 2D arrays,
    #         but only TRANSPOSE and FLIPUD work for 1D arrays.
    #         FLIPUD reverses elements in a 1D array.
    #         Commented lines also work, but are expected to
    #         be slower.
    #         For 2D arrays, NumPy's SWAPAXES = TRANSPOSE.
    #---------------------------------------------------------------
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
def idl_reform_callfunc(i,o):
    a = idl_arg_list(i)
    a = a[1:]  # remove the array argument
    s = 'reshape(%s, [%s])' % (i[0], reverse_arg_str(a))
    return s
#--------------------------------------------------------------------------
def idl_total_callfunc(i,o):
    if (idl_key_set('nan', i)):
        if (idl_key_set('cumulative',i)):
            ##  There is no "nancumsum" function ?
            cmd_str = 'cumsum(%s)'
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
def idl_strtrim_callfunc(i,o):
    if (len(i)==1): return ('%s.rstrip()' % i[0])
    flag = eval(i[1])
    if (flag == 2):
        return ('%s.strip()' % i[0])
    elif (flag == 1):
        return ('%s.lstrip()'  % i[0])
    else: return ('%s.rstrip()' % i[0])
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
        kv = kv.replace('concatenate([','')
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
        xshift = eval(i[1])
        yshift = eval(i[2])
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
def idl_close_callfunc(i,o):
    # if idl_key_set('all'):
        # Close all files
        
    cmd = ('file_%s.close()' % i[0])
    for k in range(1,len(i)):
        cmd += ('\nfile_%s.close()' % i[k])
    return cmd

#--------------------------------------------------------------------------
def idl_file_delete_callfunc(i,o):
    cmd = ('idl_func.file_delete(%s)' % i[0])
    for k in range(1,len(i)):
        cmd += ('\nidl_func_file_delete(%s)' % i[k])
    return cmd

#--------------------------------------------------------------------------
def idl_fstat_callfunc(i,o):
    #-------------------------------------------------------
    # Note:  IDL's FSTAT function returns a structure, but
    #        is commonly used to get the size of a file.
    #        e.g. temp     = fstat(unit)
    #             filesize = temp.size
    #        Could add remaining fields for FSTAT in the
    #        call to "bunch".
    #-------------------------------------------------------
    #        Would be cleaner to add an FSTAT function to
    #        "idl_func.py".  (Started one there.)
    #-------------------------------------------------------
    s  = 'I2PY_temp = bunch(size=long(0))\n'
    s += 'I2PY_stat      = os.stat(file_%s.name)\n'
    s += 'I2PY_temp.size = I2PY_stat[6])'
    return (s % i[0])

    #-------------------
    #  This also works
    #-------------------
##    s  = 'I2PY_temp = bunch(size=long(0))\n'
##    s += 'I2PY_temp.size = os.path.getsize(file_%s.name)'
##    return (s % i[0])

#--------------------------------------------------------------------------
##def idl_file_delete_callfunc(i,o):
##    #  Note:  We must use os.rmdir() to delete empty dirs,
##    #  so this is better done in idl_func.py.
##    
##    cmd = ('os.remove(%s)' % i[0])
##    for k in range(1,len(i)):
##        cmd += ('\nos.remove(%s)' % i[k])
##    return cmd
#--------------------------------------------------------------------------
def idl_finite_callfunc(i,o):
    if idl_key_set('infinity', i):
        return ('isinf(%s)' % i[0])
    if idl_key_set('nan', i):
        return ('isnan(%s)' % i[0])
    return ('isfinite(%s)' % i[0])

#--------------------------------------------------------------------------
def idl_strsplit_callfunc(i,o):
    #--------------------------------------------------------
    #  Note: The currently supported keywords are: EXTRACT,
    #        COUNT and LENGTH.
    #        Other keywords are: ESCAPE, REGEX, FOLD_CASE,
    #        and PRESERVE_NULL.
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
            cmd = ('%s.split(%s)' % (a[0], a[1]) )
    else:
        # Return positions of the substrings
        if (n_args == 1):
            cmd = ('map(%s.find, %s.split())' % (a[0], a[0]) )
        else:
            cmd = ('map(%s.find, %s.split(%s))' % (a[0], a[0], a[1]) )

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
##def idl_byte_callfunc(i,o):
##    s  = "idl_byte = lambda c: array(c, copy=0).astype('UInt8') % 256 "
##    s += "if ( str(c).isdigit() ) else'
##    s += "array(map(ord, c), copy=0)\n"    
##    return (s % (i[0],i[0],i[0],i[0])   
#--------------------------------------------------------------------------

#----------------------------------
# (SDP) General utility functions
#----------------------------------

#-----------------------------------------------------------
#  In IDL, we have "a = execute(<string>)", but in Python
#  we just have "exec(<string>)".  So here we just set the
#  IDL variable (e.g. "a") to 1 (for success) and then call
#  "exec" on the next line.
#-----------------------------------------------------------
map_func('EXECUTE', inpars=[1,2,3], noptional=2,
         callfunc=(lambda i,o: '1  # (EXEC has no return value)\nexec(%s)'
         % i[0].replace('&',';')) )
map_func('N_ELEMENTS', inpars=[1],
         callfunc=(lambda i,o: 'size(%s)' % i[0]))
#---------------------------------------------------
# (SDP) Use NumPy's REPEAT function, which can do
#  strings, numbers and structures, similar to IDL.
#  Only supports 1D arrays as written.
#---------------------------------------------------
map_func('REPLICATE', inpars=[1,2],
         callfunc=(lambda i,o: 'repeat(%s,%s)' % (i[0],i[1]) ) )
##map_func('REPLICATE', inpars=range(1,10), noptional=7,
##         callfunc=(lambda i,o: '(%s)*ones([%s])' % (i[0],
##	           ', '.join([ i[n] for n in xrange(len(i)-1, 0, -1) ]))))
map_func('SIZE', inpars=[1],
         inkeys=['DIMENSIONS','N_DIMENSIONS','N_ELEMENTS'],
         callfunc=(lambda i,o: idl_size_callfunc(i,o) ))

#  This capability is also available in Numpy because ufuncs
#  can take an optional output argument.
# map_func('TEMPORARY', inpars=[1],

##map_func('WHERE', inpars=[1], 
##         callfunc=(lambda i,o: 'where(ravel(%s))[0]' % i[0] ))
## This is not quite ready.
map_func('WHERE', inpars=[1,2,3,4], noptional=3,
         inkeys=['COMPLEMENT','NCOMPLEMENT'],
         callfunc=(lambda i,o: idl_where_callfunc(i,o)) )

map_func('SYSTIME', inpars=[1], callfunc=(lambda i,o: 'time.time()'),
          extracode='import time')

#----------------------------------
# (SDP) Type conversion functions
#-------------------------------------------------------
#  Note:  Numpy also supports 'Float96' = 'longdouble'
#-------------------------------------------------------
# map_func('BYTE',   inpars=[1], callfunc=typeconv('Int8'))
# map_func('BYTE',   inpars=[1], callfunc=(lambda i,o: idl_byte(i[0])))
map_func('BYTE',   inpars=[1],
         callfunc=(lambda i,o: 'idl_func.byte(%s)' % i[0]),
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
# map_func('COMPLEX',   inpars=[1], callfunc= ### dtype='Complex32' ###)
# map_func('DCOMPLEX',  inpars=[1], callfunc= ### dtype='Complex64' ###)
# map_func('MACHAR',    inpars=[1], callfunc= ### numpy.lib.machar  ###)

#---------------------------------
# (SDP) Array initializations
# (what about NOZERO keyword ??)
#---------------------------------
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

#---------------------------------------------
# (SDP) "Ramp functions" similar to "arange"
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
map_func('CINDGEN',    inpars=range(1,9), noptional=7, callfunc=rampgen('Complex32'))
map_func('DCINDGEN',   inpars=range(1,9), noptional=7, callfunc=rampgen('Complex64'))
map_func('SINDGEN',    inpars=range(1,9), noptional=7,
         callfunc=(lambda i,o: 'idl_func.sindgen(%s)' % i[0]),
         extracode='import idl_func')  ###########
         
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

# Next two don't work if argument is a list vs. an array
# map_func('MIN', inpars=[1], callfunc=(lambda i,o: '%s.min()' % i[0]))
# map_func('MAX', inpars=[1], callfunc=(lambda i,o: '%s.max()' % i[0]))

map_func('RANDOMN', inpars=range(1,10), noptional=9,
         inkeys=['BINOMIAL','DOUBLE','GAMMA','LONG','NORMAL','POISSON','UNIFORM'],
         callfunc=(lambda i,o: idl_random_callfunc(i,'RANDOMN') ))
map_func('RANDOMU', inpars=range(1,10), noptional=9,
         inkeys=['BINOMIAL','DOUBLE','GAMMA','LONG','NORMAL','POISSON','UNIFORM'],
         callfunc=(lambda i,o: idl_random_callfunc(i,'RANDOMU') ))
# map_func('REGRESS',  inpars=[1],
map_func('ROUND',    inpars=[1], callfunc=(lambda i,o: "around(%s).astype('Int32')" % i[0]))
map_func('TOTAL', inpars=[1,2,3,4], noptional=3,
         inkeys=['CUMULATIVE','DOUBLE','NAN'],
         callfunc=(lambda i,o: idl_total_callfunc(i,o) ))

# map_func('TRIGRID',  inpars=[1],

#--------------------------------------
# (SDP) String manipulation functions
#--------------------------------------
# map_func('READS', inpars=[1],
map_func('STRING',     inpars=[1], callfunc=(lambda i,o: 'str(%s)' % i[0]))
map_func('STRLEN',     inpars=[1], callfunc=(lambda i,o: 'len(%s)' % i[0]))
map_func('STRLOWCASE', inpars=[1], callfunc=(lambda i,o: '%s.lower()' % i[0]))
# STRMID also has a REVERSE_OFFSET keyword and accepts array arguments
map_func('STRMID',     inpars=[1,2,3], noptional=1,
         callfunc=(lambda i,o: '%s[%s:]' % (i[0],i[1])
                   if (len(i)==2) else '%s[%s:%s]' %
                   (i[0], i[1], str(eval(i[1]) + eval(i[2]))) ))

# Returns index or -1 if substring is not found, just like IDL
map_func('STRPOS', inpars=[1,2], callfunc=(lambda i,o: '%s.find(%s)' % (i[0],i[1]) ))
###  This may work to get all positions.
###  Notice need to use first "%s" twice.
###  But IDL's STRPOS just gets first occurrence.  (See STRSPLIT below.)
###  See:  http://mail.python.org/pipermail/python-list/2006-June/389388.html
###map_func('STRPOS',     inpars=[1],  callfunc(lambda i,o:
###       '[j for j in xrange(len(%s)) if %s.startswith(%s,j)]' % i[0],i[0],i[1]

# Note that STRPUT is actually a procedure.
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

#------------------------------------------------------
#  Can use methods in os.path, e.g. abspath, dirname,
#  basename, exists, getsize(filename), isdir, split
#  Also check out os.stat (for filesize, etc.)
#------------------------------------------------------

#------------------------------------
# (SDP) File manipulation functions
#    Also see procedures, above
#------------------------------------
map_func('EOF', inpars=[1],
         callfunc=(lambda i,o: 'file_%s.tell() == os.path.getsize(file_%s.name)'
         % (i[0],i[0])), extracode='import os')
# map_func('FILE_INFO',   inpars=[1],
# map_func('FILE_LINES',  inpars=[1],
# map_func('FILE_SEARCH', inpars=[1],
map_func('FILE_TEST', inpars=[1], inkeys=['DIRECTORY'],
         callfunc=(lambda i,o: 'os.path.exists(%s)' % i[0]),
         extracode='import os')
map_func('FSTAT', inpars=[1],
         callfunc=(lambda i,o: idl_fstat_callfunc(i,o)),
         extracode='import os')
map_func('PATH_SEP', callfunc=(lambda i,o: 'os.sep'),
          extracode='import os')

#-------------------------------------
# (SDP) Image manipulation functions
#-------------------------------------------------------------
#  Check out imageop module, esp. imageop.scale (like rebin)
#  Check out colorsys, imghdr, jpeg,  modules.
#-------------------------------------------------------------
# map_func('BYTSCL', inpars=[1], inkeys=['MAX','MIN','NAN','TOP'],
#           callfunc=(lambda i,o: '(
# map_func('CONGRID', inpars=[1],
# map_func('REBIN', inpars=[1],     #### maybe imageop.scale

#-------------------------------------
# (SDP) Array manipulation functions
#-------------------------------------
# map_func('ASSOC',     inpars=[1],
## See IDL help pages for the formula that is used.
# map_func('CONJ',      inpars=[1],  ### goes to conjugate() in numpy)

# Maybe only works for 1D arrays.
# map_func('CONVOLVE',  inpars=[1],  ### goes to convolve(a, kernel) in numpy)
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
map_func('HISTOGRAM',  inpars=[1], callfunc=(lambda i,o: 'histogram(%s)[0]' % i[0]))

# map_func('INTERPOL',     inpars=[1],   ##### maybe use numpy.interp

#----- from Matrix import *, then invert(a) also seems to work
map_func('INVERT', inpars=[1], callfunc=(lambda i,o: 'linalg.inv(%s)' % i[0]))
# map_func('ISHFT', inpars=[1],  ### goes to right_shift(), left_shift
map_func('NORM', inpars=[1], callfunc=(lambda i,o: 'linalg.norm(%s)' % i[0]))
## REFORM's OVERWRITE keyword is not supported yet.
map_func('REFORM', inpars=range(1,9), noptional=7, 
         callfunc=(lambda i,o: idl_reform_callfunc(i,o) ))
map_func('REVERSE', inpars=[1], callfunc=(lambda i,o: 'flipud(%s)' % i[0]) )
map_func('ROTATE', inpars=[1,2], callfunc=(lambda i,o: idl_rotate_callfunc(i,o)) )

#-------------------------------------------------------------------
# Note: This only handles 1D and 2D arrays so far.
#       A 3rd argument to SHIFT implies a 2D array, and a 4th
#       argument would imply a 3D array, etc.
#       It seems that NumPy's ROLL can only do one axis at a time?
#       If so, will need two calls to ROLL.
#       ROLL applied to 2D array with only 2 args treats array
#       as if it were 1D (flattened).
#-------------------------------------------------------------------
map_func('SHIFT', inpars=[1,2,3,4], noptional=2,
         callfunc=(lambda i,o: idl_shift_callfunc(i,o)) )

# map_func('SMOOTH',     inpars=[1],
map_func('SORT',  inpars=[1], callfunc=(lambda i,o: 'argsort(ravel(%s))' % i[0]))

## TRANSPOSE command is same in IDL and NumPy
## map_func('TRANSPOSE', inpars=[1], callfunc=(lambda i,o: 'transpose(%s)' % i[0]))

## Not quite finished yet.
map_func('UNIQ',  inpars=[1], callfunc=(lambda i,o: 'unique1d(%s, return_index=True)[0]' % i[0]))

#------------------------------------
# Native GUI dialogs (via wxPython)
#------------------------------------
# map_func('DIALOG_PICKFILE', inpars=[1],


