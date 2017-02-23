
;*******************************************************************
;   eof_test.pro

;   Author:   Dr. Scott D. Peckham, INSTAAR, Univ. of Colorado

;   Created:  October 16, 2008

;*******************************************************************
pro EOF_Test

;-------------------------------------------------------------------
;Notes:  This works, but the "Python way" is to use "while (True):"
;        and then something like "if len(data == 0): break" inside
;        the loop.  i2py now prints a warning explaining this.
;-------------------------------------------------------------------
data_file = 'EOF_TEST_DATA.bin'
unit = 5

cd, '/Users/peckhams/Desktop/Python_TopoFlow/i2py-0.2.0/SDP'
a = lindgen(10,10)
openw, unit, data_file
writeu, unit, a
close, unit
b = lonarr(10)

openr, unit, data_file
while NOT(EOF(unit)) do begin
    readu, unit, b
    print, b
endwhile
close, unit

end;  EOF_Test
;*******************************************************************
