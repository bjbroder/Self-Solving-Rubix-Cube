# -----------------------------------------------------------------------------
# rubix.py
# 
# created by:  Brielle Broder
#
# An in-perspective depiction of a rubix cube from both the front and the back.
# This cube, on user's click, will randomly shuffle itself.
# Upon user's next click, the cube solves itself step-by-step.

 #I hereby certify that this program is solely the result of my own work and is in compliance with the Academic Integrity policy of the course syllabus.
# -----------------------------------------------------------------------------


import Draw     #Used to draw the cube
import math     #Used to do square roots
import random   #Used to generate a random shuffle
import copy     #Used to create a deep copy of the cube


#FUNCTIONS NEEDED TO CREATE THE FRAME FOR THE CUBE

#Distance between two points whose coordinates are contained in a list
def distance(p, q):
    return math.sqrt( (q[0] - p[0])**2 + (q[1] - p[1])**2 ) 

#Determines the slope of a line
def slope(a, b):
    return (a[1] - b[1]) / (a[0] - b[0])

#Determines the y-intercept of a line
def yInt(a, slp): 
    return a[1] - slp * a[0]

#Determines the point of intersection between two lines
def intersection(p, q, r, s):
    slopePQ = slope(p, q)
    slopeRS = slope(r, s)    
    
    yIntPQ = yInt(p, slopePQ)
    yIntRS = yInt(r, slopeRS)
      
    x = (yIntRS - yIntPQ) / (slopePQ - slopeRS)
    y = yPoint(p, q, x)
    
    return [x,y]

def yPoint(t,u,x):
    s = slope(t, u) 
    return s * x + yInt(t, s)


#CREATES THE FRAME WITHIN WHICH TO DRAW THE RUBIX CUBE

scale = 60 #Number chosen by which to scale the sizes of the cubes

#Creates a right-triangle within which to create the cube
a = (0, 0)                              #Left side of triangle
b = (25 * scale, a[1])                  #Right side of triangle
d = (16 * scale, 12 * scale)            #Right angle of the triangle

c = (d[0], a[1])                        #Point on line AB reached when vertical line is drawn from the right angle
e = (a[0] + distance(a, d), a[1])       #Point reached on AB that is the length of AD 
f = (b[0] - distance(b, d), a[1])       #Point reached on AB that is the length of BD
g = (c[0], d[1] - d[1] / 4)             #Point on CD that is 3/4 the way down to D, the lowest point on the cube

height = 400 #Size of the cube

#Points above, to the left, and to teh right of G that are all "height" in length
h = (g[0], g[1] - height)               #Point at the top of the cube, GH is the height of the cube
i = (g[0] - height, g[1])               #Past the bottom left of the cube, makes the bottom point of the left-right diagonal axis through the cube               
j = (g[0] + height, g[1])               #Past the bottom right of the cube, makes the bottom point of the right-left diagonal axis through the cube

#Creates the bottom left and right corners of the cube, respectively
k = intersection(a, g, i, e)            #The intersection of AG and IE forms the bottom-left
l = intersection(b, g, j, f)            #The intersection of BG and JF forms the bottom right

#Creates vertical lines from the bottom left and right corners that are "height" tall
m = (k[0],k[1]-height)
n = (l[0],l[1]-height)

#Creates the top left and right corners of the cube, respectively    
o = [k[0],yPoint(a,h,k[0])]             #Point along vertical line KM that intersects with AH             
p = [l[0],yPoint(b,h,l[0])]             #Point along vertical line LN that intersects with BH

q = intersection(a,p,b,o)               #Point of intersection between BO and AP

rowHeight = (h[1]-g[1])/3               #Since there are three rows, the hight of each row is the height of the cube divided by 3        

r= (g[0],h[1]-rowHeight)                #The point on HG that is 1/3 from the topd of the cube
s= (g[0],h[1]-2*rowHeight)              #The point on HG that is 2/3 from the top of the cube


#Naming of the faces on the cube:
#On each side of the cube there are nine faces
#In order to limit conufsion,these nine face have been labeled like a matrix, using an i,j format
#i = row number, starting at 1 from the top
#j = column number, starting at 1 from the left
#Because this notation is used as variable names, the comma is dropped
#Colores are described in the variable name by using the fist letter of the color
#Ex: y11 symbolizes the upper left position on the yellow side

#In this cube, the placement of colors will be as follows:
#Yellow = top
#Blue = Front
#Red = Right
#Orange = Left
#Green = Back
#White = Bottom


#Creating points along the diagonals of the cube from the outer-upper corners to G thereby creating corners for faces that touch the inner diagonal:

t = intersection(a,r,o,g)           #Lower-right of b11; Lower-left of b12; Upper-right of b21; Upper-left of b22             
u = intersection(a,s,o,g)           #Lower-right of b22; Lower-left of b23; Upper-right of b32; Upper-left of b33
v = intersection(b,s,p,g)           #Lower-right of r21; Lower-left of r22; Upper-right of r31; Upper-left of r32 
w = intersection(b,r,p,g)           #Lower-right of r12; Lower-left of r13; Upper-right of r22; Upper left of r23

#G serves as the Bottom-right of b33 and the Bottom-left of r31

#Creating corners that touch the top edge of the cube on the front and right
z = (t[0],yPoint(a,h,t[0]))         #Upper-right of b11; Upper-left of b12
aa = (u[0],yPoint(a,h,u[0]))        #Upper-right of b12; Upper-left of b13
ab = (v[0],yPoint(b,h,v[0]))        #Upper-right of r11; Upper-left of r12
ac = (w[0],yPoint(b,h,w[0]))        #Upper-right of r12; Upper-left of r13

