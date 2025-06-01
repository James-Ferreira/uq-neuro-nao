#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from enum import Enum
import random

class Roles(Enum):
    HINTER = 1
    GUESSER = 2
    
class Variant(Enum):
    AUTO = 0
    STDIN = 1

class Player(object):
    def __init__(self, name, variant=Variant.AUTO):
        self.name = name
        self.variant = variant
        self.role = None

    def assign_role(self, role):
        self.role = role

    def get_role(self):
        return self.role
    
    def get_name(self):
        return self.name
    
    def generate_hint(self, target_word, already_hinted):

        if(self.variant == Variant.STDIN):
            return raw_input("▶ Enter {}'s hint: ".format(self.name))
        
        return "hint1"

    def generate_guess(self, target_word, already_hinted):

        if(self.variant == Variant.STDIN):
            guess = raw_input("▶ Enter {}'s guess:".format(self.name))
            return guess
        
        return target_word if random.random() < 0.5 else "guess1"
