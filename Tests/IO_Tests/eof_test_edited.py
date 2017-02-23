from numpy import *

import os

import numpy


#*******************************************************************
#   eof_test.pro

#   Author:   Dr. Scott D. Peckham, INSTAAR, Univ. of Colorado

#   Created:  October 16, 2008

#*******************************************************************
def eof_test():

    n_params = 0
    def _ret():  return None
    
    data_file = 'EOF_TEST_DATA.bin'
    unit = 5
    
    os.chdir('/Users/peckhams/Desktop/Python_TopoFlow/i2py-0.2.0/SDP')
    a = reshape(arange(10*10, dtype='Int32'), [10, 10])
    file_unit = open(data_file, 'wb')
    a.tofile(file_unit)
    file_unit.close()
    b = zeros([10], dtype='Int32')
    
    file_unit = open(data_file, 'rb')
    while bitwise_not((file_unit.tell() == os.path.getsize(file_unit.name))):
    # while (True):
        b = fromfile(file_unit, count=size(b), dtype=str(b.dtype))
        # if (len(b)==0): break
        print b
    file_unit.close()
    
    
    return _ret()
#  EOF_Test
#*******************************************************************