#Creating corners that touch the bottom edge of the cube on the front and right
ad = (z[0],yPoint(a,g,z[0]))        #Lower-right of b31; Lower-left of b32
ae = (aa[0],yPoint(a,g,aa[0]))      #Lower-right of b32; Lower-left of b33
af = (ab[0],yPoint(b,g,ab[0]))      #Lower-right of r31; Lower-left of r32
ag = (ac[0],yPoint(b,g,ac[0]))      #Lower-right of r32; Lower-left of r33

#Creating corners that touch the top edge of the cube on the back and left
#Done by finding the intersection between the top edge of the cube on its side (back or left) and the line from the outer triangle to the opposing top-edge point on the front or right
ah = intersection(a,ab,o,q)         #Upper-right of o12; Upper-left of o13
ai = intersection(a,ac,o,q)         #Upper-right of o11; Upper-left of o12
aj = intersection(b,z,q,p)          #Upper-right of g12; Upper-left of g13
ak = intersection(b,aa,q,p)         #Upper-right of g11; Upper-left of g12

#Creating inner-corners on the top face of the cube
#Done by finding the intersection of lines formed by points that are opposite each other on the outside of the top face of the cube and the line of points facing the "perpendicular" direction
al = intersection(ah,ab,z,aj)       #Lower-right of y11; Lower-left of y12; Upper-right of y21; Upper-left of y22             
am = intersection(ai,ac,z,aj)       #Lower-right of y12; Lower-left of y13; Upper-right of y22; Upper-left of y23             
an = intersection(ah,ab,aa,ak)      #Lower-right of y21; Lower-left of y22; Upper-right of y31; Upper-left of y32             
ao = intersection(ai,ac,aa,ak)      #Lower-right of y22; Lower-left of y23; Upper-right of y32; Upper-left of y33             

#Creates the corners along the side edges of the cube
ap = (o[0],yPoint(a,r,o[0]))        #Lower-right of o13; Lower-left of b11; Upper-right of o23; Upper-left of b21             
aq = (o[0],yPoint(a,s,o[0]))        #Lower-right of o23; Lower-left of b21; Upper-right of o33; Upper-left of b31   
aw = (p[0],yPoint(b,r,p[0]))        #Lower-right of r13; Lower-left of g11; Upper-right of r23; Upper-left of g21             
ax = (p[0],yPoint(b,s,p[0]))        #Lower-right of r23; Lower-left of g21; Upper-right of r33; Upper-left of g31             

#Creates the remaining inner corners
#Done by finding the intersection of the "horizontal" row line and the vertical column line
au = (v[0],yPoint(b,r,v[0]))        #Lower-right of r11; Lower-left of r12; Upper-right of r21; Upper-left of r22             
av = (w[0],yPoint(b,s,w[0]))        #Lower-right of r22; Lower-left of r23; Upper-right of r32; Upper-left of r33             
at = (u[0],yPoint(a,r,u[0]))        #Lower-right of b12; Lower-left of b13; Upper-right of b22; Upper-left of b23
ar = (t[0],yPoint(a,s,t[0]))        #Lower-right of b21; Lower-left of b22; Upper-right of b31; Upper-left of b32             
             

#CREATES THE FACES OF THE RUBIX CUBE

#Creates the faces for each side:
#Each face on the side is depicted by a list containing the four corners that make up the face

#Top
ba = [o,ah,al,z]
bb = [ah,ai,am,al]
bc = [ai,q,aj,am]
bd = [z,al,an,aa]
be = [al,am,ao,an]
bf = [am,aj,ak,ao]
bg = [aa,an,ab,h]
bh = [an,ao,ac,ab]
bi = [ao,ak,p,ac]

#Front (appears on the left side of the cube)
bj = [ap,o,z,t]
bk = [aq,ap,t,ar]
bl = [k,aq,ar,ad]
bm = [t,z,aa,at]
bn = [ar,t,at,u]
bo = [ad,ar,u,ae]
bp = [at,aa,h,r]
bq = [u,at,r,s]
br = [ae,u,s,g]

#Right (appears on the right side of the cube)
bs = [r,h,ab,au]
bt = [s,r,au,v]
bu = [g,s,v,af]
bv = [au,ab,ac,w]
bw = [v,au,w,av]
bx = [af,v,av,ag]
by = [w,ac,p,aw]
bz = [av,w,aw,ax]
ca = [ag,av,ax,l]

#UPSIDE DOWN CREATION OF CUBE
#See corresponding variables above for comments.
#"ua" represents the same point on the u-cube as "a" does on the regular cube.

#Shift from the regular cube (so that both can be viewed simultaneously)
dx = 100
dy = 652.5

ua = (a[0]-dx,a[1]+dy)
ub = (b[0]-dx,ua[1])
ud = (ub[0]-d[0],d[1]+dy)
uc = (ud[0],ua[1])

distUAUD = distance(ua,ud)
distUBUD = distance(ub,ud)

ue = (ua[0] + distUAUD,ua[1])
uf = (ub[0] - distUBUD,ua[1])

ug = (uc[0],78.75) #78.75 is the y-coordinate by which the cubes appear to be aligned vertically for these dimensions

uh = (ug[0],ug[1]+height)
ui = (ug[0]-height,ug[1])
uj = (ug[0]+height,ug[1])

uk = intersection(ua,ug,ui,ue)
ul = intersection(ub,ug,uj,uf)

um = (uk[0],uk[1]+height)
un = (ul[0],ul[1]+height)

