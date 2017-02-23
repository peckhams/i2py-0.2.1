
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
#      Known issues with current version of I2PY
#
#  (1) Adding a scalar string to string array, as in:
#        a = strarr(4) + 'this'
#      Solution is to use a for loop for this.

#  (2) The ALL keyword to CLOSE. (see idl_func.close_all_files().)
#
#  (3) WHERE returning -1 when there isn't a match.
#      Solution is to use the COUNT keyword instead.
#      Advise i2py users to search converted code for "I2PY_w"
#         and clean up code to compute "count" of "where". 
#
#  (4) FILE_SEARCH returning a null string when there's no match.
#      Solution is to use the COUNT keyword instead.
#
#  (5) All IDL line continuation characters are removed, so need to
#      go back and add Python LCCs manually to avoid long lines.
#
#  (6) IDL code should use REVERSE vs. ROTATE(y,2) to reverse the
#      elements in a 1D array.  Otherwise, converted code won't
#      work.  NumPy's rot90(y,-2) does not work on 1D arrays.
#      NumPy's flipud() works on both 1D and 2D arrays, and gives
#      same result as REVERSE for 1D arrays.  However, for 2D
#      arrays flipud() does not do same thing as rot90(y,-2).
#
#  (7) Arguments to READF, etc. can't be arrays yet, at least not
#      when the FORMAT keyword is used.
#
#  (8) I2PY can't distinguish between when to use numpy.array() vs.
#      numpy.concatenate() yet, so it issues a warning.
#
#  (9) I2PY can't always tell for sure whether to open a file for
#      binary vs. ASCII I/O, unless the SWAP_ENDIAN keyword to
#      OPENR, OPENW or OPENU is used.
#
#  (10) Give a list of unsupported functions and procedures.
#       (e.g. REBIN, SMOOTH, INTERPOL, CONVOL, etc.)
#
#  (11) IDL's "widget_*" routines are not supported yet and may be
#       difficult to convert automatically to wxPython commands.
#
################################################################################
################################################################################


################################################################################
#
#  User-defined IDL function and procedure maps
#
################################################################################

from map import map_var, map_pro, map_func
import idl_maps  ############

#-------------------------------------
#  TopoFlow routines in utils_TF.pro
#-------------------------------------
map_func('TF_String', inpars=[1], noptional=0, inkeys=['FORMAT'])
map_pro('TF_Print', inpars=[1], noptional=0, outpars=[])
map_pro('Clear_Log_Window', inpars=[], outpars=[])
map_pro('Count_Lines', inpars=[2], outpars=[1], inkeys=['SILENT'])
map_func('Current_Directory', inpars=[])
map_func('Resize', inpars=range(1,6), noptional=2, inkeys=['SAMP_TYPE'])
map_pro('Make_Savefile', inpars=[], outpars=[])
map_pro('Trace_Error', inpars=[1,2], outpars=[3], inkeys=['ABORT'])
map_pro('Check_Error_Status', inpars=[1], outpars=[2],
        inkeys=['EVENT_ID', 'TRACEBACK', 'SILENT'])
map_pro('No_Catch', inpars=[], outpars=[1])
map_pro('Read_RTI_Value', inpars=[2,3], outpars=[1],
        inkeys=['UPCASE'],
        callfunc=(lambda i,o: tf_read_rti_value_callfunc(i,o)) )
map_pro('Read_RTI_File', inpars=[1], outpars=[2,3], noptional=1,
        inkeys=['REPORT'])
map_pro('Write_RTI_File', inpars=[1,2], outpars=[], inkeys=['SILENT'])
map_pro('Get_RTI_Filename', inpars=[1], outpars=[2], inkeys=['PREFIX'])
map_pro('Get_Data_Prefix', inpars=[1], outpars=[2,3])
map_pro('Get_Run_Prefix', inpars=[], outpars=[1])
map_func('Not_Same_Byte_Order', inpars=[1])
map_pro('Read_XYZ_As_Grid', inpars=[1,2], outpars=[])
map_pro('Read_Grid', inpars=[2], outpars=[1],
        inkeys=['_TYPE','REPORT','SILENT'])
