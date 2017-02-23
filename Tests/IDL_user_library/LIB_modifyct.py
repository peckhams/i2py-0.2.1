from numarray import *

# $Id: modifyct.pro,v 1.14 2003/02/03 18:13:21 scottm Exp $

#

# Copyright (c) 1982-2003, Research Systems, Inc.  All rights reserved.

#       Unauthorized reproduction prohibited.



def modifyct(itab, name, r, g, b, file=None):	#MODIFY COLOR TABLE IN FILE

#+

# NAME:

#	MODIFYCT

#

# PURPOSE:

#	Update the distribution color table file "colors1.tbl" or the

#	user-supplied file with a new table.

#

# CATEGORY:

#	Z4 - Image processing, color table manipulation.

#

# CALLING SEQUENCE:

#	MODIFYCT, Itab, Name, R, G, B

#

# INPUTS:

#	Itab:	The table to be updated, numbered from 0 to 255.  If the

#		table entry is greater than the next available location

#		in the table, then the entry will be added to the table

#		in the available location rather than the index specified

#		by Itab.  On return, Itab will contain the index for the

#		location that was modified or extended.  The table

#		can be loaded with the IDL command:  LOADCT, Itab.

#

#	Name:	A string up to 32 characters long that contains the name for

#		the new color table.

#

#	R:	A 256-element vector that contains the values for the red

#		color gun.

#

#	G:	A 256-element vector that contains the values for the green

#		color gun.

#

#	B:	A 256-element vector that contains the values for the blue

#		color gun.

#

# KEYWORD PARAMETERS:

#	FILE:	If this keyword is set, the file by the given name is used

#		instead of the file colors1.tbl in the IDL directory.  This

#		allows multiple IDL users to have their own color table file.

#		The file specified must be a copy of the colors1.tbl file.

#		The file must exist.

#

# OUTPUTS:

#	Itab:	The index of the entry which was updated, 0 to 255.  This

#		may be different from the input value of Itab if the

#		input value was greater than the next available location

#		in the table.  If this was the case the entry was added to

#		the table in the next available location instead of leaving

#		a gap in the table.

#

# COMMON BLOCKS:

#	None.

#

# SIDE EFFECTS:

#	The distribution file "colors.tbl1" or the user-supplied file is

#	modified with the new table.

#

# PROCEDURE:

#	Straightforward.

#

# MODIFICATION HISTORY:

#	Aug, 1982, DMS, Written.

#	Unix version, 1987, DMS.

#	ACY, 9/92, Update for new color table structure, Add FILE keyword.

#		   Allow extending table.

#	WSO, 1/95, Updated for new directory structure

#

#-

   n_params = 5
   _opt = (file,)
   def _ret():
      _optrv = zip(_opt, [file])
      _rv = [itab, name, r, g, b]
      _rv += [_o[1] for _o in _optrv if _o[0] is not None]
      return tuple(_rv)
   
   # COMPILE_OPT STRICTARR
   
   
   
   # ON_IOERROR, BAD
   
   # ON_ERROR, 2                    #Return to caller if an error occurs
   
   if (lmgr(demo=True)):   
      
      message('OPENU: Feature disabled for demo mode.')
      
      return _ret()
      
   
   if bitwise_or((itab < 0), (itab > 255)):   
      message('Color table number out of range.')
   
   
   
   if (array(file, copy=0).nelements() > 0):   
      filename = file
   else:   
      filename = filepath('colors1.tbl', subdir=concatenate(['resource', 'colors']))
   
   
   
   get_lun(iunit)		#GET A LOGICAL UNIT
   
   openu(iunit, filename, block=True)  #OPEN FILE
   
   ntables = 0
   
   readu(iunit, ntables)
   
   
   
   if (itab < ntables):   	# Update an existing record
      
      aa = assoc(iunit, bytarr(32, ntables), ntables * 768 + 1)	#UPDATE NAME RECORD.
      
      a = aa[0]
      
      a[itab,:] = 32			#blank out old name
      
      a[itab,0:(strlen(name) - 1)+1] = byte(name)
      
      aa[0] = a				#Write names out
      
      
      
      aa = assoc(iunit, bytarr(256), 1)	#UPDATE VECTORS. SKIP PAST COUNT
      
      aa[itab * 3] = byte(r)		#PUT IN RED. GUARANTEE BYTE
      
      aa[itab * 3 + 1] = byte(g)		#GREEN IN 2ND BLOCK
      
      aa[itab * 3 + 2] = byte(b)		#BLUE IN 3RD BLOCK
      
      
      
   else:   			# Add a new record at the end of table
      
      itab = ntables
      
      # Add new vectors.  First, read names, then insert vectors
      
      aa = assoc(iunit, bytarr(32, ntables), ntables * 768 + 1) #UPDATE NAME RECORD.
      
      a = aa[0]
      
      # Skip past old vectors
      
      aa = assoc(iunit, bytarr(256), ntables * 768 + 1)      #UPDATE VECTORS
      
      aa[0] = byte(r)             #PUT IN RED. GUARANTEE BYTE
      
      aa[1] = byte(g)             #GREEN IN 2ND BLOCK
      
      aa[2] = byte(b)             #BLUE IN 3RD BLOCK
      
      
      
      # Skip past new vector to put in names
      
      aa = assoc(iunit, bytarr(32, ntables + 1), (ntables + 1) * 768 + 1)
      
      # Add new name to end
      
      temp = bytarr(32) + 32
      
      temp[0:(strlen(name) - 1)+1] = byte(name)
      
      allnames = bytarr(32, ntables + 1)
      
      allnames[0:(ntables - 1)+1,:] = a
      
      allnames[ntables,:] = temp
      
      aa[0] = allnames		# write the names out
      
      
      
      # Update count
      
      aa = assoc(iunit, bytarr(1))
      
      aa[0] = concatenate([ntables + 1])
      
   
   
   
   #GOTO, close_file
   free_lun(iunit)  ;  return _ret()
   
   
   
   # bad:
   
   #MESSAGE, /CONTINUE, 'Error writing file: ' + filename + ', ' + !ERROR_STATE.msg
   print 'Error writing file: ' + filename + ', ' + _sys_error_state.msg
   
   
   #close_file:
   
   #  FREE_LUN,IUNIT
   
   #  RETURN
   
   
   return _ret()