uo = [uk[0],yPoint(ua,uh,uk[0])]
up = [ul[0],yPoint(ub,uh,ul[0])]

uq = intersection(ua,up,ub,uo)

urowHeight = (uh[1]-ug[1])/3

ur= (ug[0],uh[1]-urowHeight)
us= (ug[0],uh[1]-2*urowHeight)

ut = intersection(ua,ur,uo,ug)
uu = intersection(ua,us,uo,ug)

uv = intersection(ub,us,up,ug)
uw = intersection(ub,ur,up,ug)

uz = (ut[0],yPoint(ua,uh,ut[0]))
uaa = (uu[0],yPoint(ua,uh,uu[0]))
uab = (uv[0],yPoint(ub,uh,uv[0]))
uac = (uw[0],yPoint(ub,uh,uw[0]))

uad = (uz[0],yPoint(ua,ug,uz[0]))
uae = (uaa[0],yPoint(ua,ug,uaa[0]))
uaf = (uab[0],yPoint(ub,ug,uab[0]))
uag = (uac[0],yPoint(ub,ug,uac[0]))

uah = intersection(ua,uab,uo,uq)
uai = intersection(ua,uac,uo,uq)
uaj = intersection(ub,uz,uq,up)
uak = intersection(ub,uaa,uq,up)

ual = intersection(ua,uab,uz,uaj)
uam = intersection(ua,uac,uz,uaj)
uan = intersection(ua,uab,uaa,uak)
uao = intersection(ua,uac,uaa,uak)

uap = (uo[0],yPoint(ua,ur,uo[0]))
uaq = (uo[0],yPoint(ua,us,uo[0]))
uar = (ut[0],yPoint(ua,us,ut[0]))
uat = (uu[0],yPoint(ua,ur,uu[0]))

uau = (uv[0],yPoint(ub,ur,uv[0]))
uav = (uw[0],yPoint(ub,us,uw[0]))
uaw = (up[0],yPoint(ub,ur,up[0]))
uax = (up[0],yPoint(ub,us,up[0]))


#CREATES THE FACES OF THE UPSIDE DOWN RUBIX CUBE

#Face corner-lists for each side:

#Bottom
uba = [uo,uah,ual,uz]
ubb = [uah,uai,uam,ual]
ubc = [uai,uq,uaj,uam]
ubd = [uz,ual,uan,uaa]
ube = [ual,uam,uao,uan]
ubf = [uam,uaj,uak,uao]
ubg = [uaa,uan,uab,uh]
ubh = [uan,uao,uac,uab]
ubi = [uao,uak,up,uac]

#Back (appears on the left side of the u-cube)
ubj = [uap,uo,uz,ut]
ubk = [uaq,uap,ut,uar]
ubl = [uk,uaq,uar,uad]
ubm = [ut,uz,uaa,uat]
ubn = [uar,ut,uat,uu]
ubo = [uad,uar,uu,uae]
ubp = [uat,uaa,uh,ur]
ubq = [uu,uat,ur,us]
ubr = [uae,uu,us,ug]

#Left (appears on the right side of the u-cube)
ubs = [ur,uh,uab,uau]
ubt = [us,ur,uau,uv]
ubu = [ug,us,uv,uaf]
ubv = [uau,uab,uac,uw]
ubw = [uv,uau,uw,uav]
ubx = [uaf,uv,uav,uag]
uby = [uw,uac,up,uaw]
ubz = [uav,uw,uaw,uax]
uca = [uag,uav,uax,ul]

#Creating each of the faces
#Each face is named, as explained above, using the first letter of its color name and then ij  notation for each face from top to bottom and from left to right
#Each face here is described using a list containing its "shape" (made up the corners found before) and its color name

#Top - Yellow
y11 = [ba,"YELLOW"]
y12 = [bb,"YELLOW"]
y13 = [bc,"YELLOW"]
y21 = [bd,"YELLOW"]
y22 = [be,"YELLOW"]
y23 = [bf,"YELLOW"]
y31 = [bg,"YELLOW"]
y32 = [bh,"YELLOW"]
y33 = [bi,"YELLOW"]

#Front - Blue
b11 = [bj,"BLUE"]
b21 = [bk,"BLUE"]
b31 = [bl,"BLUE"]
b12 = [bm,"BLUE"]
b22 = [bn,"BLUE"]
b32 = [bo,"BLUE"]
b13 = [bp,"BLUE"]
b23 = [bq,"BLUE"]
b33 = [br,"BLUE"]

#Right - Red
r11 = [bs,"RED"]
r21 = [bt,"RED"]
r31 = [bu,"RED"]
r12 = [bv,"RED"]
r22 = [bw,"RED"]
r32 = [bx,"RED"]
r13 = [by,"RED"]
r23 = [bz,"RED"]
r33 = [ca,"RED"]

#Bottom - White
w11 = [uba,"WHITE"]
w12 = [ubb,"WHITE"]
w13 = [ubc,"WHITE"]
w21 = [ubd,"WHITE"]
w22 = [ube,"WHITE"]
w23 = [ubf,"WHITE"]
w31 = [ubg,"WHITE"]
w32 = [ubh,"WHITE"]
w33 = [ubi,"WHITE"]

#Back - Green
g31 = [ubj,"GREEN"]
g21 = [ubk,"GREEN"]
g11 = [ubl,"GREEN"]
g32 = [ubm,"GREEN"]
g22 = [ubn,"GREEN"]
g12 = [ubo,"GREEN"]
g33 = [ubp,"GREEN"]
g23 = [ubq,"GREEN"]
g13 = [ubr,"GREEN"]

