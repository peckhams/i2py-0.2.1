
;*******************************************************************
;   i2py_test.pro

;   Author:   Dr. Scott D. Peckham, INSTAAR, Univ. of Colorado

;   Created:  Aug. 14-15, 2008
;   Modified: Aug. 19-26, 2008
;   Modified: Sept. 4-12, 2008
;   Modified: Oct. 12-16, 2008
;   Modified: Nov. 5-7, 10-11, 17-21,  2008
;   Modified: June 10-12, 2009
;   Modified: June 18-19, 2009

;*******************************************************************
pro Test_Procedure, MY_KEY=MY_KEY, KEY2=key2, KEY3=abc

FORWARD_FUNCTION Func1, Func2

;------------------------------------------
; IF STATEMENT with AND, OR and NOT tests
;------------------------------------------
if not(a or b) then n=0
if (a or b) then n=0
if (a or b or c) then n=0
if ((a or b) and c) then n=0
if (a and b and c) then n=0
if ((a or b) and not(c)) then n=0
if ((a or b) and (c or d)) then n=0
if a or b then n=0

;------------------------;  Square bracket tests;------------------------
a = my_func([1,2,3,4])
a = [1,2,3, 4]
a = [0b, 1b, 2b,3B]
a = [0s, 1S, 2s,3S]
a = [0L, 1L, 2L,3L]
a = [0d, 1d, 2D,3d]
a = [0LL, 1ll, 2LL]
a = [0.0, 1, 2.]a = ['x','y','z']
a = ["x", "y", "z"]
a = ['x', "y"]
msg = ['Error message.']
;---------------------------
a = [a, 1]
;---------------------------
a = [0, a]
;---------------------------
a = [[1,2,3], 4]
;---------------------------
a = [0, [1,2,3]]
;---------------------------
a = [[1,2], 0, [3,4]]
;---------------------------
a = [[1,2,3], b]
;---------------------------
a = [b, [1,2,3]]
;---------------------------a = [[1,2,3],[4,5,6]]
;---------------------------a = [1,2,3]b = [4,5,6]c = [a,b]
;----------------------------------
a = [[[1,2],[3,4]],[[5,6],[7,8]]]

;-------------------
; Array subscripts
;-------------------
b = a(3)
b = a(1,2)
b = a[4]
b = a[[4]]
b = a[2,2]
b = a[2,*]
b = a[0:2,1:3]
b = a[w1[w2]]

;-----------------------
;  SORT function tests
;----------------------------------------------
;Next line must use "array" vs. "concatenate"
;for converting the brackets, otherwise usage
;shown will not work in Python.
;----------------------------------------------
b  = [5,3,1,2,8,7,0,6]
s  = sort(b)
b2 = b[s]

;---------------------
; Cleaner increments
;---------------------
b12 = b12 + abc
b12 = (b12 + abc)

;----------------------------------
; Minimum/Maximum array operators
;----------------------------------
b = a < 5
a = a < 5   ;(Should we do in-place with 3rd arg to minimum() ?)
a = a > 5

;-------------------------
;  Boolean keyword tests
;------------------------------------------------
;  Note also how unset keywords are initialized
;  to KEY=None in "Test_Procedure" at the top. 
;------------------------------------------------
a = my_function(key1=0b, key2=0)          ;(unset keywords)
a = my_function(key3=1b, key4=1, /key5)   ;(set keywords)
a = my_function(key1=key1)
a = my_function(key1 = some_function(b))

;------------------------------
;  KEYWORD_SET function tests
;------------------------------
KEY1 = keyword_set(KEY1)
if (keyword_set(KEY1)) then print, 'Key is set.'
if not(keyword_set(KEY1)) then KEY1 = 0
if not(keyword_set(MY_KEY)) then MY_KEY =  0
if not(a) then b=0   ; (should be "not" vs. "logical_not")

;------------------
;  Special tests
;------------------
a = max([1,2,3])
i = indgen(5)

;-----------------------------
;  Some IDL system variables
;-----------------------------
p   = !path
d   = !d.name
os  = !version.os
osf = !version.os_family

