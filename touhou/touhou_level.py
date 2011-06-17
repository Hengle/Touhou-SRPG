'''
* This file is part of Touhou SRPG.
* Copyright (c) Hans Lo
*
* Touhou SRPG is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* Touhou SRPG is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with Touhou SRPG.  If not, see <http://www.gnu.org/licenses/>.
'''

import pygame

from core.graphics.graphic import Graphic, GraphicPositioned, GraphicList
from core.graphics.animated import Animated
from core.graphics.common import Repeated

from touhou_graphic import MapGraphic

ALIVE, DEAD = range(2)

#Touhou Level State, includes information about the map, characters, monsters, etc.
#Theoretically can be for load games, saved games, and level editors
class TouhouLevel:
    def __init__(self):
        self.creatures = {}
        self.menus = {}
        self.map = None

    def new_map(self, size):
        self.map = TouhouMap(size)

    # things objects do before turn begins.
    def begin_turn(self):
        for obj in self.map.obj_list:
            x, y = self.map.obj_list[obj]
            self.map.grid[x][y].end_turn()

    # things objects do after turn is ended.
    def end_turn(self):
        for obj in self.map.obj_list:
            x, y = self.map.obj_list[obj]
            self.map.grid[x][y].end_turn()

    def add_creature(self, name, stat):
        self.creatures[name] = stat

# Base class to hold character/monster/other attributes.
class TouhouCreature:
    def __init__(self, name):
        self.name = name
        self.status = ALIVE
        self.max_hp = None
        self.max_ap = None
        self.hp = None
        self.ap = None
        self.speed = None
        self.portrait = None

    def set_portrait(self, filename):
        self.portrait = Graphic(filename)

    def set_speed(self, value):
        self.speed = value

    def set_max_hp(self, value):
        self.max_hp = value

    def set_max_ap(self, value):
        self.max_ap = value

    def restore_hp(self, value=None):
        if value == None:
            self.hp = self.max_hp
        else:
            self.hp += value
            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def restore_ap(self, value=None):
        if value == None:
            self.ap = self.max_ap
        else:
            self.ap += value
            if self.ap > self.max_ap:
                self.ap = self.max_ap

# obj_list: quick way to get the position of an object.
# grid: grid full of references of to MapGraphic objects.
class TouhouMap:
    TILE_OFFSET = (45.0,30.0)
    TILE_DIMENSIONS = (90.0,60.0)
    TILE_DATA = (TILE_OFFSET, TILE_DIMENSIONS)
    def __init__(self, size):
        self.obj_list = {}
        self.grid = []

        # test code starts here
        
        self.setup_map(size) 
        
        # test code ends here
        self.ground = None
        
        self.load_graphics()
        
    def load_graphics(self):
        self.ground_tile = Graphic(texture="./content/gfx/sprites/grass.png")
        self.setup_ground()
        for obj in self.obj_list:
            pos = self.obj_list[obj]
            animation = Animated("./content/gfx/sprites/" + obj + ".png", "./content/metadata/" + obj + ".spr")
            self.place_object(animation, pos, obj)

    def set_ground_tile(self, tile):
        self.ground_tile = tile
        self.setup_ground()

    def setup_ground(self):
        self.ground = Repeated((self.w, self.h),self.TILE_OFFSET, self.ground_tile)
        self.ground = GraphicPositioned(self.ground, (0,0))
        self.ground.make_visible()

    def setup_map(self, size):
        self.w, self.h = size
        for y in xrange(self.h):
            temp = []
            for x in xrange(self.w):
                temp += [None]
            self.grid += [temp]

    def update_objects(self,e):
        for obj in self.obj_list:
            x,y = self.obj_list[obj]
            self.grid[x][y].update(e)

    def frame_update(self, e):
        for obj in self.obj_list:
            x,y = self.obj_list[obj]
            self.grid[x][y].frame_update(e)
          
    def draw_ground(self):
        temp = GraphicList()
        temp.add(self.ground)
        return temp

    def draw_sprites(self):
        temp = GraphicList()
        for x in xrange(self.w):
            for y in xrange(self.h):
                if self.grid[self.w-x-1][self.h-y-1]:
                    temp.add(self.grid[self.w-x-1][self.h-y-1])
        return temp
    

    def place_object(self, obj, pos, name, details=None):
        temp = MapGraphic(obj,pos,name,details)
        self.grid[pos[0]][pos[1]] = temp
        self.obj_list[name] = pos
        
    def remove_object(self, tup):
        self.grid[tup[0]][tup[1]] = None

    def update_obj_pos(self, obj):
        x,y = obj.pos
        old_x,old_y=self.obj_list[obj.name]
        self.grid[x][y] = self.grid[old_x][old_y]
        self.grid[old_x][old_y] = None
        self.obj_list[obj.name] = (x,y)

    # given the map and character information, generate which tiles can be reached.
    def generate_accessible(self, character, speed):
        """generate list of coordinates that the character is able to move to"""
        w, h = self.w, self.h
        pos = self.obj_list[character]
        
        accessible = set()
        accessible.add(pos)
        for i in xrange(speed):
            temp = set()
            for c in accessible:
                temp.add((c[0],c[1]-1))
                temp.add((c[0],c[1]+1))
                temp.add((c[0]-1,c[1]))
                temp.add((c[0]+1,c[1]))
            accessible = accessible.union(temp)
            temp = set()
            for t in accessible:
                if not (0 <= t[0] < w and 0 <= t[1] < h):
                    temp.add(t)
                elif self.grid[t[0]][t[1]]:
                    temp.add(t)
                accessible = accessible.difference(temp)
        return accessible
