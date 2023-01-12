#!/usr/bin/python
#-----------------------------------------------
#test_cube.py - simple ascii art rotating cube
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
import curses
from curses import ascii
import time
import traceback

import math
import numpy

import ascvg


class Engine3D(object):
    def __init__(self, vertices, lines):
        self.vertices = [numpy.array(v) for v in vertices]
        self.lines = lines
        self.x_angle = math.pi/6
        self.y_angle = 0
        self.z_angle = math.pi/4
    def get_lines(self, bottom_left, top_right):
        c = math.cos(self.x_angle)
        s = math.sin(self.x_angle)
        x_rot_matrix = numpy.array([[1, 0, 0],
                                    [0, c, -s],
                                    [0, s, c]])
        
        c = math.cos(self.y_angle)
        s = math.sin(self.y_angle)
        y_rot_matrix = numpy.array([[c, 0, s],
                                    [0, 1, 0],
                                    [-s, 0, c]])
        
        c = math.cos(self.z_angle)
        s = math.sin(self.z_angle)
        z_rot_matrix = numpy.array([[c, -s, 0],
                                    [s, c, 0],
                                    [0, 0, 1]])

        rot_matrix = numpy.dot(numpy.dot(x_rot_matrix, y_rot_matrix),z_rot_matrix)
        
        vertices = [numpy.dot(rot_matrix, v) for v in self.vertices]
        
        a = numpy.array(bottom_left)
        b = numpy.array(top_right)
        
        vertices = [v[:2] for v in vertices]
        
        vertices = [(idx,(v-a)/(b-a)) for idx, v in enumerate(vertices)]
        vertices = dict(vertices)
        result = []
        for a,b in self.lines:
            if a in vertices and b in vertices:
                result.append((vertices[a],vertices[b]))
        
        return result

def main_interactive():
    
    surface = ascvg.Surface(20,20)
    
    cube_vertices = [(-1,-1,-1), (1,-1,-1), (1,1,-1), (-1,1,-1),
                     (-1,-1,1), (1,-1,1), (1,1,1), (-1,1,1)]
    cube_lines = [(0,1),(1,2),(2,3),(3,0),
                  (4,5),(5,6),(6,7),(7,4),
                  (0,4),(1,5),(2,6),(3,7)]
    engine = Engine3D(cube_vertices, cube_lines)
    
    try:
        scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        scr.keypad(True)
        scr.nodelay(True)
        prev_c = '0'
        while True:
            start = time.time()
            c = scr.getch()
            if c == ord('q'):
                return
            change = {curses.KEY_LEFT: (0.1, 0),
                      curses.KEY_RIGHT: (-0.1, 0),
                      curses.KEY_UP: (0, 0.1),
                      curses.KEY_DOWN: (0, -0.1),
                     }.get(c, (0,0))
            engine.z_angle = (engine.z_angle + change[0]) % (2*math.pi)
            engine.x_angle = (engine.x_angle + change[1]) % (2*math.pi)
            
            cube_lines = engine.get_lines((-1.5,-1.5),(1.5, 1.5))
            
            scr.clear()
            surface.clear()
            try:
                for a,b in cube_lines:
                    surface.draw_line(a,b)
                surface.blit_to_curses_window(scr, 0, 0)
                
            except:
                exc_str = traceback.format_exc()
                for idx,l in enumerate(exc_str.split('\n')):
                    scr.addstr(5+idx,24,l)
            scr.refresh()
            delta = time.time()-start
            if delta < 0.033:
                time.sleep(0.033-delta)
    finally:
        curses.endwin()

if __name__ == '__main__':
    main_interactive()
