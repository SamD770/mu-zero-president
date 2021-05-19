import random
from itertools import cycle

number_name_dict = {
    1: "Ace",
    11: "Jack",
    12: "Queen",
    13: "King"
}


class Suit:
    def __init__(self, name):
        self.name = name


hearts = Suit("Hearts")
clubs = Suit("Clubs")
diamonds = Suit("Diamonds")
spades = Suit("Spades")

suits = (hearts, clubs, diamonds, spades)


class Card:
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    @staticmethod
    def number_to_name(number):
        if 2 <= number <= 10:
            return str(number)
        else:
            return number_name_dict[number]

    def __str__(self):
        return Card.number_to_name(self.number) + " of " +self.suit.name


class PresidentPlayer:
    def __init__(self, hand=None):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand

    def print_hand(self):
        for card in self.hand:
            print(card)

    def get_next_play(self):
        pass


def create_deck():
    deck = []
    for i in range(1, 14):
        for suit in suits:
            deck.append(Card(i, suit))
    return deck


def deal_hands(player_list, deck):
    for player in player_list:
        player.hand = []
    for card, player in zip(deck, cycle(player_list)):
        player.hand.append(card)


def start_game(player_list):
    player_count = len(player_list)
    deck = create_deck()
    cards_to_remove = 52 % player_count

    deck = deck[:cards_to_remove]
    random.shuffle(deck)

    deal_hands(player_list, deck)
    for player in cycle(player_list):
        next_play = player.get_next_play()