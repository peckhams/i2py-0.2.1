from numarray import *

# $Id: loadct.pro,v 1.19 2003/02/03 18:13:19 scottm Exp $

#

# Copyright (c) 1982-2003, Research Systems, Inc.  All rights reserved.

#       Unauthorized reproduction prohibited.



def loadct(table_number, silent=None, get_names=None, file=None, ncolors=None, bottom=None):
   """
   
    NAME:
   
   	LOADCT
   
   
   
    PURPOSE:
   
   	Load predefined color tables.
   
   
   
    CATEGORY:
   
   	Image display.
   
   
   
    CALLING SEQUENCE:
   
   	LOADCT [, Table]
   
   
   
    OPTIONAL INPUTS:
   
   	Table:	The number of the pre-defined color table to load, from 0
   
   		to 15.  If this value is omitted, a menu of the available
   
   		tables is printed and the user is prompted to enter a table
   
   		number.
   
   
   
    KEYWORD PARAMETERS:
   
   	FILE:	If this keyword is set, the file by the given name is used
   
   		instead of the file colors1.tbl in the IDL directory.  This
   
   		allows multiple IDL users to have their own color table file.
   
   		The specified file must exist.
   
   	GET_NAMES: If this keyword is present AND DEFINED, the names
   
   		of the color tables are returned as a string array.
   
   		No changes are made to the color table.
   
   	NCOLORS = number of colors to use.  Use color indices from 0
   
   		to the smaller of !D.TABLE_SIZE-1 and NCOLORS-1.
   
   		Default = !D.TABLE_SIZE = all available colors.
   
   	SILENT:	If this keyword is set, the Color Table message is suppressed.
   
   	BOTTOM = first color index to use. Use color indices from BOTTOM to
   
   		BOTTOM+NCOLORS-1.  Default = 0.
   
   
   
    OUTPUTS:
   
   	No explicit outputs.
   
   
   
    COMMON BLOCKS:
   
   	COLORS:	The IDL color common block.
   
   
   
    SIDE EFFECTS:
   
   	The color tables of the currently-selected device are modified.
   
   
   
    RESTRICTIONS:
   
   	Works from the file: $IDL_DIR/resource/colors/colors1.tbl or the file specified
   
   	with the FILE keyword.
   
   
   
    PROCEDURE:
   
   	The file "colors1.tbl" or the user-supplied file is read.  If
   
          the currently selected device doesn't have 256 colors, the color
   
   	data is interpolated from 256 colors to the number of colors
   
   	available.
   
   
   
   	The colors loaded into the display are saved in the common
   
   	block COLORS, as both the current and original color vectors.
   
   
   
   	Interpolation:  If the current device has less than 256 colors,
   
   	the color table data is interpolated to cover the number of
   
   	colors in the device.
   
   
   
    MODIFICATION HISTORY:
   
   	Old.  For a widgetized version of this routine, see XLOADCT in the IDL
   
   		widget library.
   
   	DMS, 7/92, Added new color table format providing for more than
   
   		16 tables.  Now uses file colors1.tbl.  Old LOADCT procedure
   
   		is now OLD_LOADCT.
   
   	ACY, 9/92, Make a pixmap if no windows exist for X windows to
   
   		determine properly the number of available colors.
   
   		Add FILE keyword.
   
   	WSO, 1/95, Updated for new directory structure
   
   	AB, 10/3/95, The number of entries in the COLORS common block is
   
   		now always !D.TABLE_SIZE instead of NCOLORS + BOTTOM as
   
   		before. This better reflects the true state of the device and
   
   		works with other color manipulations routines.
   
          DLD, 09/98, Avoid repeating a color table name in the printed list.
   
   
   
   """

   n_params = 1
   rnames = get_names
   nc1 = ncolors
   _opt = (silent, rnames, file, nc1, bottom)
   def _ret():
      _optrv = zip(_opt, [silent, rnames, file, nc1, bottom])
      _rv = [table_number]
      _rv += [_o[1] for _o in _optrv if _o[0] is not None]
      return tuple(_rv)
   
   global r_orig, g_orig, b_orig, r_curr, g_curr, b_curr
   
   
   
   
   
   # ON_IOERROR, BAD
   
   # ON_ERROR, 2		#Return to caller if error
   
   get_lun(lun)
   
   
   
   if bitwise_and(_sys_d.name == 'X', _sys_d.window == -1):     #Uninitialized?
      
      #	If so, make a dummy window to determine the # of colors available.
      
      window(free=True, pixmap=True, xs=4, ys=4)
      
      wdelete(_sys_d.window)
      
   
   
   
   if array(bottom, copy=0).nelements() > 0:   
      cbot = minimum(maximum(bottom, 0), (_sys_d.table_size - 1))
   else:   
      cbot = 0
   
   nc = _sys_d.table_size - cbot
   
   if array(nc1, copy=0).nelements() > 0:   
      nc = minimum(nc, nc1)
   
   
   
   if nc == 0:   
      message('Device has static color tables.  Cannot load.')
   
   
   
   if (array(file, copy=0).nelements() > 0):   
      filename = file
   else:   
      filename = filepath('colors1.tbl', subdir=concatenate(['resource', 'colors']))
   
   
   
   openr(lun, filename, block=True)
   
   
   
   ntables = 0
   
   readu(lun, ntables)
   
   
   
   if bitwise_or(bitwise_or((n_params == 0), (arg_present(rnames) >= 1)), (bitwise_not((silent is not None)))):   
      
      names = bytarr(32, ntables)
      
      point_lun(lun, ntables * 768 + 1)	#Read table names
      
      readu(lun, names)
      
      names = strtrim(names, 2)
      
   
   
   
   if arg_present(rnames) >= 1:   	#Return names?
      
      rnames = names
      
      #goto, close_file
      free_lun(lun)  ;  return _ret()
      
   
   
   
   if n_params < 1:   	#Summarize table?
      
      nlines = (ntables + 2) / 3	## of lines to print
      
      nend = nlines - ((nlines * 3) - ntables)
      
      for i in arange(0, (nend - 1)+(1)):
         print i, names[i], i + nlines, names[i + nlines], minimum(i + 2 * nlines, (ntables - 1)), names[minimum(i + 2 * nlines, (ntables - 1))], format="(i2,'- ',a17, 3x, i2,'- ',a17, 3x, i2,'- ',a17)"
      
      if (nend < nlines):   
         
         for i in arange(nend, (nlines - 1)+(1)):
            print i, names[i], i + nlines, names[i + nlines], format="(i2,'- ',a17, 3x, i2,'- ',a17)"
         
      
      
      
      table_number = 0
      
      read(table_number, prompt='Enter table number: ')
      
   
   
   
   if bitwise_or((table_number >= ntables), (table_number < 0)):   
      
      message('Table number must be from 0 to ' + strtrim(ntables - 1, 2))
      
   
   
   
   
   
   if array(r_orig, copy=0).nelements() < _sys_d.table_size:   	#Tables defined?
      
      r_orig = bytscl(indgen(_sys_d.table_size))
      
      g_orig = r_orig
      
      b_orig = r_orig
      
   
   
   
   
   
   if (silent is not None) == 0:   
      message('Loading table ' + names[table_number], info=True)
   
   aa = assoc(lun, bytarr(256), 1)	#Read 256 long ints
   
   r = aa[table_number * 3]
   
   g = aa[table_number * 3 + 1]
   
   b = aa[table_number * 3 + 2]
   
   
   
   if nc != 256:   	#Interpolate
      
      p = (lindgen(nc) * 255) / (nc - 1)
      
      r = r[p]
      
      g = g[p]
      
      b = b[p]
      
   
   
   
   r_orig[cbot] = r
   
   g_orig[cbot] = g
   
   b_orig[cbot] = b
   
   r_curr = r_orig
   
   g_curr = g_orig
   
   b_curr = b_orig
   
   tvlct(r, g, b, cbot)
   
   #goto, close_file
   free_lun(lun)  ;  return _ret()
   
   
   
   # bad:
   
   #message, /CONTINUE, 'Error reading file: ' + filename + ', ' + ! error_state.msg
   print 'Error reading file: ' + filename + ', ' + _sys_error_state.msg
   
   
   #close_file:
   
   #  free_lun,lun
   
   #  return
   
   
   return _ret()

