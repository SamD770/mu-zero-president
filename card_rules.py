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
        return Card.number_to_name(self.number) + " of " + self.suit.name

    def __lt__(self, other):
        return (self.priority < other.priority)

    def __eq__(self, other):
        return (self.priority == other.priority)


class PresidentAction:
    """Wrapper around a tuple of cards of the same number"""
    def __init__(self, agent, *cards):
        self.agent = agent
        self.cards = cards
        self.card_count = len(cards)
        self.first_card = self.cards[0]

    def __comp__(self, other):
        return self.first_card.__comp__(other.first_card)

    def __str__(self):
        return str(self.cards)

    def is_pass(self):
        return (self.cards is None)

    def is_legal(self):
        for card in self.cards:
            if card != self.first_card or card not in self.agent.hand:
                return False
        return True


class PresidentAgent:
    def __init__(self, name=""):
        self.name = name

    def observe_action(self, new_action: PresidentAction):
        raise NotImplementedError("Implement this method")

    def get_next_action(self, hand: list[Card]) -> PresidentAction:
        raise NotImplementedError("Implement this method")

    def handle_illegal_action(self):
        raise NotImplementedError("Implement this method")


class IllegalActionException(Exception):
    pass


def create_deck()-> list[Card]:
    deck = []
    for i in range(1, 14):
        for suit in suits:
            deck.append(Card(i, suit))
    return deck


class PresidentGame:
    def __init__(self, agent_list, starting_agent_index=0):
        self.agent_list = agent_list
        self.hand_list = self.get_blank_hands()
        self.top_of_card_stack = None
        self.winning_order = []
        self.agent_count = len(agent_list)
        self.current_agent_index = starting_agent_index

    def get_blank_hands(self):
        return [[] for _ in self.agent_list]

    def deal_hands(self, deck):
        self.hand_list = self.get_blank_hands()
        for card, hand in zip(deck, cycle(self.hand_list)):
            hand.append(card)
        for hand in self.hand_list:
            hand.sort()

    def get_agent_iterable(self, starting_agent_index):
        # make an iterable cycle which starts at the starting agent
        agent_cycle = islice(
            cycle(zip(self.agent_list, self.hand_list)),
            starting_agent_index, None
        )
        # filter out the agents with empty hands
        agent_iterable = filter(
            lambda agent, hand: hand,
            agent_cycle
        )
        return agent_iterable

    def update_agents(self, previous_action: PresidentAction) -> None:
        """Remove the cards from the player who played them and update all the players with the action played."""
        for agent, hand in zip(self.agent_list, self.hand_list):
            agent.observe_action(previous_action)
            if agent is previous_action.agent:
                for card in previous_action.cards:
                    hand.remove(card)

    def do_action(self, action: PresidentAction) -> None:
        """Update the players with what action has been played, update the top of the card stack"""
        self.update_agents(action)
        if not action.is_pass():
            self.top_of_card_stack = action.cards

    def is_legal(self, action: PresidentAction) -> bool:
        pass

    def play_hand(self, starting_agent_index):
        """"""
        agent_iterable = self.get_agent_iterable(starting_agent_index)
        last_agent_to_play = None

        for current_agent, hand in agent_iterable:
            legal_action = False

            while not legal_action:
                next_action = current_agent.get_next_action(self, hand)
                if next_action.is_legal():
                    legal_action = True
                else:
                    current_agent.handle_illegal_action()

            # if the agent passes, do nothing
            if next_action.is_pass():
                continue

            # If there are cards on the table, skip the next agent if the plays are equal
            if self.top_of_card_stack is not None:
                if self.top_of_card_stack == next_action.cards:
                    skipped_agent, skipped_hand = agent_iterable.__next__()
            # Remove the cards from this player's hand and put them on the winning list if they have no more.
            self.do_action(next_action)
            if not hand:
                self.winning_order.append(current_agent)
            # if everyone else skipped, break
            if current_agent is last_agent_to_play:
                hand_winner_index = self.agent_list.index_of(current_agent)
                break
            # record that this agent played
            last_agent_to_play = current_agent

        return hand_winner_index

    def start_game(self):
        deck = create_deck()
        cards_to_remove = 52 % self.agent_count
        deck = deck[cards_to_remove:]
        random.shuffle(deck)

        self.deal_hands(deck)
        current_agent_index = 0

        while self.active_agents() != 0:
            # Go backwards starting from the current agent until we find someone who's hand has cards
            while not self.hand_list[current_agent_index]:
                current_agent_index = (current_agent_index - 1) % self.agent_count
            # Play a hand and return the index of who "won" the hand
            current_agent_index = self.play_hand(current_agent_index)

    def active_agents(self):
        return self.agent_count - len(self.winning_order)
