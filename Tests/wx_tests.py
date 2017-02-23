from numpy import *

import wx, os

import numpy


#*******************************************************************
#   wx_tests.pro

#   Author:   Dr. Scott D. Peckham, INSTAAR, Univ. of Colorado

#   Created:  Nov. 11, 2008

#*******************************************************************
def Pickfile_Test(OPEN_TEST=False):

#----------------------------------------------------------------
#Notes:  This procedure is for testing how well I2PY converts
#        the DIALOG_PICKFILE function.  The MULTIPLE_FILES
#        option is not yet working.
#----------------------------------------------------------------
#        Keyword references must be consistent with regard to
#        case (i.e. upper or lower).
#----------------------------------------------------------------
#        First line gets converted to:
#           OPEN_TEST = (OPEN_TEST is not None).
#        However, note that (True is not None) equals True, and
#           (False is not None) is also True.
#----------------------------------------------------------------
    n_params = 0
    _opt = (OPEN_TEST,)
    def _ret():
        _optrv = zip(_opt, [OPEN_TEST])
        _rv = [_o[1] for _o in _optrv if _o[0] is not None]
        return tuple(_rv)
    
    OPEN_TEST = (OPEN_TEST is not False)
    
    if (OPEN_TEST):    
        #---------------------------
        # Choose file to open/read
        #---------------------------
        sav_file = I2PY_filepath = []
        app = wx.PySimpleApp()
        I2PY_dialog = wx.FileDialog(parent=None, defaultDir=os.getcwd(), defaultFile='myfile.txt', style=wx.OPEN | wx.MULTIPLE, wildcard='(*.*)|*.*')
        if (I2PY_dialog.ShowModal() == wx.ID_OK):
            I2PY_filepath.append(I2PY_dialog.GetPath())
        I2PY_dialog.Destroy()
    else:    
        #----------------------------
        # Choose file to save/write
        #----------------------------
        sav_file = I2PY_filepath = []
        app = wx.PySimpleApp()
        I2PY_dialog = wx.FileDialog(parent=None, defaultDir=os.getcwd(), defaultFile='myfile.sav', style=wx.SAVE, wildcard='(*.sav)|*.sav')
        if (I2PY_dialog.ShowModal() == wx.ID_OK):
            I2PY_filepath.append(I2PY_dialog.GetPath())
        I2PY_dialog.Destroy()
    
    print sav_file
    
    
    return _ret()
#  Pickfile_Test
#*******************************************************************
