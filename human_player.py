from card_rules import *


class HumanPresidentPlayer(PresidentPlayer):
    def get_next_play(self, game):
        print(f"Player {self.name}'s turn")
        print("Your hand is:")
        self.print_hand()
        print()
        input(">")


eight_of_diamonds = Card(8, diamonds)
nine_of_hearts = Card(9, hearts)

print(eight_of_diamonds)
print(nine_of_hearts)
print(eight_of_diamonds < nine_of_hearts)

player_a = HumanPresidentPlayer(name="A")
player_b = HumanPresidentPlayer(name="B")
player_c = HumanPresidentPlayer(name="C")

my_game = PresidentGame([player_a, player_b, player_c])

my_game.start_game()