import random
import time
import logging

logging.basicConfig()
# Constants
suit_index_dict = {"s": 0, "c": 1, "h": 2, "d": 3}
reverse_suit_index = ("s", "c", "h", "d")
val_string = "AKQJT98765432"
suit_value_dict = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
suit_point_dict = {"T": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
suit_dict = {'♠': 's', '♣': 'c', '♥': 'h', '♦': 'd'}
split_matrix = [
            [1,1,1,1,1,1,1,1,1,1],  # AA
            [0,0,1,1,1,1,0,0,0,0],  # 22
            [0,0,1,1,1,1,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,0,0,0,0,0],
            [1,1,1,1,1,1,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,0,1,1,0,0],
            [0,0,0,0,0,0,0,0,0,0]   #TT
        ]

suit2shape = {}
for key, val in suit_dict.items():
    suit2shape[val] = key

for num in range(2, 10):
    suit_value_dict[str(num)] = num
    suit_point_dict[str(num)] = num

class Card:
    # Takes in strings of the format: "As", "Tc", "6d"
    def __init__(self, card_string):
        value, self.suit = card_string[0], card_string[1]
        self.value = suit_value_dict[value]
        self.point = suit_point_dict[value]
        self.suit_index = suit_index_dict[self.suit]

    def __str__(self):
        return suit2shape[self.suit]+val_string[14 - self.value]

    def __repr__(self):
        return suit2shape[self.suit]+val_string[14 - self.value]

    def __eq__(self, other):
        if self is None:
            return other is None
        elif other is None:
            return False
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        if self is None:
            return other is None
        elif other is None:
            return False
        return self.value < other.value

class Deck:
    def __init__(self, deck_num):
        self.deck = []
        self.deck_num = deck_num
        self.new_deck(deck_num)

    def new_deck(self, deck_num):
        one_deck = [Card(value+suit) for value in val_string for suit in reverse_suit_index]
        for i in range(deck_num):
            self.deck += one_deck
        random.shuffle(self.deck)

    def check_deck(self):
        if len(self.deck)<10:
            print('New deck')
            self.new_deck(self.deck_num)

    def get_card(self):
        if not self.deck:
            print('New deck')
            self.new_deck(self.deck_num)
        card = self.deck.pop(0)
        return card

    def get_a_hand(self):
        return Hand([self.get_card(), self.get_card()])

class Hand:
    def __init__(self, cards) -> None:
        self.cards = sorted(cards)
        self.points = [0, 0]
        self.calc()
        
    def calc(self):
        for card in self.cards:
            self.points[0] += card.point-10 if card.point==11 else card.point
            self.points[1] += card.point if self.points[1]+card.point<21 else (card.point-10 if card.point==11 else card.point)

    def __str__(self) -> str:
        return str(self.points)
            
    def __add__(self, other):
        return Hand(self.cards+other.cards)

    def __getitem__(self, key):
        return self.cards[key]


class Player:
    def __init__(self, money) -> None:
        self.money = money
        self.hand = None
        self.second_hand = None

    def split_strategy(self, opponent_card: Card):
        if self.hand[0] == self.hand[1]:
            pass


    def strategy(self, deck, hand: Hand, opponent_card: Card) -> int:
        while self.hand.points[1] < 17:
            new_card = deck.get_card()
            print('Player get one more card '+str(new_card))
            self.hand += Hand([new_card])
            

class Bot:
    def __init__(self, hand=Hand([])) -> None:
        self.hand = None

    def strategy(self, deck):
        while self.hand.points[0] < 17:
            new_card = deck.get_card()
            print('Bot get one more card '+str(new_card))
            self.hand += Hand([new_card])
            
            # hand = Hand(hand.cards+[deck.get_card()])

class Game:
    def __init__(self):
        self.deck = Deck(4)
        self.player = Player(1000)
        self.bot = Bot()

    def play(self):
        self.deck.check_deck()
        # bet = int(input('Bet: '))
        bet = 200
        self.player.hand = self.deck.get_a_hand()
        self.bot.hand = self.deck.get_a_hand()
        print('Player hand:', self.player.hand, 'Bot hand:', self.bot.hand)
        self.player.strategy(self.deck, self.bot.hand[0])
        self.bot.strategy(self.deck)
        print('Player hand:', self.player.hand, 'Bot hand:', self.bot.hand)
        player_point = self.player.hand.points[1]
        bot_point = self.bot.hand.points[1]
        if player_point > 21 or (player_point < bot_point and bot_point <= 21):
            self.player.money -= bet
            print('Player lose! Money: '+str(self.player.money))
        elif player_point > bot_point or bot_point > 21:
            self.player.money += bet
            print('Player win! Money: '+str(self.player.money))
        else:
            print('Draw! Money:'+str(self.player.money))
        print('========================')
        
    def begin(self):
        round = 0
        while self.player.money > 0:
            self.play()
            round += 1
            time.sleep(1)
        print("Player loose all.")
        print("Total round:", round)

if __name__=='__main__':
    deck = Deck(2)
    print(sorted(deck.deck))
    hand = Hand([Card('7s'), Card('As'), Card('As')])
    
    hand += Hand([Card('2c')])
    print(hand.cards)
    print(hand)

    # bot  = Bot()
    # bot.strategy(deck)

    game = Game()
    game.begin()
