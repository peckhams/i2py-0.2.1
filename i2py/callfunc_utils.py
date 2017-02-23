
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
#-------------------------------------------------------------------------
#  Notes: Arguments to map_var, map_pro and map_func are explained
#         in map.py, in the SubroutineMapping class definition.
#
#         lambda forms may not contain statements, but starting
#         with Python 2.5 can contain conditional expressions.
#         These are used for functions like ATAN and TOTAL below.
#
#         IDL's KEYWORD_SET function is handled at the bottom of
#         the file "map.py". (SDP)
#
#         Modules to be imported (use "extracode" argument):
#         numpy.linalg, numpy, os, random, time, etc.
#
################################################################################

import numpy  # (for numpy.binary_repr, etc.)
import re

################################################################################
#
#  Convenience functions, used in callfuncs.py.
#
################################################################################

      
def arrgen(typename):
    "Returns an array-generation callfunc for type typename"
    
    return (lambda i,o: "zeros([%s], dtype='%s')" %
           (reverse_arg_str(i), typename) if not(idl_key_set('nozero',i))
           else "empty([%s], dtype='%s')" % (reverse_arg_str(i), typename) )

#--------------------------------------------------------------------
def rampgen(typename):
    "Returns a 'ramp-generation' callfunc for type typename"
    
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

#--------------------------------------------------------------------
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
        kv = kv.replace('int16','')   # (see self.LBRACKET in ir.py)
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

    #--------------------------
    # Handle the XLOG keyword
    #--------------------------
    k = idl_key_index('xlog', i)
    if (k != -1):
        msg = 'Warning: XLOG graphics keyword not supported yet.'
        print msg
        
    #----------------------------
    # Handle the XMARGIN keyword
    #----------------------------
    k = idl_key_index('xmargin', i)
    if (k != -1):
        msg = 'Warning: XMARGIN graphics keyword not supported yet.'
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

    #--------------------------
    # Handle the YLOG keyword
    #--------------------------
    k = idl_key_index('ylog', i)
    if (k != -1):
        msg = 'Warning: YLOG graphics keyword not supported yet.'
        print msg
        
    #----------------------------
    # Handle the YMARGIN keyword
    #----------------------------
    k = idl_key_index('ymargin', i)
    if (k != -1):
        msg = 'Warning: YMARGIN graphics keyword not supported yet.'
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

    #--------------------------
    # Handle the ZAXIS keyword
    #--------------------------
    k = idl_key_index('zaxis', i)
    if (k != -1):
        msg = 'Warning: ZAXIS graphics keyword not supported yet.'
        print msg

    #--------------------------
    # Handle the ZLOG keyword
    #--------------------------
    k = idl_key_index('zlog', i)
    if (k != -1):
        msg = 'Warning: ZLOG graphics keyword not supported yet.'
        print msg
        
    return cmds

#--------------------------------------------------------------------------
def print_i2py_error(message):
    
    print 'Error: ' + message

#--------------------------------------------------------------------------
def print_i2py_warning(message):
    
    print 'Warning: ' + message
    
#--------------------------------------------------------------------------
    
##def print_error_message(idl_command, err_str):
##    msg  = "\n   >>>>  ERROR in converting call to %s." % idl_command
##    msg += "\n   >>>>  (%s)\n" % err_str
##    error.conversion_error(msg, 0)    
##    # print msg
##    # error.conversion_error(msg, self.lineno)
    
#--------------------------------------------------------------------------