map_pro('Write_Grid', inpars=[1,2], outpars=[],
        inkeys=['_TYPE','REPORT','SILENT','RTI_FILE'])
map_pro('Open_RTS_File',inpars=[1], outpars=[2,3], noptional=1,
        inkeys=['READ', 'WRITE', 'VERBOSE', 'RTI_FILE',
                'ASSOCIATED', 'NX', 'NY', 'N_GRIDS'])
map_func('Number_Of_Frames', inpars=[1,2], noptional=0,
         inkeys=['NX', 'NY'])
map_pro('Open_RT3_File', inpars=[1], outpars=[2,3,4], noptional=2,
        inkeys=['READ', 'WRITE', 'NX', 'NY', 'RTI_FILE', 'VERBOSE'])
map_pro('Get_Flow_Codes', inpars=[3], outpars=[1,2], inkeys=['ARC'])
map_pro('Convert_Flow_Grid', inpars=range(1,8), noptional=2,
        outpars=[], inkeys=['REPORT'])
map_func('Parent_IDs', inpars=[1], noptional=0, inkeys=['NON_PARENTS'])
map_pro('Get_Flux_Indices', inpars=[1], outpars=range(2,20),
        noptional=2) 
map_func('Flow_Widths', inpars=[1,2],
         inkeys=['METERS', 'DOUBLE', 'METHOD2'])
map_func('Flow_Lengths', inpars=[1,2], inkeys=['METERS', 'DOUBLE'])
map_pro('Get_FS_Slope', inpars=[1,2,3,4], noptional=0, outpars=[5])
map_pro('Get_FS_Slope2', inpars=[1,2,3,4], noptional=0, outpars=[5])
map_func('Courant_Condition_OK', inpars=[1,2,3], noptional=0)
map_func('Stable_Timestep', inpars=[1,2], noptional=0)
map_func('TF_Tan', inpars=[1], noptional=0)
map_pro('TF_Get_LUN', inpars=[2], outpars=[1], noptional=0)
map_pro('TF_Engine_Test', inpars=[1], noptional=0)

#----------------------------------
#  TopoFlow routines in soil.pro
#----------------------------------
map_func('K_of_Theta', inpars=range(1,6), inkeys=['REPORT'])
map_func('Soil_Types', inpars=[], inkeys=['FORM2'])
map_pro('Get_Soil_Params', inpars=[1], outpars=range(2,17),
        noptional=0, inkeys=['REPORT'])

#------------------------------------
#  TopoFlow routines in getvars.pro
#------------------------------------
map_pro('Update_Outfile_Names', inpars=[1,2], noptional=0, outpars=[])
map_func('Total_Outfile_Size', inpars=[1], noptional=0)
map_pro('Get_Run_Vars', inpars=[], outpars=[1])
map_pro('Get_Grid_Vars', inpars=[2,3], outpars=[1], noptional=2)  ###
map_pro('Get_Stop_Vars', inpars=[], outpars=[1])
map_pro('Get_Precip_Vars', inpars=[], outpars=[1])
map_pro('Get_Channel_Vars', inpars=[2], outpars=[1], noptional=1)
map_pro('Get_Met_Vars', inpars=[], outpars=[1])
map_pro('Get_Snow_Vars', inpars=[], outpars=[1])
map_pro('Get_ET_Vars', inpars=[], outpars=[1])
map_pro('Get_GW_Vars', inpars=[2,3], outpars=[1], noptional=2)
map_pro('Get_Infil_Vars', inpars=[2], outpars=[1], noptional=1)
map_pro('Get_Overland_Vars', inpars=[], outpars=[1])
map_pro('Get_Sediment_Vars', inpars=[], outpars=[1])
map_pro('Get_Diversion_Vars', inpars=[2], outpars=[1], noptional=1)
map_pro('Read_Var', inpars=range(2,6), outpars=[1], noptional=0,
        inkeys=['GRID_TYPE','FACTOR'], outkeys=['UNIT'],
        callfunc=(lambda i,o: tf_read_var_callfunc(i,o)) )
