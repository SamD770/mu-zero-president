from card_rules import *
# from human_player import card_sequence_to_string


def group_numbered_cards(card_list: list[Card]) -> list[list[Card]]:
    """Returns a list of lists of cards grouped_cards, grouped_cards[0] contains all threes
    in card_list, grouped_cards[1] contains all fours in card_list and so on."""
    grouped_cards = [[] for _ in range(13)]
    for card in card_list:
        grouped_cards[card.priority - 3].append(card)
    return grouped_cards


class SimplePresidentAgent(PresidentAgent):
    def get_next_action(self) -> PresidentAction:
        """Just plays the lowest cards that it can."""
        top_of_card_stack = self.observation_buffer.top_of_card_stack
        hand = self.observation_buffer.player_hand
        target_length = top_of_card_stack.card_count
        # For each non-empty group of equal-numbered cards in hand, if a legal play can be made, make it.
        for group in group_numbered_cards(hand):
            if group:
                if len(group) >= target_length:
                    if top_of_card_stack.is_empty:
                        potential_play = CardTuple.from_iterable(group)
                    else:
                        potential_play = CardTuple.from_iterable(group[:target_length])
                    if potential_play > top_of_card_stack or potential_play == top_of_card_stack:
                        break
        else:
            # if no legal play was found, use an empty play to pass
            potential_play = CardTuple.create_empty()
        # print("hand:", card_sequence_to_string(hand))
        # print("play:", card_sequence_to_string(potential_play))
        # print("stack:", card_sequence_to_string(top_of_card_stack))
        return PresidentAction(self, potential_play)

    def handle_illegal_action(self):
        raise ValueError("SimplePresidentAgent error with action played")

    def handle_reward(self, reward_value):
        pass