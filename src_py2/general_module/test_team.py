import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from game.team import Team, Roles
from game.player import Player

class TestTeam(unittest.TestCase):

    def setUp(self):
        self.p1 = Player("Mario")
        self.p2 = Player("Luigi")
        self.team = Team("Bros", [self.p1, self.p2])

    def test_initial_roles(self):
        self.assertEqual(self.team.get_hinter().get_name(), "Mario")
        self.assertEqual(self.team.get_guesser().get_name(), "Luigi")

        self.assertEqual(self.team.get_player_by_name("Mario").get_role(), Roles.HINTER)
        self.assertEqual(self.team.get_player_by_name("Luigi").get_role(), Roles.GUESSER)

        self.assertEqual(self.team.players[0].get_role(), Roles.HINTER)
        self.assertEqual(self.team.players[1].get_role(), Roles.GUESSER)


    def test_rotate_role(self):
        self.team.rotate_role()
        self.assertEqual(self.team.get_hinter().get_name(), "Luigi")
        self.assertEqual(self.team.get_guesser().get_name(), "Mario")
        self.assertEqual(self.team.get_player_by_name("Mario").get_role(), Roles.GUESSER)
        self.assertEqual(self.team.get_player_by_name("Luigi").get_role(), Roles.HINTER)
        
        self.team.rotate_role()
        self.assertEqual(self.team.get_hinter().get_name(), "Mario")
        self.assertEqual(self.team.get_guesser().get_name(), "Luigi")
        self.assertEqual(self.team.get_player_by_name("Mario").get_role(), Roles.HINTER)
        self.assertEqual(self.team.get_player_by_name("Luigi").get_role(), Roles.GUESSER)


if __name__ == '__main__':
    unittest.main()