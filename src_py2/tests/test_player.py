import unittest
from game.player import Player, Roles, Variant

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Mario", Variant.AUTO)


if __name__ == '__main__':
    unittest.main()