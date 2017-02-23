from numarray import *

# $Id: filepath.pro,v 1.30 2003/02/03 18:13:13 scottm Exp $

#

# Copyright (c) 1989-2003, Research Systems, Inc.  All rights reserved.

#	Unauthorized reproduction prohibited.

#



def filepath(filename, root_dir=None, subdirectory=None, terminal=None, tmp=None):
   """
   
    NAME:
   
   	FILEPATH
   
   
   
    PURPOSE:
   
   	Given the name of a file in the IDL distribution,
   
   	FILEPATH returns the fully-qualified path to use in
   
   	opening the file. Operating system dependencies
   
   	are taken into consideration. This routine is used by RSI to
   
   	make the User Library portable.
   
   
   
    CATEGORY:
   
   	File Management.
   
   
   
    CALLING SEQUENCE:
   
   	Result = FILEPATH('filename' [, SUBDIRECTORY = subdir])
   
   
   
    INPUTS:
   
       filename:	The lowercase name of the file to be opened. No device
   
   		or directory information should be included.
   
   
   
    KEYWORDS:
   
       ROOT_DIR: The name of the directory from which the resulting path
   
   	should be based. If not present, the value of !DIR is used.
   
   	This keyword is ignored if TERMINAL or TMP are specified.
   
   
   
       SUBDIRECTORY:	The name of the subdirectory in which the file
   
   		should be found. If this keyword is omitted, the main
   
   		directory is used.  This variable can be either a scalar
   
   		string or a string array with the name of each level of
   
   		subdirectory depth represented as an element of the array.
   
   
   
       TERMINAL:	Return the filename of the user's terminal.
   
   
   
       TMP:	The file is a scratch file.  Return a path to the
   
   		proper place for temporary files under the current operating
   
   		system.
   
   
   
    OUTPUTS:
   
   	The fully-qualified file path is returned.  If one of the subdirectory
   
   	keywords is not specified, the file is assumed to exist in the
   
   	main distribution directory.
   
   
   
    COMMON BLOCKS:
   
   	None.
   
   
   
    RESTRICTIONS:
   
   	ROOT_DIR, TERMINAL, and TMP are mutually exclusive. Only one of
   
   	these should be used in a single call to FILEPATH. SUBDIRECTORY
   
   	does not make sense with TERMINAL or TMP.
   
   
   
    EXAMPLE:
   
   	To get a path to the file DETERM in the "userlib" subdirectory to the
   
   	IDL "lib" subdirectory, enter:
   
   
   
   		path = FILEPATH("determ", SUBDIRECTORY = ["lib", "userlib"])
   
   
   
   	The variable "path" contains a string that is the fully-qualified file
   
   	path for the file DETERM.
   
   
   
    MODIFICATION HISTORY:
   
   	December, 1989, AB, RSI (Formalized from original by DMS)
   
   	October, 1990, SG, RSI (added support for MSDOS)
   
   	February, 1991, SMR, RSI (added string array support for multi-level
   
   	    			  directories)
   
   	21 April 1993, AB, Added ROOT_DIR keyword.
   
          14 July  1994, KDB, RSI - Corrected logic error in VMS section
   
              of the ROOT_DIR keyword. Any sub-directory specification was
   
              being ignored when using ROOT_DIR.
   
   	March, 1995, DJE, Add a ':' if root_dir is specified on the Mac.
   
   	29 July 1995, Robert.M.Candey.1@gsfc.nasa.gov, Changed VMS case for
   
   	    no specified path to not append '.][000000]'
   
   	April, 1996, DJE, Remove call to STRLOWCASE(SUBDIR).
   
   	August, 1996, AJH, used environment variables to define TMP on Win32
   
   	12 January 1998, AB, General cleanup and added 2 improvements for VMS
   
              supplied by Paul Hick (pphick@ucsd.edu): (1) Add a colon to the
   
              end of ROOT_DIR if it doesn't end in a ':' or ']' to allow
   
              root_dir to be a logical name without the trailing ':', and
   
              (2) Remove instances of '.][' that result when using rooted
   
              logical names for ROOT_DIR. These changes make it easier to use
   
              the same FILEPATH call across VMS and other operating systems.
   
   	28 January 1999, AB, use new behavior of GETTMP('IDL_TMPDIR') to obtain
   
   	    the correct TMP directory. This means that internal IDL and PRO
   
   	    code will all treat temporary files the same way.
   
   """

   n_params = 1
   subdir = subdirectory
   
   # ON_ERROR, 2		# Return to caller if an error occurs
   
   
   
   do_tmp = (tmp is not None)		#get temporary path if existing
   
   path = ''
   
   
   
   if ((terminal is not None)):   
      
      if ((fstat(0)).isagui):   
         
         message('No terminal device available with IDLde (GUI) interface')
         
      else:   
         if (_sys_version.os == 'vms'):   
            
            path = 'SYS$OUTPUT:'
            
         else:   	# Must be Unix. Mac and Windows are always GUI
            
            path = '/dev/tty'
      
      
      
      return path
      
   
   
   
   if (do_tmp):   
      
      root_dir = getenv('IDL_TMPDIR')
      
   else:   
      
      if (bitwise_not((root_dir is not None))):   
         root_dir = _sys_dir
      
      sep = path_sep()
      
      if (_sys_version.os == 'vms'):   
         
         # Add a trailing ':' if root_dir does not end in ':' or ']'
         
         lastchar = strmid(root_dir, strlen(root_dir) - 1, 1)
         
         if bitwise_and(lastchar != "]", lastchar != ":"):   
            root_dir = root_dir + ":"
         
         sep = "."
         
      
      if ((subdir is not None)):   
         
         #if the SUBDIR keyword is set then concatenate the directories using
         
         # the proper separator character for the current OS.
         
         for i in arange(0, (array(subdir, copy=0).nelements() - 1)+(1)):
         
            path = path + subdir[i]
            
            if (i != array(subdir, copy=0).nelements() - 1):   
               path = path + sep
            
         
         if _sys_version.os == 'MacOS':   
            path = path + sep
         
      
   
   
   
   
   
   _expr = _sys_version.os
   
   if _expr == vms:   
      
      if (bitwise_not(do_tmp)):   
         
         if (path == ''):   
            
            _expr = 1
            
            if _expr == (strmid(root_dir, strlen(root_dir) - 2, 2) == ".]"):   
               root_dir = strmid(root_dir, 0, strlen(root_dir) - 2) + ']' # remove .
               
            elif _expr == (strmid(root_dir, strlen(root_dir) - 1, 1) == "]"):   
               pass # nothing
               
            else:   
               
               # If root_dir is a rooted logical and there is no explicit
               
               # subdir part, we need to fill in [000000]. However, anything
               
               # else should just be glued together as is.
               
               scr = root_dir
               
               len = strlen(scr)
               
               if (strmid(scr, len - 1, 1) == ':'):   
                  scr = strmid(scr, 0, len - 1)
               
               scr = getenv(scr)
               
               if (strmid(scr, strlen(scr) - 2, 2) == '.]'):   
                  path = '[000000]' # assume implicit '.]' or device in root_dir
               
            
            
         else:    # path is filled
            
            path = '[' + path + ']'
            
            # check for a ".]" at the end of our root directory
            
            if (bitwise_and((strmid(root_dir, strlen(root_dir) - 2, 2) != ".]"), (strmid(root_dir, strlen(root_dir) - 1, 1) == "]"))):   
               root_dir = strmid(root_dir, 0, strlen(root_dir) - 1) + '.]'
            
         
      
   elif _expr == Win32:   
      
      if (strmid(root_dir, strlen(root_dir) - 1, 1) != '\'):   
         path = '\' + path
      
      if (bitwise_and((path != ''), (path != '\'))):   
         path = path + '\'
      
   elif _expr == MacOS:   
      
      # make sure the root dir ends with a separator
      
      if (strmid(root_dir, strlen(root_dir) - 1, 1) != ':'):   
         root_dir = root_dir + ':'
      
   else:   
      
      len = strlen(root_dir)
      
      if (bitwise_and((len > 0), (strmid(root_dir, len - 1, 1) != '/'))):   
         path = '/' + path
      
      if bitwise_and((path != ''), (path != '/')):   
         path = path + '/'
      
   
   
   
   
   path = root_dir + path
   
   
   
   if (_sys_version.os == 'vms'):   
      
      chars = strpos(path, '.][')
      
      # if root_dir is something like DISKA:[IDL.] and path is something like
      
      # [DATA.TMP], an invalid VMS path will be returned: DISKA:[IDL.][DATA.TMP]
      
      # The solution is to remove the ']['. This happens if root_dir is from
      
      # translating a rooted logical name.
      
      if chars != -1:   
         path = strmid(path, 0, chars + 1) + strmid(path, chars + 3, strlen(path) - chars - 3)
      
   
   
   
   return path + filename
   
   
   

