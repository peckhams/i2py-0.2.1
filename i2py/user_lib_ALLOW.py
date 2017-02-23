
################################################################################
# 
#  Copyright (C) 2008 Scott D. Peckham <Scott.Peckham@colorado.edu>
# 
#  This file is part of i2py.
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
#--------------------------------------------------------------------
#
#  Notes: IDL procedures with multiple and/or return arguments and
#         procedures or functions with optional arguments cannot be
#         translated properly without additional information.  (i2pY
#         will issue an error message about missing arguments.) This
#         information can be provided here for user-defined IDL
#         routines using calls to i2py's map_pro() and map_func()
#         functions.

#         Arguments to map_var, map_pro and map_func are explained
#         in map.py, in the SubroutineMapping class definition.
#
#         Replaced 'TYPE' keyword with '_TYPE' in 2 routines.

#         This is imported by idl_maps.py.
#
################################################################################


################################################################################
#
#  User-defined IDL function and procedure maps
#
################################################################################

from map import map_var, map_pro, map_func
import idl_maps  ############

#--------------------------------
#  Erode2 routines in erode.pro
#--------------------------------
## map_func('Flow_Codes', inpars=[1], noptional=0, inkeys=['ARC'])
# map_func() does not accept "outkeys"
map_func('Flow_Codes', inpars=[1], noptional=0,
         inkeys=['ARC'], outkeys=['MAP','INCS','OPPS'])
##map_func('Parent_IDs', inpars=[1], noptional=0)
# map_func() does not accept "outkeys"
map_func('Parent_IDs', inpars=[1], noptional=0,
         outkeys=['NON_PARENTS'])
map_pro('Get_Flux_Indices', inpars=[1],
        outpars=range(2,20), noptional=2)
map_pro('Update_Flow_Widths', inpars=range(1,23), outpars=[1],
        noptional=0, inkeys=['REPORT'])
map_pro('Update_Flow_Lengths', inpars=range(1,23), outpars=[1],
        noptional=0, inkeys=['REPORT'])
map_func('Filled_DEM', inpars=range(1,4), outpars=[1], noptional=0,
         inkeys=['SILENT'])
map_func('Flow_Grid', inpars=range(1,8), noptional=0,
         inkeys=['LR_PERIODIC','TB_PERIODIC','ALL_PERIODIC',
                 'DO_FLATS','FILE', 'REPORT'])
map_func('Initial_Flow_Grid', inpars=range(1,7), noptional=0,
         inkeys=['LR_PERIODIC','TB_PERIODIC','ALL_PERIODIC'])
map_pro('Break_Flow_Code_Ties', inpars=[1,2], outpars=[1],
        noptional=0)
map_pro('Link_Flats', inpars=range(1,5), outpars=[1,5],
        noptional=0)
map_func('Area_Grid', inpars=range(1,5), noptional=0,
         inkeys=['FILE','REPORT'])
map_func('Slope_Grid', inpars=[1,2,3], noptional=0,
         inkeys=['FILE','REPORT'])
map_func('Q_Grid', inpars=[1,2,3], noptional=1,
         inkeys=['FILE','REPORT'])
map_func('Qs_Grid', inpars=range(1,8), noptional=0,
         inkeys=['FILE','REPORT'])
map_func('Initial_DEM', inpars=range(1,5),
        noptional=0, inkeys=['GAUSSIAN','PLANE1','PLANE2','SLOPE'])
map_pro('Update_DEM', inpars=range(1,31), outpars=[31],
        noptional=1, inkeys=['FILE','REPORT'])
map_pro('Update_DEM2', inpars=range(1,30), outpars=[30],
        noptional=1, inkeys=['FILE','REPORT'])
map_pro('Update_DEM3', inpars=range(1,30), outpars=[1,30,31],
        noptional=0, inkeys=['FILE','REPORT'])
map_pro('Get_Timestep', inpars=range(1,7), outpars=[7],
        noptional=0)
map_func('Stable_Timestep', inpars=[1,2], noptional=0,
         inkeys=['DX','DY','DT','R','THETA','M','N','K'])
map_pro('Erode', inpars=[], outpars=[],
        inkeys=['PREFIX','NT','NX','NY','DX','DY','KF','NF',
                'MF','R','P','BLR','U','PLANE1','PLANE2',
                'GAUSSIAN','FILL_PITS','LR_PERIODIC',
                'TB_PERIODIC','ALL_PERIODIC','DO_FLATS',
                'DIRECTORY','INPUT_FILE','RIGHT','BOTTOM',
                'CORNER','FOUR_SIDES'])

#--------------------------------------
#  Erode2 routines in erode_utils.pro
#--------------------------------------
map_func('Not_Same_Byte_Order',inpars=[1], noptional=0)
map_pro('Get_Byte_Order', inpars=[], outpars=[])
map_func('To_String', inpars=[1], noptional=0,
         inkeys=['FORMAT'])
map_func('New_String', inpars=[1], noptional=0)
map_pro('Print_Finished', inpars=[1])
map_pro('Print_Time', inpars=range(1,4), outpars=[4],
        noptional=4, inkeys=['SUB','SILENT','SECONDS'])
map_pro('Print_Line', inpars=[1], noptional=0,
        inkeys=['ASTERIX'])
map_pro('Get_Scalar', inpars=[], outpars=[1], noptional=0,
        inkeys=['TYPE','VALUE'])
map_pro('Get_Array', outpars=[1], inpars=[2,3], noptional=1,
        inkeys=['TYPE','NOZERO','VALUE'])
