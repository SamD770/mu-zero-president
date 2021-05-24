from card_rules import *


class HumanPresidentAgent(PresidentAgent):

    def observe_action(self, new_action: PresidentAction):
        if new_action.is_pass():
            print(f"{new_action.agent} passed")
        else:
            print(f"{new_action.agent} played {new_action.cards}")

    def get_next_action(self, hand: list[Card]) -> PresidentAction:
        print(f"Player {self.name}'s turn")
        print("Your hand is:")
        print(hand)
        new_action_string = input(">")
        new_action = self.get_action_from_string(new_action_string)
        return new_action

    def handle_illegal_action(self):
        print("that action is illegal")

    @staticmethod
    def get_action_from_string(new_action_string: str) -> PresidentAction:
        return PresidentAction(None, None)


eight_of_diamonds = Card(8, diamonds)
nine_of_hearts = Card(9, hearts)

print(eight_of_diamonds)
print(nine_of_hearts)
print(eight_of_diamonds < nine_of_hearts)

player_a = HumanPresidentAgent(name="A")
player_b = HumanPresidentAgent(name="B")
player_c = HumanPresidentAgent(name="C")

my_game = PresidentGame([player_a, player_b, player_c])

my_game.start_game()