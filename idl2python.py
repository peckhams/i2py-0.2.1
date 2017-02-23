#!/usr/bin/env python

# 
#  Copyright (C) 2009 Scott D. Peckham <Scott.Peckham@colorado.edu>
# 
#  This file is part of i2py.  This is a simplified version of the
#  idl2python shell script that is used on Unix systems, written
#  for use on a PC running windows.
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

import sys
import os.path
import i2py

################################################################################
#
# Define some work functions
#
################################################################################

#
# Parses the contents of open file object infile and generates the output code.
# If no errors occur, returns the output string.  Otherwise, prints the errors
# to stderr (with infile.name prepended to each message) and returns None.
#

def process_input(infile):
   output = i2py.parse(infile.read())

   if output:
      output = output.pycode()

   if (not output) or i2py.error_occurred():
      for err in i2py.get_error_list():
         sys.stderr.write('%s:%s\n' % (infile.name, err))
      return None

   return output

#
# Returns infilename with the extension changed to '.py'.  Assumes infilename
# has a non-empty basename (i.e. it's a file name, not a directory name).
#

def make_outfile_name(infilename):
   dirname, basename = os.path.split(infilename)
   dot_index = basename.rfind('.')
   if dot_index > 0:
      basename = basename[0:dot_index]
   return os.path.join(dirname, basename + '.py')


################################################################################
#
# Do the actual work
#
################################################################################

def convert(*args):

   exit_stat = 0    # Exit status
   outfile = None   # Output file object
   
   for infilename in args:
      #
      # Process the input file
      #

      ## print 'infilename =', infilename  ########

      # Read from a file
      infile = file(infilename, 'U')   # Open in universal newline mode
      try:
         output = process_input(infile)
      finally:
         infile.close()

      #
      # Write the output file
      #       
      # If an error occurred, don't write any output
      if not output:
         exit_stat = 1
         continue

      # Output goes to a file
      outfile = file(make_outfile_name(infilename), 'w')
      ## print 'outfilename =', outfile.name ########
      
      try:
         outfile.write(output)
      finally:
         outfile.close()