map_pro('Read_RTG_File', outpars=[1], inpars=[2], noptional=0,
        inkeys=['TYPE','REPORT'])
map_pro('View_RTG_File', inpars=[1], noptional=0)
map_pro('Open_RTS_File', inpars=[1], outpars=[2,3,4], noptional=1,
        inkeys=['READ','WRITE','NX','NY','RTI_FILE'])
map_pro('Convert_Flow_Grid', inpars=range(1,8), noptional=2,
        inkeys=['REPORT'])
map_func('File_Found', inpars=[1], noptional=0, inkeys=['SILENT'])
map_pro('Check_Overwrite', inpars=[1], outpars=[2], noptional=1)
map_func('Resolve_Array_Cycle',  inpars=[1,2], noptional=0)
map_func('RT_Resolve_Array', inpars=[])

#------------------------------------
#  Erode2 routines in rti_files.pro
#------------------------------------
map_func('RTI_Record', inpars=[])
map_pro('Make_RTI_File', inpars=[1,2], noptional=0,
        inkeys=['SILENT'])
map_pro('Read_RTI_Value', outpars=[1], inpars=[2,3], noptional=0,
        inkeys=['UPCASE'])
map_pro('Read_RTI_File', inpars=[1], outpars=[2], inkeys=['REPORT'])
map_pro('Get_RTI_Filename', inpars=[1], outpars=[2],
        inkeys=['PREFIX'])
map_pro('Get_Data_Prefix', inpars=[1], outpars=[2,3], noptional=1)

#------------------------------------
#  Erode2 routines in fill_pits.pro
#------------------------------------
## map_func('Start_Pixels', inpars=[1,2,3], noptional=0,
##          inkeys=['EDGES_ONLY','USE_64_BITS','NODATA','CLOSED_BASIN_CODE'])
# map_func() does not accept outpars keyword
map_func('Start_Pixels', inpars=[1,2,3], outpars=[4], noptional=0,
         inkeys=['EDGES_ONLY','USE_64_BITS','NODATA','CLOSED_BASIN_CODE'])
map_pro('Fill_Pits', inpars=range(1,5), noptional=0,
        inkeys=['USE_64_BITS','NODATA'])

#-------------------------------
#  Erode2 routines in heap.pro
#-------------------------------
map_pro('Heap_Init', outpars=range(1,5), inpars=[5,6,7], noptional=0)
map_pro('Heap_Insert', inpars=range(1,6), noptional=0)
## map_func('Heap_Get_Min', inpars=[1,2,3], noptional=0)
# map_func() does not accept "outkeys"
map_func('Heap_Get_Min', inpars=[1,2,3], noptional=0,
         outkeys=['MIN_ID'])
map_pro('Heap_Test', inpars=[1], outpars=[2,3], noptional=2)

################################################################
#
#  Special Erode "callfuncs" (ones below are from TopoFlow)
#
################################################################
##def tf_read_vars_callfunc(i,o):
##    
##    i[0] = 'file_' + i[0]
##    inpars  = ', '.join(i)
##    outpars = ', '.join(o)
##    cmd = '%s = Read_Vars(%s)' % (outpars, inpars)
##    return cmd
##
##def tf_read_rti_value_callfunc(i,o):
##    
##    i[0] = 'file_' + i[0]
##    inpars  = ', '.join(i)
##    outpars = ', '.join(o)
##    cmd = '%s = Read_RTI_File(%s)' % (outpars, inpars)
##    return cmd
##
##def tf_read_var_callfunc(i,o):
##
##    inpars = ', '.join(i)  
##    var_name = o[0]
##    p = var_name.find('.')
##    if (p != -1):  var_name = var_name[p+1:]
##    p = var_name.find('[')
##    if (p != -1):  var_name = var_name[:p]
##    outpars = ', '.join([var_name, o[1]])
##    cmds  = "%s = Read_Var(%s)\n" % (outpars, inpars)
##    ## cmds  = "%s = Read_Var(%s)\n" % (var_name, inpars)
##    cmds += "if (%s != None): %s = %s" % (var_name, o[0], var_name)
##    return cmds
##
##def tf_read_next_var_callfunc(i,o):
##
##    inpars = ', '.join(i)
##    
##    # a = idl_maps.idl_arg_list(i)
##    ## a = ', '.join([a[2], a[0], a[1]])  # (move unit to front)
##    ## a = ', '.join(a[1],a[0])
##    ## a[0] = 'file_' + a[0]
##    # inpars = ', '.join(a)
##    
##    var_name = o[0]
##    p = var_name.find('.')
##    if (p != -1):  var_name = var_name[p+1:]
##    p = var_name.find('[')
##    if (p != -1):  var_name = var_name[:p]
##    cmds  = "%s = Read_Next_Var(%s)\n" % (var_name, inpars)
##    cmds += "if (%s != None): %s = %s" % (var_name, o[0], var_name)
##    return cmds
##
##def tf_load_var_callfunc(i,o):
##
##    inpars = ', '.join(i)  
##    var_name = o[0]
##    p = var_name.find('.')
##    if (p != -1):  var_name = var_name[p+1:]  # (first dot)
##    p = var_name.find('.')
##    if (p != -1):  var_name = var_name[p+1:]  # (second dot)
##    p = var_name.find('[')
##    if (p != -1):  var_name = var_name[:p]
##    outpars = ', '.join([var_name, o[1]])
##    cmds  = "%s = Load_Var(%s)\n" % (outpars, inpars)
##    cmds += "%s = %s" % (o[0], var_name)
##    return cmds   
