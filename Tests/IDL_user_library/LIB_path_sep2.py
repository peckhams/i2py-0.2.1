from numarray import *

# $Id: path_sep.pro,v 1.6 2003/02/03 18:13:22 scottm Exp $

#

# Copyright (c) 2001-2003, Research Systems, Inc.  All rights reserved.

#	Unauthorized reproduction prohibited.

#



#+

# NAME:

#	PATH_SEP

#

# PURPOSE:

#	Return the proper file path segment separator character for the

#	current operating system. This is the character used by

#	the host operating system for delimiting subdirectory names

#	in a path specification. Use of this function instead

#	of hardwiring separators makes code more portable.

#

# CATEGORY:

#	File Management.

#

# CALLING SEQUENCE:

#	Result = PATH_SEP()

#

# INPUTS:

#	None

#

# KEYWORDS:

#    SEARCH_PATH

#	If set, PATH_SEP returns the character used to separate entries

#	in a search path.

#

#    PARENT_DIRECTORY

#	If set, PATH_SEP returns the standard directory notation used

#	by the host operating system to indicate the parent of a

#	directory.

#

# OUTPUTS:

#	The path separator character is returned as a scalar string.

#

# COMMON BLOCKS:

#	None.

#

# MODIFICATION HISTORY:

#	4 April 2001, AB

#-



def path_sep(search_path=None, parent_directory=None):



   n_params = 0
   searchsep = search_path
   pdir = parent_directory
   
   idx = (where(ravel(concatenate(['MacOS', 'Windows', 'unix']) == _sys_version.os_family))[0])[0]
   
   
   
   if ((searchsep is not None)):   
      
      if (pdir is not None):   
         message('Conflicting keywords specified: SEARCH_PATH and PARENT_DIRECTORY. Returning SEARCH_PATH.', info=True)
      
      return (concatenate([',', ';', ':']))[idx]
      
   
   if ((pdir is not None)):   
      return (concatenate([':', '..', '..']))[idx]
   
   return (concatenate([':', '\', '/']))[idx]
   

