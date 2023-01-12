#!/usr/bin/python
#-----------------------------------------------
#ascvg.py - ascii graphics
#Copyright (c) 2007, Imri Goldberg
#All rights reserved.
#
#Redistribution and use in source and binary forms,
#with or without modification, are permitted provided
#that the following conditions are met:
#
#    * Redistributions of source code must retain the
#        above copyright notice, this list of conditions
#        and the following disclaimer.
#    * Redistributions in binary form must reproduce the
#        above copyright notice, this list of conditions
#        and the following disclaimer in the documentation
#        and/or other materials provided with the distribution.
#    * Neither the name of the algorithm.co.il nor the names of
#        its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
#LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-----------------------------------------------

import numpy
import math



SMALL = 0.000000001


USE_EXTRA_SYMBOL=False

def round(x):
    return int(math.floor(x+0.5))

def sign(x):
    if x<0:
        return -1
    if x>0:
        return 1
    return 0

def clip_line(line_pt_1, line_pt_2, min_xy, max_xy):
    """Clip line to the rect specified
    Parameters:
        line_pt_1 - a tuple (x,y) for the first point of the line
        line_pt_2 - a tuple (x,y) for the second point of the line
        rect_bottom_left - a tuple (x,y) for the bottom left of the 
                           clipping rect
        rect_top_right - a tuple (x,y) for the top right of the 
                           clipping rect
    Return value:
        None if the line is completely outside the rect
        otherwise ((x0,y0),(x1,y1)) - two points that represent the 
                                      clipped line
    """
    ##How (and why) the code works:
    ##We use the representation x(t) = a + t*(b-a) (0<=t<=1) for lines
    ##We first check for special cases (vertical or horizontal line,
    ##    line completely inside rect).
    ##Then, we computes the four intersections of the line with 
    ##    edges of the rect. Note that these intersections may be 
    ##    anywhere on the infinite-lines, even outside the specific segments.
    ##    (that means, t<0 or t>1).
    ##It is guaranteed that for any convex polygon, when the list of t values
    ##    (including the end points of the original line, 0 and 1) are sorted, 
    ##    the two middle points will lie inside the polygon.
    ##Using this result, the list of t_values is sorted. Since the list is of length
    ##    six (four intersections, two original points), the required values are
    ##    t_list[2],t_list[3]. Given these two values, it is easy to compute
    ##    the actual points using the line representation given above.
    
    
    
    #line delta-x is zero
    if abs(line_pt_1[0] - line_pt_2[0]) < SMALL:
        new_start, new_end =  ((line_pt_1[0], max(min(line_pt_1[1], line_pt_2[1]), min_xy[1])),
                               (line_pt_1[0], min(max(line_pt_1[1], line_pt_2[1]), max_xy[1])))
        if (new_start[0] < min_xy[0]) or (new_start[0] >= max_xy[0]):
            return None
        if (new_start[1] >= max_xy[1]) or (new_end[1] < min_xy[1]):
            return None
        return new_start, new_end

    #line delta-y is zero
    if abs(line_pt_1[1] - line_pt_2[1]) < SMALL:
        if (line_pt_1[1] < min_xy[1]) or (line_pt_1[1] >= max_xy[1]):
            return None
        new_start, new_end = ((max(min(line_pt_1[0], line_pt_2[0]), min_xy[0]), line_pt_1[1]),
                              (min(max(line_pt_1[0], line_pt_2[0]), max_xy[0]), line_pt_1[1]))
        if (new_start[1] < min_xy[1]) or (new_start[1] >= max_xy[1]):
            return None
        if (new_start[0] >= max_xy[0]) or (new_end[0] < min_xy[0]):
            return None
        return new_start, new_end

    #check if completely inside the rect
    if ((min_xy[0] <= line_pt_1[0] and line_pt_1[0] <= max_xy[0]) and
        (min_xy[1] <= line_pt_1[1] and line_pt_1[1] <= max_xy[1]) and
        (min_xy[0] <= line_pt_2[0] and line_pt_2[0] <= max_xy[0]) and
        (min_xy[1] <= line_pt_2[1] and line_pt_2[1] <= max_xy[1])):
        return line_pt_1, line_pt_2

    #the endpoints of the line
    t_list = [0.0,1.0]

    #compute the 4 intersections
    t1 = float(min_xy[0]-line_pt_1[0])/(line_pt_2[0]-line_pt_1[0])
    t2 = float(max_xy[0]-line_pt_1[0])/(line_pt_2[0]-line_pt_1[0])
    t3 = float(min_xy[1]-line_pt_1[1])/(line_pt_2[1]-line_pt_1[1])
    t4 = float(max_xy[1]-line_pt_1[1])/(line_pt_2[1]-line_pt_1[1])
    int_t_list = [t1,t2,t3,t4]
    t_list += int_t_list
    #check if all four intersections are outside
    p1 = line_pt_1[1] + t1*(line_pt_2[1]-line_pt_1[1])
    p2 = line_pt_1[1] + t2*(line_pt_2[1]-line_pt_1[1])
    p3 = line_pt_1[0] + t3*(line_pt_2[0]-line_pt_1[0])
    p4 = line_pt_1[0] + t4*(line_pt_2[0]-line_pt_1[0])
    
    r1 = min_xy[1]<=p1<=max_xy[1]
    r2 = min_xy[1]<=p2<=max_xy[1]
    r3 = min_xy[0]<=p3<=max_xy[0]
    r4 = min_xy[0]<=p4<=max_xy[0]
    if all(not x for x in [r1,r2,r3,r4]):
        return None
    
    #find the two innermost points
    t_list.sort()
    if t_list[2] < 0 or t_list[2] >= 1 or t_list[3] < 0 or t_list[2]>= 1:
        return None
    result = [(pt_1 + t*(pt_2-pt_1)) for t in (t_list[2],t_list[3]) for (pt_1, pt_2) in zip(line_pt_1, line_pt_2)]
    return (result[0],result[1]), (result[2], result[3])