#Left - Orange
o31 = [ubs,"ORANGE"]
o21 = [ubt,"ORANGE"]
o11 = [ubu,"ORANGE"]
o32 = [ubv,"ORANGE"]
o22 = [ubw,"ORANGE"]
o12 = [ubx,"ORANGE"]
o33 = [uby,"ORANGE"]
o23 = [ubz,"ORANGE"]
o13 = [uca,"ORANGE"]

#For each "mini-cube" in the cube there are either 1, 2, or 3 faces (ie middles, edges, and corners)
#Each mini-cube variable contains a list of its faces:

#Top cubes
#These cubes contain all of the faces that touch the top of the cube. Therefore, each of these cubes contains a face from the top set of faces (yellow). 
#For convenience, the yellow face is always listed first. If the mini-cube is a corner, after yellow, the "left-most" face is listed.
#Since these mini-cubes transverse a face, the labelling of variables follows the left->right, top->bottom pattern as seen earlier with the yellow face. The numbers here, however, go from 1-9.
top1 = [y11,o13,b11]
top2 = [y12,o12]
top3 = [y13,g13,o11]
top4 = [y21,b12]
top5 = [y22]
top6 = [y23,g12]
top7 = [y31,b13,r11]
top8 = [y32,r12]
top9 = [y33,r13,g11]

#Middle cubes
#Cubes around the middle starting from the orange and blue edge (the piece directly underneath the top1 mini-cube) and going clockwise around the cube.
#The "more clockwise" face is listed first (ie the face most to the left)
mid1 = [o23,b21]
mid2 = [o22]
mid3 = [g23,o21]
mid4 = [g22]
mid5 = [r23,g21]
mid6 = [r22]
mid7 = [b23,r21]
mid8 = [b22]

#Bottom cubes
#These cubes contain all of the faces that touch the bottom of the cube. Therefore, each of these cubes contains a face from the bottom set of faces (white). 
#For convenience, the white face is always listed last. If the mini-cube is a corner, the order faces is right, left, bottom.
#Since these mini-cubes transverse a face, the labelling of variables follows the left->right, top->bottom pattern as seen earlier with the white face. The numbers here, however, go from 1-9.
bot1 = [g31,r33,w11]
bot2 = [r32,w12]
bot3 = [r31,b33,w13]
bot4 = [g32,w21]
bot5 = [w22]
bot6 = [b32,w23]
bot7 = [o31,g33,w31]
bot8 = [o32,w32]
bot9 = [b31,o33,w33]

#DIFFERENT WAYS TO UNDERSTAND RUBIX CUBES

#Lists of types of cubes:
corners = [top1,top3,top7,top9,bot1,bot7,bot9,bot3]
edges = [top2,top4,top6,top8,mid1,mid3,mid5,mid7,bot2,bot4,bot6,bot8]
centers = [top5,mid6,mid4,mid8,mid2,bot5]

#Lists of layers of cubes:
tops = [top1,top2,top3,top4,top5,top6,top7,top8,top9]
mids = [mid1,mid2,mid3,mid4,mid5,mid6,mid7,mid8]
bots = [bot1,bot2,bot3,bot4,bot5,bot6,bot7,bot8,bot9]

#Sides of a rubix cube:
#The lists are organized so that each item in the list is "touching" the previous and next cubes on the list. This will be helpful when rotating any of the sides because their colors will "shift"
right = [top7,top8,top9,mid5,bot1,bot2,bot3,mid7]
left = [top3,top2,top1,mid1,bot9,bot8,bot7,mid3]

front = [top1,top4,top7,mid7,bot3,bot6,bot9,mid1]
back = [top9,top6,top3,mid3,bot7,bot4,bot1,mid5]

up = [top7,top4,top1,top2,top3,top6,top9,top8]      #top
down = [bot3,bot6,bot9,bot8,bot7,bot4,bot1,bot2]    #bottom

#Ways to think of an overall rubix cube:
layers = [tops,mids,bots]
types = [corners,edges,centers]    
sides = [right,left,front,back,up,down]

#Unchanging copies of what a solved rubix cube looks like:
endLayers = copy.deepcopy(layers)
endTypes = copy.deepcopy(types)

#DRAWING FUNCTIONS

#Draws the Rubiks cube
def drawCube(z):
    Draw.clear()
    for i in range(len(z)):                        
        for j in range(len(z[i])):                 
            for k in range(len(z[i][j])):           
                Draw.setColor(z[i][j][k][1])
                Draw.filledPolygon(z[i][j][k][0])
                drawOutline(z[i][j][k][0])
    Draw.show(time)

#Draws the black border surrounding each of the mini-cubes
def drawOutline(pol):
    Draw.setColor(Draw.BLACK)
    Draw.polygon(pol)
    Draw.polygon(pol)
    
#Draws a shape over the rubix cube containing text
def drawButton(text):                       #Takes parameter of text to finish the "Click to" sentence
    Draw.setColor("WHITE")
    Draw.filledOval(500,250,399,199)
    Draw.setColor("BLACK")
    Draw.oval(500,250,400,200)

    Draw.setFontSize(40)
    Draw.setFontFamily("Minion Pro")
    Draw.string("CLICK TO", 580, 275)
    Draw.string(text, 580, 350)             #Finishes the "Click to" sentence on the next line
    
    Draw.show(time)
    waitForClick()

#Button remains on screen from the time it is drawn until the client clicks anywhere on the screen
def waitForClick():
    while True:
        if Draw.mousePressed():
            Draw.clear()
            return