map_pro('Read_Next_Var', inpars=[2,3], noptional=0, inkeys=['FACTOR'],
        outpars=[1], callfunc=(lambda i,o: tf_read_next_var_callfunc(i,o)) )
map_pro('Read_Precip_Vars_In_Files', inpars=[1,2,3], noptional=0,
        outpars=[1])
map_pro('Read_Channel_Vars_In_Files', inpars=[1,2,3], noptional=0,
        outpars=[1])
map_pro('Read_Met_Vars_In_Files', inpars=[1,2,3], noptional=0,
        outpars=[1])
map_pro('Read_Snow_Vars_In_Files', inpars=[1,2,3], noptional=0,
        outpars=[1])
map_pro('Read_ET_Var', inpars=range(2,8), noptional=0, outpars=[1],
        inkeys=['UNIT','COPY'])
map_pro('Read_ET_Vars_In_Files', inpars=[1,2,3,4], noptional=0,
        outpars=[1])
map_pro('Read_GW_Vars_In_Files', inpars=[1,2,3], noptional=0,
        outpars=[1])
map_pro('Read_Infil_Vars_In_Files', inpars=[1,2,3], noptional=0,
        outpars=[1])
map_pro('Free_Pointers', inpars=[1], outpars=[], noptional=0)
map_pro('Close_Input_Files', inpars=[1], outpars=[], noptional=0)
map_pro('Update_Grid_Vars', inpars=[1,2], outpars=[2], noptional=0)
map_pro('Update_Precip_Vars', inpars=[1], outpars=[1], noptional=0)
map_pro('Update_Met_Vars',    inpars=[1], outpars=[1], noptional=0)
map_pro('Update_Snow_Vars',   inpars=[1], outpars=[1], noptional=0)
map_pro('Update_ET_Vars',     inpars=[1,2], outpars=[1], noptional=1)
map_pro('Update_Infil_Vars',  inpars=[1,2,3], outpars=[1], noptional=0)
map_pro('Update_GW_Vars',     inpars=[1], outpars=[1], noptional=0)
map_pro('Update_Precip_Vars', inpars=[1], outpars=[1], noptional=0)
map_func('Var_Setting', inpars=[1,2,3], noptional=0, inkeys=['FACTOR'])

#----------------------------------
#  TopoFlow routines in route.pro
#----------------------------------
##map_func('Precipitation', inpars=range(1,6))
##map_func('Snowmelt', inpars=[1,2])
##map_func('Evaporation', inpars=range(1,9))
##map_func('Infiltration', inpars=[1,2,3,4,5,6,8,9,10,11], outpars=[7,8])
##map_func('Seepage', inpars=range(1,27))
##map_func('Number_of_Samples', inpars=range(1,4))
##map_func('Sample_Step', inpars=[1,2])
##map_func('RTG', inpars=range(1,4))
##map_func('Pixel_Var', inpars=[1,2])
##map_func('Stack', inpars=range(1,4))
##map_func('Profile_Var', inpars=[1,2])
map_pro('Remove_Bad_Slopes', inpars=[1], outpars=[1], inkeys=['FLOAT'])
map_pro('Update_Flow_Volume', inpars=range(1,22), outpars=[5])
map_pro('Update_Flow_Depth', inpars=[1,3,4,5,6], outpars=[1,2])
map_pro('Update_Overland_Flow', inpars=range(1,13), outpars=[])
map_pro('Update_Water_Table', inpars=range(1,23), outpars=[6])
map_pro('Update_Mass_Totals', inpars=range(1,18), outpars=range(11,18))
map_pro('Update_Volume_In', inpars=range(1,9), outpars=[1])
map_pro('Update_Volume_Out', inpars=range(1,5), outpars=[1])
map_pro('Update_Velocity_Dynamic', inpars=range(1,28), outpars=[1])
map_pro('Initialize_Precip_Vars', inpars=[1], outpars=[1,2])
map_pro('Initialize_Channel_Vars', inpars=range(1,5),
        outpars=range(5,19))
