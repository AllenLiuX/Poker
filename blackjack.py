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
            self.points[0] += card.point-10 if card.point==11 else card.point   # A treated as 1
            self.points[1] += card.point if self.points[1]+card.point<=21 else (card.point-10 if card.point==11 else card.point)    # A treated as 11 if not exceed

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
        self.split_count = 0

    def split_strategy(self, opponent_card: Card, deck: Deck, manual_mode: bool=False):
        if self.hand[0].value != self.hand[1].value:
            return
        self_pos = self.hand[0].point-1 if self.hand[0].point!=11 else 0
        oppo_pos = opponent_card.point-1 if opponent_card.point!=11 else 0
        split = split_matrix[self_pos][oppo_pos]
        if manual_mode:
            split_choice = input("Split? (y/n): ")
            split = 1 if split_choice=='y' else 0
        if split:
            pre_card = self.hand[0]
            self.hand = Hand([pre_card, deck.get_card()])
            self.second_hand = Hand([pre_card, deck.get_card()])
            self.split_count += 1
            print("-------- Split! Two hands:", self.hand, self.second_hand)

    def strategy(self, deck, hand: Hand, opponent_card: Card, manual_mode: bool=False) -> int:
        if manual_mode:
            while hand.points[1]<21:
                add_choice = input("Add? (y/n): ")
                if add_choice=='y':
                    new_card = deck.get_card()
                    print('Player get one more card '+str(new_card))
                    hand += Hand([new_card])
                elif add_choice=='n':
                    break
        else:
            while hand.points[1] < 17:
                new_card = deck.get_card()
                print('Player get one more card '+str(new_card))
                hand += Hand([new_card])
        return hand
            

class Bot:
    def __init__(self, hand=Hand([])) -> None:
        self.hand = None

    def strategy(self, deck):
        while self.hand.points[0] < 17:
            new_card = deck.get_card()
            print('Bot get one more card '+str(new_card))
            self.hand += Hand([new_card])
            
class Game:
    def __init__(self):
        self.deck = Deck(4)
        self.player = Player(1000)
        self.bot = Bot()
        self.blackjack_count = 0

    def play(self, manual_mode: bool = False, bet: int = 200):
        self.deck.check_deck()
        if manual_mode:
            bet = int(input('Bet: '))
        self.player.hand = self.deck.get_a_hand()
        self.player.second_hand = None
        self.bot.hand = self.deck.get_a_hand()
        if manual_mode:
            print('Player cards:', self.player.hand.cards, 'Bot cards:', self.bot.hand.cards[0], ', xx')
        else:
            print('Player cards:', self.player.hand.cards, 'Bot cards:', self.bot.hand.cards)
            print('Player points:', self.player.hand, 'Bot points:', self.bot.hand)
        self.player.split_strategy(self.bot.hand[0], self.deck, manual_mode)
        
        self.player.hand = self.player.strategy(self.deck, self.player.hand, self.bot.hand[0], manual_mode)
        if self.player.second_hand:
            self.player.second_hand = self.player.strategy(self.deck, self.player.second_hand, self.bot.hand[0], manual_mode)
        self.bot.strategy(self.deck)
        self.compare(self.player, self.player.hand, self.bot.hand, bet)
        if self.player.second_hand:
            self.compare(self.player, self.player.second_hand, self.bot.hand, bet)
            
    def compare(self, player: Player, player_hand: Hand, bot_hand: Hand, bet: int):
        print('Player hand:', player_hand, 'Bot hand:', bot_hand)
        player_point = player_hand.points[1]
        bot_point = bot_hand.points[1]
        if player_point > 21 or (player_point < bot_point and bot_point <= 21):
            player.money -= bet
            print('Player lose! Money: '+str(player.money))
        elif player_point > bot_point or bot_point > 21:
            player.money += bet
            # blackjack:
            if player_point == 21 and len(player_hand.cards)==2:
                player.money += bet*0.5
                self.blackjack_count += 1
                print("------ BlackJack!! ------")
            print('Player win! Money: '+str(player.money))
        else:
            print('Draw! Money:'+str(player.money))
        print('========================')

    def begin(self, manual_mode: bool=False):
        print("====== Game Begin! ======")
        print(f"Total money: {self.player.money}")
        round = 0
        while self.player.money > 0:
            self.play(manual_mode)
            round += 1
            time.sleep(1)
        print("Player lose all.")
        print(f"Total round: {round}. Blackjack count: {self.blackjack_count}")

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
    game.begin(manual_mode=True)
