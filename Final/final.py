"""
Comp112: Best Fitting Circles: Final Project
Oren Finard

Note: This program is meant to run on closed, solid objects.  It is
        not meant for use on lines or rings, or anything of a similar
        variety.
"""

import Image
import ImageDraw
import ImageFilter
import math


def xy2linear(x, y, w):
    """
    x: int
    y: int
    w: int

    return x+y*w: int

    Takes the xy-coordinates of a pixel and the width
    of the image and returns its linear coordinate
    """
    return x+y*w

def xy2reverse(inte, w):
    """
    inte: int
    w: int

    return (p,q): int*int

    Takes the linear coordinate of a pixel and width of
    the image, and returns the xy-coordinates of the
    pixel
    """
    p = inte%w
    q = (inte - p)/w
    return (p, q)

def xy2revtrans(inte, w, x_bar, y_bar):
    """
    inte: int
    w: int
    x_bar: int
    y_bar: int

    Takes the linear coordinate of a pixel, the width of the image,
    and translation-shift coordinates x_bar and y_bar, and returns
    the xy-coordinates of the pixel, translate-shifted.
    """
    p,q = xy2reverse(inte, w)
    u = p - x_bar
    v = q - y_bar
    return u,v


def producer(r):
    """
    r: int

    return (2+r) + (2+r)*width: int

    producer takes the given r, and creates a
    circle of radius r, and saves it under the
    filename ```"new" +str((2+r) + (2+r)*width) + ".jpg"```

    So for a circle of radius 15, the center would be at
    pixel 782, so the file would be named "new782.jpg"

    The returned integer is the circle center pixel
    """
    
    img = Image.new('L', (3*r, 3*r), 'white')
    width, height = img.size
    draw = ImageDraw.Draw(img)
    draw.ellipse((r/2, r/2, r/2+2*r, r/2+2*r), outline = 'black', fill = 'black')
    img.save("new" + str((2+r) + (2+r)*width) +".jpg")

    return (2+r) + (2+r)*width
        

def summer(u_set, (upow, vpow)):
    """
    u_set: set of tuples of int*int
    upow,vpow: int*int

    return u_sum: int

    summer iterates through u_set, and summs the terms in the tuples (u,v)
    by performing THE SUMMATION OF:(u**upow)*(v**vpow).
    """
    u_sum = 0
    for u,v in u_set:
        u_sum += (u**upow)*(v**vpow)
    
    return u_sum


