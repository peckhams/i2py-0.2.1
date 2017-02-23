
;*******************************************************************
;   wx_tests.pro

;   Author:   Dr. Scott D. Peckham, INSTAAR, Univ. of Colorado

;   Created:  Nov. 11, 2008

;*******************************************************************
pro Pickfile_Test, OPEN_TEST=OPEN_TEST

;----------------------------------------------------------------
;Notes:  This procedure is for testing how well I2PY converts
;        the DIALOG_PICKFILE function.  The MULTIPLE_FILES
;        option is not yet working.
;----------------------------------------------------------------
;        Keyword references must be consistent with regard to
;        case (i.e. upper or lower).
;----------------------------------------------------------------
;        First line gets converted to:
;           OPEN_TEST = (OPEN_TEST is not None).
;        However, note that (True is not None) equals True, and
;           (False is not None) is also True.
;----------------------------------------------------------------
OPEN_TEST = keyword_set(OPEN_TEST)

if (OPEN_TEST) then begin 
     ;---------------------------
     ; Choose file to open/read
     ;---------------------------
     sav_file = dialog_pickfile(FILTER='*.*', FILE='myfile.txt', $
                       /READ, /MULTIPLE)
endif else begin
     ;----------------------------
     ; Choose file to save/write
     ;----------------------------
     sav_file = dialog_pickfile(FILTER='*.sav', FILE='myfile.sav')
endelse

print, 'sav_file = ', sav_file

end;  Pickfile_Test
;*******************************************************************
