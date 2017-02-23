
;*******************************************************************
;   waves.pro

;   Author:   Dr. Scott D. Peckham, INSTAAR, Univ. of Colorado

;   Created:  June 9, 2003
;   Modified: June 10-19, 27. July 10 - August 22, 2003.
;   Modified: March, December 2004 (collected here)
;   Modified: January 2005

;   Purpose:  Routines that use linear wave theory to compute
;             grids of wave properties, such as wavelength,
;             wave number, wave height, group velocity, etc.
;             This includes a wave refraction calculator and
;             some visualization tools.

;   Idea:     Starting from a grid of water depths (bathymetry)
;             and the deep-water wave period, T, we can compute:
;              (1) L, wavelength grid, using Newton's method to
;                  solve the dispersion relation. NB! The contours
;                  of L will always match the contours of d.
;              (2) k, wave number grid, using k = (2 pi / L).
;              (3) C, wave speed grid, using C = (L / T).
;              (4) Cg, group velocity grid, using k, d, L & T.
;              (5) a, wave ray angle grid, using the fact that the
;                  curl of k is zero.  Can also use Snell's law,
;                  but that is only valid for straight coastlines.
;              (6) P, wave power grid, using the "conservation of
;                  wave power" equation (ignoring diffraction).
;              (7) H, wave height grid, from the grid P.
;              (8) E, energy density grid, from E=(rho/8)*g*H^2.
;              (9) umax, max orbital velocity grid.

;   Notes:    All of the fully-developed sea formulas were
;             moved to fds.pro, which should be .RUN first.
;             Should also .RUN plot_LT.pro.
;*******************************************************************
;   Close_Windows

;-------------------
;   Functions
;-------------------
;   New_String
;   Gravity
;   Density

;   X_Coordinates      ;(only used by longshore.pro ??)
;   Y_Coordinates
;   Test_Bathymetry
;   Water_Depth

;   Wave_Length        ;(can only handle d and T)
;   Wave_Length2       ;(can also handle u, v and theta)
;   Wave_Length2_Test  ;(a procedure to compare last 2)

;   Wave_Speed
;   Group_Velocity
;   Wave_Speed_Ratio   ;(n = Cg/C)
;   Deep_Water
;   Shallow_Water

;   Wave_Number
;   Wave_Number2        ;(failed experiment)
;   Wave_Number3

;   Wave_Frequency
;   Intrinsic_Frequency

;--------------------------
;   THESE MAY BE OBSOLETE
;--------------------------
;   Wave_Angle          ;(from curl of k equals zero.)
;   Theta1              ;(for stability tests)
;   Wave_Angle_TEST     ;(experimental idea)

;   Wave_Height         ;(from cons. of wave power)
;   Wave_Energy
;   Wave_Power

;   Max_Orbital_Velocity

;   Surf_Zone
;   Breaker_Zone

;   Make_Spur_Plot   ;************* 2/26/05

;--------------------
;   Procedures
;--------------------
;   Refract_Wave   (in extras.pro)

;*******************************************************************
pro Close_Windows

while (!d.window ne -1) do wdelete, !d.window

end;  Close_Windows
;******************************************************************
function New_String, number

;------------------------------------
;If type is BYTE, convert to INTEGER
;------------------------------------
code = size(number, /TYPE)
if (code eq 1) then num=fix(num) else num=number

RETURN, strtrim(string(num), 2)
end;  New_String
;*******************************************************************
function Gravity

RETURN, 9.81d  ;(m/s^2)
end;  Gravity
;*******************************************************************
function Density, substance

;---------------------------------------------------------
;Notes:  These values are given on pp. 213-25 by Martinez
;        and Harbaugh (1993).  Units are (kg / m^3).
;        NB!  The value they give on p. 213 for seawater
;        is wrong.  (It should be about 1025 vs. 1146.)
 
;        Published densities for air range from 1.225
;        to 1.2929 kg/m^3. 
;---------------------------------------------------------
substance = strlowcase(substance)

case (substance) of
    'air'       : rho = 1.275d  ;(near sea level)
    'water'     : rho = 1000d 
    'seawater'  : rho = 1025d  ;****************
    'quartz'    : rho = 2650d
    'sand'      : rho = 2650d
    'limestone' : rho = 2710d
    'dolomite'  : rho = 2876d
    'clay'      : rho = 2500d  ;(2200 - 2750)
    'shale'     : rho = 2500d
    'lignite'   : rho = 1100d  ;(700 - 1500)
    'muscovite' : rho = 2800d  ;(2760 - 2880)
    'coal'      : rho = 1400d  ;(1300 - 1500)
    'feldspar'  : rho = 2550d  ;(2540 - 2570)
    'garnet'    : rho = 4000d  ;(3500 - 4300)
    'magnetite' : rho = 5180d
    'corundum'  : rho = 4020d
    ;---------------------------------------------
    'zircon'    : rho = 4680d
    'pyrite'    : rho = 5020d
    'gold'      : rho = 17000d ;(15000 - 19300)
    ;---------------------------------------------
    else        : begin
                  print,'Case found no matches.'
                  rho = -1d
                  end
endcase

RETURN, rho
end;  Density
;*******************************************************************
function X_Coordinates, nx, dx, NY=ny

;----------------------------------------------------------------
;Notes:  x is oriented perpendicular to coastline.
;        y is approximately along the coastline (x=0),
;        although coastline can be any curve.

;        7/20/03. Modified for new coordinate system.
;        Put coast on left-hand side.  For Barrow, AK, we'll
;        need to rotate DEM to put south at the top.
;----------------------------------------------------------------

;---------------------
;Start with 1D vector
;---------------------
x = dx * dindgen(nx)

;----------------------------------
;Option to return x values as grid
;----------------------------------
if (keyword_set(NY)) then begin
    x = x # (dblarr(ny) + 1d)
endif

RETURN, x
end;  X_Coordinates
;*******************************************************************
function Y_Coordinates, ny, dy, NX=nx

;-------------------------------------
;Notes:  See notes for X_Coordinates.
;-------------------------------------

;---------------------
;Start with 1D vector
;---------------------
y = dy * dindgen(ny)

;----------------------------------
;Option to return y values as grid
;----------------------------------
if (keyword_set(NX)) then begin
    y = (dblarr(nx) + 1d) # y
endif

RETURN, y
end;  Y_Coordinates
;*******************************************************************
function Test_Bathymetry, DX=dx, DY=dy, NX=nx, NY=ny, $
              SLOPE=slope, NDRY=ndry, $
              ;--------------------------------------------
              PLANE1=PLANE1, PLANE2=PLANE2, BRUN=BRUN, $
              DUCK=DUCK, RIP_DUCK=RIP_DUCK, SPURS=SPURS, $
              ;*** SPURS2=SPURS2, $
              GAUSS_CHAN=GAUSS_CHAN, GAUSS4=GAUSS4, $
              CHANNEL=CHANNEL, BAY=BAY, SINE=SINE, $
              ;--------------------------------------------
              ADD_HILL=ADD_HILL, ADD_PIT=ADD_PIT, $
              ADD_ISLAND=ADD_ISLAND, $
              ;--------------------------------------------
              M1=m1, M2=m2, XC=xc, XB=xB, XT=xT, $
              FB=fB, FT=fT, LS=Ls

;----------------------------------------------------
;Notes:  Grid is 20 km on a side by default
;        x-axis points toward sea,
;        y-axis points along shore

;        Later incorporate the Save_Island routine
;        that is in extras.pro.
;----------------------------------------------------
FORWARD_FUNCTION X_Coordinates, Y_Coordinates