#Sets up the cube to be mixed
def setCube():     drawCube(layers)         #Although this is really just calling the drawCube function, it was more consistant to use a function in my main that 1) started with an s and 2) didn't take any parameters

#MOVING FUNCTIONS

#Function that rotates a given side clockwise
def clockwise(side):
    #Temporary copies of cube colors so that they can be re-given to the appropriate cube after it has been replaced with the new colors
    temp0 = [copy.deepcopy(side[0][0][1]),copy.deepcopy(side[0][1][1]),copy.deepcopy(side[0][2][1])]
    temp1 = [copy.deepcopy(side[1][0][1]),copy.deepcopy(side[1][1][1])]    
    temp6 = [copy.deepcopy(side[6][0][1]),copy.deepcopy(side[6][1][1]),copy.deepcopy(side[6][2][1])]
    temp7 = [copy.deepcopy(side[7][0][1]),copy.deepcopy(side[7][1][1])]    
    
    #Because the items are all in the same plane, turning this side is different from turning sides that contain mini-cubes from different planes
    if side == up:
        for i in range(7,1,-1):
            for j in range(len(side[i])):
                side[i][j][1]=side[i-2][j][1]
        #side1:
        side[1][0][1] = temp7[0]
        side[1][1][1] = temp7[1]
        #side0:
        side[0][0][1] = temp6[0]
        side[0][1][1] = temp6[1]
        side[0][2][1] = temp6[2]
    elif side == down:                              
        for i in range(0,6):
            for j in range(len(side[i])):
                side[i][j][1]=side[i+2][j][1]
        #side7:
        side[7][0][1] = temp1[0]
        side[7][1][1] = temp1[1]
        #side6:
        side[6][0][1] = temp0[0]
        side[6][1][1] = temp0[1]
        side[6][2][1] = temp0[2]
    
    #right, left, front, and back all behave similarly when turned
    else:    
        #side6:
        side[6][0][1] = side[4][1][1]
        side[6][1][1] = side[4][2][1]
        side[6][2][1] = side[4][0][1]
        #side4:
        side[4][0][1] = side[2][0][1]
        side[4][1][1] = side[2][1][1]
        side[4][2][1] = side[2][2][1]
        #side2:
        side[2][0][1] = side[0][1][1]
        side[2][1][1] = side[0][2][1]
        side[2][2][1] = side[0][0][1]
        #side0:
        side[0][0][1] = temp6[1]
        side[0][1][1] = temp6[2]
        side[0][2][1] = temp6[0]
        #side7:
        side[7][0][1] = side[5][1][1]
        side[7][1][1] = side[5][0][1]
        #side5:
        side[5][0][1] = side[3][0][1]
        side[5][1][1] = side[3][1][1]
        #side3:
        side[3][0][1] = side[1][1][1]
        side[3][1][1] = side[1][0][1]
        #side1:
        side[1][0][1] = temp7[0]
        side[1][1][1] = temp7[1]
    drawCube(layers)
    Draw.show(time)
    
#Function that roates a given side counter-clockwise
#See notes by "clockwise"
def counterClockwise(side):
    temp0 = [copy.deepcopy(side[0][0][1]),copy.deepcopy(side[0][1][1]),copy.deepcopy(side[0][2][1])]
    temp1 = [copy.deepcopy(side[1][0][1]),copy.deepcopy(side[1][1][1])]
    temp6 = [copy.deepcopy(side[6][0][1]),copy.deepcopy(side[6][1][1]),copy.deepcopy(side[6][2][1])]
    temp7 = [copy.deepcopy(side[7][0][1]),copy.deepcopy(side[7][1][1])]       
    if side == up:
        for i in range(0,6):
            for j in range(len(side[i])):
                side[i][j][1]=side[i+2][j][1]
        #side7:
        side[7][0][1] = temp1[0]
        side[7][1][1] = temp1[1]
        #side0:
        side[6][0][1] = temp0[0]
        side[6][1][1] = temp0[1]
        side[6][2][1] = temp0[2]
    elif side == down:
        for i in range(7,1,-1):
            for j in range(len(side[i])):
                side[i][j][1]=side[i-2][j][1]
        #side1:
        side[1][0][1] = temp7[0]
        side[1][1][1] = temp7[1]
        #side0:
        side[0][0][1] = temp6[0]
        side[0][1][1] = temp6[1]
        side[0][2][1] = temp6[2]
    else:
        #side0:
        side[0][0][1] = side[2][2][1]
        side[0][1][1] = side[2][0][1]
        side[0][2][1] = side[2][1][1]
        #side2:
        side[2][0][1] = side[4][0][1]
        side[2][1][1] = side[4][1][1]
        side[2][2][1] = side[4][2][1]
        #side4:
        side[4][0][1] = side[6][2][1]
        side[4][1][1] = side[6][0][1]
        side[4][2][1] = side[6][1][1]
        #side6:
        side[6][0][1] = temp0[2]
        side[6][1][1] = temp0[0]
        side[6][2][1] = temp0[1]
        #side1:
        side[1][0][1] = side[3][1][1]
        side[1][1][1] = side[3][0][1]
        #side3:
        side[3][0][1] = side[5][0][1]
        side[3][1][1] = side[5][1][1]
        #side5:
        side[5][0][1] = side[7][1][1]
        side[5][1][1] = side[7][0][1]
        #side7:
        side[7][0][1] = temp1[0]
        side[7][1][1] = temp1[1]
    drawCube(layers)
    Draw.show(time)

