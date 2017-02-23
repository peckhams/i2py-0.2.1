from numpy import *

import os

import numpy


#*******************************************************************
#   eof_test.pro

#   Author:   Dr. Scott D. Peckham, INSTAAR, Univ. of Colorado

#   Created:  October 16, 2008

#*******************************************************************
def eof_test():

#-------------------------------------------------------------------
#Notes:  This works, but the "Python way" is to use "while (True):"
#        and then something like "if len(data == 0): break" inside
#        the loop.  i2py now prints a warning explaining this.
#-------------------------------------------------------------------
    n_params = 0
    def _ret():  return None
    
    data_file = 'EOF_TEST_DATA.bin'
    unit = 5
    
    os.chdir('/Users/peckhams/Desktop/Python_TopoFlow/i2py-0.2.0/SDP')
    a = reshape(arange(10*10, dtype='Int32'), [10, 10])
    file_unit = open(data_file, 'wb')
    I2PY_SWAP_ENDIAN = False
    I2PY_GET_LUN = False
    if (I2PY_SWAP_ENDIAN):
        array(a, copy=0).byteswap(True)
    a.tofile(file_unit)
    file_unit.close()
    b = zeros([10], dtype='Int32')
    
    file_unit = open(data_file, 'rb')
    I2PY_SWAP_ENDIAN = False
    I2PY_GET_LUN = False
    while bitwise_not((file_unit.tell() == os.path.getsize(file_unit.name))):
        b = fromfile(file_unit, count=size(b), dtype=str(b.dtype))
        if (I2PY_SWAP_ENDIAN):
            array(b, copy=0).byteswap(True)
        print b
    file_unit.close()
    
    
    return _ret()
#  EOF_Test
#*******************************************************************
