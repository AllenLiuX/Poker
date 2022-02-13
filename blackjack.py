import random
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass


def set_logger():
    # LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    LOG_FORMAT = "%(message)s"
    logging.basicConfig(filename='test.log', level=logging.INFO, format=LOG_FORMAT, filemode='w')
    # info_filter = logging.Filter()
    # info_filter.filter = lambda record: record.level == logging.INFO
    # logging.basicConfig(filename='test.log', level=logging.INFO, format=LOG_FORMAT, handlers=info_filter)

set_logger()

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

strategy_matrix = [ # 0 is stop, 1 is add, 2 is double
        #2,3,4,5,6,7,8,9,T,A oppnent/player
        [1,1,1,1,1,1,1,1,1,1],  # 8
        [1,2,2,2,2,1,1,1,1,1],
        [2,2,2,2,2,2,2,2,1,1],
        [2,2,2,2,2,2,2,2,2,2],
        [1,1,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,1,1,1,1,1],
        [0,0,0,0,0,0,0,0,0,0],  # 17
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
            logging.info('New deck')
            self.new_deck(self.deck_num)

    def get_card(self):
        if not self.deck:
            logging.info('New deck')
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
        oppo_pos = opponent_card.point-2
        split = split_matrix[self_pos][oppo_pos]
        if manual_mode:
            split_choice = input("Split? (y/n): ")
            split = 1 if split_choice=='y' else 0
        if split:
            pre_card = self.hand[0]
            self.hand = Hand([pre_card, deck.get_card()])
            self.second_hand = Hand([pre_card, deck.get_card()])
            self.split_count += 1
            logging.info(f"-------- Split! Two hands: {self.hand}, {self.second_hand}")

    def add_a_card(self, hand: Hand, deck: Deck):
        new_card = deck.get_card()
        logging.info(f'Player get one more card {new_card}')
        hand += Hand([new_card])
        return hand
    
    def strategy(self, deck, hand: Hand, opponent_card: Card, manual_mode: bool=False) -> Hand:
        bet_multiplier = 1
        if manual_mode:
            while hand.points[1]<21:
                add_choice = input("Add? (y/n): ")
                if add_choice=='y':
                    hand = self.add_a_card(hand, deck)
                elif add_choice=='n':
                    break
        else:
            while hand.points[1] < 9:
                hand = self.add_a_card(hand, deck)
            while hand.points[1] < 17:
                strat = strategy_matrix[hand.points[1]-8][opponent_card.point-2]
                if strat == 0:
                    break
                elif strat == 1:
                    hand = self.add_a_card(hand, deck)
                elif strat == 2:
                    if len(hand.cards) == 2:
                        logging.info("----- Double Bet! -----")
                        bet_multiplier = 2
                    hand = self.add_a_card(hand, deck)
                    break
        return hand, bet_multiplier
            

class Bot:
    def __init__(self, hand=Hand([])) -> None:
        self.hand = None

    def strategy(self, deck):
        while self.hand.points[0] < 17:
            new_card = deck.get_card()
            logging.info(f'Bot get one more card {new_card}')
            self.hand += Hand([new_card])

@dataclass
class Result:
    win: int = 0
    lose: int = 0
    draw: int = 0

class Game:
    def __init__(self, money: int = 2000, blackjack_ratio=0.2, commission=0):
        self.deck = Deck(4)
        self.player = Player(money)
        self.bot = Bot()
        self.blackjack_ratio = blackjack_ratio
        self.blackjack_count = 0
        self.result: Result = Result()
        self.commission = commission
        
    def play(self, manual_mode: bool = False, bet: int = 200):
        self.deck.check_deck()
        if manual_mode:
            bet = int(input('Bet: '))
        # bet = self.player.money*0.03
        bet_multiplier_1, bet_multiplier_2 = 1, 1
        self.player.hand = self.deck.get_a_hand()
        self.player.second_hand = None
        self.bot.hand = self.deck.get_a_hand()
        if manual_mode:
            logging.info(f'Player cards: {self.player.hand.cards}, Bot cards:{self.bot.hand.cards[0]}, xx')
        else:
            logging.info(f'Player cards: {self.player.hand.cards}, Bot cards:{self.bot.hand.cards}')
            logging.info(f'Player points: {self.player.hand}, Bot points:{self.bot.hand}')
        self.player.split_strategy(self.bot.hand[0], self.deck, manual_mode)
        
        self.player.hand, bet_multiplier_1 = self.player.strategy(self.deck, self.player.hand, self.bot.hand[0], manual_mode)
        if self.player.second_hand:
            logging.info("For second hand:")
            self.player.second_hand, bet_multiplier_2 = self.player.strategy(self.deck, self.player.second_hand, self.bot.hand[0], manual_mode)
        self.bot.strategy(self.deck)
        self.compare(self.player, self.player.hand, self.bot.hand, bet*bet_multiplier_1)
        if self.player.second_hand:
            self.compare(self.player, self.player.second_hand, self.bot.hand, bet*bet_multiplier_2)
        self.player.money -= self.commission
            
    def compare(self, player: Player, player_hand: Hand, bot_hand: Hand, bet: int):
        logging.info(f'Player point: {player_hand.points[1]}, Bot point: {bot_hand.points[1]}')
        player_point = player_hand.points[1]
        bot_point = bot_hand.points[1]
        if player_point > 21 or (player_point < bot_point and bot_point <= 21) or bot_point==21:
            player.money -= bet
            self.result.lose += 1
            logging.info('Player lose! Money: '+str(player.money))
        elif player_point > bot_point or bot_point > 21:
            player.money += bet
            # blackjack:
            if player_point == 21 and len(player_hand.cards)==2:
                player.money += bet*self.blackjack_ratio
                self.blackjack_count += 1
                logging.info("------ BlackJack!! ------")
            self.result.win += 1
            logging.info('Player win! Money: '+str(player.money))
        else:
            self.result.draw += 1
            logging.info('Draw! Money:'+str(player.money))
        logging.info('========================')

    def simulate(self, manual_mode: bool=False, bet:int = 200, iterations:int = 1000):
        logging.info("====== Game Begin! ======")
        logging.info(f"Total money: {self.player.money}")
        round = 0
        money_data = []
        while self.player.money > 0 and round < iterations:
            self.play(manual_mode=manual_mode, bet=bet)
            logging.info(f"Round #{round}")
            round += 1
            money_data.append(self.player.money)
            # time.sleep(1)
        # logging.info("Player lose all.")
        logging.info(f"Total round: {round}. Blackjack count: {self.blackjack_count}")
        return money_data



def unit_test():
    # Deck
    deck = Deck(2)
    logging.info(str(sorted(deck.deck)))

    # Hand
    hand = Hand([Card('7s'), Card('As'), Card('As')])
    hand += Hand([Card('2c')])
    logging.info(hand.cards)
    logging.info(hand)

    # Bot
    bot  = Bot()
    bot.strategy(deck)

if __name__=='__main__':
    game = Game(money=1000, blackjack_ratio=0.3, commission=0)
    data = game.simulate(manual_mode=False, bet=30, iterations=1000)
    logging.info(str(game.result))
    # plot(data)
    