map_pro('Initialize_Snow_Vars', inpars=range(1,7), outpars=[1])
map_pro('Initialize_ET_Vars', inpars=range(1,7), outpars=[1,7,8,9])
map_pro('Build_Layered_Var', inpars=range(1,6), outpars=[1,4])
map_pro('Initialize_Infil_Vars', inpars=range(1,7), outpars=[1,7])
map_pro('Initialize_GW_Vars', inpars=[1,2], outpars=[1,3,4,5,6])
map_pro('Route_Flow', inpars=range(1,19), outpars=range(14,19),
        noptional=5,  # the outpars; outlet values of q,d,u, etc.
        inkeys=['DIRECTORY','NAME','COMMENT','LOG_FILE','VERBOSE',
                'STOP_ID','DRAW_ID','PLOT'])
map_pro('Check_Flow_Depth', inpars=range(1,5), outpars=[4])
map_pro('Check_Flow_Velocity', inpars=range(1,6), outpars=[5])
map_pro('Check_Infiltration', inpars=[1,2], outpars=[2])
map_pro('Check_Steady_State', inpars=range(1,7), outpars=[4,6])
map_pro('Print_Final_Report', inpars=range(1,35), outpars=[])
map_pro('Print_Mins_and_Maxes', inpars=range(1,8),
        noptional=1, outpars=[],
        inkeys=['QMIN','QMAX','FINAL'])  ### QMIN & QMAX RETURNED ? ###
map_pro('Print_Uniform_Precip_Data', inpars=range(1,4), outpars=[])
map_pro('Print_Dimless_Number_Data', inpars=range(1,7), outpars=[])
map_pro('Check_Output_Options', inpars=range(1,10), outpars=range(10,14))
map_pro('Open_New_RTS_Files', inpars=range(1,9), outpars=range(2,9))
map_pro('Write_Pixel_File_Header', inpars=[1,2], outpars=[], inkeys=['VARNAME'])
map_pro('Open_New_Pixel_Files', inpars=range(1,9),outpars=range(2,8))
map_pro('Save_Pixel_Values', inpars=range(1,25), outpars=[])
map_pro('Save_Grid_Values', inpars=range(1,27), outpars=[])
map_pro('Write_Profile', inpars=range(1,6), outpars=[])
map_pro('Close_All_Output_Files', inpars=range(1,6), outpars=[])

#--------------------------------------
#  TopoFlow routines in save_load.pro
#--------------------------------------
map_pro('Save_Var', inpars=range(1,6), outpars=[], noptional=2)
map_pro('Save_Var2', inpars=range(1,8), outpars=[],
        inkeys=['NOT_PTR','FACTOR'])
map_pro('Save_Var3', inpars=range(1,6), outpars=[])
map_pro('Save_All_TF_Vars', inpars=[1], noptional=0)
map_pro('Read_Vars', inpars=[1], outpars=[2,3,4,5], noptional=3,
        inkeys=['NAME','_TYPE'],
        callfunc=(lambda i,o: tf_read_vars_callfunc(i,o)) )
map_pro('Load_Var', inpars=[1,2], outpars=[3,4], inkeys=['FACTOR'],
        callfunc=(lambda i,o: tf_load_var_callfunc(i,o)))
# map_func('Type_Code', inpars=[1], noptional=0)
map_pro('Load_All_TF_Vars', inpars=[1,2], outpars=[1], noptional=0)

#---------------------------------------
#  TopoFlow routines in smooth_DEM.pro
#---------------------------------------
map_pro('Best_SA_Curve_Fit', inpars=range(1,6), noptional=3,
        inkeys=['ITMAX','REPORT','TOL','WEIGHTS'])