;----------------------------
;Boolean keyword inheritance
;----------------------------
PLANE1     = keyword_set(PLANE1)
PLANE2     = keyword_set(PLANE2)
BRUN       = keyword_set(BRUN)
GAUSS_CHAN = keyword_set(GAUSS_CHAN)
GAUSS4     = keyword_set(GAUSS4)
DUCK       = keyword_set(DUCK)
RIP_DUCK   = keyword_set(RIP_DUCK)
CHANNEL    = keyword_set(CHANNEL)
SPURS      = keyword_set(SPURS)
;** SPURS2     = keyword_set(SPURS2)
BAY        = keyword_set(BAY)
SINE       = keyword_set(SINE)
;-----------------------------------
ADD_HILL   = keyword_set(ADD_HILL)
ADD_PIT    = keyword_set(ADD_PIT)
ADD_ISLAND = keyword_set(ADD_ISLAND)
;-------------------------------------------------
if NOT(keyword_set(DX)) then dx = 15d   ;[meters]
if NOT(keyword_set(DY)) then dy = 15d   ;[meters]
if NOT(keyword_set(NX)) then nx = 100L
if NOT(keyword_set(NY)) then ny = 100L
if NOT(keyword_set(NDRY)) then ndry = 3L  ;[# dry cols]

;---------------------------------------------------
;This is very important as it partially determines
;where the waves will break, and that may not be in
;the domain, depending on nx, ny, dx & dy.
;---------------------------------------------------
if NOT(keyword_set(SLOPE)) then begin
    slope=-0.025d
endif else begin
    if (slope gt 0) then slope = (-1d * slope)
endelse

;---------------------------
;Define x and y coordinates
;---------------------------
xx = X_Coordinates(nx, dx, NY=ny)   ;(axis toward sea; right)
yy = Y_Coordinates(ny, dy, NX=nx)   ;(axis along shore; up)
z  = dblarr(nx, ny)

;----------------------------------------
;Shift xx because of dry pixels, so that
;zero value occurs for first wet pixel
;----------------------------------------
xx = xx - (ndry * dx)
xx[0:ndry-1L] = 0d

;-----------------------------
;Inclined plane with contours
;parallel to shore
;-----------------------------
if (PLANE1) then z = slope * xx

;-----------------------------
;Inclined plane at 45 degrees
;-----------------------------
if (PLANE2) then begin
    a = 0.5d * slope
    b = 0.5d * slope
    z = (a * xx) + (b * yy)
endif

;----------------------------------------
;Brun (or Dean ??) "equilibrium" profile
;----------------------------------------
;NB!  b prevents infinite slope at x=0.

;If (z0 eq 0) then z[0]=0
;----------------------------------------
if (BRUN) then begin
    xmax = max(xx)
    b    = 1d    ;[meters, horizontal offset]
    z0   = 4d    ;[meters, highest shore above sea-level]
    p    = (2d / 3d)
    a    = xmax / (b^p - (xmax + b)^p)
    z    = slope * a * (b^p - (xx + b)^p) + z0
endif

;------------------------------------------
;Case of a plane with one Gaussian channel
;------------------------------------------
;Maybe channel should only extend for some
;distance and then "blend into" plane
;------------------------------------------
if (GAUSS_CHAN) then begin
    p1   = slope * xx
    ymax = max(yy)
    ;*** a    = -120d / ymax^2d
    a    = -80d / ymax^2d        ;(2/13/05)
    y0   = (ymax / 2d)
    b    = 0.01d
    ;b    = 0.05d
    ;b    = 0.1d   
    p2   = (1d + b * exp(a * (yy-y0)^2d))
    ;---------------------------------------------------
    ;a2   = -0.007d
    ;p2   = (1d + b * exp(a * (yy-y0)^2d) * exp(a2 * xx))
    ;---------------------------------------------------
    z    = p1 * p2 
endif

;------------------------------------------
;Case of a plane with one channel that is
;of the form exp(-x^4); flatter bottom
;------------------------------------------
if (GAUSS4) then begin    ;(2/13/05)
    p1   = slope * xx
    ymax = max(yy)
    a    = -2000d / (ymax/2d)^4d
    y0   = (ymax / 2d)
    b    = 0.01d       ;(This works, for some settings.)
    ;b    = 0.05d
    ;b    = 0.1d   
    p2   = (1d + b * exp(a * (yy-y0)^4d))
    z    = p1 * p2 
endif

;-------------------------------------
;Simulated spur-and-groove bathymetry
;-------------------------------------
ASPURS = 0b
if (ASPURS) then begin
    ;------------------------------------------
    ;These values assume that dx=25 and nx=100
    ;Top & bottom of slope should occur for:

    ;   xT = xc - (3/b),   f(xT) = fT
    ;   xB = xc + (3/b),   f(xB) = fB
    ;------------------------------------------
    fT = -8d     ;[meters, elev. at top of slope]
    fB = -20d     ;[meters, elev. at toe of slope]
    ;---------------------------------------------------------
    ;m1 seems to be between 1/45 and 1/65
    ;---------------------------------------------------------
    ;*** p  = 0.8d
    p  = 1d
    q  = 1d
    ;------------
    xc = 1250d
    xf = 150d       ;m1 = 1/70
    ;------------
    ;xc = 1200d
    ;xf = 200d       ;m1 = 1/70
    ;------------
    xT = xc - xf
    xB = xc + xf
    b  = (3d / xf)    ;[xf = 3/b]
    ;-----------------
    m1 = -fB / xB^q
    m2 = (fT + (m1 * xT^q)) / ((1d/p) * (xT+1d)^p)
    ;---------------------------------
    f1 = -1d * m1 * xx^q
    f2 = (m2/p) * ((xx+1d)^p) * (1d - tanh(b*(xx-xc)))/2d
    ;-----------------------------------------
    xmax = max(xx)
    a1   = (-1d * 0.02d / xmax)
    if NOT(keyword_set(LS)) then $
        Ls   = 500d  ;[meters, spur wavelength]  ;(should be 100)
    b1   = (2d * !dpi / Ls)
    f3   = (sin(b1 * yy) + 1d)/2d
    f4   = exp(a1*(xx-(1d*xc))^2d)
    ;----------------------------------
    z  = f1 + (f2 * (1d - (f3 * f4)))
    ;----------------------------------

    print,'m1 = ', m1
    print,'m2 = ', m2
    print,'xc = ', xc
    print,'b  = ', b
    print,'xT = ', xT
    print,'xB = ', xB
    print,'fT = ', fT
    print,'fB = ', fB
    print,' '
endif

;-------------------------------------
;Simulated spur-and-groove bathymetry
;-------------------------------------
if (SPURS) then begin
    ;------------------------------------------
    ;These values assume that dx=25 and nx=100
    ;Top & bottom of slope should occur for:

    ;   xT = xc - (3/b),   f(xT) = fT
    ;   xB = xc + (3/b),   f(xB) = fB
    ;------------------------------------------
    fT = -9d     ;[meters, elev. at top of slope]
    fB = -20d     ;[meters, elev. at toe of slope]
    ;---------------------------------------------------------
    ;m1 seems to be between 1/45 and 1/65
    ;---------------------------------------------------------
    ;p  = 0.93d
    ;------------
    xc = 1200d
    xf = 150d
    ;------------
    xT = xc - xf
    xB = xc + xf
    b  = (3d / xf)    ;[xf = 3/b]
    ;--------------
    m1 = (-fB / xB)
    xm = (2d * xT)
    a  = (fT + (m1*xT)) / (xT * (xm-xT))
    m2 = (a * xm)
    if (m2 gt m1) then STOP
    ;---------------------------------
    f1 = -1d * m1 * xx
    f2 = (a*xx*(xm-xx)) * (1d - tanh(b*(xx-xc)))/2d
    ;*** f2 = (a*(xx+1d)^p - a) * (1d - tanh(b*(xx-xc)))/2d
    ;*** f2 = tanh(m2*xx) * (1d - tanh(b*(xx-xc)))/2d

    ;-----------------------------------------
    xmax = max(xx)
    a1   = (-1d * 0.02d / xmax)
    if NOT(keyword_set(LS)) then $
        Ls   = 600d  ;[meters, spur wavelength]  ;(should be 100)
    b1   = (2d * !dpi / Ls)
    f3   = (cos(b1*yy) + 0.25d * cos(2d*b1*yy)) - 0.25d
    ;** f3   = sin(b1 * yy)
    f3   = (f3 + 1d) / 2d

    f4   = exp(a1*(xx-(1d*xc))^2d)
    ;----------------------------------
    z  = f1 + (f2 * (1d - (f3 * f4)))
    ;** z  = (z - 0.1d)
    ;----------------------------------

    print,'m1 = ', m1
    print,'m2 = ', m2
    print,'xc = ', xc
    print,'a  = ', a
    print,'b  = ', b
    print,'xT = ', xT
    print,'xB = ', xB
    print,'fT = ', fT
    print,'fB = ', fB
    print,' '
endif

;-------------------------------------
;Simulated spur-and-groove bathymetry
;-------------------------------------
NSPURS = 0b
if (NSPURS) then begin
    ;------------------------------------------
    ;These values assume that dx=25 and nx=100
    ;Top & bottom of slope should occur for:
    ;   xT = xc - (3/b),   f(xT) = fT
    ;   xB = xc + (3/b),   f(xB) = fB
    ;------------------------------------------
    fT = -5d     ;[meters, elev. at top of slope]
    fB = -20d     ;[meters, elev. at toe of slope]
    ;---------------------------------------------------------
    ;m1 seems to be between 1/45 and 1/65
    ;To have m3 > 0,  we need fB < -m1*xc,
    ;                 or abs(fB) > m1*xc
    ;To have m2 < m1, we need fB > -2*m1*xc,
    ;                 or abs(fB) < 2*m1*xc
    ;So we set m1 = (-fB / (1.2 * xc))
    ;NB! (20 / (1.2 * 1000)) = (1/60)
    ;---------------------------------------------------------
    p = 0.5d
    ;xc = 1200d
    ;m1 = 1d/62d   ;[xc * m1 = 19.35; compare to fB]
    xc = 1300d
    m1 = 1d/70d   ;[xc * m1 = 18.57; compare to fB]
    ;-----------------------------------------------
    m2 = m1 + (fT / ((2d*xc) + (fB/m1)))  ;[unitless]
    m3 = (-1.5d * m2) / (1d + (fB/(m1*xc)))
    m3b = (1.5d * m2) / (1d + (fT/(xc*(m1-m2))))
         ;[unitless, slope of "reef slope"]
    ;---------------------------------------------------------
    ;xc = 1400d
    ;m1 = fB / (-1.05d * xc)  ;[unitless, volcanic cone slope]
    ;m2 = m1 + (fT / ((2d*xc) + (fB/m1)))  ;[unitless]
    ;m3 = (-1.5d * m2) / (1d + (fB/(m1*xc))) 
         ;[unitless, slope of "reef slope"]
    ;---------------------------------------------------------
    ;m1 = 1d/70d      ;[unitless, volcanic cone slope]
    ;xc = 1400d       ;[meters, dist. to top of "reef slope"]
    ;m2 = m1 + (fT / ((2d*xc) + (fB/m1)))  ;[unitless]
    ;m3 = (-1.5d * m2) / (1d + (fB/(m1*xc))) 
         ;[unitless, slope of "reef slope"]
    ;---------------------------------------------------------
    ;m1 = 1d/50d      ;[unitless, volcanic cone slope]
    ;** m2 = 1d/80d      ;[unitless, slope of coral growth]
    ;m2 = 1d/70d      ;[unitless, slope of coral growth]
    ;xc = -0.5d * ((fT/(m1-m2)) + (fB/m1))
    ;m3 = (1.5d * m2) / (1d + (fB/(m1*xc))) 

            ;[unitless, slope of "reef slope"]
    ;---------------------------------------------------------
    b  = (2d * m3) / (m2 * xc)  ;[1/meters]
    xT = xc - (3d/b)
    xB = xc + (3d/b)
    ;-----------------------------------------------------
    f1 = -1d * m1 * xx
    p  = 1d

    f2 = (m2/2d) * sqrt(xx) * (1d - tanh(b*(xx-xc)))^p
    ;-----------------------------------------
    z  = (f1 + f2)
    ;-----------------------------------------
    print,'m1 = ', m1
    print,'m2 = ', m2
    print,'m3 = ', m3
    print,'m3b = ', m3b
    print,'xc = ', xc
    print,'b  = ', b
    print,'xT = ', xT
    print,'xB = ', xB
    print,'fT = ', fT
    print,'fB = ', fB
    print,' '
endif



;-----------------------------------------
;Old simulated spur-and-groove bathymetry
;-----------------------------------------
OLD_SPURS = 0b

if (OLD_SPURS) then begin
    xmax = max(xx)
    a    = (10d / xmax)
    Ls   = 10d  ;[meters, spur wavelength]  ;(should be 80 ??)
    b    = (2d * !dpi / Ls)
    m    = 0.03d    ;[slope near shore and at depth]
    p1   = (1d - tanh(a*xx - 5d)) / 2d
    p1   = p1 - (m * xx) - 1d
    p2   = (sin(b * yy) - 1d)
    p3   = exp(-0.5d * (a*xx - 4d)^2d)
    ;--------------------------------

    z    = (23d * p1) + (10d * p2 * p3)
endif

;--------------------------------
;Rip channel (Noda et al., 1974)
;--------------------------------
if (CHANNEL) then begin
    p    = (1d / 3d)
    lam  = 80d        ;[meters, length of periodic beach]
    ;** lam  = 200d
    ;** lam  = 100d
    a    = 20d        ;[meters, amplitude of bottom variation]
    beta = 30d        ;[degrees, angle of channel to beach normal]
    beta = beta * (!dpi / 180d)  ;[radians]
    ;---------------------------------------------------
    f1   = a * exp(-3d * (xx/20d)^p)
    f2   = sin((!dpi / lam) * (yy - (xx * tan(beta))))
    f2   = f2^10d
    ;-----------------------------------
    z    = slope * xx * (1d + (f1 * f2))
endif

;-------------------------------------
;Duck, North Carolina (approximation)
;-------------------------------------
if (DUCK OR RIP_DUCK) then begin
    xc    = 80d        ;[meters, location of longshore bar]
    beta1 = 0.075d     ;[beach slope angle, near shore]
    beta2 = 0.0064d    ;[slope angle offshore of bar]
    b1    = tan(beta1)
    g1    = tan(beta1) / tan(beta2)
    a1    = 2.97d   ;[meters]
    a2    = 1.5d    ;[meters]
    ;---------------------------------------------
    p1    = (a1 - (a1 / g1)) * tanh(b1 * xx / a1)
    p2    = (b1 * xx / g1)
    p3    = -1d * a2 * exp(-5d * ((xx-xc)/xc)^2d)
    ;---------------------------------------------
    z     = -1d * (p1 + p2 + p3)
    ;----------------------------
    slope = -1d * tan(beta1)    ;(for dry land part)
endif

;-----------------------------------------------------
;Duck profile, with sinusoidal longshore perturbation
;(Yu and Slinn, 2003).  Flow field depends on a, Lr
;and the incoming wave angle.
;-----------------------------------------------------
if (RIP_DUCK) then begin
    a  = 0.1d      ;[meters, depth of rip channels]
    Lr = 256d      ;[meters, spacing of rip channels]
    p1 = a * cos(2d * !dpi * yy / Lr)
    p2 = exp(-5d * ((xx-xc)/xc)^2d)
    z  = z * (1d + (p1 * p2))
endif
 
;-------------
;A simple bay
;-------------
if (BAY) then begin
    ;------------------------------------------------
    ;Note: Asymmetry in Rainbow color tables makes
    ;phi image appear asymmetric and its not.
    ;------------------------------------------------
    ymax = max(yy, min=ymin)
    b    = (!dpi / ymax)
    a    = 0.01d
    p1   = (a * sin(yy * b) + 1d)

    ;---------------------------------------
    z  = (slope * xx * p1)
    z  = (z < 0d)   ;(Set pos values to zero.)
endif

;-----------------------
;A sinusoidal coastline
;-----------------------
if (SINE) then begin
    ;-----------------------------------------------
    ;Setting z=0 shows that coastline is sinusoidal
    ;and offset from top of grid by a bit.
    ;-----------------------------------------------
    ymin = min(yy, max=ymax)
    yy2  = (yy - ymin)/(ymax - ymin)  ;(rescale)
    yy2  = yy2 * (5d * !dpi)

    ;--------------------------------
    ;These three constants must all
    ;be scaled by the slope so as to
    ;preserve the look of the plot.

    ;--------------------------------
    b  = slope             ;(was 0.005d)
    c1 = 800d  * slope     ;(was 4d)
    z0 = 1100d * slope     ;(was 5.5d)
    ;------------------------------------
    z  = (b * xx) - (c1*sin(yy2)) + z0
    z  = (z < 0d)   ;(Set pos values to zero.)
endif

;---------------------------
;Add a Gaussian Hill or Pit
;---------------------------
factor = 1d
if (ADD_PIT) then begin
    ADD_HILL = 1b
    factor = -1d
endif
;----------------------------
if (ADD_ISLAND) then begin
    ADD_HILL = 1b
    factor = 2d
endif
;----------------------------
if (ADD_HILL) then begin
    xmin  = min(xx, max=xmax)
    ymin  = min(yy, max=ymax)
    x0    = (xmax + xmin) / 2d
    y0    = (ymax + ymin) / 2d
    ;*** print,'x0, y0 = ',x0,y0

    ;-----------------------------
    ;Also used for ADD_PIT option
    ;but w/ factor < 1.
    ;-----------------------------
    zmin  = min(z, max=zmax)
    ;*** a     = 0.7d
    a     = 0.05d
    f0    = a * (abs(zmin + zmax) / 2d)
    f0    = (factor * f0)
    ;--------------------------------------
    ;sigma = "width at half maximum", set
    ;equal to 1/8 of the total range of x
    ;--------------------------------------
    sigma = (xmax - xmin) / 8d
    rsqr  = (xx - x0)^2d + (yy - y0)^2d
    f     = f0 * exp(-rsqr / (2d * sigma^2d))
    z     = z + f

    ;------------------------
    ;Set scale factor and f0
    ;------------------------
    ;scale = 5000d  &  f0=10d  ;(cool)
    ;scale = 5000d  &  f0=50d  ;(cooler)
    ;scale = 3000d  &  f0=80d
    ;scale = 3000d  &  f0=85d   ;(perfect)

endif

;----------------------------------------------
;This part is meant to help with shoreline BCs
;----------------------------------------------
;Make all values the same in first wet column.

;----------------------------------------------
if NOT(PLANE1 OR DUCK OR BRUN) then begin
    z[1,*] = max(z[1,*])    ;(neg. value closest to zero)
endif

;--------------------------------------------
;Add several dry columns on land as a plane.
;Default for ndry is 10; min should be 1.
;--------------------------------------------
z0 = abs(slope) * ndry * dx
z  = shift(z, ndry, 0)

z[0:ndry-1L, *] = z0 + (slope*xx[0:ndry-1L, *])

RETURN, z

end;  Test_Bathymetry
;*******************************************************************
function Water_Depth, bathy, phi

d = (-1d * bathy) > 0d

;-------------------------
;Set d=NaN where d > 0d ?
;-------------------------
;Led to infinite loop when
;solving for Wavelengths.
;-------------------------
;d = (-1d * bathy)
;w = where(d gt 0, nw)

;if (nw ne 0) then d[w]=!values.d_nan

;---------------------------
;Set d=0 where phi has NaNs
;---------------------------
;w = where(finite(phi) ne 1, nw)
;if (nw ne 0) then d[w]=0d

;------------------------------
;Inherit NaN values from phi ?
;------------------------------
;w = where(finite(phi) ne 1, nw)
;if (nw ne 0) then d[w]=!values.d_nan 

RETURN, d
end;  Water_Depth
;*******************************************************************
function Wave_Length, d, T, TOL=tol

;----------------------------------------------------------
;Note:  This routine uses a grid-based Newton-Raphson
;       iterative scheme to solve the dispersion relation
;       for wavelength, L, as a function of d and T.
;       T is not affected by refraction.
;----------------------------------------------------------
print,"Computing wavelengths by Newton's method..."

;------------------------------
;Set tolerance for convergence
;------------------------------
if NOT(keyword_set(TOL)) then tol = 0.001d

;--------------------------------
;Compute local constants (grids)
;--------------------------------
g = Gravity()
K = (g * T^2) / (2d * !dpi)
B = 2d * !dpi * d

;--------------------------------
;Get dimensions of depth grid, d
;--------------------------------
s = size(d, /dimensions)
nx = s[0]
ny = s[1]

;-------------------------------
;Initialize wave length grid, L
;-------------------------------
L0 = tol   ;(meters)
L  = dblarr(nx, ny) + L0

;-----------------------------
;Iterate entire grid to get L
;-----------------------------
DONE = 0b
while NOT(DONE) do begin
    ;-------------------------------
    ;Use grid-based Newton's method
    ;-------------------------------
    last_L = L
    numer  = L - (K * tanh(B/L))
    denom  = 1d + (K * B * (1d/(cosh(B/L)*L))^2d)
    L = L - (numer/denom)

    ;-----------------------------
    ;Compute difference from goal
    ;Note: gap = abs(numer/denom)
    ;-----------------------------
    gap = abs(L - last_L)
    gmin = min(gap, max=gmax, /NAN)
    print,'     gmin, gmax = ',gmin, gmax

    ;------------------
    ;Are we done yet ?
    ;------------------
    w = where(gap gt tol, nw)
    print,'     # remaining = ',nw
    DONE = (nw eq 0)

    ;-----------------------------
    ;Make sure L doesn't get wild
    ;-----------------------------
    ;Lmax = max(L, min=Lmin, /NAN)
    ;if (Lmax gt 1000.0) OR (Lmin lt 0) then DONE=1b
    ;print,'Lmin, Lmax = ',Lmin,Lmax

endwhile

print,'Finished computing wavelengths.'
print,' '

RETURN, L
end;  Wave_Length
;*******************************************************************
function Wave_Length2, d, u, v, a, T, TOL=tol, $
                       INIT_L=INIT_L, SILENT=SILENT

;----------------------------------------------------------
;Note:  This routine uses a grid-based Newton-Raphson
;       iterative scheme to solve the dispersion relation
;       for wavelength, L, as a function of d, T, u, v
;       and wave angle, theta.  An earlier version had
;       good convergence properties but did not include
;       u, v and theta (or a).  Other attempts to compute
;       k by Newton iteration were not reliable, so went
;       back to an f(L) that is very similar to the one
;       we had before but with u,v,a included.

;       Note that T is not affected by refraction.

;       Newton's method solves an equation f(L)=0, by
;       iterating the equation:
;             L(n+1) = L(n) + [f(L)/f'(L)]
;       until the difference between L(n+1) and L(n)
;       drops below the specified tolerance for all
;       pixels in the grid.  This usually takes about

;       10 iterations.  Max # of iterations is nmax.

;       Some of the equations used here are:

;       w     = 2 * pi / T
;       sig^2 = g * k * tanh(k * d)
;       B     = [u*cos(a) + v*sin(a)]

;       sig + (k * B) = w
;       sig^2 = (w - (k*B))^2    
;----------------------------------------------------------
SILENT = keyword_set(SILENT)
if NOT(SILENT) then $
    print,"Computing wavelengths by Newton's method..."

;------------------------------
;Set tolerance for convergence
;------------------------------
;*** if NOT(keyword_set(TOL)) then tol = 0.001d
;*** if NOT(keyword_set(TOL)) then tol = 0.000001d  ;[2/20/05]
if NOT(keyword_set(TOL)) then tol = 0.00000001d  ;[2/20/05]

;--------------------------------
;Get dimensions of depth grid, d
;--------------------------------
s = size(d, /dimensions)
nx = s[0]
ny = s[1]

;-------------------------------
;Initialize wave length grid, L
;----------------------------------
;Convergence is faster if we start
;from the L of the last timestep
;----------------------------------
if NOT(keyword_set(INIT_L)) then begin
    INIT_L = tol   ;(meters)

    L  = dblarr(nx, ny) + INIT_L
endif else begin
    L = INIT_L
endelse

;--------------------------------
;Compute local constants (grids)
;NB!  These must not include L!
;--------------------------------
g     = Gravity()
B     = (u * cos(a)) + (v * sin(a))
twopi = (2d * !dpi)
w     = (twopi / T)
M     = (T^2d) / twopi    ;[equal to twopi / w^2]

;-----------------------------
;Iterate entire grid to get L
;-----------------------------
n_tries = 0L
nmax    = 40L
DONE    = 0b
while NOT(DONE) do begin
    ;-------------------------------
    ;Use grid-based Newton's method
    ;-------------------------------
    last_L = L

    ;-----------------------------
    ;These must be inside of loop
    ;-----------------------------
    t1 = g * tanh(twopi * d / L)
    t2 = 2d * B
    t3 = twopi * (B^2d) / L
    ;-------------------------------------
    d1 = (T / L)^2d
    d2 = g * d / (cosh(twopi * d / L)^2d)
    ;--------------------------------------------
    numer = L - (M * (t1 + t2 - t3))
    denom = 1d + d1*(d2 - (B^2d))
    
    ;--------------------
    ;Get next value of L
    ;--------------------
    L = L - (numer/denom)

    ;-----------------------------
    ;Compute difference from goal

    ;Note: gap = abs(numer/denom)
    ;-----------------------------
    gap = abs(L - last_L)
    gmin = min(gap, max=gmax, /NAN)
    if NOT(SILENT) then $
         print,'     gmin, gmax = ',gmin, gmax

    ;------------------
    ;Are we done yet ?
    ;------------------
    n_tries = (n_tries + 1L)
    w = where(gap gt tol, nw)
    if NOT(SILENT) then $
        print,'     # remaining = ',nw
    DONE = (nw eq 0) OR (n_tries gt nmax)

    ;-------------------------------
    ;Make sure L doesn't get wild ?
    ;-------------------------------
    ;Lmax = max(L, min=Lmin, /NAN)
    ;if (Lmax gt 1000.0) OR (Lmin lt 0) then DONE=1b
    ;print,'Lmin, Lmax = ',Lmin,Lmax

endwhile

;----------------------------
;Failure-to-converge message
;----------------------------
if (n_tries gt nmax) then begin
    nmstr = strtrim(string(nmax), 2)
    print,'************************************************'
    print,'ERROR:  Newton method iteration failed to'
    print,'        converge after ' + nmstr + ' iterations.'
    print,'************************************************'
    print,' '
endif

tstr = strtrim(string(tol), 2)
nstr = strtrim(string(n_tries), 2)

if NOT(SILENT) then begin
    print,'Tolerance used was:       ' + tstr
    print,'Number of iterations was: ' + nstr
    print,'Finished computing wavelengths.'

    print,' '
endif

RETURN, L
end;  Wave_Length2 
;*******************************************************************
pro Wave_Length2_Test, PLANE1=PLANE1, PLANE2=PLANE2, $
                       SLOPE=SLOPE, BAY=BAY, SINE=SINE, $
                       ADD_HILL=ADD_HILL, ADD_PIT=ADD_PIT, $
                       ADD_ISLAND=ADD_ISLAND

;--------------------------------
;Test & demo bathymetry keywords
;--------------------------------
PLANE1     = keyword_set(PLANE1)
PLANE2     = keyword_set(PLANE2)
BAY        = keyword_set(BAY)
SINE       = keyword_set(SINE)
ADD_HILL   = keyword_set(ADD_HILL)
ADD_PIT    = keyword_set(ADD_PIT)
ADD_ISLAND = keyword_set(ADD_ISLAND)
;---------------------------------------------------
if NOT(keyword_set(SLOPE)) then begin
    slope = -0.02d
endif else begin
    if (slope gt 0) then slope = (-1d * slope)
endelse

;----------------------------
;Generate test bathymetry
;(Defined in longshore.pro)
;----------------------------
dx = 2d
dy = 2d
nx = 100L
ny = 100L
if (PLANE1 OR PLANE2 OR BAY OR SINE) then begin
    z = Test_Bathymetry(dx, dy, nx, ny, PLANE1=PLANE1, $
             PLANE2=PLANE2, SLOPE=SLOPE, BAY=BAY, $
             SINE=SINE, ADD_HILL=ADD_HILL, $
             ADD_PIT=ADD_PIT, ADD_ISLAND=ADD_ISLAND)

    ;----------------------------------------
    ;Must rotate if BOTTOM keyword is set
    ;----------------------------------------
    BOTTOM = 1b
    if (BOTTOM) then z = rotate(z, 1)

endif

;----------------------
;Get the depth grid ??
;----------------------
d = Water_Depth(z)

;------------------------------------
;Compute k for the case where u=v=0.
;In this case angle doesn't matter,
;so set it to zero as well.
;------------------------------------
u = 0d
v = 0d
a = 0d
T = 10d

;-----------------------
;Compute via new method
;-----------------------
L = Wave_Length2(d, u, v, a, T)

;** k = Wave_Number2(d, u, v, a, T)
;** L = 2d * !dpi / k

;-------------------------
;Compute L via old method
;-------------------------
L2 = Wave_Length(d, T)

;----------------------------
;Compare old and new methods
;----------------------------
w = where(abs(L - L2) gt 0.001d, nw)
print, 'nw = ', nw

end;  Wave_Length2_Test
;*******************************************************************
function Wave_Speed, d, L, SHALLOW=SHALLOW, DEEP=DEEP

print,'Computing wave speeds...'

DEEP    = keyword_set(DEEP)
SHALLOW = keyword_set(SHALLOW)
GENERAL = NOT(DEEP) AND NOT(SHALLOW)

g = Gravity()   ;(m/s^2)

;--------------------------------------
;General case Airy wave (Wiegel, 1964)
;Airy waves are sinusoidal.
;--------------------------------------
if (GENERAL) then begin
    k = Wave_Number(L)
    C = sqrt((g / k) * tanh(k * d))
endif

;-------------------
;Shallow-water wave
;-------------------
if (SHALLOW) then C = sqrt(g * d)

;----------------
;Deep-water wave
;----------------
if (DEEP) then begin
    k = Wave_Number(L)
    C = sqrt(g / k)
endif

print,'Finished computing wave speeds.'
print,' '

RETURN, C
end;  Wave_Speed
;*******************************************************************
function Group_Velocity, C, d, L

FORWARD_FUNCTION Wave_Number

r  = 2d * Wave_Number(L) * d
Cg = (C / 2d) * (1d + (r / sinh(r)))

;--------------------
;Inherit NaNs from d
;--------------------
;w = where(finite(d) ne 1, nw)
;if (nw ne 0) then Cg[w] = d[w]

RETURN, Cg
end;  Group_Velocity
;*******************************************************************
function Wave_Speed_Ratio, k, d

;--------------------------------------------------
;Notes:  n = (Cg / C)
;        "r" is proportional to (d/L)
;        SINH(0)=0
;        SINH(x) goes to Infinity for large r

;        Let F(r) = (r / SINH(r))
;        F(0) = 1   and F(Infinity) = 0
 
;        So we have n = 1 for (d/L) small (SHALLOW)
;        and n = 1/2 for (d/L) large (DEEP)
;---------------------------------------------------        
r = 2d * k * d
n = 0.5d * (1d + (r / sinh(r)))

RETURN, n
end;    Wave_Speed_Ratio
;*******************************************************************
function Deep_Water, d, L

;-----------------------------------------------------------
;Notes:  Error in using wave speed formula for deep-water
;        waves (C = sqrt(g L / 2 pi)) is at most 3% if this
;        function returns true.
;        See Lighthill (1978) Waves in Fluids, p. 216-17.
;-----------------------------------------------------------


RETURN, (d gt (0.28 * L))
end;  Deep_Water
;*******************************************************************
function Shallow_Water, d, L

;----------------------------------------------------------
;Notes:  Error in using wave speed formula for deep-water
;        waves (C = sqrt(g d)) is at most 3% if this
;        function returns true.
;        See Lighthill (1978) Waves in Fluids, p. 216-17.
;----------------------------------------------------------
;*** RETURN, (d lt (L / 2.0))

RETURN, (d lt (0.07 * L))
end;  Shallow_Water
;*******************************************************************
function Wave_Number, L

;*** print,'Computing wave numbers...'

RETURN, (2d * !dpi) / L
end;  Wave_Number
;*******************************************************************
function Wave_Number2, d, u, v, a, T, TOL=tol

;----------------------------------------------------------
;Note:  This routine uses a grid-based Newton-Raphson
;       iterative scheme to solve the dispersion relation
;       for wave number, k, as a function of d, u, v,
;       theta (or a) and T.  Recall that T is not affected

;       by refraction.

;       NB!  As written, this routine has very poor
;       convergence properties as compared to the new

;       Wave_Length2 function.

;       Newton's method solves an equation f(k)=0, by
;       iterating the equation:

;             k(n+1) = k(n) + [f(k)/f'(k)]
;       until the difference between k(n+1) and k(n)
;       drops below the specified tolerance for all
;       pixels in the grid.
;----------------------------------------------------------
print,"Computing wave numbers by Newton's method..."

;------------------------------
;Set tolerance for convergence
;------------------------------
if NOT(keyword_set(TOL)) then tol = 0.001d

;--------------------------------
;Compute local constants (grids)
;--------------------------------
;NB! These cannot depend on k !!
;--------------------------------
g = Gravity()
w = (2d * !dpi / T)   ;(omega)

;--------------------------------
;Get dimensions of depth grid, d
;--------------------------------
s = size(d, /dimensions)
nx = s[0]
ny = s[1]

;-------------------------------
;Initialize wave number grid, k
;-------------------------------
;*** k0 = (1d / tol)   ;[1/meters]
;*** k0 = 1e-5
k0 = 1000d
k  = dblarr(nx, ny) + k0

;-----------------------------
;Iterate entire grid to get k
;-----------------------------
n_tries = 0L
DONE = 0b
while NOT(DONE) do begin

    ;-------------------------------
    ;Use grid-based Newton's method
    ;-------------------------------
    last_k = k

    ;---------------------------
    ;Method 1; poor convergence
    ;---------------------------
    ;n1 = k * d
    ;n2 = tanh(n1)
    ;n3 = sqrt(g * k * n2)
    ;n4 = (u * cos(a)) + (v * sin(a))
    ;---------------------------------
    ;d1 = n1 / (cosh(n1)^2d)
    ;-----------------------------------------
    ;numer = n3 + (k * n4) - w
    ;denom = ((g/2d) * (n2 + d1)/n3) + n4

    ;---------------------------
    ;Method 2
    ;---------------------------
    n1 = k * d
    n2 = tanh(n1)
    n3 = sqrt(g * n2)
    n4 = u * cos(a)
    n5 = v * sin(a)
    n6 = w / sqrt(k)
    ;------------------------
    d1 = (g / 2d) * d
    d2 = cosh(n1)^2d
    d3 = (n4 + n5) / (2d * sqrt(k))
    d4 = (0.5d * w / k^1.5d)
    ;-----------------------------------------
    numer = n3 + (sqrt(k) * (n4 + n5)) - n6
    denom = (d1 / (n3 * d2)) + d3 + d4

    ;--------------------
    ;Get next value of k
    ;--------------------
    k = k - (numer/denom)

    ;-----------------------------
    ;Compute difference from goal

    ;Note: gap = abs(numer/denom)
    ;-----------------------------
    gap  = abs(k - last_k)
    gmin = min(gap, max=gmax, /NAN)
    print,'     gmin, gmax = ',gmin, gmax

    ;------------------
    ;Are we done yet ?
    ;------------------
    n_tries = (n_tries + 1L)
    w = where(gap gt tol, nw)
    print,'     # remaining = ',nw
    DONE = (nw eq 0) OR (n_tries gt 30L)


    ;--------------------------------
    ;Make sure k doesn't get wild ?
    ;--------------------------------
    ;kmax = max(k, min=kmin, /NAN)
    ;if (kmax gt 1000.0) OR (kmin lt 0) then DONE=1b
    ;print,'kmin, kmax = ',kmin,kmax

endwhile

print,'Finished computing wave numbers.'
print,' '

RETURN, k

end;  Wave_Number2
;*******************************************************************
function Wave_Number3, d, U, V, theta, T, INIT_K=init_k, $
                       TOL=tol, PLOT=PLOT, SILENT=SILENT

;----------------------------------------------------------
;Note:  This routine uses a grid-based Newton-Raphson
;       iterative scheme to solve the dispersion relation
;       for wave number, k, as a function of d, T, u, v,
;       and wave angle, theta.  This version takes wave-
;       current interaction into account, and converges
;       rapidly since it is initialized with the values
;       of k at the last time step.

;       This may converge faster than the Wave_Length2
;       function due to different functional forms.

;       T is not affected by refraction.
;----------------------------------------------------------
SILENT = keyword_set(SILENT)

if NOT(SILENT) then begin
    print,"Computing wave number by Newton's method..."
endif

;------------------------------
;Set tolerance for convergence
;------------------------------
;*** if NOT(keyword_set(TOL)) then tol = 0.001d
if NOT(keyword_set(TOL)) then tol = 0.0000001d
;*** if NOT(keyword_set(TOL)) then tol = 0.0000000001d

;------------------------
;Compute local constants
;(Cannot depend on k.)
;------------------------
g = Gravity()
B = 2d * !dpi / T
C = sqrt(g) / 2d

;--------------------------------
;Get dimensions of depth grid, d
;--------------------------------
s  = size(d, /dimensions)
nx = s[0]
ny = s[1]

;-------------------------------
;Initialize wave number grid, k
;-------------------------------
if NOT(keyword_set(INIT_K)) then init_k = tol  ;[1/meters]
k = dblarr(nx, ny) + init_k

;-----------------------------
;Iterate entire grid to get k
;-----------------------------
repeat begin
    ;-------------------------------
    ;Use grid-based Newton's method
    ;-------------------------------
    last_k = k
    a      = (k * d)
    vterm  = (U * cos(theta)) + (V * sin(theta))
    numer  = sqrt(g * k * tanh(a)) + (k * vterm) - B
    denom  = C *((a * (1d/cosh(a))^2d) + tanh(a)) / sqrt(k * tanh(a))
    denom  = denom + vterm
    k = k - (numer / denom)

    ;-----------------------------
    ;Compute difference from goal
    ;Note: gap = abs(numer/denom)
    ;We're done when (nw eq 0).
    ;-----------------------------
    gap = abs(k - last_k)
    w   = where(gap gt tol, nw)

    ;------------------
    ;Print messages ??
    ;------------------
    if NOT(SILENT) then begin
        gmin = min(gap, max=gmax, /NAN)
        print,'     gmin, gmax = ',gmin, gmax
        print,'     # remaining = ',nw

    endif

endrep until (nw eq 0)

PLOT = keyword_set(PLOT)
if (PLOT) then Plot_Grid, k, /equalize

if NOT(SILENT) then begin

    print,'Finished computing wave number, k.'
    print,' '
endif

RETURN, k

end;  Wave_Number3
;*******************************************************************
function Wave_Frequency, T

print,'Computing wave frequency...'

RETURN, (2d * !dpi) / T
end;  Wave_Frequency
;*******************************************************************
function Intrinsic_Frequency, d, k

g = Gravity()

sigma = sqrt(g * k * tanh(k * d))

RETURN, sigma

end;  Intrinsic_Frequency
;*******************************************************************
function Wave_Angle, a0, k, d, A2=A2, DX=DX, DY=DY, $
                     LEFT=LEFT, RIGHT=RIGHT, $
                     BOTTOM=BOTTOM, TOP=TOP, $
                     PLOT=PLOT,  K_TEST=K_TEST, $
                     A_TEST1=A_TEST1, A_TEST2=A_TEST2

;----------------------------------------------------------
;Notes:  This routine computes a wave angle grid, theta
;        from a wave number grid, so that the curl of
;        the wave number vector is zero everywhere.
;        Note that dx and dy have no effect if they
;        are equal.  However, if the values in the k

;        grid or the angle values along the boundary
;        change too fast, then the method is unstable
;        and the argument of ASIN may be outside of the
;        closed interval [-1,1].  So dx and dy still
;        play a role in this sense.  It may also happen
;        that the given boundary values for theta may be
;        incompatible with the corresponding values of k.
;        The K_TEST succeeds for small values of theta0,
;        such as 0.1 and 0.2.


;        Theta is defined as the angle that the wave
;        number vector makes with the x-axis, so that
;        the x and y components of k are (k cos(theta))
;        and (k sin(theta)), respectively.

;        Note that since k is computed via the dispersion
;        relation, it is valid for all water depths, and
;        hence the wave angles are as well.

;        12/8/04.  If the LEFT keyword is set, then
;        the approach is to solve first for all of the
;        pixels below the diagonal and then to use a
;        slightly different differencing method to solve
;        for the pixels above the diagonal.

;        For the special case of planar d (& L & k),

;        the computed values agree perfectly with those
;        predicted by Snell's Law.  This was tested for
;        several different theta0 values.
;----------------------------------------------------------
;** FORWARD_FUNCTION Test_Bathymetry

PLOT    = keyword_set(PLOT)
K_TEST  = keyword_set(K_TEST)
A_TEST1 = keyword_set(A_TEST1)
A_TEST2 = keyword_set(A_TEST2)

print,'Computing wave angles...'

;---------------------
;Set keyword defaults
;---------------------
LEFT    = keyword_set(LEFT)
RIGHT   = keyword_set(RIGHT)
BOTTOM  = keyword_set(BOTTOM)
TOP     = keyword_set(TOP)
KEY_SUM = (LEFT + RIGHT + BOTTOM + TOP)
if (KEY_SUM eq 0b) then LEFT=1b
;-----------------------------------
if NOT(keyword_set(DX)) then dx=1d
if NOT(keyword_set(DY)) then dy=1d

;----------------------
;Set argument defaults
;----------------------
if (n_elements(k) eq 0) then begin
    nx = 50
    ny = 50
    ;------------------------------
    ;Set depth as a simple ramp,
    ;decreasing to the right
    ;This assumes that LEFT is set
    ;------------------------------
    dm = 30d

    ad = dm * reverse(dindgen(nx) / (nx-1d))
    T  = 8d  ;[seconds]
    b  = dblarr(ny) + 1d
    d  = (ad # b)

    if (K_TEST) then begin
        dm = 2d
        b = dist(2*nx,2*ny)
        d = b[nx:2*nx-1, ny:2*ny-1L]   ;[depth grid]
        d = dm * (d / max(d))
    endif

    ;--------------------
    ;Avoid depth of zero      ;*********************************
    ;--------------------
    d = (d + 1L)

    ;---------------------------------------
    ;If BOTTOM is set, must rotate grid
    ;so that depth increases toward bottom.
    ;NB!  Must have nx=ny for this to work.
    ;---------------------------------------
    if (BOTTOM) then d = rotate(d, 3)

    ;-----------------------------------
    ;Compute wavelength and wave number
    ;-----------------------------------
    L = Wave_Length(d, T)
    k = Wave_Number(L)

    ;------------------------------------
    ;Print min and max values of d, L, k
    ;------------------------------------
    dmin = min(d, max=dmax, /NAN)
    print,'(dmin, dmax) = ', dmin, dmax
    Lmin = min(L, max=Lmax, /NAN)
    print,'(Lmin, Lmax) = ', Lmin, Lmax
    kmin = min(k, max=kmax, /NAN)
    print,'(kmin, kmax) = ', kmin, kmax
endif

if (n_elements(a0) eq 0) then begin
    a0_rad = (60d * (!dpi/180d))
endif else begin
    a0_rad = (a0  * (!dpi/180d))
endelse

;-----------------------------------
;Get dimensions of wave number grid
;-----------------------------------
s  = size(k, /dimensions)
nx = s[0]
ny = s[1]

;-----------------------------------
;Create "index grids" for neighbors
;-----------------------------------
;CI = lindgen(nx,ny)
;LI = shift(CI,  1,  0)
;RI = shift(CI, -1,  0)
;TI = shift(CI,  0,  1)
;BI = shift(CI,  0, -1)

;-------------------------------------
;Initialize angle grid with boundary
;conditions along any one edge
;------------------------------------
ND = 9d   ;(nodata value)
a = dblarr(nx ,ny) + ND
if (LEFT)   then a[0,*]    = a0_rad
if (RIGHT)  then a[nx-1,*] = a0_rad

if (BOTTOM) then a[*,ny-1] = a0_rad
if (TOP)    then a[*,0]    = a0_rad
 
;------------------------------------
;Experimental: Algorithm still works
;but not if angles change too fast.
;------------------------------------

if (LEFT AND A_TEST1) then begin
    a[0,*] = dindgen(ny) * (!dpi/180d) / 2d
endif
if (BOTTOM AND A_TEST1) then begin
    a[*,ny-1] = dindgen(nx) * (!dpi/180d) / 2d
endif
;---------------------------------------------------
if (LEFT AND A_TEST2) then begin
    a[0,*] = (sqrt(dindgen(ny))*3d) * (!dpi/180d)
endif
if (BOTTOM AND A_TEST2) then begin
    a[*,ny-1] = (sqrt(dindgen(nx))*3d) * (!dpi/180d)
endif

;---------------------------------------------
;Recursively compute remaining angle values
;from BCs on the LEFT edge using BACKWARD
;differences for the y-derivatives
;---------------------------------------------
DONE = (1b - LEFT)
;*** DONE = 0b
while NOT(DONE) do begin
    LL = shift(a, 1, -1)
    LL[0,*] = ND
    LL[*,ny-1] = ND
    ;-------------------
    CL = shift(a, 1, 0)
    CL[0,*] = ND

    wC = where((a eq ND) AND (LL ne ND) AND (CL ne ND), nwC)

    if (nwC ne 0) then begin
        wLL = (wC+nx-1L)
        wCL = (wC-1L)
        ;--------------------------
        ;Assumed that dx = dy here
        ;--------------------------
        t1  = k[wCL] * cos(a[wCL])  ;[* dx/dy ???]
        t2  = k[wLL] * cos(a[wLL])  ;[* dx/dy ???]
        t3  = k[wCL] * sin(a[wCL])
        ;----------------------------
        arg = ((t1 - t2) + t3) / k[wC]

        ;----------------------------
        ;Force arg to be in range ?
        ;Doesn't seem to help.
        ;----------------------------
        ;arg = (-1d > arg) < 1d

        ;--------------------------------
        ;Is argument of ASIN in range ??
        ;--------------------------------
        ;wbad = where(abs(arg) gt 1d, nbad)
        ;if (nbad ne 0) then begin
        ;    print,'WARNING:  Argument to ASIN is out of range.'
        ;    print,'          Values in k grid or angle values'
        ;    print,'          along the boundary vary too fast.' 
        ;    print,'nbad = ', nbad
        ;    ;*** STOP
        ;endif

        ;------------------------
        ;Assign new angle values
        ;------------------------
        wOK = where(abs(arg) le 1d, nOK)
        if (nOK ne 0) then a[wC[wOK]] = asin(arg[wOK])
        ;-----------------------------------------------
        nbad = (nWC - nOK)
        if (nbad ne 0) then begin
            print,'WARNING:  Argument to ASIN is out of range.'
            print,'nbad = ', nbad
        endif
        ;-----------------
        DONE = (nOK eq 0)

    endif else begin
        DONE = 1b
    endelse
endwhile

;---------------------------------------------
;Recursively compute remaining angle values
;from BCs on the LEFT edge using FORWARD
;differences for the y-derivatives
;---------------------------------------------
DONE = (1b - LEFT)
;** DONE = 0b
while NOT(DONE) do begin
    UL = shift(a, 1, 1)
    UL[0,*] = ND
    UL[*,0] = ND
    CL = shift(a, 1, 0)
    CL[0,*] = ND

    wC = where((a eq ND) AND (UL ne ND) AND (CL ne ND), nwC)

    if (nwC ne 0) then begin
        wUL = (wC-nx-1L)
        wCL = (wC-1L)
        ;--------------------------
        ;Assumed that dx = dy here
        ;--------------------------
        t1  = k[wUL] * cos(a[wUL])  ;[* dx/dy ????]
        t2  = k[wCL] * cos(a[wCL])  ;[* dx/dy ????]
        t3  = k[wCL] * sin(a[wCL])
        ;----------------------------
        arg = ((t1 - t2) + t3) / k[wC]

        ;----------------------------
        ;Force arg to be in range ?
        ;Doesn't seem to help.
        ;----------------------------
        ;arg = (-1d > arg) < 1d

        ;--------------------------------
        ;Is argument of ASIN in range ??
        ;--------------------------------
        ;wbad = where(abs(arg) gt 1d, nbad)
        ;if (nbad ne 0) then begin
        ;    print,'WARNING:  Argument to ASIN is out of range.'
        ;    print,'          Values in k grid or angle values'
        ;    print,'          along the boundary vary too fast.' 
        ;    print,'nbad = ', nbad
        ;    ;*** STOP
        ;endif

        ;------------------------
        ;Assign new angle values
        ;------------------------
        wOK = where(abs(arg) le 1d, nOK)
        if (nOK ne 0) then a[wC[wOK]] = asin(arg[wOK])
        ;-----------------------------------------------
        nbad = (nWC - nOK)
        if (nbad ne 0) then begin
            print,'WARNING:  Argument to ASIN is out of range.'
            print,'nbad = ', nbad
        endif
        ;------------------
        DONE = (nOK eq 0)
    endif else begin
        DONE = 1b
    endelse

endwhile

;---------------------------------------------
;Recursively compute remaining angle values
;from BCs on the BOTTOM edge using BACKWARD
;differences for the x-derivatives.
;---------------------------------------------
DONE = (1b - BOTTOM)
;** DONE = 0b
;** DONE=1b
while NOT(DONE) do begin
    LL = shift(a, 1, -1)
    LL[0,*] = ND
    LL[*,ny-1] = ND
    ;---------------------
    LR = shift(a, -1, -1)      ;(for centered diff)
    LR[nx-1,*] = ND
    LR[*,ny-1] = ND
    ;---------------------
    CB = shift(a, 0, -1)
    CB[*,ny-1] = ND

    wC = where((a eq ND) AND (LL ne ND) AND (CB ne ND), nwC)

    if (nwC ne 0) then begin
        wLR = (wC + nx + 1L)       ;(for centered diff)
        wLL = (wC + nx - 1L)
        wCB = (wC + nx)
        ;--------------------------
        ;Assumed that dx = dy here
        ;-----------------------------------------
        t1  = k[wCB] * sin(a[wCB])   ;[* (dy/dx)]
        t2  = k[wLL] * sin(a[wLL])   ;[* (dy/dx)]
        t3  = k[wCB] * cos(a[wCB])
        t4  = k[wLR] * sin(a[wLR])
        ;-----------------------------------------
        arg = ((t1 - t2) + t3) / k[wC]

        ;-----------------------------------
        ;Use centered diffs, where possible
        ;-----------------------------------
        ;wR  = where(LR[wC] ne ND, nwR)
        ;if (nwR ne 0) then begin
        ;    arg[wR] = ((t4[wR] - t2[wR])/2d + t3[wR]) / k[wC[wR]]
        ;endif

        ;----------------------------
        ;Force arg to be in range ?
        ;Doesn't seem to help.
        ;----------------------------
        ;arg = (-1d > arg) < 1d

        ;--------------------------------
        ;Is argument of ACOS in range ??
        ;--------------------------------
        ;wbad = where(abs(arg) gt 1d, nbad)
        ;if (nbad ne 0) then begin
        ;    print,'WARNING:  Argument to ACOS is out of range.'
        ;    print,'          Values in k grid or angle values'
        ;    print,'          along the boundary vary too fast.' 
        ;    print,'nbad = ', nbad
        ;    ;*** STOP
        ;endif

        ;------------------------
        ;Assign new angle values
        ;------------------------
        wOK = where(abs(arg) le 1d, nOK)
        if (nOK ne 0) then a[wC[wOK]] = acos(arg[wOK])
        ;-----------------------------------------------
        nbad = (nWC - nOK)
        if (nbad ne 0) then begin
            print,'WARNING:  Argument to ASIN is out of range.'
            print,'nbad = ', nbad
        endif
        ;-----------------
        DONE = (nOK eq 0)
    endif else begin
        DONE = 1b
    endelse
endwhile

;---------------------------------------------
;Recursively compute remaining angle values
;from BCs on the BOTTOM edge using FORWARD
;differences for the x-derivatives.
;---------------------------------------------
DONE = (1b - BOTTOM)
;** DONE = 0b

;** DONE = 1b
while NOT(DONE) do begin
    LL = shift(a, 1, -1)      ;(for centered diff)
    LL[0,*] = ND
    LL[*,ny-1] = ND
    ;---------------------
    LR = shift(a, -1, -1)
    LR[nx-1,*] = ND
    LR[*,ny-1] = ND
    ;---------------------
    CB = shift(a, 0, -1)
    CB[*,ny-1] = ND

    wC = where((a eq ND) AND (LR ne ND) AND (CB ne ND), nwC)

    if (nwC ne 0) then begin
        wLL = (wC + nx - 1L)   ;(for centered diff)
        wLR = (wC + nx + 1L)
        wCB = (wC + nx)
        ;--------------------------
        ;Assumed that dx = dy here
        ;-----------------------------------------
        t1  = k[wLR] * sin(a[wLR])   ;[* (dy/dx)]
        t2  = k[wCB] * sin(a[wCB])   ;[* (dy/dx)]
        t3  = k[wCB] * cos(a[wCB])
        t4  = k[wLL] * sin(a[wLL])   ;(for centered diff)
        ;-----------------------------------------
        arg = ((t1 - t2) + t3) / k[wC]

        ;-----------------------------------
        ;Use centered diffs, where possible
        ;-----------------------------------
        ;wL  = where(LL[wC] ne ND, nwL)
        ;if (nwL ne 0) then begin
        ;    arg[wL] = ((t1[wL] - t4[wL])/2d + t3[wL]) / k[wC[wL]]
        ;    print,'nwL = ', nwL
        ;endif

        ;----------------------------
        ;Force arg to be in range ?
        ;Doesn't seem to help.
        ;----------------------------
        ;arg = (-1d > arg) < 1d

        ;--------------------------------
        ;Is argument of ACOS in range ??
        ;--------------------------------
        ;wbad = where(abs(arg) gt 1d, nbad)
        ;if (nbad ne 0) then begin
        ;    print,'WARNING:  Argument to ACOS is out of range.'
        ;    print,'          Values in k grid or angle values'
        ;    print,'          along the boundary vary too fast.' 
        ;    print,'nbad = ', nbad
        ;    ;*** STOP
        ;endif

        ;------------------------
        ;Assign new angle values
        ;------------------------
        wOK = where(abs(arg) le 1d, nOK)
        if (nOK ne 0) then a[wC[wOK]] = acos(arg[wOK])
        ;-----------------------------------------------
        nbad = (nWC - nOK)
        if (nbad ne 0) then begin
            print,'WARNING:  Argument to ASIN is out of range.'
            print,'nbad = ', nbad
        endif
        ;-----------------
        DONE = (nOK eq 0)
    endif else begin
        DONE = 1b
    endelse

endwhile

;-----------------------------
;Set nodata pixels to zero ??
;-----------------------------
;w0 = where(a eq ND, nw0)
;if (nw0 ne 0) then a[w0]=0d

;-----------------------------
;Compare to using Snell's Law
;--------------------------------
;Only works if a[w[0]] is in the
;first quadrant at this point.
;--------------------------------
;dmax = max(d, /NAN)
;w    = where(d eq dmax)
;cc0  = k[w[0]] * sin(a[w[0]])
;a2   = asin(cc0 / k)
;** if (a[w[0]] gt (!dpi/2d)) then a2 = (a2 + (!dpi/2d))

;---------------------------------
;Print mins and maxes of a and a2
;---------------------------------
a_min = min(a, max=a_max, /NAN)
print,'( a_min,  a_max) = ', a_min, a_max
;a2_min = min(a2, max=a2_max, /NAN)
;print,'(a2_min, a2_max) = ', a2_min, a2_max

;----------------------------
;Optional plot of theta grid
;----------------------------
if (PLOT) then begin
    device, decomposed=0
    loadct, 34, /silent   ;(rainbow)
    ;loadct, 39, /silent   ;(rainbow + white)
    !order = 1
    ;----------------------
    FACTOR = 5L
    xwin   = (FACTOR * nx)
    ywin   = (FACTOR * ny)
    ;-----------------------------------------------
    window, /free, xsize=xwin, ysize=ywin, $
            title='Theta grid (Numerical)'
    im = rebin(a, nx*FACTOR, ny*FACTOR, sample=1)
    tvscl, im
    ;-----------------------------------------------
    if (n_elements(a2) ne 0) then begin
        window, /free, xsize=xwin, ysize=ywin, $
                title="Theta grid (Snell's Law)"
        im2 = rebin(a2, nx*FACTOR, ny*FACTOR, sample=1)
        tvscl, im2
    endif
    ;-----------------------------------------------
    if (n_elements(d) ne 0) then begin
       window, /free, xsize=xwin, ysize=ywin, $
               title="Depth grid"
       im3 = rebin(d, nx*FACTOR, ny*FACTOR, sample=1)
       tvscl, im3
    endif
endif

RETURN, a

end;  Wave_Angle
;*******************************************************************
function Theta1, R, R1, R2, theta, theta2

a1  = R * (sin(theta) - cos(theta))
a2  = R2 * cos(theta2)
arg = (a1 + a2) / R1
T1  = asin(arg)

print,'arg    = ', arg
print,'theta1 = ', T1

RETURN, T1

end;  Theta1
;*******************************************************************
function Wave_Angle_TEST, a0, k, A2=A2, LEFT=LEFT, RIGHT=RIGHT, $
                    BOTTOM=BOTTOM, TOP=TOP, DX=DX, DY=DY, $
                    PLOT=PLOT,  K_TEST=K_TEST, $
                    A_TEST1=A_TEST1, A_TEST2=A_TEST2

;----------------------------------------------------------
;Notes:  This routine computes a wave angle grid, theta
;        from a wave number grid, so that the curl of
;        the wave number vector is zero everywhere.
;        Note that dx and dy have no effect if they
;        are equal.  However, if the values in the k
;        grid or the angle values along the boundary
;        change too fast, then the method is unstable
;        and the argument of ASIN may be outside of the
;        closed interval [-1,1].  So dx and dy still
;        play a role in this sense.  It may also happen
;        that the given boundary values for theta may be

;        incompatible with the corresponding values of k.
;        The K_TEST succeeds for small values of theta0,
;        such as 0.1 and 0.2.

;        Theta is defined as the angle that the wave

;        number vector makes with the x-axis, so that
;        the x and y components of k are (k cos(theta))
;        and (k sin(theta)), respectively.

;        Note that since k is computed via the dispersion
;        relation, it is valid for all water depths, and
;        hence the wave angles are as well.

;        12/8/04.  If the LEFT keyword is set, then
;        the approach is to solve first for all of the
;        pixels below the diagonal and then to use a
;        slightly different differencing method to solve
;        for the pixels above the diagonal.

;        For the special case of planar d (& L & k),
;        the computed values agree perfectly with those
;        predicted by Snell's Law.  This was tested for
;        several different theta0 values.
;----------------------------------------------------------
K_TEST  = keyword_set(K_TEST)
A_TEST1 = keyword_set(A_TEST1)
A_TEST2 = keyword_set(A_TEST2)

;----------------------
;Set argument defaults
;----------------------
if (n_elements(k) eq 0) then begin
    nx = 50
    ny = 50
    ;------------------------------
    ;Set depth as a simple ramp,
    ;decreasing to the right
    ;This assumes that LEFT is set
    ;------------------------------
    dm = 30d
    ad = dm * reverse(dindgen(nx) / (nx-1d))
    T  = 8d  ;[seconds]
    b  = dblarr(ny) + 1d
    d  = (ad # b)

    if (K_TEST) then begin
        dm = 2d
        b  = dist(2*nx,2*ny)
        d  = b[nx:2*nx-1, ny:2*ny-1L]   ;[depth grid]
        d  = dm * (d / max(d))
    endif

    ;-----------------------------------
    ;Compute wavelength and wave number
    ;-----------------------------------
    L = Wave_Length(d, T)
    k = Wave_Number(L)

    ;------------------------------------
    ;Print min and max values of d, L, k
    ;------------------------------------
    dmin = min(d, max=dmax)
    print,'(dmin, dmax) = ', dmin, dmax
    Lmin = min(L, max=Lmax)
    print,'(Lmin, Lmax) = ', Lmin, Lmax
    kmin = min(k, max=kmax)
    print,'(kmin, kmax) = ', kmin, kmax
endif

if (n_elements(a0) eq 0) then begin
    a0_rad = (60d * (!dpi/180d))
endif else begin
    a0_rad = (a0  * (!dpi/180d))
endelse

;---------------------
;Set keyword defaults
;---------------------
LEFT   = keyword_set(LEFT)
RIGHT  = keyword_set(RIGHT)
BOTTOM = keyword_set(BOTTOM)
TOP    = keyword_set(TOP)
PLOT   = keyword_set(PLOT)
;-----------------------------------
LEFT = 1b  ;***********************
;-----------------------------------
if NOT(keyword_set(DX)) then dx=1d
if NOT(keyword_set(DY)) then dy=1d

;-----------------------------------
;Get dimensions of wave number grid
;-----------------------------------
s  = size(k, /dimensions)
nx = s[0]
ny = s[1]

;-------------------------------------
;Initialize angle grid with boundary
;conditions along any one edge
;------------------------------------
ND = 9d   ;(nodata value)
a = dblarr(nx ,ny) + ND
if (BOTTOM) then a[*,ny-1] = a0_rad
if (LEFT)   then a[0,*]    = a0_rad
if (RIGHT)  then a[nx-1,*] = a0_rad
if (TOP)    then a[*,0]    = a0_rad
 
;------------------------------------
;Experimental: Algorithm still works
;but not if angles change too fast.
;------------------------------------
if (LEFT AND A_TEST1) then begin
    a[0,*] = dindgen(ny) * (!dpi/180d) / 2d
endif

if (LEFT AND A_TEST2) then begin
    a[0,*] = (sqrt(dindgen(ny))*3d) * (!dpi/180d)
    ;**a[0,*] = (dindgen(ny)^2d)/48d * (!dpi/180d)
endif

;---------------------------------------------
;Recursively compute remaining angle values
;(If LEFT, we get values below diagonal only)
;---------------------------------------------
DONE = 0b
while NOT(DONE) do begin
    UL = shift(a, 1, 1)
    UL[0,*] = ND
    UL[*,0] = ND
    CL = shift(a, 1, 0)
    CL[0,*] = ND

    wC = where((a eq ND) AND (UL ne ND) AND (CL ne ND), nw)

    if (nw ne 0) then begin
        wUL = (wC-nx-1L)
        wCL = (wC-1L)

        ;---------------------------------
        ;Method from Wave_Theta2 function
        ;---------------------------------
        ;t1  = k[wUL] * cos(a[wUL])
        ;t2  = k[wCL] * cos(a[wCL])
        ;t3  = k[wCL] * sin(a[wCL])
        ;arg = ((dx/dy)*(t1 - t2) + t3) / k[wC]
 
        ;----------------------------------------
        ;This is experimental and does not seem
        ;to work correctly.  See paper notes.
        ;----------------------------------------
        top = (k[wC]^2d + k[wUL]^2d) - (2d * k[wCL]^2d)
        bot = 2d * k[wC] * k[wUL]
        arg = (top / bot)

        t1  = a[wUL] + (!dpi/2d)

        ;----------------------------
        ;Force arg to be in range ?
        ;Doesn't seem to help.
        ;----------------------------
        ;arg = (-1d > arg) < 1d

        ;--------------------------------
        ;Is argument of ASIN in range ??
        ;--------------------------------
        wbad = where(abs(arg) gt 1d, nbad)
        if (nbad ne 0) then begin
            print,'WARNING:  Argument to ASIN is out of range.'
            print,'          Values in k grid or angle values'
            print,'          along the boundary vary too fast.' 
            print,'nbad = ', nbad
            STOP
        endif

        ;------------------------
        ;Assign new angle values
        ;------------------------
        a[wC] = t1 - acos(arg)
        ;** a[wC] = acos(arg) - t1

    endif else begin
        DONE = 1b
    endelse
endwhile

;---------------------------------------------
;Recursively compute remaining angle values
;(If LEFT, we get values above diagonal only)
;---------------------------------------------
;NB!  This has not been updated to match the
;     method of the previous WHILE loop.
;---------------------------------------------
DONE = 1b
while NOT(DONE) do begin
    LL = shift(a, 1, -1)
    LL[0,*] = ND
    LL[*,ny-1] = ND
    ;*** UL[0,*] = ND
    ;*** UL[*,0] = ND
    CL = shift(a, 1, 0)
    CL[0,*] = ND

    wC = where((a eq ND) AND (LL ne ND) AND (CL ne ND), nw)

    if (nw ne 0) then begin
        wLL = (wC+nx-1L)
        wCL = (wC-1L)
        ;----------------------------
        t1  = k[wCL] * cos(a[wCL])
        t2  = k[wLL] * cos(a[wLL])
        t3  = k[wCL] * sin(a[wCL])
        ;----------------------------
        arg = ((dx/dy)*(t1 - t2) + t3) / k[wC]

        ;----------------------------
        ;Force arg to be in range ?
        ;Doesn't seem to help.
        ;----------------------------
        ;arg = (-1d > arg) < 1d

        ;--------------------------------
        ;Is argument of ASIN in range ??
        ;--------------------------------
        wbad = where(abs(arg) gt 1d, nbad)
        if (nbad ne 0) then begin
            print,'WARNING:  Argument to ASIN is out of range.'
            print,'          Values in k grid or angle values'
            print,'          along the boundary vary too fast.' 
            print,'nbad = ', nbad
            STOP
        endif

        ;------------------------
        ;Assign new angle values
        ;------------------------
        a[wC] = asin(arg)   
    endif else begin
        DONE = 1b
    endelse

endwhile

;-----------------------------
;Set nodata pixels to zero ??
;-----------------------------
w0 = where(a eq ND, nw0)
if (nw0 ne 0) then a[w0]=0d

;-----------------------------
;Compare to using Snell's Law
;-----------------------------
kmin = min(k, max=kmax, /NAN)
w    = where(k eq kmax)
a0 = k[w[0]] * sin(a[w[0]])
a2 = asin(a0 / k)

;---------------------------------
;Print mins and maxes of a and a2
;---------------------------------
a_min = min(a, max=a_max)
print,'( a_min,  a_max) = ', a_min, a_max
a2_min = min(a2, max=a2_max)
print,'(a2_min, a2_max) = ', a2_min, a2_max

;----------------------------
;Optional plot of theta grid
;----------------------------
if (PLOT) then begin
    device, decomposed=0
    loadct, 34, /silent   ;(rainbow)
    ;loadct, 39, /silent   ;(rainbow + white)
    !order = 1
    ;----------------------
    FACTOR = 5L
    xwin   = (FACTOR * nx)
    ywin   = (FACTOR * ny)
    ;-----------------------------------------------
    window, /free, xsize=xwin, ysize=ywin, $
            title='Theta grid (Numerical)'
    im = rebin(a, nx*FACTOR, ny*FACTOR, sample=1)
    tvscl, im
    ;-----------------------------------------------
    window, /free, xsize=xwin, ysize=ywin, $
            title="Theta grid (Snell's Law)"
    im2 = rebin(a2, nx*FACTOR, ny*FACTOR, sample=1)
    tvscl, im2
    ;-----------------------------------------------
    if (n_elements(d) ne 0) then begin
       window, /free, xsize=xwin, ysize=ywin, $
               title="Depth grid"
       im3 = rebin(d, nx*FACTOR, ny*FACTOR, sample=1)
       tvscl, im3
    endif
endif

RETURN, a

end;  Wave_Angle_TEST
;*******************************************************************
function Wave_Height, d, a, P, A0=A0, H0=H0, T=T, $
                      DX=DX, DY=DY, NX=NX, NY=NY, $
                      PLOT=PLOT, CLOSE=CLOSE, NO_BREAK=NO_BREAK, $
                      ;-------------------------------------------
                      LEFT=LEFT, RIGHT=RIGHT, $
                      BOTTOM=BOTTOM, TOP=TOP, $
                      ;-----------------------------
                      K_TEST=K_TEST, $
                      H_TEST1=H_TEST1, H_TEST2=H_TEST2, $
                      ;------------------------------------------
                      PLANE1=PLANE1, PLANE2=PLANE2, $
                      SLOPE=SLOPE, BAY=BAY, $
                      SINE=SINE, $
                      ADD_HILL=ADD_HILL, ADD_PIT=ADD_PIT, $
                      ADD_ISLAND=ADD_ISLAND

;------------------------------------------------------------
;Notes:  This routine computes a wave height grid, H,
;        from a water-depth grid, d and the incident wave
;        period, T.  As an intermediate step, the wave
;        number grid, k, and wave angle grid, a, are
;        computed.

;        Refracted wave height is computed by solving a
;        first order PDE that states that the divergence
;        of the wave energy flux (or power) is zero.
;        This is the so-called conservation of wave energy
;        equation for monochromatic waves.

;        The grid k is computed by the Wave_Number routine
;        by iteratively solving the dispersion relation.

;        The grid theta is computed by Wave_Theta3, by
;        solving the equation that states that the curl of
;        the wave number vector field is zero. 
;          
;        Note that dx and dy have no effect if they
;        are equal.  However, if the values in the k
;        grid or the angle values along the boundary
;        change too fast, then the method is unstable.
;        See the Notes for the Wave_Theta3 routine.

;        Theta is defined as the angle that the wave
;        number vector makes with the x-axis, so that
;        the x and y components of k are (k cos(theta))
;        and (k sin(theta)), respectively.

;        Note that since k is computed via the dispersion
;        relation, it is valid for all water depths, and
;        hence the wave angles are as well.

;        12/8/04.  If the LEFT keyword is set, then
;        the approach is to solve first for all of the
;        pixels below the diagonal and then to use a
;        slightly different differencing method to solve
;        for the pixels above the diagonal.
;------------------------------------------------------------
FORWARD_FUNCTION Test_Bathymetry

PLOT     = keyword_set(PLOT)
CLOSE    = keyword_set(CLOSE)
NO_BREAK = keyword_set(NO_BREAK)
K_TEST   = keyword_set(K_TEST)
H_TEST1  = keyword_set(H_TEST1)
H_TEST2  = keyword_set(H_TEST2)

;--------------------------------
;Test & demo bathymetry keywords
;--------------------------------
PLANE1     = keyword_set(PLANE1)
PLANE2     = keyword_set(PLANE2)
BAY        = keyword_set(BAY)
SINE       = keyword_set(SINE)
ADD_HILL   = keyword_set(ADD_HILL)
ADD_PIT    = keyword_set(ADD_PIT)
ADD_ISLAND = keyword_set(ADD_ISLAND)

;---------------------
;Set keyword defaults
;---------------------
LEFT   = keyword_set(LEFT)
RIGHT  = keyword_set(RIGHT)
BOTTOM = keyword_set(BOTTOM)
TOP    = keyword_set(TOP)
;---------------------------------------------------
if NOT(keyword_set(A0)) then a0 = 20d   ;[degrees]
if NOT(keyword_set(H0)) then H0 = 2.5d  ;[meters]
if NOT(keyword_set(T))  then T  = 10d   ;[seconds]
;---------------------------------------------------
if NOT(keyword_set(DX)) then dx = 1d    ;[meters]
if NOT(keyword_set(DY)) then dy = 1d    ;[meters]
if NOT(keyword_set(NX)) then nx = 200
if NOT(keyword_set(NY)) then ny = 200
;---------------------------------------------------
if NOT(keyword_set(SLOPE)) then begin
    slope = -0.02d
endif else begin
    if (slope gt 0) then slope = (-1d * slope)
endelse

;--------------------------
;Get the grid dimensions ?
;--------------------------
;if (n_elements(z) ne 0) then begin
;    s  = size(z, /dimensions)
;    nx = s[0]
;    ny = s[1]
;endif

;-------------------------------------------
;Could get deep-water wave vars, H0, L0 & T
;from fully-developed sea (FDS) functions.
;-------------------------------------------
;uu = 28d  ;[mph]
;T  = FDS_Mean_Period2(uu)
;L0 = FDS_Mean_Length2(uu)
;H0 = FDS_Mean_Height2(uu)

if NOT(NO_BREAK) then begin
    print,'Computing wave heights...'
endif else begin
    print,'Computing nonbreaking wave heights...'
endelse

;---------------------------------------
;Generate test bathymetry, if requested
;(Defined in longshore.pro)
;---------------------------------------
if (PLANE1 OR PLANE2 OR BAY OR SINE) then begin
    z = Test_Bathymetry(dx, dy, nx, ny, PLANE1=PLANE1, $
             PLANE2=PLANE2, SLOPE=SLOPE, BAY=BAY, $
             SINE=SINE, ADD_HILL=ADD_HILL, $
             ADD_PIT=ADD_PIT, ADD_ISLAND=ADD_ISLAND)
   
    ;----------------------------------------
    ;Must flip x-axis if LEFT keyword is set
    ;----------------------------------------
    if (LEFT) then z = rotate(z, 5)

    ;----------------------------------------
    ;Must rotate if BOTTOM keyword is set
    ;----------------------------------------
    if (BOTTOM) then z = rotate(z, 1)

endif

;----------------------
;Get the depth grid ??
;----------------------
d = Water_Depth(z)

;----------------------
;Get the depth grid ??     ;******************************
;----------------------
if (n_elements(d) eq 0) then begin
    nx = 50
    ny = 50
    ;------------------------------
    ;Set depth as a simple ramp,
    ;decreasing to the right
    ;This assumes that LEFT is set
    ;------------------------------
    dm = 30d
    ad = dm * reverse(dindgen(nx) / (nx-1d))
    b  = dblarr(ny) + 1d
    d  = (ad # b)

    if (K_TEST) then begin
        dm = 2d
        b = dist(2*nx,2*ny)
        d = b[nx:2*nx-1, ny:2*ny-1L]   ;[depth grid]
        d = dm * (d / max(d))
    endif
endif

;-----------------------------------
;Get dimensions of the depth grid
;-----------------------------------
s  = size(d, /dimensions)
nx = s[0]
ny = s[1]

;-----------------------------------------
;Convert deep-water wave angle to radians
;-----------------------------------------
a0_rad = (a0 * (!dpi/180d))   ;[radians]

;-----------------------------------
;Compute wavelength and wave number
;-----------------------------------
L = Wave_Length(d, T)
k = Wave_Number(L)
;a = Wave_Angle(a0, k, LEFT=LEFT, BOTTOM=BOTTOM, $
;               RIGHT=RIGHT, TOP=TOP)
a = Wave_Angle(a0, k, LEFT=LEFT, BOTTOM=BOTTOM, $
               RIGHT=RIGHT, TOP=TOP)

;---------------------------------------
;Print min and max values of d, L, k, t
;---------------------------------------
dmin = min(d, max=dmax, /NAN)
print,'(dmin, dmax) = ', dmin, dmax, '   [meters]'
Lmin = min(L, max=Lmax, /NAN)
print,'(Lmin, Lmax) = ', Lmin, Lmax, '   [meters]'
kmin = min(k, max=kmax, /NAN)
print,'(kmin, kmax) = ', kmin, kmax, '   [1/meters]'
amin = min(a, max=amax, /NAN)
amin_deg = amin * (180d / !dpi)
amax_deg = amax * (180d / !dpi)
print,'(amin, amax) = ', amin_deg, amax_deg, '   [degrees]'

;-----------------------------------
;Create "index grids" for neighbors
;-----------------------------------
;CI = lindgen(nx,ny)
;LI = shift(CI,  1,  0)
;RI = shift(CI, -1,  0)
;TI = shift(CI,  0,  1)
;BI = shift(CI,  0, -1)

;---------------------------------
;Compute value of power along the
;deep-water boundary
;---------------------------------
L0 = max(L, /NAN)
P0 = (H0 / T)^2d * L0 * !dpi            ;(DOUBLE-CHECK)

;-------------------------------------
;Initialize height grid with boundary
;conditions along any one edge
;------------------------------------
ND = -9999d   ;[nodata value]
P  = dblarr(nx ,ny) + ND
if (LEFT)   then P[0,*]    = P0
if (RIGHT)  then P[nx-1,*] = P0
if (BOTTOM) then P[*,ny-1] = P0
if (TOP)    then P[*,0]    = P0
 
;------------------------------------
;Experimental: Algorithm still works
;but not if heights change too fast.
;------------------------------------
if (LEFT AND H_TEST1) then begin
    Hvals  = 1d + (dindgen(ny) / (ny-1L))  ;(in [1,2] meters)
    P[0,*] = (Hvals / T)^2d * L0 * !dpi
endif

;---------------------------------------------
;Recursively compute remaining power values
;from BCs on the LEFT edge (below diagonal)
;---------------------------------------------
DONE = (1b - LEFT)
while NOT(DONE) do begin
    UL = shift(P, 1, 1)
    UL[0,*] = ND
    UL[*,0] = ND
    CL = shift(P, 1, 0)
    CL[0,*] = ND

    wC = where((P eq ND) AND (UL ne ND) AND (CL ne ND), nw)

    if (nw ne 0) then begin
        wUL = (wC-nx-1L)
        wCL = (wC-1L)
        ;-------------------------------------------
        t1  = P[wCL] * (cos(a[wCL]) + sin(a[wCL]))
        t2  = P[wUL] * sin(a[wUL])
        t3  = cos(a[wC])
        ;-----------------------
        P[wC] = (t1 - t2) / t3

    endif else begin
        DONE = 1b
    endelse
endwhile

;---------------------------------------------
;Recursively compute remaining angle values
;from BCs on the LEFT edge (above diagonal)
;---------------------------------------------
DONE = (1b - LEFT)
while NOT(DONE) do begin
    LL = shift(P, 1, -1)
    LL[0,*] = ND
    LL[*,ny-1] = ND
    CL = shift(P, 1, 0)
    CL[0,*] = ND

    wC = where((P eq ND) AND (LL ne ND) AND (CL ne ND), nw)

    if (nw ne 0) then begin
        wLL = (wC+nx-1L)
        wCL = (wC-1L)
        ;------------------------------------------
        t1  = P[wCL] * (cos(a[wCL]) - sin(a[wCL]))
        t2  = P[wLL] * sin(a[wLL])
        t3  = cos(a[wC])
        ;-----------------------
        P[wC] = (t1 + t2) / t3

    endif else begin
        DONE = 1b
    endelse
endwhile

;---------------------------------------------
;Recursively compute remaining angle values
;from BCs on the BOTTOM edge (below diagonal)
;---------------------------------------------
DONE = (1b - BOTTOM)
while NOT(DONE) do begin
    LR = shift(P, -1, -1)
    LR[nx-1,*] = ND
    LR[*,ny-1] = ND
    CB = shift(P, 0, -1)
    CB[*,ny-1] = ND

    wC = where((P eq ND) AND (LR ne ND) AND (CB ne ND), nw)

    if (nw ne 0) then begin
        wLR = (wC+nx+1L)
        wCB = (wC+nx)
        ;-------------------------------------
        t1  = P[wCB] * sin(a[wCB])
        t2  = P[wCB] * cos(a[wCB]) * (dy/dx)
        t3  = P[wLR] * cos(a[wLR]) * (dy/dx)
        ;-------------------------------------
        P[wC] = ((t1 + t2) - t3) / sin(a[wC])
  
    endif else begin
        DONE = 1b
    endelse
endwhile

;---------------------------------------------
;Recursively compute remaining angle values
;from BCs on the BOTTOM edge (above diagonal)
;---------------------------------------------
DONE = (1b - BOTTOM)
while NOT(DONE) do begin
    LL = shift(P, 1, -1)
    LL[0,*] = ND
    LL[*,ny-1] = ND
    CB = shift(P, 0, -1)
    CB[*,ny-1] = ND

    wC = where((P eq ND) AND (LL ne ND) AND (CB ne ND), nw)

    if (nw ne 0) then begin
        wLL = (wC+nx-1L)
        wCB = (wC+nx)

        ;-------------------------------------
        t1  = P[wCB] * sin(a[wCB])
        t2  = P[wCB] * cos(a[wCB]) * (dy/dx)
        t3  = P[wLL] * cos(a[wLL]) * (dy/dx)
        ;-------------------------------------
        P[wC] = ((t1 - t2) + t3) / sin(a[wC])
  
    endif else begin
        DONE = 1b
    endelse
endwhile

;-----------------------------
;Set nodata pixels to zero ??
;-----------------------------
w0 = where(P le ND, nw0)
if (nw0 ne 0) then P[w0]=0d

;----------------------------------
;Compute the Cg grid from C, d & L
;----------------------------------
;*** C  = Wave_Speed(d, L)
C  = (L / T)
Cg = Group_Velocity(C, d, L)

;--------------------------------
;Compute H grid from P, Cg and T
;--------------------------------
H = sqrt( abs(P/Cg) * (0.5d * T / !dpi))

;-----------------------
;Apply wave breaking ??
;-----------------------
if NOT(NO_BREAK) then begin
    ;------------------------------------
    ;Use ARMY breaking condition for now
    ;------------------------------------
    gamma = 0.78d
    sz = where(H gt (gamma * d), nsz)
    if (nsz ne 0) then begin
        H[sz] = (gamma * d[sz])    ;[for now]  ;****************
    endif
endif

;---------------------------------
;Print mins and maxes of P and H
;---------------------------------
P_min = min(P, max=P_max, /NAN)
print,'(P_min,  P_max) = ', P_min, P_max
;-----------------------------------------
H_min = min(H, max=H_max, /NAN)
print,'(H_min,  H_max) = ', H_min, H_max, ' [meters]'
;-----------------------------------------
;H2_min = min(H2, max=H2_max, /NAN)
;print,'(H2_min, H2_max) = ', H2_min, H2_max

;----------------------------
;Optional plot of H grid
;----------------------------
if (PLOT) then begin
    if (CLOSE) then Close_Windows
    device, decomposed=0
    loadct, 34, /silent   ;(rainbow)
    ;loadct, 39, /silent   ;(rainbow + white)
    !order = 1
    ;------------------------
    FACTOR = (600 / nx) > 1L
    xwin   = (FACTOR * nx)
    ywin   = (FACTOR * ny)
    ;-----------------------------------------------
    window, /free, xsize=xwin, ysize=ywin, $
            title='Wave height grid (Numerical)'
    im = rebin(H, nx*FACTOR, ny*FACTOR, sample=1)
    if (H_min ne H_max) then begin
        tv, hist_equal(im)
    endif else begin
        tvscl, im
    endelse
    ;-----------------------------------
    ;Overplot the wave rays & crests ??
    ;-----------------------------------
    LINE_POINTS = 0b
    if (LINE_POINTS) then RS=2 else RS=10
    beta = a
    beta0 = a0_rad
    plot_rays, beta, RS, beta0, FACTOR=FACTOR, /OVERPLOT, $
               DX=dx, DY=dy, /TRANSFORM
    plot_rays, beta, RS, beta0, FACTOR=FACTOR, /OVERPLOT, $
               DX=dx, DY=dy, /TRANSFORM, /CRESTS
    ;-----------------------------------------------------
    window, /free, xsize=xwin, ysize=ywin, $
            title="Power grid (Numerical)"
    P2  = abs(P)  ;*****************
    im2 = rebin(P2, nx*FACTOR, ny*FACTOR, sample=1)
    if (P_min ne P_max) then begin
        tv, hist_equal(im2)
    endif else begin
        tvscl, im2
    endelse
    ;-----------------------------------------------
    if (n_elements(d) ne 0) then begin
       window, /free, xsize=xwin, ysize=ywin, $
               title="Depth grid"
       im3 = rebin(d, nx*FACTOR, ny*FACTOR, sample=1)
       tvscl, im3
       ;-----------------------------------
       ;Overplot the wave rays & crests ??
       ;-----------------------------------
       plot_rays, beta, RS, beta0, FACTOR=FACTOR, /OVERPLOT, $
                  DX=dx, DY=dy, /TRANSFORM
       plot_rays, beta, RS, beta0, FACTOR=FACTOR, /OVERPLOT, $
                  DX=dx, DY=dy, /TRANSFORM, /CRESTS
    endif
    ;-----------------------------------------------
    if (n_elements(a) ne 0) then begin
       window, /free, xsize=xwin, ysize=ywin, $
               title="Wave Angle grid"
       im4 = rebin(a, nx*FACTOR, ny*FACTOR, sample=1)
       if (amin ne amax) then begin
           tv, hist_equal(im4)
       endif else begin
           tvscl, im4
       endelse
       ;-----------------------------------
       ;Overplot the wave rays & crests ??
       ;-----------------------------------
       plot_rays, beta, RS, beta0, FACTOR=FACTOR, /OVERPLOT, $
                  DX=dx, DY=dy, /TRANSFORM
       plot_rays, beta, RS, beta0, FACTOR=FACTOR, /OVERPLOT, $
                  DX=dx, DY=dy, /TRANSFORM, /CRESTS
    endif
endif

RETURN, H

end;  Wave_Height
;*******************************************************************
function Wave_Energy, H, SILENT=SILENT

;---------------------------------------------------
;Notes:  This is wave energy per unit area.
;        H should correspond to RMS value.

;        (Not per unit length of wave crest.)
;        See Komar(1976).
;        1 Joule = 1 kg * m^2 / s^2
;        E has units of (kg / s^2) = (Joule / m^2);
;        See Martinez & Harbaugh, p. 218.
;---------------------------------------------------
SILENT = keyword_set(SILENT)
SILENT = 1b   ;*********

if NOT(SILENT) then begin
    print,'Computing wave energy density...'

endif

g   = Gravity()
rho = Density('seawater')
E   = (rho * g / 8d) * H^2d

;--------------------
;Inherit NaNs from H
;--------------------
;w = where(finite(H) ne 1, nw)
;if (nw ne 0) then E[w] = H[w]

if NOT(SILENT) then begin
    print,'Finished computing wave energy density.'
    print,' '
endif

RETURN, E

end;  Wave_Energy
;*******************************************************************
function Wave_Power, H, Cg

E = Wave_Energy(H)

RETURN, (E * Cg)
end;  Wave_Power
;*******************************************************************
function Max_Orbital_Velocity, H, L, d, T, SILENT=SILENT

SILENT = keyword_set(SILENT)
SILENT = 1b   ;******

if NOT(SILENT) then begin
    print,'Computing max orbital velocity...'
endif

k = Wave_Number(L)
umax_orb = (!dpi * H) / (T * sinh(k * d))

;---------------------------------------------
;Set umax to zero where d (and so H) are zero
;---------------------------------------------
wz = where((d eq 0) OR (finite(d) ne 1), nwz)
if (nwz ne 0) then umax_orb[wz] = 0d

;--------------------
;Inherit NaNs from d
;--------------------
;w = where(finite(d) ne 1, nw)
;if (nw ne 0) then umax_orb[w] = d[w]

if NOT(SILENT) then begin
    print,'Finished computing max orbital velocity.'
    print,' '
endif

RETURN, umax_orb
end;  Max_Orbital_Velocity
;*******************************************************************
function Surf_Zone, d, L, T, a, a0, H0, H=H, NSZ=nsz, $

                    COMPLEMENT=complement, $
                    US_ARMY=US_ARMY, MICHE=MICHE, $
                    LE_MEHAUTE=LE_MEHAUTE

;------------------------------------------------------
;Notes:  The surf zone is defined as the set of pixels
;        shoreward of the breaker zone where the waves
;        break.

;        Pixels seaward of the breaker zone can be
;        returned with the COMPLEMENT keyword.

;        A0  = deep-water wave angle (angle between
;              wave rays and x-axis)
;        NSZ = number of pixels in surf zone

;NB!     Deep-water waves will break when their
;        steepness, H/L reaches 1/7.  But that is not
;        relevant for the surf zone.
;------------------------------------------------------
US_ARMY    = keyword_set(US_ARMY)
MICHE      = keyword_set(MICHE)
LE_MEHAUTE = keyword_set(LE_MEHAUTE)
KEY_SUM    = (US_ARMY + MICHE + LE_MEHAUTE)

if (KEY_SUM eq 0) then US_ARMY = 1b
;*** if (KEY_SUM eq 0) then MICHE = 1b
;*** if (KEY_SUM eq 0) then LE_MEHAUTE = 1b

;------------------------------------
;Get "raw" wave heights via NO_BREAK
;------------------------------------
if NOT(keyword_set(H)) then begin
    print,'Using raw wave heights to find surf zone...'
    H = Wave_Height(d, a, A0=A0, H0=H0, T=T, /NO_BREAK, $
                    DX=DX, DY=DY)
endif

;---------------------------------
;Pixels inside the surf zone
;using US Army Corp approximation
;---------------------------------
if (US_ARMY) then begin
    print,'Using US Army Corps criterion for wave breaking...'
    w = where((H / d) ge 0.78, nsz, COMPLEMENT=COMPLEMENT)
    cstr = '_ARMY'
endif

;--------------------------------
;Pixels inside the surf zone
;using modified Miche criterion
;--------------------------------
if (MICHE) then begin
    print,'Using modified Miche criterion for wave breaking...'

    k = Wave_Number(L)
    w = where(H ge (0.88d / k) * tanh((0.78d/0.88d) * k * d), $
              nsz, COMPLEMENT=complement)
    cstr = '_MICHE'
endif

;-------------------------------------
;Pixels inside the surf zone
;based on theory in Le Mehaute (1961)
;-------------------------------------
if (LE_MEHAUTE) then begin
    print,'Using LeMehaute criterion for wave breaking...'

    k = Wave_Number(L)
    w = where((H/L) ge (0.12 * tanh(k * d)), nsz, $
              COMPLEMENT=complement)
    cstr = '_LEME'
endif

if (nsz eq 0) then begin

    print,'**********************************************'
    print,'WARNING: No pixels inside surf zone.'
    print,'             Try reducing dx and dy.'
    print,'**********************************************'
    print,' '
    RETURN, -1L
endif

;----------------------------------
;Save Surf Zone pixels to RTM file
;----------------------------------
SAVE_RTM = 1b
if (SAVE_RTM) then begin
    print,'Saving surf zone pixels to RTM...'
    outfile = 'SURF_ZONE' + cstr + '.rtm'
    openw, unit, outfile, /get_lun
    writeu, unit, -1L, w, -1L
    free_lun, unit
    print,'Finished creating RTM file.'
    print,' '

endif

;-----------------
;Optional message
;-----------------
nstr = strtrim(string(nsz),2)
print,'   Number of pixels in surf zone = ' + nstr

RETURN, w
end;  Surf_Zone
;*******************************************************************
function Breaker_Zone, sz_IDs, d, nx, ny, NBZ=nbz

;------------------------------------------------------
;Notes:  Idea is to create a mask grid where surf zone
;        pixels have the value 1 and all other pixels
;        have the value 0.  Then a convolution with a
;        3x3 kernel of 1's will result in values of 1
;        and 0 for pixels that are entirely inside or
;        outside of the surf zone and intermediate
;        values for pixels on the boundary of the surf
;        zone, which is the breaker zone.  As a final


;        step, pixels on land ((d le 0) OR (d eq NaN))
;        are excluded.
;------------------------------------------------------
if (sz_IDs[0] eq -1L) then begin
    nbz = 0L  &  RETURN, -1L
endif

mask = intarr(nx, ny)

mask[sz_IDs] = 1

;--------------------------------------------
;Include land pixels in the mask so we don't
;include any pixels adjacent to the shore
;--------------------------------------------
land = where((d le 0) OR (finite(d) ne 1), nland)
if (nland ne 0) then mask[land] = 1

K = bytarr(3,3) + 1  ;(kernel)
C = convol(mask, K)
;C = convol(mask, K, /edge_wrap)
;C = convol(mask, K, /edge_truncate)

;--------------
;Exclude edges
;--------------
C[1,*] = 0
C[nx-2,*] = 0
C[*,1] = 0
C[*,ny-2] = 0

;--------------------------------
;Find pixels in the breaker zone
;--------------------------------
;**** DMIN = 0.1  ;(11/9/04)
DMIN = 0d
bz_IDs = where((mask eq 1) AND (finite(C) eq 1) AND $
               (C ne 0) AND (C ne 9), nbz)
               ;**** AND (d gt DMIN) AND (finite(d) eq 1), nbz)

;-------------------------------------
;Save Breaker Zone pixels to RTM file
;-------------------------------------
SAVE_RTM = 1b
if (SAVE_RTM) then begin
    print,'Saving breaker zone pixels to RTM...'
    openw, unit, 'BREAKER_ZONE.rtm', /get_lun
    writeu, unit, -1L, bz_IDs, -1L
    free_lun, unit

    print,'Finished creating RTM file.'
    print,' '
endif

;-----------------
;Optional message
;-----------------
nstr = strtrim(string(nbz),2)
print,'   Number of pixels in breaker zone = ' + nstr

RETURN, bz_IDs
end;  Breaker_Zone
;*******************************************************************
pro Make_Spur_Plot

;**********************************************
;FOR ORIGINAL SPURS, W/ Ls=500, ny=100, dy=25
;**********************************************
;nx = 100
;ny = 100
;dx = 25d
;dy = 25d
;S_row  = 14
;G_row  = 4
;T1_row = 9
;T2_row = 11

;*****************************************
;FOR NEW SPURS, W/ Ls=600, ny=100, dy=12
;*****************************************
nx = 200
ny = 100
dx = 12d
dy = 12d
S_row  = 25
G_row  = 50
T1_row = 36
T2_row = 43

;---------------------------------
;Get the spur & groove bathymetry
;---------------------------------
x = dindgen(nx) * dx
z = test_bathymetry(/spurs, nx=nx, ny=ny, dx=dx, dy=dy, $
                    M1=m1, M2=m2, XC=xc, XB=xB, XT=xT, $
                    FB=fB, FT=fT)
ymin = min(z)

;----------------
;Prepare to plot
;----------------
device, decomposed=0
loadct, 0, /silent
black = 0
white = 255
window, /free, xsize=800, ysize=400, $
        title='Idealized Molokai Reef Profile'

;-----------------------------
;Plot the top-of-spur profile
;-----------------------------                    
plot, x, z[*,S_row], color=black, background=white, thick=2, $
      xtitle='Distance offshore [meters]', $
      ytitle='Bed elevation [meters]', $
      yrange=[ymin, 5], ystyle=1

;--------------------------------------
;Overplot the center-of-groove profile
;--------------------------------------
oplot, x, z[*,G_row],  color=black, linestyle=0   ;[centerline]
oplot, x, z[*,T1_row], color=black, linestyle=2
oplot, x, z[*,T2_row], color=black, linestyle=2

;-------------------------------------
;Overplot the "volcanic cone" profile
;-------------------------------------
y1 = -1d * m1 * x
oplot, x, y1 + 1, color=black

;-------------------------------------
;Overplot the still-water sea surface
;-------------------------------------
xmin = min(x, max=xmax)
oplot, [xmin,xmax], [0,0], color=black, linestyle=2

xc_str = strtrim(string(fix(xc)), 2)
xc_str = 'xc = ' + xc_str + ' meters'
;--------------------------------------
xf = (xB - xc)
xf_str = strtrim(string(fix(xf)), 2)
xf_str = 'xf = ' + xf_str + ' meters'
;--------------------------------------
m1inv = fix(1d / m1)
m1_str = strtrim(string(m1inv), 2)
m1_str = 'm1 = 1/' + m1_str
;--------------------------------------
m2inv = fix(1d / m2)
m2_str = strtrim(string(m2inv), 2)
m2_str = 'm2 = 1/' + m2_str
;--------------------------------------
m3 = (fT - fB) / xf
m3inv = fix(1d / m3)
m3_str = strtrim(string(m3inv), 2)
m3_str = 'm3 = 1/' + m3_str

;--------------------
;Add some annotation
;--------------------
xyouts, 0.35, 0.5,  m1_str, /normal, color=black
xyouts, 0.72, 0.60, xc_str, /normal, color=black
xyouts, 0.72, 0.55, xf_str, /normal, color=black
xyouts, 0.72, 0.50, m2_str, /normal, color=black
xyouts, 0.72, 0.45, m3_str, /normal, color=black

;-----------------------------
;Option to show locator lines
;-----------------------------
LINES = 1b
if (LINES) then begin
    oplot, [xc,xc],[-50,10], color=black, linestyle=1
    oplot, [xB,xB],[-50,10], color=black, linestyle=1
    oplot, [xT,xT],[-50,10], color=black, linestyle=1
    ;-------------------------------------------------
    oplot, [xmin,xmax], [fT,fT], color=black, $
           linestyle=1
    oplot, [xmin,xmax], [fB,fB], color=black, $
           linestyle=1
endif

end;  Make_Spur_Plot
;*******************************************************************

