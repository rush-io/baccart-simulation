import statistics
import random
import itertools
from timeit import default_timer as timer

class Baccarat:

    def __init__(self, cash, bet, max_hands, num_decks, style, num_sims):

        self.cash = cash
        self.bet = bet
        self.max_hands = max_hands
        self.num_decks = num_decks
        self.style = style
        self.num_sims = num_sims

        self.values = {
            'K':10,
            'Q':10,
            'J':10,
            'T':10,
            '9':9,
            '8':8,
            '7':7,
            '6':6,
            '5':5,
            '4':4,
            '3':3,
            '2':2,
            'A':1,
        }

    def initialize_deck(self,num_decks):
    
        unflat = [key*num_decks*4 for key in self.values.keys()]
        deck = list(itertools.chain.from_iterable(unflat))

        return deck
        
    def simulate(self, losses):

        num_hands = 0
        num_decks = 6
        num_wins =  0
        cash = self.cash
        odd_primes = [3,5,7,11]
        # banker_moves = {
        #     0: [0,1,2,3,4,5,6,7,8,9,10],
        #     1: [0,1,2,3,4,5,6,7,8,9,10],
        #     2: [0,1,2,3,4,5,6,7,8,9,10],
        #     3: [1,2,3,4,5,6,7,9,10],
        #     4: [2,3,4,5,6,7],
        #     5: [4,5,6,7],
        #     6: [6,7],
        # }

        deck = self.initialize_deck(num_decks=self.num_decks)
        random.shuffle(deck)
        
        cut_position = random.randint(len(deck)-62, len(deck)-42)
        
        #burn 
        deck = deck[random.randint(0,9):]
        
        while cash > 0:
        
            if self.style == 'randomly':
                bet_side = random.choice(['player', 'banker'])
            else:
                bet_side = self.style

            player_draw, banker_draw = True, True
            player, banker = 0,0
            player_cards, banker_cards = [], []

            if cut_position > len(deck):

                deck = self.initialize_deck(num_decks=self.num_decks)
                random.shuffle(deck)
                cut_position = random.randint(len(deck)-62, len(deck)-42)

            for i in range(4):
                x = deck.pop(0)
                
                if i % 2 == 0:                
                    player += self.values[x]
                    player_cards.append(x)
                else:
                    banker += self.values[x]
                    banker_cards.append(x)
                    
            player %= 10 
            banker %= 10

            # natural
            if player in [8,9] or banker in [8,9]:
                player_draw = False
                banker_draw = False

            #stand
            if player in [6,7]:
                player_draw = False
            if banker == 7:
                banker_draw = False

            if player_draw:
                x = deck.pop(0)    
                player += self.values[x]
                player %= 10
                player_cards.append(x)

            if 2 < banker < 6:
                if (player % 7) <= (odd_primes[banker-3] - 1) / 2:
                    banker_draw = False
            else:
                x = deck.pop(0)
                banker += self.values[x]
                banker_cards.append(x)
                banker %=10

            if banker > player:
                if bet_side == 'banker':
                    num_wins += 1
                    cash += 0.95*self.bet
                else:
                    cash -= self.bet

            elif player > banker:
                if bet_side == 'player':
                    num_wins += 1
                    cash += self.bet
                else:
                    cash -= self.bet
            else:
                pass

            num_hands +=1
            if num_hands == self.max_hands:
                break
        if cash <= 0:
            losses += 1
        winrate = round((num_wins/num_hands)*100)   
        return cash, num_hands, winrate, losses

    def run(self):
        
        print(f'\n{self.num_sims} simulations of {self.max_hands} hands of Baccarat betting {self.style}\n')

        session_cash = []
        session_winrate = []
        session_hands = []
        L = 0
        for i in range(self.num_sims):
            cash, num_hands, winrate, L = self.simulate(losses=L)
            session_cash.append(cash)
            session_winrate.append(winrate)
            session_hands.append(num_hands)
        
        
        print(f'starting cash: {self.cash}')
        print(f'bet size: {self.bet}\n')
        print(f'avg winrate: {round(statistics.mean(session_winrate),1)}%')
        print(f'avg finishing cash: ${round(statistics.mean(session_cash))}')
        print(f'avg number of hands: {round(statistics.mean(session_hands))}')
        print(f'bankruptcy chance: {round((L/self.num_sims)*100)}%')


simulations = Baccarat(cash=1000, bet=10, max_hands=10000, num_decks=6, style='randomly', num_sims=1000)

start = timer()

simulations.run()
end = timer()

print(f'simulation time: {round(end - start)}s')