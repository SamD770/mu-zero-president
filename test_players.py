import unittest

from card_rules import *
from simple_greedy_player import *
from human_player import *


class SimpleAgentTest(unittest.TestCase):
    def test_group_numbered(self):
        deck = create_deck()
        random.shuffle(deck)
        grouped = group_numbered_cards(deck)
        self.assertEqual(len(grouped), 13)
        for group in grouped:
            self.assertEqual(len(group), 4)

    def test_game(self):
        human_player = HumanPresidentAgent(name="Human")
        player_b = SimplePresidentAgent(name="B")
        player_c = SimplePresidentAgent(name="C")
        player_d = SimplePresidentAgent(name="D")

        my_game = PresidentGame([human_player, player_b, player_c, player_d])

        my_game.start_game()


if __name__ == '__main__':
    unittest.main()