;-------------------------
; NaN and Infinity tests
;-------------------------
f_nan = !values.f_nan
f_inf = !values.f_inf
d_nan = !values.d_nan
d_inf = !values.d_inf
;------------------------
print, finite(a)
print, finite(a, /NAN)
print, finite(a, /INF)
print, finite(a, /INFIN)
print, finite(a, /INFINITY)

;----------------------------
;  PATH_SEP function tests
;----------------------------
sep = path_sep()
   
;-----------------------------------------------
;  PRINT procedure tests (with FORMAT keyword)
;-----------------------------------------------
print, 3.14159, 'hello', 456
print, 3.14159, 'hello', 456, format='(F6.3, A7, 4X, I3)'
print, 3.14159, 2.718, 1.000, 'hello', format='(3F6.3, A7)'
print, 'my_string'
print, 'this '+'that'
print, 'this' + 'that'
;-------------------------------------------------------
;  Equals sign inside of quotes vs. keyword assignment
;-------------------------------------------------------
print, 'path separator = ' + path_sep()
print, "path separator = " + path_sep()

;-------------------------
;  STRING function tests
;-------------------------
s = string(number)
s = string(number, FORMAT=format)   ;;;;;;;;;;;;
s = string(3.14159, 'hello', 456)
s = string(3.14159, 'hello', 456, format='(F6.3, A7, 4X, I3)')
;---------------------------------------
;  Special behavior (not supported yet)
;---------------------------------------
s = string(indgen(5))     ;(should be a string array)
s = string([72b, 101b, 108b, 108b, 111b])   ;(should be "Hello")

;-----------------------------------
; Scalar constant assignment tests
;-----------------------------------
a = 1      ;In assignments, wrap ints with "int16()"
a = 1L
a = 1.0
a = 1d
a = 1LL
a = 1ULL
a = 1UL
a = 1b

;------------------
; Structure tests
;------------------
v = {a:0L, b:0b, c:0.0, d:intarr(5), e:'this'}  ;(anonymous)
V = {my_struct, a:0L, b:0b, c:'this'}  ;(named)
print, v.(0)      ;(tag numbers or field indices)
print, v.(1)
;(Note:  Use "repeat" to "replicate" an IDL structure.)

;-------------------------
;  READF procedure tests
;-------------------------
readf, 1, a, b
readf, unit, a, b
readf, unit, a, b, format=('F8.3, I3')

;---------------------------------
; "if (N_ELEMENTS(g) eq 0)" TEST
;---------------------------------
if (n_elements(g) eq 0)   then g = 1
if (N_ELEMENTS(a_b) eq 0) then a_b = 1 
if (n_elements(a + b) eq 0) then c = 1
if (n_elements(g) eq 1) then g = 2

;------------------------------------------
; OPENR procedure tests (and SWAP_ENDIAN)
;------------------------------------------
openr, unit, 'my_file.bin', /get_lun, /swap_endian
openr, unit, 'my_file.bin', swap_endian=1
openr, unit, 'my_file.bin', swap_endian=not_same_byte_order(byte_order)
openr, unit, 'my_file.txt', /get_lun

;------------------------------------------
; OPENU procedure tests (and SWAP_ENDIAN)
;------------------------------------------
openu, unit, 'my_file.bin', /get_lun, /swap_endian
openu, unit, 'my_file.bin', swap_endian=1
openu, unit, 'my_file.bin', swap_endian=not_same_byte_order(byte_order)
openu, unit, 'my_file.txt', /get_lun

;------------------------------------------
; OPENW procedure tests (and SWAP_ENDIAN)
;------------------------------------------
openw, unit, 'my_file.bin', /get_lun, /swap_endian
openw, unit, 'my_file.bin', swap_endian=1
openw, unit, 'my_file.bin', swap_endian=not_same_byte_order(byte_order)
openw, unit, 'my_file.txt', /get_lun

;-----------------------------
;  MAKE_ARRAY function tests
;-----------------------------
a = make_array(2,3, type=5, /nozero, /index)
a = make_array(10, type=1)
a = make_array(10, type=2, /nozero)

