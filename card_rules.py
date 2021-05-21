import random
from itertools import cycle, islice

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

    def __lt__(self, other):
        return (self.priority < other.priority)

    def __eq__(self, other):
        return (self.priority == other.priority)


class PresidentPlay:
    """Wrapper around a tuple of cards of the same number"""
    def __init__(self, player, *cards):
        self.player = player
        self.cards = cards
        self.card_count = len(cards)
        self.first_card = self.cards[0]

    def __comp__(self, other):
        return self.first_card.__comp__(other.first_card)

    def __str__(self):
        return str(self.cards)

    def is_legal(self):
        for card in self.cards:
            if card != self.first_card or card not in self.player.hand:
                return False
        return True


class PresidentPlayer:
    def __init__(self, hand=None, name=""):
        if hand is None:
            self._hand = []
        else:
            self.hand = hand
        self.name = name

    def print_hand(self):
        for card in self.hand:
            print(card)

    @property
    def hand(self):
        self._hand.sort()
        return self._hand

    @hand.setter
    def hand(self, value):
        self._hand = value

    def remove_play(self, play):
        pass

    def get_next_play(self, game):
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
    def __init__(self, player_list, starting_player_index=0):
        self.player_list = player_list
        self.winning_order = []
        self.card_stack = []
        self.player_count = len(player_list)
        self.current_player_index = starting_player_index

    def deal_hands(self, deck):
        for player in self.player_list:
            player.hand = []
        for card, player in zip(deck, cycle(self.player_list)):
            player.hand.append(card)

    def get_player_iterable(self, starting_player_index):
        # make an iterable cycle which starts at the starting player
        player_cycle = islice(
            cycle(self.player_list),
            starting_player_index, None
        )
        # filter out the players with empty hands
        player_iterable = filter(
            lambda player: player.hand,
            player_cycle
        )

        return player_iterable

    def play_hand(self, starting_player_index):
        """"""
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
                elif next_play < current_play or not next_play.is_legal():
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
        deck = deck[cards_to_remove:]
        random.shuffle(deck)

        self.deal_hands(deck)
        current_player_index = 0

        while self.active_players() != 0:
            # Go backwards starting from the current player until we find someone who's hand has cards
            while not self.player_list[current_player_index].hand:
                current_player_index = (current_player_index - 1) % self.player_count
            # Play a hand and return the index of who "won" the hand
            current_player_index = self.play_hand(current_player_index)

    def active_players(self):
        return self.player_count - len(self.winning_order)