def get_draw_symbol(start, end):
    delta = end-start
    x,y = delta
    cos_alpha = x/((x**2+y**2)**0.5)
    alpha = math.acos(cos_alpha)
    if 0 <= alpha < math.pi/6:
        if y>0:
            return '-','/'
        else:
            return '-','\\'
    if 5*math.pi/6 <= alpha < math.pi:
        if y<0:
            return '-','/'
        else:
            return '-','\\'
    if math.pi/3 <= alpha < 2*math.pi/3:
        if x*y>0:
            return '|','/'
        else:
            return '|','\\'
    if delta[0]*delta[1] > 0:
        if (x>0 and x>y) or (x<0 and x<y):
            return '\\','|'
        else:
            return '\\','-'
    
    if (x>0 and x>-y) or (x<0 and -x<y):
        return '/','|'
    else:
        return '/','-'

class Surface(object):
    def __init__(self, x_size, y_size, bg_init=' '):
        self.x_size = x_size
        self.y_size = y_size
        self.fill(bg_init)
        
        self.size = numpy.array([x_size, y_size])
    
    def _to_buf_coord(self, point):
        result = point*(self.size-(1,1))
        result = numpy.array(map(round,result))
        return result
    
    def _to_float_buf_coord(self, point):
        result = point*(self.size-(1,1))
        return result
    
    def set_at(self, x, y, value):
        self.buffer[y][x] = value
    
    def get_at(self, x, y):
        return self.buffer[y][x]
    
    def render(self):
        return "\n".join("".join(line) for line in self.buffer)
    
    def blit_to_curses_window(self, curses_window, x, y):
        lines = ["".join(line) for line in self.buffer]
        for idx, line in enumerate(lines):
            curses_window.addstr(y+idx, x, line)
    
    
    def blit(self, source, x, y):
        self.buffer[x:,y:] = source.buffer
    
    def fill(self, value=' ', rect = None):
        if rect is None:
            self.buffer = numpy.array([[value]*self.x_size]*self.y_size)
            return
        raise NotImplementedError()
    
    def clear(self):
        self.fill()
    
    def draw_line(self, start, end):
        start = numpy.array(start).astype(float)
        end = numpy.array(end).astype(float)
        
        start_coord = self._to_buf_coord(start)
        end_coord = self._to_buf_coord(end)

        if all(start_coord == end_coord):
            return
        orig_start, orig_end = start, end
        clipped_line = clip_line(start, end, (0.0,0.0), (1.0, 1.0))
        if clipped_line is None:
            return
        start,end = clipped_line
        start = numpy.array(start).astype(float)
        end = numpy.array(end).astype(float)
        
        start_coord = self._to_buf_coord(start)
        end_coord = self._to_buf_coord(end)

        x0,y0 = start_coord
        x1,y1 = end_coord
        if all(start_coord == end_coord):
            #TODO: Should draw?
            return

        draw_symbol, extra_draw_symbol = get_draw_symbol(start, end)
        try:

            delta = end-start
            delta_coord = self._to_float_buf_coord(delta)
            if abs(delta_coord[0])>abs(delta_coord[1]):
                s = sign(delta_coord[0])
                slope = float(delta_coord[1])/delta_coord[0]
                for i in range(0,int(abs(delta_coord[0])+1)):
                    cur_draw_symbol = draw_symbol
                    temp = round(slope*i)
                    if (USE_EXTRA_SYMBOL and 
                        round(slope*(i-1)) == temp and 
                        temp == round(slope*(i+1))):
                        cur_draw_symbol = extra_draw_symbol
                    x = i*s
                    cur_y = round(y0+slope*x)
                    try:
                        self.set_at(x0+x,cur_y,cur_draw_symbol)
                    except:
                        raise
            else:
                s = sign(delta_coord[1])
                slope = float(delta_coord[0])/delta_coord[1]
                for i in range(0,int(abs(delta_coord[1])+1)):
                    y = i*s
                    cur_draw_symbol = draw_symbol
                    temp = round(slope*i)
                    if (USE_EXTRA_SYMBOL and 
                        round(slope*(i-1)) == temp and 
                        temp == round(slope*(i+1))):
                        cur_draw_symbol = extra_draw_symbol
                    cur_y = y0+y
                    x = round(x0+slope*y)
                    try:
                        self.set_at(x,cur_y,cur_draw_symbol)
                    except:
                        raise
                
        except:
            print (orig_start, orig_end)
            print (start, end)
            print (start_coord, end_coord)
            raise

        return
    
    def draw_pixel(self, where, value):
        if 0.0<=where[0]<=1.0 and 0.0<=where[1]<=1.0:
            coord = self._to_buf_coord(where)
            self.set_at(coord[0],coord[1],value)
    
    def draw_circle(self, center, radius, filled = False):
        center = numpy.array(center)
        center_coord = self._to_buf_coord(center)
        radius_pixels = max(self._to_buf_coord(radius))
        if self.x_size == self.y_size:
            #handle some special cases
            #for ratio==1
            if radius_pixels == 0:
                #self.set_at(center_coord[0], center_coord[1],'.')
                self.draw_pixel(center,'.')
                return
            if radius_pixels == 1:
                #self.set_at(center_coord[0], center_coord[1],'O')
                self.draw_pixel(center,'O')
                return
            
            step = radius/radius_pixels
            for j in numpy.arange(0,radius/2, step):
                k = math.sqrt(radius**2-j**2)
                self.draw_pixel(center+(j,k),'-')
                self.draw_pixel(center+(k,j),'|')
                self.draw_pixel(center+(-j,k),'-')
                self.draw_pixel(center+(-k,j),'|')
                self.draw_pixel(center+(j,-k),'-')
                self.draw_pixel(center+(k,-j),'|')
                self.draw_pixel(center+(-j,-k),'-')
                self.draw_pixel(center+(-k,-j),'|')
            for j in numpy.arange(radius/2,radius, step):
                if j>radius:
                    k = 0.0
                else:
                    k = math.sqrt(radius**2-j**2)
                self.draw_pixel(center+(j,k),'/')
                self.draw_pixel(center+(k,j),'/')
                self.draw_pixel(center+(-j,k),'\\')
                self.draw_pixel(center+(-k,j),'\\')
                self.draw_pixel(center+(j,-k),'\\')
                self.draw_pixel(center+(k,-j),'\\')
                self.draw_pixel(center+(-j,-k),'/')
                self.draw_pixel(center+(-k,-j),'/')
            return
        raise NotImplementedError()
##        prev_x = radius
##        prev_y = 0.0
##        for i in xrange(0, (radius_pixels+1)):
##            alpha = math.pi*i/(radius_pixels*2)
##            x = radius*math.cos(alpha)
##            y = radius*math.sin(alpha)
##            print x,y
##            #print (center+(prev_x,prev_y),center+(x,y))
##            self.draw_line(center+(prev_x,prev_y),center+(x,y))
##            #print (center+(-prev_y,prev_x),center+(-y,x))
##            self.draw_line(center+(-prev_y,prev_x),center+(-y,x))
##            #print (center+(-prev_x,-prev_y),center+(-x,-y))
##            self.draw_line(center+(-prev_x,-prev_y),center+(-x,-y))
##            #print (center+(prev_y,-prev_x),center+(y,-x))
##            self.draw_line(center+(prev_y,-prev_x),center+(y,-x))
##            prev_x, prev_y = x,y
        
    def draw_rect(self, top_left, bottom_right, filled = False):
        raise NotImplementedError()
