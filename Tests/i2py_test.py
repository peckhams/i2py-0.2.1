from numpy import *
import numpy
import idl_func
import sys

import os

import wx, os

import time

import idl_func

import webbrowser

import matplotlib.pyplot

import matplotlib.axes3d

import os, idl_func

import idl_func, os

#*******************************************************************
#   i2py_test.pro

#   Author:   Dr. Scott D. Peckham, INSTAAR, Univ. of Colorado

#   Created:  Aug. 14-15, 2008
#   Modified: Aug. 19-26, 2008
#   Modified: Sept. 4-12, 2008
#   Modified: Oct. 12-16, 2008
#   Modified: Nov. 5-7, 10-11, 17-21,  2008
#   Modified: June 10-12, 2009
#   Modified: June 18-19, 2009

#*******************************************************************
def Test_Procedure(MY_KEY=None, KEY2=None, KEY3=None):

    n_params = 0
    key2 = KEY2
    abc = KEY3
    _opt = (MY_KEY, key2, abc)
    def _ret():
    def _ret():
        _opt_rv = zip(_opt, [MY_KEY, key2, abc])
        _rv = [_o[1] for _o in _opt_rv if _o[0] is not None]
        if (len(_rv) == 1):
            return _rv[0]
        else:
            return tuple(_rv)
    
    # FORWARD_FUNCTION Func1, Func2
    
    #------------------------------------------
    # IF STATEMENT with AND, OR and NOT tests
    #------------------------------------------
    if not(logical_or(a, b)):    
        n = int16(0)
    if (logical_or(a, b)):    
        n = int16(0)
    if (logical_or(logical_or(a, b), c)):    
        n = int16(0)
    if (logical_and((logical_or(a, b)), c)):    
        n = int16(0)
    if (logical_and(logical_and(a, b), c)):    
        n = int16(0)
    if (logical_and((logical_or(a, b)), not(c))):    
        n = int16(0)
    if (logical_and((logical_or(a, b)), (logical_or(c, d)))):    
        n = int16(0)
    if logical_or(a, b):    
        n = int16(0)
    
    #------------------------
    #  Square bracket tests
    #------------------------
    a = my_func(int16([1, 2, 3, 4]))
    a = int16([1, 2, 3, 4])
    a = uint8([0, 1, 2, 3])
    a = int16([0, 1, 2, 3])
    a = int32([0, 1, 2, 3])
    a = float64([0, 1, 2, 3])
    a = int64([0, 1, 2])
    a = float32([0.0, 1, 2.])
    a = array(['x', 'y', 'z'])
    a = array(["x", "y", "z"])
    a = array(['x', "y"])
    msg = array(['Error message.'])
    #---------------------------
    a = concatenate((a,[1]))
    #---------------------------
    a = concatenate(([0],a))
    #---------------------------
    a = concatenate(([1,2,3],[4]))
    #---------------------------
    a = concatenate(([0],[1,2,3]))
    #---------------------------
    a = concatenate(([1,2],[0],[3,4]))
    #---------------------------
    a = concatenate(([1,2,3],b))
    #---------------------------
    a = concatenate((b,[1,2,3]))
    #---------------------------
    a = array([int16([1, 2, 3]), int16([4, 5, 6])])
    #---------------------------
    a = int16([1, 2, 3])
    b = int16([4, 5, 6])
    c = concatenate((a, b))
    #----------------------------------
    a = array([array([int16([1, 2]), int16([3, 4])]), array([int16([5, 6]), int16([7, 8])])])
    
    #-------------------
    # Array subscripts
    #-------------------
    b = a(3)
    b = a(1, 2)
    b = a[4]
    b = a[array([4])]
    b = a[2,2]
    b = a[:,2]
    b = a[1:4,0:3]
    b = a[w1[w2]]
    
    #-----------------------
    #  SORT function tests
    #----------------------------------------------
    #Next line must use "array" vs. "concatenate"
    #for converting the brackets, otherwise usage
    #shown will not work in Python.
    #----------------------------------------------
    b = int16([5, 3, 1, 2, 8, 7, 0, 6])
    s = argsort(ravel(b))
    b2 = b[s]
    
    #---------------------
    # Cleaner increments
    #---------------------
    b12 += abc
    b12 += abc
    
    #----------------------------------
    # Minimum/Maximum array operators
    #----------------------------------
    b = minimum(a, 5)
    a = minimum(a, 5)   #(Should we do in-place with 3rd arg to minimum() ?)
    a = maximum(a, 5)
    
    #-------------------------
    #  Boolean keyword tests
    #------------------------------------------------
    #  Note also how unset keywords are initialized
    #  to KEY=None in "Test_Procedure" at the top.
    #------------------------------------------------
    a = my_function(key1=uint8(0), key2=0)          #(unset keywords)
    a = my_function(key3=uint8(1), key4=1, key5=True)   #(set keywords)
    a = my_function(key1=key1)
    a = my_function(key1=some_function(b))
    
    #------------------------------
    #  KEYWORD_SET function tests
    #------------------------------
    KEY1 = (KEY1 not in [0,None])
    if ((KEY1 not in [0,None])):    
        print 'Key is set.'
    if (KEY1 in [0,None]):    
        KEY1 = int16(0)
    if (MY_KEY in [0,None]):    
        MY_KEY = int16(0)
    if not(a):    
        b = int16(0)   # (should be "not" vs. "logical_not")
    
    #------------------
    #  Special tests
    #------------------
    a = int16([1, 2, 3]).max()
    i = arange(5, dtype='Int16')
    
    #-----------------------------
    #  Some IDL system variables
    #-----------------------------
    p = sys.path
    d = idl_func.device_name()
    os = platform.system()
    osf = ('Windows' if (platform.system()=='Windows') else 'UNIX')
    
    #-------------------------
    # NaN and Infinity tests
    #-------------------------
    f_nan = float32(numpy.NaN)
    f_inf = float32(numpy.Infinity)
    d_nan = float64(numpy.NaN)
    d_inf = float64(numpy.Infinity)
    #------------------------
    print isfinite(a)
    print isnan(a)
    print isinf(a)
    print isinf(a)
    print isinf(a)
    
    #----------------------------
    #  PATH_SEP function tests
    #----------------------------
    sep = os.sep
    
    #-----------------------------------------------
    #  PRINT procedure tests (with FORMAT keyword)
    #-----------------------------------------------
    print float32(3.14159), 'hello', 456
    I2PY_out_str = idl_func.string(float32(3.14159), 'hello', 456, format='(F6.3, A7, 4X, I3)')
    print I2PY_out_str
    I2PY_out_str = idl_func.string(float32(3.14159), float32(2.718), float32(1.000), 'hello', format='(3F6.3, A7)')
    print I2PY_out_str
    print 'my_string'
    print 'this ' + 'that'
    print 'this' + 'that'
    #-------------------------------------------------------
    #  Equals sign inside of quotes vs. keyword assignment
    #-------------------------------------------------------
    print 'path separator = ' + os.sep
    print "path separator = " + os.sep
    
    #-------------------------
    #  STRING function tests
    #-------------------------
    s = str(number)
    s = idl_func.string(number, format=format)   #;;;;;;;;;;;
    s = idl_func.string(float32(3.14159), 'hello', 456)
    s = idl_func.string(float32(3.14159), 'hello', 456, format='(F6.3, A7, 4X, I3)')
    #---------------------------------------
    #  Special behavior (not supported yet)
    #---------------------------------------
    s = idl_func.string()     #(should be a string array)
    s = str(uint8([72, 101, 108, 108, 111]))   #(should be "Hello")
    
    #-----------------------------------
    # Scalar constant assignment tests
    #-----------------------------------
    a = int16(1)      #In assignments, wrap ints with "int16()"
    a = int32(1)
    a = float32(1.0)
    a = float64(1)
    a = int64(1)
    a = uint64(1)
    a = uint32(1)
    a = uint8(1)
    
    #------------------
    # Structure tests
    #------------------
    v = idl_func.bunch(a=int32(0), b=uint8(0), c=float32(0.0), d=zeros([5], dtype='Int16'), e='this')  #(anonymous)
    V = idl_func.bunch(a=int32(0), b=uint8(0), c='this')  #(named)
    print v.__dict__.values()[0]      #(tag numbers or field indices)
    print v.__dict__.values()[1]
    #(Note:  Use "repeat" to "replicate" an IDL structure.)
    
    #-------------------------
    #  READF procedure tests
    #-------------------------
    a, b = idl_func.readf(file_1, a, b)
    a, b = idl_func.readf(file_unit, a, b)
    a, b = idl_func.readf(file_unit, a, b, format=('F8.3, I3'))
    
    #---------------------------------
    # "if (N_ELEMENTS(g) eq 0)" TEST
    #---------------------------------
    if (idl_func.n_elements(g) == 0):    
        g = int16(1)
    if (idl_func.n_elements(a_b) == 0):    
        a_b = int16(1)
    if (idl_func.n_elements(a + b) == 0):    
        c = int16(1)
    if (idl_func.n_elements(g) == 1):    
        g = int16(2)
    
    #------------------------------------------
    # OPENR procedure tests (and SWAP_ENDIAN)
    #------------------------------------------
    file_unit = open('my_file.bin', 'rb')
    I2PY_SWAP_ENDIAN = True
    file_unit = open('my_file.bin', 'rb')
    I2PY_SWAP_ENDIAN = True
    file_unit = open('my_file.bin', 'rb')
    I2PY_SWAP_ENDIAN = Not_Same_Byte_Order(byte_order)
    file_unit = open('my_file.txt', 'r')
    I2PY_SWAP_ENDIAN = False
    
    #------------------------------------------
    # OPENU procedure tests (and SWAP_ENDIAN)
    #------------------------------------------
    file_unit = open('my_file.bin', 'rb+')
    I2PY_SWAP_ENDIAN = True
    file_unit = open('my_file.bin', 'rb+')
    I2PY_SWAP_ENDIAN = True
    file_unit = open('my_file.bin', 'rb+')
    I2PY_SWAP_ENDIAN = Not_Same_Byte_Order(byte_order)
    file_unit = open('my_file.txt', 'r+')
    I2PY_SWAP_ENDIAN = False
    
    #------------------------------------------
    # OPENW procedure tests (and SWAP_ENDIAN)
    #------------------------------------------
    file_unit = open('my_file.bin', 'wb')
    I2PY_SWAP_ENDIAN = True
    file_unit = open('my_file.bin', 'wb')
    I2PY_SWAP_ENDIAN = True
    file_unit = open('my_file.bin', 'wb')
    I2PY_SWAP_ENDIAN = Not_Same_Byte_Order(byte_order)
    file_unit = open('my_file.txt', 'w')
    I2PY_SWAP_ENDIAN = False
    
    #-----------------------------
    #  MAKE_ARRAY function tests
    #-----------------------------
    a = reshape(arange(2*3, dtype='Float64'), [3, 2])
    a = zeros([10], dtype='UInt8')
    a = empty([10], dtype='Int16')
    
    #----------------------------------
    #  DIALOG_PICKFILE function tests
    #----------------------------------
    sav_file = []
    app = wx.PySimpleApp()
    I2PY_dialog = wx.FileDialog(parent=None, defaultDir=os.getcwd(), defaultFile='myfile.sav', style=wx.SAVE, wildcard='(*.sav)|*.sav')
    if (I2PY_dialog.ShowModal() == wx.ID_OK):
        sav_file.append(I2PY_dialog.GetPath())
    I2PY_dialog.Destroy()
    
    #-------------------------
    #  CASE statement tests
    #-------------------------
    I2PY_expr = a + b       #(an expression)
    if (I2PY_expr == 0):    
        value = int16(0)
    elif (I2PY_expr == 1):    
        value = int16(1)
    else:    
        value = int16(2)
    
    #--------------------------
    if (TYPE == 'THIS'):    
        value = int16(0)
    elif (TYPE == 'THAT'):    
        value = int16(1)
    else:    
        value = int16(2)
    
    #--------------------------
    if (result == 0):    
        value = int16(0)
    elif (result == 1):    
        value = int16(1)
    else:    
        value = int16(2)
    
    
    #---------------------------
    #  PTR_NEW function tests
    #---------------------------
    a = float64(1)
    a = b
    a = int32(0)
    
    #----------------------------
    #  GET_LUN procedure tests
    #----------------------------
    # Note: Removed unneeded GET_LUN call from here.
    # Note: Removed unneeded GET_LUN call from here.
    
    #--------------------------
    #  Special variable tests
    #--------------------------
    start = time.time()
    dpi = numpy.pi
    fpi = nympy.pi
    _in = int16(20)
    _in = int16(20)
    _pow = int16(30)
    TYPE = 'DOUBLE'
    TYPE = 'FLOAT'
    print str(TYPE)
    print str(1)
    
    #-----------------------
    #  BYTE function tests
    #--------------------------------
    #  Python has ord() and chr().
    #--------------------------------
    b = idl_func.byte(257)    # should be 1
    b = idl_func.byte('a')    # should be 97
    b = idl_func.byte('abc')  # should be [97, 98, 99]
    
    #-------------------------------------
    #  BYTE function test (special case)
    #-------------------------------------
    big_endian = (sys.byteorder == 'big')
    
    #-------------------------------
    #  ONLINE_HELP procedure tests
    #-------------------------------
    filepath = '/Applications/TopoFlow/help/about_TF.htm'
    result = webbrowser.open('file://' + filepath)
    result = webbrowser.open('file://' + filepath)
    result = webbrowser.open('file://' + 'some_help_file.htm')
    # online_help, /quit  ;(not supported yet)
    
    #---------------------
    #  For loop tests
    #--------------------
    for k in xrange(n, -1, -1):
        print k
    #-------------------------------
    for k in xrange(n):
        print k
    #-------------------------------
    for k in xrange(n):
        print k
    #-------------------------------
    for k in xrange(int32(0), n):
        print k
    
    #----------------
    # Pointer tests
    #----------------
    w = where(T_air != T_surf)
    nw = size(w[0])
    #------------------------------------------------
    (var)[i[j]:(i[j + 1] - 1)+1] = v_by_layer[j]
    n = idl_func.n_elements(v[k])
    A = v[k]
    v2 = vol + dt * ((R * da) - Q)
    #------------------------------------------------
    a = (T_air * 5) + T_surf
    b = (c * d)
    B = (C * d)
    b = (c * d)
    b = (1 * d)
    b = (d + c)
    b = (1 + 5)
    b = (5 * 1)
    
    #-----------------------
    #  SIZE function tests
    #-----------------------
    s = idl_func.size(A, dimensions=True)
    s = idl_func.size(a, n_elements=True)
    s = idl_func.size(a, n_dimensions=True)
    s = idl_func.size(a, TYPE=True)
    #----------------------------------------------
    s = idl_func.size(a)
    
    #---------------------------------
    #  LOGICAL OR, AND and NOT tests
    #---------------------------------
    print logical_or(0, 1)
    print logical_and(0, 1)
    DONE = uint8(0)
    if not(DONE):    
        print 'Not done.'
    a = int16([0, 1, 0])
    b = int16([1, 1, 0])
    print (logical_or(a, b))
    print (logical_and(a, b))
    print (logical_and(a, logical_not(b)))
    print (logical_or(a, logical_not(b)))
    print logical_not(a)   #([-1,-2,-1]; caution)
    if (0):    
        print 'Hello'
    if (1):    
        print 'Hello'
    print (3 < 5)   #(= 1 in IDL, = True in Python)
    print (3 > 5)   #(= 0 in IDL, = False in Python)
    
    #-------------------------
    #  PTRARR function tests
    #-------------------------
    #p = ptrarr(2,2)
    
    #-------------------------
    #  STRARR function tests
    #-------------------------
    s = zeros([2, 2], dtype='|S100')
    s = zeros([5], dtype='|S100') 
    s.fill('this')   #*** Use s.fill()
    
    #-----------------------
    #  TV procedure tests
    #-----------------------
    matplotlib.pyplot.imshow(image, origin='upper')
    matplotlib.pyplot.show()
    
    #--------------------------
    #  CONTOUR procedure tests
    #--------------------------
    matplotlib.pyplot.contour(z, 10)
    matplotlib.pyplot.show()
    matplotlib.pyplot.contour(z, float32([100.0, 200.0, 300.0]))
    matplotlib.pyplot.show()
    matplotlib.pyplot.contour(z, my_levels)
    matplotlib.pyplot.show()
    matplotlib.pyplot.contourf(x, y, z)
    matplotlib.pyplot.show()
    matplotlib.pyplot.contour(x, y, z, 20)
    matplotlib.pyplot.axis('equal')
    matplotlib.pyplot.show()
    
    #--------------------------
    #  SURFACE procedure tests
    #--------------------------
    fig = matplotlib.pylab.figure()
    ax  = matplotlib.axes3d.Axes3DI(fig)
    (nx, ny) = numpy.shape(z)
    xv = numpy.linspace(0,nx-1,nx)
    yv = numpy.linspace(0,ny-1,ny)
    (xgrid, ygrid) = numpy.meshgrid(xv, yv)
    ax.plot_wireframe(xgrid, ygrid, z)
    matplotlib.pylab.show()
    #-----------------------------------------
    fig = matplotlib.pylab.figure()
    ax  = matplotlib.axes3d.Axes3DI(fig)
    ax.plot_wireframe(x, y, z)
    matplotlib.pyplot.xlabel('X')
    matplotlib.pyplot.ylabel('Y')
    matplotlib.pylab.show()
    
    #------------------------------
    #  SHADE_SURF procedure tests
    #------------------------------
    fig = matplotlib.pylab.figure()
    ax  = matplotlib.axes3d.Axes3DI(fig)
    (nx, ny) = numpy.shape(z)
    xv = numpy.linspace(0,nx-1,nx)
    yv = numpy.linspace(0,ny-1,ny)
    (xgrid, ygrid) = numpy.meshgrid(xv, yv)
    ax.plot_surface(xgrid, ygrid, z)
    matplotlib.pylab.show()
    #--------------------------------------------
    fig = matplotlib.pylab.figure()
    ax  = matplotlib.axes3d.Axes3DI(fig)
    ax.plot_surface(x, y, z)
    matplotlib.pyplot.xlabel('X')
    matplotlib.pyplot.ylabel('Y')
    matplotlib.pylab.show()
    
    #--------------------------
    #  PRINTF procedure tests
    #--------------------------
    file_unit.write(a, 1, 2 + "\n")
    I2PY_out_str = idl_func.string(a, 1, format='(F8.3, I3)')
    file_unit.write(I2PY_out_str + "\n")
    
    #--------------------------
    #  Line continuation tests
    #--------------------------
    if (THIS):    
        do_this = int16(1)
    else:    
        do_that = int16(1)
    #--------------------------
    f = my_function(a, b, c, d, e)
    
    #-----------------------------
    #  FILE_CHMOD function tests
    #-----------------------------
    os.chmod('my_file',755)
    
    #-------------------------
    #  SPAWN procedure tests
    #-------------------------
    os.system('notepad')
    
    #---------------------
    #  CD function tests
    #---------------------
    os.chdir(newdir)
    os.chdir(newdir)
    olddir = os.getcwd()
    curdir = os.getcwd()
    
    #--------------------------
    #  XYOUTS procedure tests
    #--------------------------
    matplotlib.pyplot.text(float32(1.5), float32(2.0), 'Hello')
    matplotlib.pyplot.text(float32(1.5), float32(2.0), 'Hello', color='r')
    matplotlib.pyplot.text(float32(0.4), float32(0.6), 'Hello', transform=ax.transAxes)
    #xyouts, 'Hello'  ;(unsupported case)
    
    #------------------------------
    #  PLOT_FIELD procedure tests
    #------------------------------
    matplotlib.pyplot.quiver(u, v, scale=float32(0.1))
    matplotlib.pyplot.title('Arrows!')
    
    #------------------------
    #  PLOT procedure tests
    #------------------------
    matplotlib.pyplot.plot(y)
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(x, y)
    matplotlib.pyplot.axes(axisbg='w')
    matplotlib.pyplot.axes((0, 0, 1, 1))
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(x, y)
    matplotlib.pyplot.title('Long. Profile Plot')
    matplotlib.pyplot.xlabel('Distance [km]')
    matplotlib.pyplot.ylabel('Elevation [m]')
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(x, y)
    matplotlib.pyplot.axis('equal')
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(x, y, marker='+', markersize=float32(2.0))
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(x, y, marker='d', linestyle='None', markersize=float32(2.0))
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(x, y, marker='None', linestyle='None', markersize=float32(0.5))
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.polar(theta, r)
    matplotlib.pyplot.show()
    matplotlib.pyplot.loglog(x, y)
    matplotlib.pyplot.show()
    matplotlib.pyplot.semilogx(x, y)
    matplotlib.pyplot.show()
    matplotlib.pyplot.semilogy(x, y)
    matplotlib.pyplot.show()
    matplotlib.pyplot.semilogy(y, linewidth=2)
    matplotlib.pyplot.show()
    matplotlib.pyplot.plot(x, y, color='b', linestyle='-.')
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(x, y)
    matplotlib.pyplot.xticks(numpy.linspace(x.min(), x.max(), 5))
    matplotlib.pyplot.yticks(numpy.linspace(y.min(), y.max(), 10))
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(float32[1.1, 2, 3], float32[1.1, 2, 3])
    matplotlib.pyplot.axis('image')
    matplotlib.pyplot.show()
    #-------------------------------------------------
    matplotlib.pyplot.plot(float32[1.1, 2, 3], float32[1.1, 2, 3])
    matplotlib.pyplot.axis('image')
    matplotlib.pyplot.axis('off')
    matplotlib.pyplot.show()
    
    #-------------------------
    #  WINDOW function tests
    #-------------------------
    matplotlib.pyplot.figure(1, figsize=(8, 6), dpi=80)
    matplotlib.pyplot.show()
    matplotlib.pyplot.figure(2, figsize=(500/80.0, 6), dpi=80)
    matplotlib.pyplot.show()
    matplotlib.pyplot.figure(2, figsize=(500/80.0, 300/80.0), dpi=80)
    matplotlib.pyplot.show()
    matplotlib.pyplot.figure(2, figsize=(nx/80.0, ny/80.0), dpi=80)
    matplotlib.pyplot.show()
    matplotlib.pyplot.figure(2, figsize=(8, 6), dpi=80)
    matplotlib.pyplot.show()
    matplotlib.pyplot.figure(2, figsize=(8, 6), dpi=80)
    matplotlib.pyplot.show()
    
    #--------------------------
    #  WDELETE function tests
    #--------------------------
    matplotlib.pyplot.close(1)
    matplotlib.pyplot.close(2)
    matplotlib.pyplot.close(3)
    matplotlib.pyplot.close(4)
    matplotlib.pyplot.close(n+1)
    
    #-----------------------
    #  WSET function tests
    #-----------------------
    matplotlib.pyplot.figure(1)
    matplotlib.pyplot.figure(2)
    matplotlib.pyplot.figure(n+1)
    
    #-------------------------
    #  BYTSCL function tests
    #-------------------------
    b = ((255 + 1) * (a - a.min()) - 1) / (a.max() - a.min())
    b = ((top + 1) * (a - amin) - 1) / (amax - amin)
    
    #--------------------------
    #  RANDOMN function tests
    #--------------------------
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = random.normal(loc=0.0, scale=1.0, size=None)
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = random.normal(loc=0.0, scale=1.0, size=(10))
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = random.normal(loc=0.0, scale=1.0, size=(4, 3))
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = random.binomial(5, 0.3, size=(4, 3))
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = random.gamma(scale=float32(2.0), size=(4, 3))
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = random.normal(loc=0.0, scale=1.0, size=(4, 3))
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = random.poisson(lam=float32(2.3), size=(4, 3))
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = random.uniform(low=0.0, high=1.0, size=(4, 3))
    #-----------------------------------------------
    if ('seed1' in locals()): numpy.random.seed(seed1)
    a = -5 + (random.uniform(low=0.0, high=1.0, size=(4, 3)) * 10)
    
    #--------------------------
    #  RANDOMU function tests
    #--------------------------
    #similar
    
    #--------------------------
    #  REFORM function tests
    #--------------------------
    #  NumPy also has SQUEEZE
    #--------------------------
    a = arange(24, dtype='Int16')
    b = reshape(a, [4, 6])  #(note reverse indices)
    c = reshape(b, [24])
    #-----------------------
    a = arange(24 * 3, dtype='Int16')
    b = reshape(a, [3, 4, 6])
    
    #-------------------------------------
    #  ROTATE and REVERSE function tests
    #-------------------------------------
    a = reshape(arange(3*4, dtype='Int16'), [4, 3])
    b = transpose(a)
    #-----------------
    b = a
    b = rot90(a, -1)
    b = rot90(a, -2)  ## Use FLIPUD to reverse 1D arrays
    b = rot90(a, -3)
    b = transpose(a)   #(same as transpose)
    b = fliplr(a)   #(flip x-axis)
    b = transpose(rot90(a, 2))
    b = flipud(a)   #(flip y-axis)
    #----------------
    a = arange(4, dtype='Int16')
    b = flipud(a)
    
    #--------------------------
    #  EXECUTE function tests
    #--------------------------
    a = 1  # (EXEC has no return value)
    exec("print, 'Hello'")
    a = 1  # (EXEC has no return value)
    exec("print, 'Hello' ;  a=1  ;  print, 'a =', a")   #(multiple statements)
    
    #------------------------
    #  SHIFT function tests
    #------------------------
    a = arange(5, dtype='Int16')     #[0,1,2,3,4]
    b = numpy.roll(a, 1, axis=0)   #[4,0,1,2,3]
    b = numpy.roll(a, -1, axis=0)  #[1,2,3,4,0]
    #--------------------------------------
    #  Note that array axes are reversed
    #--------------------------------------
    a = reshape(arange(3*4, dtype='Int16'), [4, 3])
    b = numpy.roll(a, 1, axis=1)
    b = numpy.roll(a, -1, axis=1)
    c = numpy.roll(a, 1, axis=0)
    c = numpy.roll(a, -1, axis=0)
    c = numpy.roll(numpy.roll(a, -1, axis=0), 1, axis=1)
    #--------------------------------------
    #   These 3D cases need more testing
    #--------------------------------------
    a = reshape(arange(3*4*5, dtype='Int16'), [5, 4, 3])
    c = numpy.roll(a, 1, axis=2)
    c = numpy.roll(a, 1, axis=1)
    c = numpy.roll(a, 1, axis=0)
    c = numpy.roll(numpy.roll(numpy.roll(a, 3, axis=0), 2, axis=1), 1, axis=2)   #(this case works)
    
    #---------------------------
    # REPLICATE function tests
    #---------------------------
    a = repeat('-',10)
    a = repeat(5,10)
    a = repeat(structure,10)
    
    #-----------------------
    # Array indexing tests
    #-----------------------
    print a[0:6]  #(note upper limit is adjusted)
    print a[0,:]  #(note reversed indices)
    
    #----------------------
    #  IF statement tests
    #----------------------
    if a < 5:    
        print 'a is smaller than 5'
    if (a < 5):    
        print 'a is smaller than 5'
    else:    
        print 'a is GE 5'
    
    #-----------------------
    # TOTAL function tests
    #-----------------------
    a = sum(b)
    a = sum(double(b))
    a = cumsum(b)
    a = cumsum(b)
    a = cumsum(double(b))
    a = cumsum(double(b))
    a = nansum(double(b))
    a = nansum(b)
    a = cumsum(nan_to_num(b))   #(there is no "nancumsum")
    
    #---------------------------
    # Deliberate casting tests
    #---------------------------
    a = uint8(0)
    a = int32(0)
    a = float64(0)
    a = float32(0.0)
    a = int64(0)
    a = uint16(0)
    a = uint64(0)
    a = 0x15
    
    #----------------------------
    # POINT_LUN procedure tests
    #----------------------------
    file_unit.seek((nx * 5))     #(set position)
    pos = file_2.tell()            #(return position)
    pos = file_unit.tell()   #(return position)
    
    #------------------------
    #  FSTAT function tests
    #------------------------
    file_unit1 = open('my_filename.txt', 'r')
    I2PY_SWAP_ENDIAN = False
    temp = idl_func.fstat(file_unit1)
    filesize = temp.size
    file_unit1.close()
    
    #----------------
    # File I/O tests
    #----------------
    file_unit = open('my_filename.txt', 'rb')
    I2PY_SWAP_ENDIAN = True
    a = zeros([5, 5], dtype='Int16')
    I2PY_shape = a.shape
    I2PY_dtype = str(a.dtype)
    a = fromfile(file_unit, count=size(a), dtype=I2PY_dtype)
    a = reshape(a, I2PY_shape)
    if (I2PY_SWAP_ENDIAN):
        array(a, copy=0).byteswap(True)
    
    #---------------------------------------
    #  CLOSE and FREE_LUN procedure tests
    #---------------------------------------
    file_3.close()
    file_unit.close()
    file_unit1.close()
    file_unit2.close()
    #------------------------
    file_3.close()
    file_unit.close()
    file_unit1.close()
    file_unit2.close()
    file_unit3.close()
    
    #--------------------------------
    #  FILE_DELETE procedure tests
    #--------------------------------
    idl_func.file_delete('dirname/my_filename.txt')
    a = '/dir1/dir2/my_file.txt'
    idl_func.file_delete(a)
    idl_func.file_delete(a, b, c)
    
    #-----------------------------
    #  FILE_TEST function tests
    #-----------------------------
    exists = os.path.exists('dirname/my_filename.txt')
    
    #---------------------
    # EOF function tests
    #---------------------
    while not(idl_func.eof(file_unit)):
        I2PY_shape = a.shape
        I2PY_dtype = str(a.dtype)
        a = fromfile(file_unit, count=size(a), dtype=I2PY_dtype)
        a = reshape(a, I2PY_shape)
        if (I2PY_SWAP_ENDIAN):
            array(a, copy=0).byteswap(True)
    
    #-------------------------
    #  Type conversion tests
    #-------------------------
    a = arange(5, dtype='Int16')
    a = float32(a)
    g = idl_func.byte(257)   #should be 1.  ( Python has ord() and chr(). )
    g = int16(float32(1.5))    #should be 1
    g = float32(1)    #should be 1.0
    
    #-------------------------------
    #  Array initialization tests
    #-------------------------------
    B_arr = zeros([5], dtype='UInt8')
    I_arr = zeros([5, 3], dtype='Int16')   #(note reversed indices)
    L_arr = zeros([5], dtype='Int32')
    F_arr = zeros([5], dtype='Float32')
    D_arr = zeros([5], dtype='Float64')
    #-----------------------------
    B_arr = empty([5], dtype='UInt8')
    I_arr = empty([5, 3], dtype='Int16')
    L_arr = empty([5], dtype='Int32')
    F_arr = empty([5], dtype='Float32')
    D_arr = empty([5], dtype='Float32')
    
    #----------------------
    #  Array "ramp" tests
    #----------------------
    a = arange(5, dtype='Float32')
    a = reshape(arange(3*5, dtype='Float32'), [5, 3])
    a = reshape(arange(3*5*8, dtype='Float32'), [8, 5, 3])
    a = arange(5, dtype='UInt8')
    a = arange(5, dtype='Int16')
    a = arange(5, dtype='Int32')
    a = arange(5, dtype='Float64')
    
    #------------------------------
    #  MIN and MAX function tests
    #------------------------------
    amin = a.min()
    #------------------------
    amin = a.min()
    amin_sub = a.argmin()
    #------------------------
    amin = a.min()
    amin_sub = a.argmin()
    amax = a.max()
    #------------------------
    amin = a.min()
    amin_sub = a.argmin()
    amax = a.max()
    amax_sub = a.argmax()
    #------------------------
    amin = a.min()
    amin_sub = a.argmin()
    amax = a.max()
    amax_sub = a.argmax()
    #------------------------
    amax = a.max()
    #------------------------
    amax = a.max()
    amax_sub = a.argmax()
    amin = a.min()
    amin_sub = a.argmin()
    #------------------------
    amax = a.max()
    amax_sub = a.argmax()
    amin = a.min()
    amin_sub = a.argmin()
    
    #------------------------
    #  WHERE function tests
    #------------------------
    a[where(a < 0)] = int16(0)
    #----------------------------------------
    a[where(a < 0)
    wc = where(invert(a < 0))
    nc = size(wc[0])] = int16(0)    #(doesn't work yet)
    #----------------------------------------
    w = where(a < 10)
    #--------------------------
    w = where(a < 10)
    nw = size(w[0])
    #--------------------------
    w = where(a < 10)
    nw = size(w[0])
    wc = where(invert(a < 10))
    nc = size(wc[0])
    #-------------------------------------------
    # These have arguments with an equals sign
    #-------------------------------------------
    w = where(a == 10)
    w = where(a <= 10)
    w = where(a >= 10)
    w = where(a != 10)
    #-------------------------
    # "Nested" WHERE example
    #-------------------------
    a = reshape(arange(4*4, dtype='Int16'), [4, 4]) - 8
    w1 = where(a < 0)
    w2 = where(a[w1] > -3)
    a[w1[w2]] = int16(99)
    
    #-----------------------
    #  ATAN function tests
    #-----------------------
    a = arctan(x)
    a = arctan2(x,y)
    
    #---------------------------
    #  STRSPLIT function tests
    #---------------------------
    s = ' Parse this sentence.'
    words = s.split()
    words = s.split()
    words = s.split()
    my_count = len(words)
    words = s.split()
    my_length = map(len, words)
    #-------------------------------------
    indices = [j for j in xrange(len(s)) if (ord(s[j]) > 32) and ((j==0) or ((j>0) and (ord(s[j-1]) < 33)))]
    indices = [j for j in xrange(len(s)) if (ord(s[j]) > 32) and ((j==0) or ((j>0) and (ord(s[j-1]) < 33)))]
    s.split()
    my_count = len(indices)
    my_length = map(len, indices)
    #-------------------------------------
    dstr = '1,2,3,4,5,'
    data = dstr.split(',')
    indices = [j for j in xrange(len(dstr)) if (dstr[j] not in ',') and ((j==0) or ((j>0) and (dstr[j-1] in ',')))]
    
    #---------------------------
    #  STRTRIM function tests
    #---------------------------
    name = '   Scott   '.rstrip()
    name = '   Scott   '.rstrip()
    name = '   Scott   '.lstrip()
    name = '   Scott   '.strip()
    name = '   Scott   '.rstrip()
    
    #-----------------------------
    #  String manipulation tests
    #-----------------------------
    word = s[4:4+3]
    word = 'the red fox'[4:4+3]   #(should be 'red')
    s = 'the red fox'
    s = (s[:8] + 'dog' + s[8+len('dog'):])[:len(s)]
    s = ('dog' + s[len('dog'):])[:len(s)]
    _len = len('this')
    name = 'Scott'.upper()
    name = 'Scott'.lower()
    print 'path separator = ' + os.sep
    
    
#  Test_Procedure
#*******************************************************************


