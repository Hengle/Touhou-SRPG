from objects import *

TILE_BASE, TILE_HEIGHT, TILE_OFFSET = 41, 22, 12

class Level:
    def __init__( self, width, height ):
        self.w, self.h = width, height
        self.map = []
        for y in xrange(height):
            temp = []
            for x in xrange(width):
                temp += [None]
            self.map += [temp]
        self.print_map()
        self.ground_tile = Tile(0.0,0.0,1.0,TILE_BASE, TILE_HEIGHT, TILE_OFFSET,"grass.png", 2.0)
            
    def print_map( self ):
        for r in reversed(self.map):
            print r
            
    def insert( self, coords, item ):
        if 0 <= coords[0] < self.w and 0 <= coords[1] < self.h:
            self.map[coords[1]][coords[0]] = item

    def remove (self, coords ):
        self.map[coords[1]][coords[0]] = None
            
    def move( self, before, after ):
        self.map[after[0]][after[1]] = self.map[before[0]][before[1]]
        self.map[before[0]][before[1]] = None
        
