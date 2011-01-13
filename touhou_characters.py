from touhou_objects import *
from ui import *
import glFreeType
import pygame
import touhou_events

class Reimu(PlayerCharacter):
    SPEED = 4
    MAX_AP = 100
    def __init__(self, position, touhou_map, touhou):
        PlayerCharacter.__init__(self, 15, 15, "reimu", position, touhou_map, touhou)
        self.menu = ReimuMenu(self)
        
        self.ap = self.MAX_AP
        
        self.attackable = [(0,1),(0,-1),(1,0),(-1,0)]

        self.move_cost = 30

    def menu_on(self):
        """Turn the menu on """
        self.menu.menu_on()

    def menu_off(self):
        """Turn the menu off"""
        self.menu.menu_off()

    def hovering_menu(self, mouse_coords):
        print self.menu.within_menu(*mouse_coords)
        return self.menu.within_menu(*mouse_coords)
        
    def restore_ap(self):
        self.ap = self.MAX_AP

class ReimuMenu(Menu):
    def __init__(self, reimu, font = None):
        Menu.__init__(self, "Reimu")
        self.add_entry(MenuEntry("Move", 0, self.move_function, "menu_option.png","menu_option_hover.png", "menu_option_clicked.png"))
        self.add_entry(MenuEntry("Attack", 1, self.attack_function, "menu_option.png","menu_option_hover.png", "menu_option_clicked.png"))
        self.reimu = reimu
        
    def draw(self):
        Menu.draw(self)

    def move_function(self):
        if self.reimu.ap > self.reimu.move_cost:
            pygame.event.post(pygame.event.Event(touhou_events.CLICKEVENT, button = touhou_events.MOVE, character=self.reimu))
            self.menu_off()

    def attack_function(self):
        pygame.event.post(pygame.event.Event(touhou_events.CLICKEVENT, button = touhou_events.ATTACK, character = self.reimu))
        self.menu_off()