#Function that takes many movements as parameters through "shorthand" and implements the movements in order
#"c" stands for clockwise
#"cc" stands for counter-clockwise
#sides are abbreviated to their first letter
def chain(*args):
    for i in args:
        if i == "cr":          clockwise(right)
        elif i == "ccr":       counterClockwise(right)
        elif i == "cl":        clockwise(left)
        elif i == "ccl":       counterClockwise(left)
        elif i == "cf":        clockwise(front)
        elif i == "ccf":       counterClockwise(front)
        elif i == "cb":        clockwise(back)
        elif i == "ccb":       counterClockwise(back)
        elif i == "cu":        clockwise(up)
        elif i == "ccu":       counterClockwise(up)
        elif i == "cd":        clockwise(down)
        else:                  counterClockwise(down)        

#MIXING UP THE RUBIX CUBE

#Shuffles the cube
def shuffleCube():
    drawButton("SHUFFLE!")              #The drawButton function already contains the instructions to print "Click to" and takes a pararmeter to finish the setence                          #
    
    #randomly chooses 100 numbers
    #if the number is even, a randomly chosen side is turned clockwise, if the nuber is odd, a randomly chosen side is turned counterclockwise
    for i in range(100):
        if random.randint(1,2)%2 == 0:
            clockwise(random.choice(sides))
        else:
            counterClockwise(random.choice(sides))

#SOLVING THE RUBIX CUBE

#Steps to solve a rubix cube
def solveCube():
    drawButton("  SOLVE!")              #The drawButton function draws texts that is left-aligned; the spaces before the word "solve" serve to center the text
    fixTop()
    fixMiddle()
    fixBottom()

#SOLVING THE TOP OF THE CUBE

#Fixes the top of the cube  
def fixTop():
    fix("corner")
    fix("edge")

#Fixes the mini-cubes on the top layer of the cube
def fix(kind):
    if kind == "corner":     x = 0
    if kind == "edge":       x = 1
    for i in range(4):   #There are 4 corners and 4 edges on the top side of the cube that need to be checked for accuracy
        if types[x][i] != endTypes[x][i]:       #Checks if current piece matches the "original"/right mini-cube in that place
            place,orientation = find(kind,endTypes[x][i]) #Finds where the right piece is on the cube
            if place < 4:               #This means that the right piece is found on the top of the cube but in an incorrect position or orientation
                offTop(kind,place,orientation)
                place,orientation = find(kind,endTypes[x][i])
            place,orientation = inLine(kind,i,place,orientation)
            putIn(kind,i,place,orientation)
        reset("top")

#Finds the location of any piece in the cube
#Function behaves differently for corners and edges
#Returns its position and orientation
def find(kind,endNum):
    if kind == "corner":
        for j in range(len(types[0])):
            if corners[j][0][1] == endNum[0][1] and \
               corners[j][1][1] == endNum[1][1] and \
               corners[j][2][1] == endNum[2][1]:
                return j, 0
            if corners[j][0][1] == endNum[1][1] and \
               corners[j][1][1] == endNum[2][1] and \
               corners[j][2][1] == endNum[0][1]:
                return j, 2
            if corners[j][0][1] == endNum[2][1] and \
               corners[j][1][1] == endNum[0][1] and \
               corners[j][2][1] == endNum[1][1]:
                return j, 1
            if corners[j][0][1] == endNum[0][1] and \
               corners[j][1][1] == endNum[2][1] and \
               corners[j][2][1] == endNum[1][1]:
                return j, 0
            if corners[j][0][1] == endNum[1][1] and \
               corners[j][1][1] == endNum[0][1] and \
               corners[j][2][1] == endNum[2][1]:
                return j, 1
            if corners[j][0][1] == endNum[2][1] and \
               corners[j][1][1] == endNum[1][1] and \
               corners[j][2][1] == endNum[0][1]:
                return j, 2           
    if kind == "edge":
        for j in range(len(edges)):
                if edges[j][0][1] == endNum[0][1] and \
                   edges[j][1][1] == endNum[1][1]:
                    return j, 0
                if edges[j][0][1] == endNum[1][1] and \
                   edges[j][1][1] == endNum[0][1]:
                    return j, 1
        

#"Knocks out" a piece that belongs on the top of the but is currently on the top in an incorrect position or orientation. Function ensures that the piece taken down does not end up with its yellow face on the bottom of the cube
#Function behaves differently for corners and edges
def offTop(kind,p,o):
    if kind == "corner":
        if p == 0:
            if o != 2:      chain("cl","cd","ccl")                         
            else:           chain("ccf","ccd","cf")
        if p == 1:
            if o != 2:      chain("cb","cd","ccb")
            else:           chain("ccl","ccd","cl")
        if p == 2:
            if o != 2:      chain("cf","cd","ccf")
            else:           chain("ccr","ccd","cr")
        if p == 3:
            if o != 2:      chain("cr","cd","ccr")
            else:           chain("ccb","ccd","cb")
    if kind == "edge":
        if o == 0:
            if p == 0:      chain("cf","ccb","cl","ccf","cb")
            if p == 1:      chain("cr","ccl","cf","ccr","cl")
            if p == 2:      chain("cl","ccr","cb","ccl","cr")
            if p == 3:      chain("ccf","cb","cr","cf","ccb")
        if o == 1:
            if p == 0:      chain("cl","cu","ccd","ccb","ccu")
            if p == 1:      chain("cf","cu","ccd","ccl","ccu")
            if p == 2:      chain("cb","cu","ccd","ccr","ccu")
            if p == 3:      chain("cr","cu","ccd","ccf","ccu")
            