def lscf(filename):
    """

    filename: file

    return xc, yc, rad_int, rad_raw: int*int*int*int


    lsfc (stands for Least-Squares Circle Fit) takes an image file and
    calculates the Least-Squared Circle by treating each edge point like an
    individual data point.  The LSC is, arguably, the definition of the
    BFC in terms of statistics.
    It returns the xy-coordinates of the center of the LSC (xc, yc), as well
    as the radius used (rad_int) and the radius calculated (rad_raw)
    """


    
    img = Image.open(filename)
    img = img.convert('L')
    img_e = img.filter(ImageFilter.FIND_EDGES)
    width, height = img.size
    
    sseett = set()
    edata = list(img_e.getdata())
    
    #inversion engine
    for x in range(len(edata)):
        x_lin, y_lin = xy2reverse(x, width)
        if x_lin in [0, width - 1] or y_lin in [0, height - 1]:
            edata[x] = 255
        else:
            edata[x] = abs(edata[x]-255)
    
    
        if edata[x] !=0:
            edata[x] =255
        else:
            sseett.add(x)
        
    
    img_e.putdata(edata)
    #img.show()
    

    x_bar = 0
    y_bar = 0
    u_set = set()
    

    for x in sseett:
        xi, yi = xy2reverse(x, width)
        x_bar += xi
        y_bar += yi
    
    x_bar = x_bar/len(sseett)
    y_bar = y_bar/len(sseett)


    for x in sseett:
        u, v = xy2revtrans(x, width, x_bar, y_bar)
        u_set.add((u,v))
    

    vc = (1/2)*(summer(u_set, (0,3)) + summer(u_set, (2,1)) - (summer(u_set, (1,1)))*((summer(u_set, (3,0)) + summer(u_set, (1,2)))/(summer(u_set, (2,0)))))/(summer(u_set, (0,2)) - (((summer(u_set, (1,1)))**2)/(summer(u_set, (2,0)))))
    uc = (((1/2)*(summer(u_set, (3,0)) + summer(u_set, (1,2))) - vc*summer(u_set, (1,1)))/(summer(u_set, (2,0))))

    
    xc = uc + x_bar
    yc = vc + y_bar

    

    R2 = uc**2 + vc**2 + ((summer(u_set, (2,0)) + (summer(u_set, (0,2))))/len(sseett))

    rad_raw = math.sqrt(R2)
    rad_int = int(rad_raw)
    print("{0} is the raw radius, {1} is the radius used".format(rad_raw, rad_int))

    data = list(img.getdata())
    for x in range(len(data)):
        edata[x] = (edata[x], edata[x], edata[x])
        data[x] = (data[x], data[x], data[x])


    img_new = Image.new("RGB", (width,height))
    img_ed = Image.new("RGB", (width,height))
    img_new.putdata(data)
    img_ed.putdata(edata)
    draw = ImageDraw.Draw(img_new)
    draw_ed = ImageDraw.Draw(img_ed)
    draw.ellipse((xc - rad_int, yc-rad_int, xc + rad_int, yc + rad_int), outline = 'red')
    draw_ed.ellipse((xc - rad_int, yc - rad_int, xc + rad_int, yc + rad_int), outline = 'red')
    img_new.show()
    img_ed.show()

    
    #drawable = ImageDraw.Draw(img)
    #drawable.ellipse((xc-rad_int, yc-rad_int, xc+rad_int, yc+rad_int), outline = 'grey')
    #img.show()

    '''website where I found the math to back this method up: http://www.dtcenter.org/met/users/docs/write_ups/circle_fit.pdf'''

    
    return (xc, yc), rad_int, rad_raw