#--------------------------------------
#  TopoFlow routines in Qnet_file.pro
#--------------------------------------
map_func('Equation_Of_Time', inpars=[1,2], noptional=1,
         inkeys=['DEGREES','DMS'])
map_func('Julian_Day', inpars=[1,2,3], noptional=1)
map_func('True_Solar_Noon', inpars=range(1,5), noptional=2)
map_pro('Get_Time_Zone_List', inpars=[1,2], noptional=1)

#-------------------------------------
#  TopoFlow routines in richards.pro
#-------------------------------------
map_pro('BW_Solution', inpars=[1,2,3], noptional=3,
        inkeys=['ZMAX','QS','QI','QR','R','T','CN','G','NZ',
                'PLOT_Z1','PLOT_Z2','PARAM_SET1','PARAM_SET2'])

#---------------------------------------
#  TopoFlow routines in pixel_size.pro
#---------------------------------------
map_func('Meters_Per_Degree_Lat', inpars=range(1,5), noptional=3)
map_func('Meters_Per_Degree_Lon', inpars=range(1,5), noptional=3)
map_pro('Get_Pixel_Sizes', inpars=[5], outpars=range(1,5),
        noptional=0, inkeys=['REPORT', 'METERS'])

#---------------------------------
#  TopoFlow routines in plot.pro
#---------------------------------
map_func('Color_Start', inpars=[1], noptional=1)
map_func('Color_Width', inpars=[1], noptional=1)

################################################################
#
#  Special TopoFlow "callfuncs"
#
################################################################
def tf_read_vars_callfunc(i,o):
    
    i[0] = 'file_' + i[0]
    inpars  = ', '.join(i)
    outpars = ', '.join(o)
    cmd = '%s = Read_Vars(%s)' % (outpars, inpars)
    return cmd

def tf_read_rti_value_callfunc(i,o):
    
    i[0] = 'file_' + i[0]
    inpars  = ', '.join(i)
    outpars = ', '.join(o)
    cmd = '%s = Read_RTI_File(%s)' % (outpars, inpars)
    return cmd

def tf_read_var_callfunc(i,o):

    inpars = ', '.join(i)  
    var_name = o[0]
    p = var_name.find('.')
    if (p != -1):  var_name = var_name[p+1:]
    p = var_name.find('[')
    if (p != -1):  var_name = var_name[:p]
    outpars = ', '.join([var_name, o[1]])
    cmds  = "%s = Read_Var(%s)\n" % (outpars, inpars)
    ## cmds  = "%s = Read_Var(%s)\n" % (var_name, inpars)
    cmds += "if (%s != None): %s = %s" % (var_name, o[0], var_name)
    return cmds

def tf_read_next_var_callfunc(i,o):

    inpars = ', '.join(i)
    
    # a = idl_maps.idl_arg_list(i)
    ## a = ', '.join([a[2], a[0], a[1]])  # (move unit to front)
    ## a = ', '.join(a[1],a[0])
    ## a[0] = 'file_' + a[0]
    # inpars = ', '.join(a)
    
    var_name = o[0]
    p = var_name.find('.')
    if (p != -1):  var_name = var_name[p+1:]
    p = var_name.find('[')
    if (p != -1):  var_name = var_name[:p]
    cmds  = "%s = Read_Next_Var(%s)\n" % (var_name, inpars)
    cmds += "if (%s != None): %s = %s" % (var_name, o[0], var_name)
    return cmds

def tf_load_var_callfunc(i,o):

    inpars = ', '.join(i)  
    var_name = o[0]
    p = var_name.find('.')
    if (p != -1):  var_name = var_name[p+1:]  # (first dot)
    p = var_name.find('.')
    if (p != -1):  var_name = var_name[p+1:]  # (second dot)
    p = var_name.find('[')
    if (p != -1):  var_name = var_name[:p]
    outpars = ', '.join([var_name, o[1]])
    cmds  = "%s = Load_Var(%s)\n" % (outpars, inpars)
    cmds += "%s = %s" % (o[0], var_name)
    return cmds   
