import random
from itertools import cycle, islice, filterfalse

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

    @property
    def priority(self):
        """2 is the highest number, then ace, then king, queen and so on."""
        if self.number <= 2:
            # Add 13 to 'shift' 2 and ace above the king
            return self.number + 13
        else:
            return self.number

    def __str__(self):
        return Card.number_to_name(self.number) + " of " +self.suit.name

    def __comp__(self, other):
        own_priority = self.priority
        other_priority = other.priority
        return own_priority.__comp__(other_priority)


class PresidentPlay:
    """Wrapper around a tuple of cards of the same number"""
    def __init__(self, cards):
        self.cards = cards
        self.card_count = len(cards)
        self.first_card = self.cards[0]

    def __comp__(self, other):
        return self.first_card.__comp__(other.first_card)

    def check_legal(self):
        for card in self.cards:
            if card != self.first_card:
                return False
        return True


class PresidentPlayer:
    def __init__(self, hand=None):
        if hand is None:
            self.hand = []
        else:
            self.hand = hand

    def print_hand(self):
        for card in self.hand:
            print(card)

    def remove_play(self, play):
        pass

    def get_next_play(self):
        raise NotImplementedError("Implement this method")


class IllegalPlayException(Exception):
    pass


def create_deck():
    deck = []
    for i in range(1, 14):
        for suit in suits:
            deck.append(Card(i, suit))
    return deck


class PresidentGame:
    def __init__(self, player_list):
        self.player_list = player_list
        self.winning_order = []
        self.card_stack = []
        self.player_count = len(player_list)

    def player_iterator(self):
        pass

    def deal_hands(self, deck):
        for player in self.player_list:
            player.hand = []
        for card, player in zip(deck, cycle(self.player_list)):
            player.hand.append(card)

    def get_player_iterable(self, starting_player_index, reverse=False):

        if reverse:
            loop_over = reversed(self.player_list)
            starting_index = (self.player_count - 1) - starting_player_index
        else:
            loop_over = self.player_list
            starting_index = starting_player_index

        # make an iterable cycle which starts at the starting player
        player_cycle = islice(
            cycle(loop_over),
            starting_index, None
        )

        # filter out the players with empty hands
        player_iterable = filter(
            lambda player: player.hand,
            player_cycle
        )

        return player_iterable

    def play_hand(self, starting_player_index):

        player_iterable = self.get_player_iterable(starting_player_index)

        last_player_to_play = None
        current_play = None

        for current_player in player_iterable:
            next_play = current_player.get_next_play(self)
            # if the player skips, do nothing
            if next_play is None:
                continue

            # if there are cards on the table, skip the player if the plays are equal and check the play is legal
            if current_play is not None:
                if next_play == current_play:
                    skipped_player = player_iterable.__next__()
                elif next_play < current_play:
                    raise IllegalPlayException("A player tried to play lower than the current play")

            # remove the play from the player's hand and put them on the winning list if they have no more players
            current_player.remove_play(next_play)
            if not current_player.hand:
                self.winning_order.append(current_player)

            # if everyone else skipped, break
            if current_player is last_player_to_play:
                hand_winner_index = self.player_list.index_of(current_player)
                break

            # record that this player played and put their play at the top of the pile
            last_player_to_play = current_player
            current_play = next_play

        return hand_winner_index

    def start_game(self):
        deck = create_deck()
        cards_to_remove = 52 % self.player_count
        deck = deck[:cards_to_remove]
        random.shuffle(deck)

        self.deal_hands(deck)
        current_player_index = 0
        while len(self.winning_order) != self.player_count:
            hand_winner_index = self.play_hand(current_player_index)