#Lines up the correct piece in "front" of its true location for easy fixing
#Function behaves differents for corners, edges that go on top, and edges that go in the middle layer
def inLine(kind,i,p,o):
    if kind == "corner":
        if i == 0:
            while p != 6:
                clockwise(down)
                p, o, = find("corner",endTypes[0][i])
        if i == 1:
            while p != 5:
                clockwise(down)
                p, o, = find("corner",endTypes[0][i])
        if i == 2:
            while p != 7:
                clockwise(down)
                p, o, = find("corner",endTypes[0][i])
        if i == 3:
            while p != 4:
                clockwise(down)
                p, o, = find("corner",endTypes[0][i])            
        if o == 2:
            if p == 4:      chain("cr","ccd","ccr")
            elif p == 7:    chain("ccr","cd","cr")
            elif p == 5:    chain("ccl","cd","cl")
            elif p == 6:    chain("cl","ccd","ccl")
            chain("cd","cd")
        p, o, = find("corner",endTypes[0][i])
        return p,o
    if kind == "edge":
        if p > 7:
            while i + p != 11:
                clockwise(down)
                p, o, = find("edge",endTypes[1][i])
        else:
            if (p == 4 and o == 0) or (p == 7 and o == 1):
                if i == 0:     counterClockwise(up)
                if i == 2:     chain("cu", "cu")
                if i == 3:     clockwise(up)           
            if (p == 5 and o == 0) or (p == 4 and o == 1):   
                if i == 1:     clockwise(up)
                if i == 2:     counterClockwise(up)
                if i == 3:     chain("cu","cu")
            if (p == 6 and o == 0) or (p == 5 and o == 1) :
                if i == 0:     clockwise(up)
                if i == 1:     chain("cu","cu")
                if i == 3:     counterClockwise(up)             
            if (p == 7 and o == 0) or (p == 6 and o == 1):
                if i == 0:     chain("cu","cu")
                if i == 1:     counterClockwise(up) 
                if i == 2:     clockwise(up)
        p, o, = find("edge",endTypes[1][i])
        return p,o        
    if kind == "middle":                    
        while types[1][p][0][1] != types[2][p-7][0][1]:
            clockwise(down)
            p,o = find("edge",endTypes[1][i])
        return        
    
#Puts a piece into its true place on the cube
#Function behaves differents for corners, edges that go on top, and edges that go in the middle layer
def putIn(kind,i,p,o):
    if kind == "corner":
        if i == 0:
            if o == 0:      chain("cd","cl","ccd","ccl")
            if o == 1:      chain("ccd","ccf","cd","cf")               
        if i == 1:
            if o == 0:      chain("cd","cb","ccd","ccb")
            if o == 1:      chain("ccd","ccl","cd","cl")
        if i == 2:
            if o == 0:      chain("cd","cf","ccd","ccf")            
            if o == 1:      chain("ccd","ccr","cd","cr")
        if i == 3:
            if o == 0:      chain("cd","cr","ccd","ccr")
            if o == 1:      chain("ccd","ccb","cd","cb")
    if kind == "edge":
        if p == 8:
            if o == 0:     chain("cd","ccf","cb","ccr","cf","ccb")
            if o == 1:     chain("ccf","cb","ccr","ccr","cf","ccb")
        if p == 9:
            if o == 0:     chain("cd","ccr","cl","ccb","cr","ccl")
            if o == 1:     chain("ccr","cl","ccb","ccb","cr","ccl")
        if p == 10:
            if o == 0:     chain("cd","cr","ccl","ccf","ccr","cl")
            if o == 1:     chain("cr","ccl","ccf","ccf","ccr","cl")
        if p == 11:
            if o == 0:     chain("cd","cf","ccb","ccl","ccf","cb")
            if o == 1:     chain("cf","ccb","ccl","ccl","ccf","cb")
        if p == 4:
            if o == 0:     chain("ccu","ccr","cu","ccd","cf")
            if o == 1:     chain("cu","cb","ccu","cd","ccl")
        if p == 5:
            if o == 0:     chain("ccu","ccf","cu","ccd","cl")
            if o == 1:     chain("cu","cr","ccu","cd","ccb")
        if p == 6:
            if o == 0:     chain("ccu","ccl","cu","ccd","cb")
            if o == 1:     chain("cu","cf","ccu","cd","ccr")
        if p == 7:
            if o == 0:     chain("ccu","ccb","cu","ccd","cr")
            if o == 1:     chain("cu","cl","ccu","cd","ccf")
    if kind == "middle":
        if p < 8: k = p
        else:     k = i
        if k == 4:
            if o == 0:     chain("ccd","ccf","cd","cf","cd","cl","ccd","ccl")
            else:          chain("cd","cl","ccd","ccl","ccd","ccf","cd","cf")
        if k == 5:
            if o == 0:     chain("ccd","ccl","cd","cl","cd","cb","ccd","ccb")
            if o == 1:     chain("cd","cb","ccd","ccb","ccd","ccl","cd","cl")
        if k == 6:
            if o == 0:     chain("ccd","ccb","cd","cb","cd","cr","ccd","ccr")
            if o == 1:     chain("cd","cr","ccd","ccr","ccd","ccb","cd","cb")
        if k == 7:
            if o == 0:     chain("ccd","ccr","cd","cr","cd","cf","ccd","ccf")
            if o == 1:     chain("cd","cf","ccd","ccf","ccd","ccr","cd","cr")        

#Sets the given layer to its original orientation by taking a correct piece and rotating the side given until the correct piece is where it should be)
#Function behaves differently for top and bottom
def reset(side):
    if side == "top":
        while types[0][0][1][1] != "ORANGE":    clockwise(up)
    if side == "bottom":
        while bot6[0][1] != "BLUE":             clockwise(down) 

