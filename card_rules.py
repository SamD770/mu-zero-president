import random
from itertools import cycle, islice


class Suit:
    def __init__(self, name):
        self.name = name


hearts = Suit("Hearts")
clubs = Suit("Clubs")
diamonds = Suit("Diamonds")
spades = Suit("Spades")

suits = (hearts, clubs, diamonds, spades)


class Card:
    def __init__(self, number: int, suit: Suit):
        self.number = number
        self.suit = suit

    @property
    def priority(self) -> int:
        """2 is the highest number, then ace, then king, queen and so on."""
        if self.number <= 2:
            # Add 13 to 'shift' 2 and ace above the king
            return self.number + 13
        else:
            return self.number

    def __lt__(self, other: 'Card') -> bool:
        return (self.priority < other.priority)

    def __eq__(self, other: 'Card') -> bool:
        return (self.priority == other.priority)


class CardTuple:
    """A thin wrapper around a tuple of cards (supposedly of the same number)"""
    def __init__(self, cards: tuple):
        self.cards = cards

    def __iter__(self):
        return self.cards.__iter__()

    @property
    def is_empty(self) -> bool:
        if self.cards:
            return False
        else:
            return True

    @property
    def first_card(self) -> Card:
        if self.is_empty:
            return None
        else:
            return self.cards[0]

    @property
    def priority(self) -> int:
        if self.is_empty:
            return 1
        else:
            return self.first_card.priority

    @property
    def card_count(self) -> int:
        return len(self.cards)

    @property
    def of_same_number(self):
        for card in self.cards:
            if card != self.first_card:
                return False
        return True

    def __lt__(self, other: 'CardTuple') -> bool:
        return (self.priority < other.priority)

    def __eq__(self, other: 'CardTuple') -> bool:
        return (self.priority == other.priority)

    @staticmethod
    def create_empty():
        return CardTuple(tuple())


class PresidentAction:
    def __init__(self, agent: 'PresidentAgent', cards: CardTuple):
        self.agent = agent
        self.cards = cards

    @property
    def is_pass(self) -> bool:
        return self.cards.is_empty

    def is_legal(self, player_hand: list[Card], top_of_card_stack: CardTuple) -> bool:
        if self.is_pass:
            return True
        # Check cards are all the same number
        if not self.cards.of_same_number:
            return False
        # Check cards are in the agent's hand
        for card in self.cards:
            if card not in player_hand:
                print(card.number, card.suit.name)
                print(player_hand)
                return False
        # Check that they are allowed to go at the top of the card stack
        if top_of_card_stack.is_empty:
            return True
        elif self.cards.card_count != top_of_card_stack.card_count:
            return False
        elif self.cards < top_of_card_stack:
            return False
        else:
            return True

    @staticmethod
    def create_pass(agent: 'PresidentAgent'):
        return PresidentAction(agent, CardTuple.create_empty())

# class PresidentAction:
#     """Wrapper around a tuple of cards of the same number"""
#     def __init__(self, agent, cards):
#         self.agent = agent
#         self.cards = cards
#
#     @property
#     def first_card(self):
#         if self.is_pass():
#             return None
#         else:
#             return self.cards[0]
#
#     @property
#     def card_count(self):
#         return len(self.cards)
#
#     def is_pass(self):
#         return self.card_count == 0
#
#     def __str__(self):
#         return str(self.cards)
#
#     def __lt__(self, other):
#         return self.first_card < other.first_card
#
#     def __eq__(self, other):
#         return self.first_card == other.first_card


class PresidentGameObservation:
    def __init__(self, agent_list, winning_order, action_list, top_of_card_stack, player_hand):
        self.agent_list = agent_list
        self.winning_order = winning_order
        self.action_list = action_list
        self.top_of_card_stack = top_of_card_stack
        self.player_hand = player_hand


class PresidentAgent:
    def __init__(self, name=""):
        self.name = name
        self.observation_buffer = None

    def update_observation_buffer(self, new_observation: PresidentGameObservation):
        self.observation_buffer = new_observation

    # def observe_action(self, new_action: PresidentAction):
    #     raise NotImplementedError("Implement this method")

    def get_next_action(self) -> PresidentAction:
        raise NotImplementedError("Implement this method")

    def handle_illegal_action(self):
        raise NotImplementedError("Implement this method")

    def handle_reward(self, reward_value):
        raise NotImplementedError("Implement this method")


def create_deck() -> list[Card]:
    deck = []
    for i in range(1, 14):
        for suit in suits:
            deck.append(Card(i, suit))
    return deck