;----------------------------------
;  DIALOG_PICKFILE function tests
;----------------------------------
sav_file = dialog_pickfile(FILTER='*.sav', FILE='myfile.sav')

;-------------------------
;  CASE statement tests
;-------------------------
case (a+b) of       ;(an expression)
    0 : value = 0
    1 : value = 1
 else : value = 2
endcase
;--------------------------
case (type) of     ;(a variable)
    'THIS' : value = 0
    'THAT' : value = 1
     ELSE  : value = 2
endcase
;--------------------------
case (result) of
    0 : value = 0
    1 : value = 1
  else: value = 2
endcase

;---------------------------
;  PTR_NEW function tests
;---------------------------
a = ptr_new(1d)
a = ptr_new(b)
a = ptr_new(0L, /ALLOCATE_HEAP)

;----------------------------
;  GET_LUN procedure tests
;----------------------------
get_lun, unit
GET_LUN, unit

;--------------------------
;  Special variable tests
;--------------------------
start = systime(1)
dpi = !DPI
fpi = !PI
in  = 20
IN  = 20
pow = 30
type = 'DOUBLE'
Type = 'FLOAT'
print, string(type)
print, string(1)

;-----------------------
;  BYTE function tests
;--------------------------------
;  Python has ord() and chr().
;--------------------------------
b = byte(257)    ; should be 1
b = byte('a')    ; should be 97
b = byte('abc')  ; should be [97, 98, 99]

;-------------------------------------
;  BYTE function test (special case)
;-------------------------------------
big_endian = (byte(1,0,2))[0] eq 0b

;-------------------------------
;  ONLINE_HELP procedure tests
;-------------------------------
filepath = '/Applications/TopoFlow/help/about_TF.htm'
online_help, book=filepath, /full_path
online_help, book=filepath, full_path=1
online_help, book='some_help_file.htm', /full_path
; online_help, /quit  ;(not supported yet)

;---------------------
;  For loop tests
;--------------------
for k=n,0,-1 do begin
    print, k
endfor
;-------------------------------
for k=0,(n-1) do begin
    print, k
endfor
;-------------------------------
for k = 0, (n - 1) do begin
    print, k
endfor
;-------------------------------
for k=0L,(n-1L) do begin
    print, k
endfor

;----------------
; Pointer tests
;----------------
w = where(*T_air ne *T_surf, nw)
;------------------------------------------------
(*var)[ i[j]: i[j+1]-1 ] = *(v_by_layer[j])
n = n_elements(*(v[k]))
A = *(v[k])
v2 = vol + dt*((R*da) - Q)
;------------------------------------------------
a = (*T_air * 5) + *T_surf
b = (c*d)
B = (C * d)
b = (c *d)
b = (1 *d)
b = (d +*c)
b = (*1 + 5)
b = (5 *1)

;-----------------------
;  SIZE function tests
;-----------------------
s = size(A, /dimensions)
s = size(a, /n_elements)
s = size(a, /n_dimensions)
s = size(a, /type)
;----------------------------------------------
s = size(a)

;---------------------------------
;  LOGICAL OR, AND and NOT tests
;---------------------------------
print, 0 or 1
print, 0 and 1
DONE = 0b
if NOT(DONE) then print,'Not done.'
a = [0,1,0]
b = [1,1,0]
print, (a or b) 
print, (a and b)
print, (a and not(b))
print, (a or not(b))
print, not(a)   ;([-1,-2,-1]; caution)
if (0) then print,'Hello'
if (1) then print,'Hello'
print, (3 lt 5)   ;(= 1 in IDL, = True in Python)
print, (3 gt 5)   ;(= 0 in IDL, = False in Python)

;-------------------------
;  PTRARR function tests
;-------------------------
;p = ptrarr(2,2)

;-------------------------
;  STRARR function tests
;-------------------------
s = strarr(2,2)
s = strarr(5) + 'this'   ;*** Use s.fill()

;-----------------------
;  TV procedure tests
;-----------------------
tv, image, /order

