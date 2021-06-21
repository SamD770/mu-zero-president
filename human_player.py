from card_rules import *

number_name_dict = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K"
}


def number_to_name(number):
    if 2 <= number <= 10:
        return str(number)
    else:
        return number_name_dict[number]


name_number_dict = {
    number_to_name(i): i for i in range(1, 14)
}

name_suit_dict = {
    suit.name[:1]: suit for suit in suits
}


def card_to_string(card: Card):
    return number_to_name(card.number) + "o" + card.suit.name[:1]


def string_to_card(card_string: str):
    if card_string[:2] == "10":
        name_char = "10"
        suit_char = card_string[-1:]
    else:
        name_char, o, suit_char = card_string
    return Card(name_number_dict[name_char], name_suit_dict[suit_char])


def card_sequence_to_string(cards):
    return "".join(card_to_string(card) + " " for card in cards)


def string_to_card_tuple(card_strings):
    splitted = card_strings.split(" ")
    return CardTuple(tuple(string_to_card(card_string) for card_string in splitted))


class HumanPresidentAgent(PresidentAgent):
    def observe_action(self, new_action: PresidentAction):
        if new_action.is_pass:
            print(f"{new_action.agent.name} passed")
        else:
            cards_string = card_sequence_to_string(new_action.cards)
            print(f"{new_action.agent.name} played {cards_string}")

    def get_next_action(self) -> PresidentAction:
        counter = len(self.observation_buffer.action_list)
        for action in reversed(self.observation_buffer.action_list):
            if action.agent is self:
                break
            else:
                counter -= 1
        for action in self.observation_buffer.action_list[counter:]:
            self.observe_action(action)
        print(f"Player {self.name}'s turn")
        print("Your hand is:")
        hand_string = card_sequence_to_string(self.observation_buffer.player_hand)
        print(hand_string)
        while True:
            new_action_string = input(">")
            try:
                new_action = self.get_action_from_string(new_action_string)
            except Exception:
                pass
            else:
                break
        return new_action

    def handle_illegal_action(self):
        print("That action is illegal")

    def handle_reward(self, reward_value):
        print(f"You got a reward of {reward_value}")

    def get_action_from_string(self, new_action_string: str) -> PresidentAction:
        if new_action_string == "pass":
            cards = CardTuple.create_empty()
        else:
            cards = string_to_card_tuple(new_action_string)
        return PresidentAction(self, cards)


player_a = HumanPresidentAgent(name="A")
player_b = HumanPresidentAgent(name="B")
player_c = HumanPresidentAgent(name="C")
player_d = HumanPresidentAgent(name="D")

my_game = PresidentGame([player_a, player_b, player_c, player_d])

my_game.start_game()