class PresidentGame:
    def __init__(self, agent_list: list[PresidentAgent], starting_agent_index=0):
        self.agent_list = agent_list
        self.hand_list = self.get_blank_hands()
        self.top_of_card_stack = None
        self.winning_order = []
        self.action_list = []
        self.agent_count = len(agent_list)
        self.starting_agent_index = starting_agent_index
        self.current_agent_index = starting_agent_index

    def get_blank_hands(self) -> list[list[Card]]:
        return [[] for _ in self.agent_list]

    def deal_hands(self, deck: list[Card]):
        self.hand_list = self.get_blank_hands()
        for card, hand in zip(deck, cycle(self.hand_list)):
            hand.append(card)
        for hand in self.hand_list:
            hand.sort()

    def next_agent(self, forwards=True) -> tuple[PresidentAgent, list]:
        while True:
            if forwards:
                self.current_agent_index += 1
            else:
                self.current_agent_index -= 1
            self.current_agent_index = self.current_agent_index % self.agent_count
            if self.hand_list[self.current_agent_index]:
                break
        return self.agent_list[self.current_agent_index], self.hand_list[self.current_agent_index]

    # def get_agent_iterable(self, starting_agent_index: int):
    #     # make an iterable cycle which starts at the starting agent
    #     agent_cycle = islice(
    #         cycle(zip(self.agent_list, self.hand_list)),
    #         starting_agent_index, None
    #     )
    #     # filter out the agents with empty hands
    #     agent_iterable = filter(
    #         lambda tup: tup[1],
    #         agent_cycle
    #     )
    #     return agent_iterable

    def create_observation(self, hand):
        return PresidentGameObservation(
            self.agent_list, self.winning_order, self.action_list, self.top_of_card_stack, hand)

    def send_observations(self):
        for agent, hand in zip(self.agent_list, self.hand_list):
            agent.update_observation_buffer(self.create_observation(hand))

    def get_legal_play(self, current_agent: PresidentAgent, hand: list) -> PresidentAction:
        while True:
            next_action = current_agent.get_next_action(hand)
            if next_action.is_legal(hand, self.top_of_card_stack):
                return next_action
            else:
                current_agent.handle_illegal_action()

    def active_agents(self):
        return self.agent_count - len(self.winning_order)

    def play_game(self):
        """This function contains most of the logic for playing a game of President."""
        game_over = False

        while not game_over:
            # Reset the game for a new hand
            self.top_of_card_stack = CardTuple.create_empty()
            current_hand_winner = None
            agent_before_hand_winner, _ = self.next_agent(forwards=False)

            while True:
                current_agent, hand = self.next_agent()
                self.send_observations()

                # If everyone else passed, break and start a new hand.
                if current_hand_winner is current_agent:
                    break

                # Get a legal action from the current agent.
                next_action = self.get_legal_play(current_agent, hand)

                # If there are cards on the table, skip the next agent if the plays are equal.
                if not (self.top_of_card_stack.is_empty or next_action.is_pass):
                    if next_action.cards == self.top_of_card_stack:
                        skipped_agent, _ = self.next_agent()

                # Record that this agent played and put their cards at the top of the card stack.
                self.action_list.append(next_action)
                if not next_action.is_pass:
                    self.top_of_card_stack = next_action.cards
                    current_hand_winner = current_agent

                # Remove the cards from this player's hand.
                for card in next_action.cards:
                    hand.remove(card)

                # Put the agent on the winning order if they have no more cards.
                if not hand:
                    self.winning_order.append(current_agent)
                    # Break if no other players have cards either
                    if self.active_agents() == 0:
                        game_over = True
                        break
                    # Step backwards to find a player with a hand, and make this player win if no one else plays.
                    current_hand_winner, _ = self.next_agent(forwards=False)

    def start_game(self):
        deck = create_deck()
        cards_to_remove = 52 % self.agent_count
        deck = deck[cards_to_remove:]
        random.shuffle(deck)
        self.deal_hands(deck)

        self.current_agent_index = self.starting_agent_index

        self.play_game()
        # while self.active_agents() != 0:
        #     # Go backwards starting from the current agent until we find someone who's hand has cards
        #     while not self.hand_list[current_agent_index]:
        #         current_agent_index = (current_agent_index - 1) % self.agent_count
        #     # Play a hand and return the index of who "won" the hand
        #     current_agent_index = self.play_hand(current_agent_index)

        self.send_observations()
        for index, agent in enumerate(self.agent_list):
            # Have linearly scaled rewards between 1 and -1
            reward_value = (self.agent_count - 1 - 2*index)/(self.agent_count - 1)
            agent.handle_reward(reward_value)

    # def do_action(self, action: PresidentAction) -> None:
    #     """Update the players with what action has been played, update the top of the card stack"""
    #     self.update_agents(action)
    #     if not action.is_pass:
    #         self.top_of_card_stack = action
    #
    # def update_agents(self, previous_action: PresidentAction) -> None:
    #     """Remove the cards from the player who played them and update all the players with the action played."""
    #     for agent, hand in zip(self.agent_list, self.hand_list):
    #         agent.observe_action(previous_action)
    #         if agent is previous_action.agent:
    #             for card in previous_action.cards:
    #                 hand.remove(card)
    #             if not hand:
    #                 self.winning_order.append(agent)