;--------------------------
;  CONTOUR procedure tests
;--------------------------
contour, z, nlevels=10
contour, z, levels=[100.0, 200.0, 300.0]
contour, z, levels=my_levels
contour, z, x, y, /fill
contour, z, x, y, /isotropic, nlevels=20

;--------------------------
;  SURFACE procedure tests
;--------------------------
surface, z
;-----------------------------------------
surface, z, x, y, xtitle='X', ytitle='Y'

;------------------------------
;  SHADE_SURF procedure tests
;------------------------------
shade_surf, z
;--------------------------------------------
shade_surf, z, x, y, xtitle='X', ytitle='Y'

;--------------------------
;  PRINTF procedure tests
;--------------------------
printf, unit, a, 1, 2
printf, unit, a, 1, format='(F8.3, I3)'

;--------------------------
;  Line continuation tests
;--------------------------
if (THIS) then $
    do_this = 1 $
else $
    do_that = 1
;--------------------------
f = my_function(a, b, $
    c, d, e)

;-----------------------------
;  FILE_CHMOD function tests
;-----------------------------
file_chmod, 'my_file', 755

;-------------------------
;  SPAWN procedure tests
;-------------------------
spawn, 'notepad'

;---------------------
;  CD function tests
;---------------------
cd, newdir
cd, newdir, current=olddir
cd, current=curdir

;--------------------------
;  XYOUTS procedure tests
;--------------------------
xyouts, 1.5, 2.0, 'Hello'
xyouts, 1.5, 2.0, 'Hello', color=100
xyouts, 0.4, 0.6, 'Hello', /normal
;xyouts, 'Hello'  ;(unsupported case)

;------------------------------
;  PLOT_FIELD procedure tests
;------------------------------
plot_field, u, v, title='Arrows!', length=0.1

;------------------------
;  PLOT procedure tests
;------------------------
plot, y
;-------------------------------------------------
plot, x, y, position=[0,0,1,1], background=white
;-------------------------------------------------
plot, x, y, xtitle='Distance [km]', ytitle='Elevation [m]', title='Long. Profile Plot'
;-------------------------------------------------
plot, x, y, /isotropic
;-------------------------------------------------
plot, x, y, psym=-1, symsize=2.0
;-------------------------------------------------
plot, x, y, psym=4, symsize=2.0
;-------------------------------------------------
plot, x, y, psym=8, symsize=0.5
;-------------------------------------------------
plot, /polar, r, theta
plot, x, y, /xlog, /ylog
plot, x, y, /xlog
plot, x, y, /ylog
plot, y, /ylog, thick=2
plot, x, y, linestyle=3, color=blue
;-------------------------------------------------
plot, x, y, xticks=5, yticks=10
;-------------------------------------------------
plot, [1.1,2,3], [1.1,2,3], xstyle=1
;-------------------------------------------------
plot, [1.1,2,3], [1.1,2,3], xstyle=5

;-------------------------
;  WINDOW function tests
;-------------------------
window, 0
window, 1, xsize=500
window, 1, xsize=500, ysize=300
window, 1, xsize=nx, ysize=ny
window, 1, title='My Title'
window, 1, xpos=100, ypos=100

;--------------------------
;  WDELETE function tests
;--------------------------
wdelete, 0
wdelete, 1,2,3
wdelete, n

;-----------------------
;  WSET function tests
;-----------------------
wset, 0
wset, 1
wset, n

;-------------------------
;  BYTSCL function tests
;-------------------------
b = bytscl(a)
b = bytscl(a, min=amin, max=amax, top=top)

;--------------------------
;  RANDOMN function tests
;--------------------------
a = randomn(seed1)
a = randomn(seed1, 10)
a = randomn(seed1, 3, 4)
a = randomn(seed1, 3, 4, binomial=[5,0.3])
a = randomn(seed1, 3, 4, gamma=2.0)
a = randomn(seed1, 3, 4, /normal)
a = randomn(seed1, 3, 4, poisson=2.3)
a = randomn(seed1, 3, 4, /uniform)
;-----------------------------------------------
a = -5 + (randomn(seed1, 3, 4, /uniform) * 10)