def rad_test(inte, (width,height), (minrd, maxrd), bag):
    """
    inte:  int
    width, height: int*int
    minrd, maxrd: int*int
    bag : list

    return maxr, maxcount : int, int

    rad_test takes inte, the linear pixel coordinate of a given pixel,
    the width and height of the image the pixel is in, the minimum and
    maximum radius (minrd & maxrd) of the possible circles at that point,
    and bag, the list of edge points  of the original image,
    and returns the radius (maxr) of the circle that has the initial pixel as a center
    and intersects the most edge points of all possible circles.
    It also returns the number of points that this 'best circle' intersects (maxcount).
    """
    
    xp, yp = xy2reverse(inte, width)
    
    
    length = width*height
    maxcount = 0
    maxr = 0
    for r in range(minrd,maxrd+1):
        img= Image.new('L', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        draw.ellipse((xp - r, yp - r, xp + r, yp + r), outline = 'black')
        data = list(img.getdata())
        counter = 0
        
        jkj = 0
        for x in bag:
            if data[x] == 0:
                counter +=1
        
        if counter > maxcount:
            maxcount = counter
            maxr = r
            
    return (maxr, maxcount)




def kindle(filename):
    """
    filename: string

    return x_small, y_small, minrd_small : int*int*int

    kindle takes an image file, opens it, then resizes the image down to a
    size that fire_starter can handle efficiently.  fire_starter returns the
    best fitting circle for that image, and then kindle upgrades all the info,
    and runs more circle tests until the best fitting circle for the original
    size is found and returned.  It then shows us the image and the BFC in two
    ways: the original image, with the overlaid BFC in red, and the edge-filtered image
    with the overlaid BFC in red.
    It returns the xy-coordinates of best-fitting circle's center (x_small & y_small),
    and also the radius of the best-fitting circle (minrd_small).
    """

    
    img = Image.open(filename)
    img = img.convert('L')
    img_e = img.filter(ImageFilter.FIND_EDGES)
    
    
    squid = 0 #the downsizing counter: how many exponents of 2 the image width and height are divided by
    width, height = img.size
    width_new, height_new = width, height
    while width_new >50:
        width_new = width_new/2
        height_new = height_new/2
        squid += 1
    img_low = img.resize((width/(2**squid), height/(2**squid))) #after checking different filters, the default NEAREST filter was found to be most efficient
    x_small, y_small, minrad_small, maxcount, bagsize = fire_starter(img_low, (0,0),0, 0)
    x_big, y_big, minrad_big = (x_small+1)*2-1, (y_small+1)*2-1, minrad_small*2 #this resizing is not exact, but defines the upper limits of the 3x3 box of possible best-fitting points
    squid += -1

    
    while squid >-1:
        img_mid = img.resize((width/(2**squid), height/(2**squid)))
        x_small, y_small, minrad_small, maxcount, bagsize = fire_starter(img_mid, (x_big, y_big), minrad_big, 1)
        x_big, y_big, minrad_big = (x_small+1)*2-1, (y_small+1)*2-1, minrad_small*2
        squid += -1


    
    data = list(img.getdata())
    edata = list(img_e.getdata())
    for x in range(len(data)):
        data[x] = (data[x], data[x], data[x])
        x_lin,y_lin = xy2reverse(x, width)

        if x_lin in [0, width - 1] or y_lin in [0, height - 1]:
            edata[x] = (255,255,255)
        else:
            edata[x] = abs(edata[x]-255)
            if edata[x] != 0:
                edata[x] = (255, 255, 255)
            else:
                edata[x] = (0,0,0)


    img_new = Image.new("RGB", (width,height))
    img_ed = Image.new("RGB", (width,height))
    img_new.putdata(data)
    img_ed.putdata(edata)
    draw = ImageDraw.Draw(img_new)
    draw_ed = ImageDraw.Draw(img_ed)
    draw.ellipse((x_small - minrad_small, y_small-minrad_small, x_small + minrad_small, y_small + minrad_small), outline = 'red')
    draw_ed.ellipse((x_small - minrad_small, y_small - minrad_small, x_small + minrad_small, y_small + minrad_small), outline = 'red')
    img_new.show()
    img_ed.show()

    print("the best fitting circle has center {0} and radius {1}, and intersects roughly {2} out of {3} points".
          format((x_small,y_small), minrad_small, maxcount, bagsize))
    print("document size is {0}".format((width, height)))


    
    return (x_small, y_small), minrad_small


def fire_starter(img, (x_big, y_big), maxrad, first):
    """
    img: Image
    x_big, y_big: int*int
    maxrad: int
    first: int (=0 or !=0)

    return xwin, ywin, maxr: int*int*int

    
    fire_starter either proccesses small images (50x50 or smaller) and checks every pixel
    and radius in search of the BFC (which happens if first = 0), or searches a specific
    box of pixels and a specific set of radii to find the BFC (which happens if first !=0
    """
    
    img = img.filter(ImageFilter.FIND_EDGES)
    #img = img.convert('L')
    width, height = img.size
    #img.show()
    
    bag = set()
    data = list(img.getdata())
    starter = 0
   
    #inversion engine
    for x in range(len(data)):
        x_lin, y_lin = xy2reverse(x, width)
        if x_lin in [0, width - 1] or y_lin in [0, height - 1]:
            data[x] = 255
        else:
            data[x] = abs(data[x]-255)

        if data[x] == 0:
            bag.add(x)
            if first == 0:
                if starter == 0:
                    xmin = xmax = x_lin
                    ymin = ymax = y_lin
                    starter = 1
                else:
                    if x_lin > xmax:
                        xmax = x_lin
                    elif x_lin < xmin:
                        xmin = x_lin
                    if y_lin > ymax:
                        ymax = y_lin
                    elif y_lin < ymin:
                        ymin = y_lin
        else:
            data[x] = 255
    
    
    img.putdata(data)
    #img.show()
    

    maxpoint = 0
    maxcount = 0
    maxr = 0
    #the box of possible centers
    if first == 0:
        maxrad_y= abs(ymax-ymin)/2
        maxrad_x= abs(xmax-xmin)/2
        maxradile = maxrad_x
        if maxrad_y > maxrad_x:
            maxradile = maxrad_y


        xstart = xmin
        xstop = xmax + 1
        ystart = ymin
        ystop = ymax + 1
        radstart = 0
        radstop = maxradile
    
    else:
        xstart = x_big -2
        xstop = x_big + 2
        ystart = y_big - 2
        ystop = y_big + 2
        radstart = maxrad - 8
        radstop = maxrad + 5
    
    for xi in range(xstart, xstop):
        for yi in range(ystart, ystop):
            x = xy2linear(xi, yi, width)
            
            (tempr, tempcount) = rad_test(x, (width, height), (radstart, radstop), bag) # minrd alternative (safer option): int((3.0/4)*(maxrad))
            if tempcount > maxcount:
               
                maxcount = tempcount
                maxpoint = x
                maxr = tempr
                

    xwin, ywin = xy2reverse(maxpoint, width)


    #draw = ImageDraw.Draw(img)
    #draw.ellipse((xwin-maxr, ywin-maxr, xwin + maxr, ywin + maxr), outline = 'grey')
    #img.show()

    #print("the best fitting circle has center {0} and radius {1}, and intersects roughly {2} out of {3} points.  Center is {4}".
    #      format((xwin,ywin), maxr, maxcount, len(bag), maxpoint))
    #print("document size is {0}".format((width, height)))


    return xwin, ywin, maxr, maxcount, len(bag)





def txt2pic(filename, name, harsh, save):
    """
    filename: file.txt
    name: str
    harsh: int
    save: str

    return: None

    txt2pic takes the filename of a matrix text file, opens it, changes it into a picture
    and if save = 'yes', saves the picture as "name.bmp".  Because the matrices of data
    have only numbers between 500 and up to 30,000, the harsh is the number that, for
    numbers below the harsh value, are not included in the image.
    """
    file_in = file(filename, 'r')
    text = file_in.readlines()
    file_in.close()
    cup = []
    cupp = []
    m = 0
    new_cup = []
    edata_new =[]

    for line in text:
        jar = line.split()
        jarr = map(int, jar)
        for x in range(len(jarr)):
            if jarr[x] > harsh:
                cup.append(255)
            else:
                cup.append(0)


    img = Image.new('L', (1024, 1024))
    img.putdata(cup)
    img.show()
    if save == 'yes':
        img.save(name + ".bmp")
    
    
    return


def cropper(filename, name):
    """
    filename: file
    name: str

    return: None

    cropper takes the Image file named `filename`, and crops it down to a square
    image that includes all the non-background points in an image produced by txt2pic.
    It also converts the image to greyscale.  Then it saves the image under the name
    ``name.bmp``
    """

    
    img = Image.open(filename)
    data = list(img.getdata())
    width, height = img.size
    bag = set()
    starter = 0
    for x in range(len(data)):
        x_lin, y_lin = xy2reverse(x, width)
        if x_lin in [0, width - 1] or y_lin in [0, height - 1]:
            data[x] = 255
        else:
            data[x] = abs(data[x]-255)
            if data[x] != 0:
                data[x] = 255

        if data[x] == 0:
            bag.add(x)
            if starter == 0:
                xmin = xmax = x_lin
                ymin = ymax = y_lin
                starter = 1
            else:
                if x_lin > xmax:
                    xmax = x_lin
                elif x_lin < xmin:
                    xmin = x_lin
                if y_lin > ymax:
                    ymax = y_lin
                elif y_lin < ymin:
                    ymin = y_lin
        else:
            data[x] = 255

    
    xlen = abs(xmin - xmax)
    ylen = abs(ymin - ymax)
    if ylen >xlen: #this assumes lots of free space, which is true if using the data from the plasma pictures
        xmin =xmin - (ylen -xlen)/2
        xmax = xmax + (ylen -xlen)/2
        if xmin < 0:
            xmax += -xmin
            xmin = 0
    else:
        ymin = ymin - (xlen - ylen)/2
        ymax = ymin + (xlen - ylen)/2
        if ymin < 0:
            ymax += -ymin
            ymin = 0
    img.putdata(data)
    rad = img.crop((xmin, ymin, xmax, ymax))
    rad.save(name + ".bmp")
    rad.show()
    return
    
