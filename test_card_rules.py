import unittest
import card_rules


class TestCards(unittest.TestCase):
    def setUp(self):
        self.seven_of_diamonds = card_rules.Card(7, card_rules.diamonds)
        self.two_of_clubs = card_rules.Card(2, card_rules.clubs)
        self.two_of_spades = card_rules.Card(2, card_rules.spades)
        self.queen_of_clubs = card_rules.Card(12, card_rules.clubs)
        self.queen_of_hearts = card_rules.Card(12, card_rules.hearts)
        self.seven_tuple = card_rules.CardTuple((self.seven_of_diamonds, ))
        self.two_tuple = card_rules.CardTuple((self.two_of_clubs, self.two_of_spades))
        self.queen_tuple = card_rules.CardTuple((self.queen_of_clubs, self.queen_of_hearts))
        self.bad_tuple = card_rules.CardTuple((self.seven_of_diamonds, self.two_of_spades))
        self.empty_tuple = card_rules.CardTuple.create_empty()

    def test_comparison(self):
        self.assertLess(self.seven_of_diamonds, self.queen_of_clubs)
        self.assertLess(self.queen_of_clubs, self.two_of_spades)
        self.assertEqual(self.two_of_spades,  self.two_of_clubs)
        self.assertLess(self.queen_tuple, self.two_tuple)
        self.assertLess(self.empty_tuple, self.queen_tuple)

    def test_tuples(self):
        self.assertEqual(self.seven_tuple.first_card, self.seven_of_diamonds)
        self.assertEqual(self.two_tuple.card_count, 2)
        self.assertEqual(self.empty_tuple.card_count, 0)
        self.assertTrue(self.two_tuple.of_same_number)
        self.assertFalse(self.bad_tuple.of_same_number)
        self.assertFalse(self.two_tuple.is_empty)
        self.assertTrue(self.empty_tuple.is_empty)


class DummyPresidentAgent(card_rules.PresidentAgent):
    def set_next_action(self, next_action: card_rules.PresidentAction):
        self.next_action = next_action

    def get_next_action(self) -> card_rules.PresidentAction:
        return self.next_action

    def handle_illegal_action(self):
        raise ValueError("That was an illegal move")

    def handle_reward(self, reward_value):
        self.reward_value = 0


class TestGame(unittest.TestCase):
    def setUp(self):
        self.dummy_agent_1 = card_rules.PresidentAgent("steve")
        self.dummy_agent_2 = card_rules.PresidentAgent("geoff")
        self.dummy_game = card_rules.PresidentGame([self.dummy_agent_1, self.dummy_agent_2])
        self.deck = card_rules.create_deck()
        self.dummy_game.deal_hands(self.deck)

    def test_deck(self):
        self.assertEqual(len(self.deck), 52)
        for hand in self.dummy_game.hand_list:
            self.assertEqual(len(hand), 52//2)

    def test_action(self):
        pass


if __name__ == '__main__':
    unittest.main()