;--------------------------
;  RANDOMU function tests
;--------------------------
;similar

;--------------------------
;  REFORM function tests
;--------------------------
;  NumPy also has SQUEEZE
;--------------------------
a = indgen(24)
b = reform(a, 6, 4)  ;(note reverse indices)
c = reform(b, 24)
;-----------------------
a = indgen(24 * 3)
b = reform(a, 6, 4, 3)

;-------------------------------------
;  ROTATE and REVERSE function tests
;-------------------------------------
a = indgen(3,4)
b = transpose(a)
;-----------------
b = rotate(a, 0)
b = rotate(a, 1)
b = rotate(a, 2)
b = rotate(a, 3)
b = rotate(a, 4)   ;(same as transpose)
b = rotate(a, 5)   ;(flip x-axis)
b = rotate(a, 6)
b = rotate(a, 7)   ;(flip y-axis)
;----------------
a = indgen(4)
b = reverse(a)

;--------------------------
;  EXECUTE function tests
;--------------------------
a = execute("print, 'Hello'")
a = execute("print, 'Hello' &  a=1  &  print, 'a =', a")   ;(multiple statements)

;------------------------
;  SHIFT function tests
;------------------------
a = indgen(5)     ;[0,1,2,3,4]
b = shift(a, 1)   ;[4,0,1,2,3]
b = shift(a, -1)  ;[1,2,3,4,0]
;--------------------------------------
;  Note that array axes are reversed
;--------------------------------------
a = indgen(3,4) 
b = shift(a, 1, 0)
b = shift(a, -1, 0)
c = shift(a, 0, 1)
c = shift(a, 0, -1)
c = shift(a, 1, -1)
;--------------------------------------
;   These 3D cases need more testing
;--------------------------------------
a = indgen(3,4,5)
c = shift(a, 1, 0, 0)
c = shift(a, 0, 1, 0)
c = shift(a, 0, 0, 1)
c = shift(a, 1, 2, 3)   ;(this case works)

;---------------------------
; REPLICATE function tests
;---------------------------
a = replicate('-', 10)
a = replicate(5, 10)
a = replicate(structure, 10)

;-----------------------
; Array indexing tests
;-----------------------
print, a[0:5]  ;(note upper limit is adjusted)
print, a[*,0]  ;(note reversed indices)

;----------------------
;  IF statement tests
;----------------------
if a lt 5 then print, 'a is smaller than 5'
if (a lt 5) then print, 'a is smaller than 5' else print, 'a is GE 5'

;-----------------------
; TOTAL function tests
;-----------------------
a = total(b)
a = total(b, /double)
a = total(b, /cumulative)
a = total(b, cumulative=1)
a = total(b, /cumulative, /double)
a = total(b, /double, /cumulative)
a = total(b, /double, /nan)
a = total(b, /nan)
a = total(b, /nan, /cumulative)   ;(there is no "nancumsum")

;---------------------------
; Deliberate casting tests
;---------------------------
a = 0b
a = 0L
a = 0d
a = 0.0
a = 0LL
a = 0U
a = 0ULL
a = '15'X

;----------------------------
; POINT_LUN procedure tests
;----------------------------
point_lun, unit, (nx * 5)     ;(set position)
point_lun, -2, pos            ;(return position)
point_lun, (-1 * unit), pos   ;(return position)

;------------------------
;  FSTAT function tests
;------------------------
openr, unit1, 'my_filename.txt', /get_lun
temp = fstat(unit1)
filesize = temp.size
close, unit1

;----------------
; File I/O tests
;----------------
openr, unit, 'my_filename.txt', /get_lun, /swap_endian
a = intarr(5,5)
readu, unit, a

;---------------------------------------
;  CLOSE and FREE_LUN procedure tests
;---------------------------------------
close, 3
close, unit
close, unit1, unit2
;------------------------
free_lun, 3
free_lun, unit
free_lun, unit1, unit2, unit3

;--------------------------------
;  FILE_DELETE procedure tests
;--------------------------------
file_delete, 'dirname/my_filename.txt'
a = '/dir1/dir2/my_file.txt'
file_delete, a
file_delete, a, b, c

