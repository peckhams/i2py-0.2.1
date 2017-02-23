import numpy

def write_test(filename):
    _dir = '/Users/peckhams/Desktop/'
    a = numpy.arange(64, dtype='int32')
    a.tofile(_dir + filename)

def read_test(filename):
    _dir = '/Users/peckhams/Desktop/'
    file_obj = open(_dir + filename, 'rb')
    a = numpy.fromfile(file_obj, count=64, dtype='int32')
    file_obj.close()
    print a

def write_test_text(filename):
    _dir = '/Users/peckhams/Desktop/'
    file_obj = open(_dir + filename, 'w')
    a = numpy.arange(64, dtype='int32')
    #------------------------
    # Converts to binary
    #------------------------
    # s = a.tostring()
    # print s
    #------------------------
    s = str(a)
    print s
    s = s.replace('[','')
    s = s.replace(']','')
    #------------------------
    # s = repr(a)
    # print s
    #------------------------    
    file_obj.write(s)
    # file_obj.write(s)
    file_obj.close()

def read_test_text(filename):
    _dir = '/Users/peckhams/Desktop/'
    file_obj = open(_dir + filename, 'r')
    s = file_obj.read()
    #print s
    a = numpy.fromstring(s, dtype='int32', count=64, sep=' ')
    a = numpy.reshape(a, (8,8))
    print a
