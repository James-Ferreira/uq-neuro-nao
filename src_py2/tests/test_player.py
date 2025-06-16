import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from game.player import Player, Roles, Variant

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Mario", Variant.AUTO)


if __name__ == '__main__':
    unittest.main()