;-----------------------------
;  FILE_TEST function tests
;-----------------------------
exists = file_test('dirname/my_filename.txt')

;---------------------
; EOF function tests
;---------------------
while NOT(EOF(unit)) do readu, unit, a

;-------------------------
;  Type conversion tests
;-------------------------
a = indgen(5)
a = float(a)
g = byte(257)   ;should be 1.  ( Python has ord() and chr(). )
g = fix(1.5)    ;should be 1
g = float(1)    ;should be 1.0

;-------------------------------
;  Array initialization tests
;-------------------------------
B_arr = bytarr(5)
I_arr = intarr(3,5)   ;(note reversed indices)
L_arr = lonarr(5)
F_arr = fltarr(5)
D_arr = dblarr(5)
;-----------------------------
B_arr = bytarr(5, /nozero)
I_arr = intarr(3,5, /NOZERO)
L_arr = lonarr(5, nozero=1)
F_arr = fltarr(5, NOZERO=1)
D_arr = fltarr(5, NOzero=1)

;----------------------
;  Array "ramp" tests
;----------------------
a = findgen(5)
a = findgen(3,5)
a = findgen(3,5,8)
a = bindgen(5)
a = indgen(5)
a = lindgen(5)
a = dindgen(5)

;------------------------------
;  MIN and MAX function tests
;------------------------------
amin = min(a)
;------------------------
amin = min(a, amin_sub)
;------------------------
amin = min(a, amin_sub, max=amax)
;------------------------
amin = min(a, amin_sub, max=amax, subscript_max=amax_sub)
;------------------------
amin = min(a, subscript_max=amax_sub, max=amax, amin_sub)
;------------------------
amax = max(a)
;------------------------
amax = max(a, amax_sub, min=amin, subscript_min=amin_sub)
;------------------------
amax = max(a, subscript_min=amin_sub, min=amin, amax_sub)

;------------------------
;  WHERE function tests
;------------------------
a[where(a lt 0)] = 0
;----------------------------------------
a[where(a lt 0, comp=wc, ncomp=nc)] = 0    ;(doesn't work yet)
;----------------------------------------
w = where(a lt 10)
;--------------------------
w = where(a lt 10, nw)
;--------------------------
w = where(a lt 10, nw, comp=wc, ncomp=nc)
;-------------------------------------------
; These have arguments with an equals sign
;-------------------------------------------
w = where(a eq 10)
w = where(a le 10)
w = where(a ge 10)
w = where(a ne 10)
;-------------------------
; "Nested" WHERE example
;-------------------------
a  = indgen(4,4)-8
w1 = where(a lt 0)
w2 = where(a[w1] gt -3)
a[w1[w2]] = 99

;-----------------------
;  ATAN function tests
;-----------------------
a = atan(x)
a = atan(y,x)

;---------------------------
;  STRSPLIT function tests
;---------------------------
s = ' Parse this sentence.'
words = strsplit(s, /extract)
words = strsplit(s, extract=1)
words = strsplit(s, /extract, count=my_count)
words = strsplit(s, /extract, length=my_length)
;-------------------------------------
indices = strsplit(s)
indices = strsplit(s, count=my_count, length=my_length)
;-------------------------------------
dstr = '1,2,3,4,5,'
data   = strsplit(dstr, ',', /extract)
indices = strsplit(dstr, ',')

;---------------------------
;  STRTRIM function tests
;---------------------------
name = strtrim('   Scott   ')
name = strtrim('   Scott   ', 0)
name = strtrim('   Scott   ', 1)
name = strtrim('   Scott   ', 2)
name = strtrim('   Scott   ', 3)

;-----------------------------
;  String manipulation tests
;-----------------------------
word = strmid(s, 4, 3)
word = strmid('the red fox', 4, 3)   ;(should be 'red')
s = 'the red fox'
strput, s, 'dog', 8
strput, s, 'dog'
len = strlen('this')
name = strupcase('Scott')
name = strlowcase('Scott')
print, 'path separator = ' + path_sep()


end;  Test_Procedure
;*******************************************************************