#SOLVING THE MIDDLE LAYER OF THE CUBE

def fixMiddle():
    for i in range(4,8):
        if types[1][i] != endTypes[1][i]:
            p,o = find("edge",endTypes[1][i])
            while p < 8:                        #If the right cube is in the middle layer but in the wrong place or orientation
                putIn("middle",i,p,0)        #Puts a wrong middle mini-cube into its place to knock the true piece down to the bottom to be fixed
                p,o = find("edge",endTypes[1][i])
            inLine("middle",i,p,o)
            putIn("middle",i,p,o) 

#SOLVING THE BOTTOM OF THE CUBE

def fixBottom():
    havePlus()
    haveEdges()
    haveCorners()

#Looking for a white plus sign on the bottom of the cube
#If there is no plus, get it
def havePlus():
    while bot2[1][1] != "WHITE" or bot4[1][1] != "WHITE" or \
       bot6[1][1] != "WHITE" or bot8[1][1] != "WHITE":  
        get("plus")      
    reset("bottom")
    
#Looking for the non-white edges to be in the right place
#If they are not, set up and get them
def haveEdges():
    while bot2[0][1] != "RED" or bot4[0][1] != "GREEN" or \
       bot8[0][1] != "ORANGE":      #Looking if the non-white sides of the edges are in the right places
        setBottom("edge")
        get("edge")
        reset("bottom")
        
def haveCorners():
    while "RED" not in [bot1[0][1],bot1[1][1],bot1[2][1]] or "GREEN" not in \
          [bot1[0][1],bot1[1][1],bot1[2][1]] or "RED" not in \
          [bot3[0][1],bot3[1][1],bot3[2][1]] or "BLUE" not in \
          [bot3[0][1],bot3[1][1],bot3[2][1]] or "ORANGE" not in \
          [bot7[0][1],bot7[1][1],bot7[2][1]] or "GREEN" not in \
          [bot7[0][1],bot7[1][1],bot7[2][1]]:
        setBottom("corner")
        get("corner")
        reset("bottom")       
    orientCorners()
    reset("bottom")


def get(what):
    if what == "plus":
        #Makes a white plus sign on the bottom of the cube
        #There are two different functions that can be used to get the plus (fur and fru), each is more helpful in particular circumstances
        #plus checks the curent circumstances and then calls the more appropriate function
        #If there is a circustance where neither will immediately get the plus, fru is used
        if bot8[1][1] == bot2[1][1]:
            do("fru")
        elif bot6[1][1] == bot4[1][1]:
            clockwise(down)
            do("fru")
        elif bot8[1][1] == bot6[1][1]:
            do("fur")
        elif bot8[1][1] == bot4[1][1]:
            clockwise(down)
            do("fur")
        elif bot4[1][1] == bot2[1][1]:
            chain("cd","cd")
            do("fur")
        elif bot2[1][1] == bot6[1][1]:
            counterClockwise(down)
            do("fur")
        else:
            do("fru")
    if what == "edge":
         #Formula to fix the bottom edges
        chain("cr","cd","ccr","cd","cr","cd","cd","ccr")
    if what == "corner":
        chain("cd","cr","ccd","ccl","cd","ccr","ccd","cl")  #Formula to fix the bottom corners
        
#A chain of movements that will help get a plus sign on the bottom if there is a straight line of whites already there
def do(formula):
    if formula == "fru":     chain("cb","cr","cd","ccr","ccd","ccb")
    else:                    chain("cb","cd","cr","ccd","ccr","ccb")


#Sets up mini-cubes in a way that will be helpful when using formulas to solve them
def setBottom(kind):
    if kind == "edge":
        #Helpful position for fixing bottom edges: having two correct edge next to each other or having one right edge in the back
        
        #Because we just reset the bottom, we know that bot6 is blue (that is the criteria for a completed reset)
        if bot2[0][1] == "RED":
            return
        else:
            chain("cd","cd")        #Putting the known blue edge in the black
    if kind == "corner":
        #Helpful position for fixing bottom corners: having to have two correct corners next to each other or having one right corner in the back right
        if "RED" in [bot1[0][1],bot1[1][1],bot1[2][1]] and \
           "GREEN" in [bot1[0][1],bot1[1][1],bot1[2][1]]:
            pass
        elif "RED" in [bot3[0][1],bot3[1][1],bot3[2][1]] and \
             "BLUE" in [bot3[0][1],bot3[1][1],bot3[2][1]]:
            clockwise(down)
        elif "ORANGE" in [bot7[0][1],bot7[1][1],bot7[2][1]] and \
             "GREEN" in [bot7[0][1],bot7[1][1],bot7[2][1]]:    
            counterClockwise(down)
        else:
            chain("cd","cd")        
           
#Reorients the corners so that white is on the bottom
#DEpending on how poorly the corner is oriented, it will need a particulr number of readjustments
def orientCorners():
    for i in range(4):
        if bot1[0][1] == "WHITE":
            doubleDownAway()
            doubleDownAway()
        if bot1[1][1] == "WHITE":
            doubleDownAway()
        counterClockwise(down)

#Takes the incorrectly oriented corner out or puts it back in with a different orientation
def downAway():
    counterClockwise(right)
    counterClockwise(up)
    clockwise(right)
    clockwise(up)

#Two times the previous function (Takes the corner out and puts it back in)
def doubleDownAway():
    downAway()  
    downAway()

################################################################################

Draw.setCanvasSize(1500,1500)   
time = 50
setCube()
shuffleCube()
time = 200
solveCube()
