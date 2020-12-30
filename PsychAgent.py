from experta import *
import schema
from experta.fact import *
import random
import itertools

global agent_hand, played_card, winner


class WinTotals(Fact):
    agent = Field(int, default=0)


class Results(Fact):
    winner = Field(str, mandatory=True)


class ValidAnswer(Fact):
    answer = Field(str, mandatory=True)
    key = Field(int, mandatory=True)


class Action(Fact):
    pass


class AgentChoice(Fact):
    pass


class PriorPlayerChoice(Fact):
    pass


class WinningCard(Fact):
    pass


class CardGamePlay(KnowledgeEngine):

    @DefFacts()
    def game_rules(self):
        self.valid_answers = dict()
        yield Results(winner='AS')
        yield ValidAnswer(answer='2S', key=1)
        yield ValidAnswer(answer='3S', key=2)
        yield ValidAnswer(answer='4S', key=3)
        yield ValidAnswer(answer='5S', key=4)
        yield ValidAnswer(answer='6S', key=5)
        yield ValidAnswer(answer='7S', key=6)
        yield ValidAnswer(answer='8S', key=7)
        yield ValidAnswer(answer='9S', key=8)
        yield ValidAnswer(answer='10S', key=9)
        yield ValidAnswer(answer='JS', key=10)
        yield ValidAnswer(answer='QS', key=11)
        yield ValidAnswer(answer='KS', key=12)
        yield ValidAnswer(answer='AS', key=13)

        yield ValidAnswer(answer='2C', key=14)
        yield ValidAnswer(answer='3C', key=15)
        yield ValidAnswer(answer='4C', key=16)
        yield ValidAnswer(answer='5C', key=17)
        yield ValidAnswer(answer='6C', key=18)
        yield ValidAnswer(answer='7C', key=19)
        yield ValidAnswer(answer='8C', key=20)
        yield ValidAnswer(answer='9C', key=21)
        yield ValidAnswer(answer='10C', key=22)
        yield ValidAnswer(answer='JC', key=23)
        yield ValidAnswer(answer='QC', key=24)
        yield ValidAnswer(answer='KC', key=25)
        yield ValidAnswer(answer='AC', key=26)

        yield ValidAnswer(answer='2H', key=27)
        yield ValidAnswer(answer='3H', key=28)
        yield ValidAnswer(answer='4H', key=29)
        yield ValidAnswer(answer='5H', key=30)
        yield ValidAnswer(answer='6H', key=31)
        yield ValidAnswer(answer='7H', key=32)
        yield ValidAnswer(answer='8H', key=33)
        yield ValidAnswer(answer='9H', key=34)
        yield ValidAnswer(answer='10H', key=35)
        yield ValidAnswer(answer='JH', key=36)
        yield ValidAnswer(answer='QH', key=37)
        yield ValidAnswer(answer='KH', key=38)
        yield ValidAnswer(answer='AH', key=39)

        yield ValidAnswer(answer='2D', key=40)
        yield ValidAnswer(answer='3D', key=41)
        yield ValidAnswer(answer='4D', key=42)
        yield ValidAnswer(answer='5D', key=43)
        yield ValidAnswer(answer='6D', key=44)
        yield ValidAnswer(answer='7D', key=45)
        yield ValidAnswer(answer='8D', key=46)
        yield ValidAnswer(answer='9D', key=47)
        yield ValidAnswer(answer='10D', key=48)
        yield ValidAnswer(answer='JD', key=49)
        yield ValidAnswer(answer='QD', key=50)
        yield ValidAnswer(answer='KD', key=51)
        yield ValidAnswer(answer='AD', key=52)

    @Rule()
    def startup(self):
        print('Hi! My Name is ' + Player.get_name(Player))
        res = input('Am I first Player?')
        if res == 'yes' or res == 'Yes' or res == 'YES':
            self.declare(Action('get-first-agent-move'))
        else:
            self.declare(Action('get-player-move'))
        # if turn != p1:
        #     self.declare(Action('get-player-move'))
        #     print(self.valid_answers);
        # else:

    @Rule(NOT(Action()), ValidAnswer(answer=MATCH.answer, key=MATCH.key))
    def store_valid_answers(self, answer, key):
        self.valid_answers[key] = answer

    @Rule(Action('get-first-agent-move'))
    def get_first_agent_move(self):
        card_in_hand = [];
        for x, y in self.valid_answers.items():
            card_in_hand.append(x);
        print(max(Player.get_hand(Player)))

    @Rule(Action('get-player-move'))
    def get_previous_player_action(self):
        res = input("What other player played?")
        self.declare(PriorPlayerChoice(res))

    @Rule(AS.f1 << PriorPlayerChoice(MATCH.choice),
          ValidAnswer(answer=MATCH.choice,
                      key=MATCH.key),
          AS.f2 << Action('get-player-move'))
    def good_player_move(self, f1, f2, choice):
        self.retract(f1)
        self.retract(f2)
        self.declare(PriorPlayerChoice(choice))
        self.declare(Action('get-agent-move'))

    @Rule(AS.f1 << PriorPlayerChoice(MATCH.choice),
          NOT(ValidAnswer(answer=MATCH.choice)),
          AS.f2 << Action('get-player-move'))
    def bad_player_move(self, f1, f2, choice):
        print("%s is not a valid" % choice)
        self.retract(f1)
        self.retract(f2)
        self.declare(Action('get-player-move'))

    @Rule(AS.f1 << PriorPlayerChoice(MATCH.choice), ValidAnswer(answer=MATCH.choice, key=MATCH.key),
          AS.f2 << Action('get-agent-move'))
    def get_agent_move(self, f2, choice, key):
        # print(choice)
        # print(key)
        # for x in self.valid_answers.values():
        #     if choice == self.valid_answers[x]:
        #         playerchoice = valid_answers[x]
        # print(playerchoice)
        get_hand_list = Player.get_hand(Player)
        hand_list = []
        for x, y in self.valid_answers.items():
            for z in get_hand_list:
                if z == y:
                    hand_list.append(x);
        played_card = Player.play_card(Player, key, hand_list)
        print(self.valid_answers.get(played_card))


class Player(object):
    def get_name(self):
        agent_name = "PsychAgent"
        return agent_name

    def get_hand(self):
        agent_hand = []
        card = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = list(itertools.product(range(1, 13), ['S', 'H', 'D', 'C']))
        random.shuffle(deck)
        for i in range(13):
            temp = deck[i][0]
            agent_hand.append(card[temp] + deck[i][1])
        print("Cards in Hand: ", agent_hand)
        return agent_hand
        # """
        # Returns a list of two character strings representing cards in the agent's hand

    def play_card(self, lead, trick=[]):
        suit_hand = []
        no_suit = []
        agent_card_play = {}
        other_player_card = lead
        # print(trick)
        if other_player_card in range(1, 13):
            lowrange = 1;
            highrange = 13;
        elif other_player_card in range(14, 26):
            lowrange = 14;
            highrange = 26;
        elif other_player_card in range(27, 39):
            lowrange = 27;
            highrange = 39;
        elif other_player_card in range(40, 52):
            lowrange = 40;
            highrange = 52;
        else:
            lowrange = 0;
            highrange = 0;

        # print(lowrange)
        # print(highrange)
        for x in agent_hand:
            if x in range(lowrange, highrange + 1):
                suit_hand.append(x)
            else:
                no_suit.append(x)
        if len(suit_hand) != 0:
            suit_hand.sort()
            for i in range(len(suit_hand)):
                if i > other_player_card:
                    return i
            return suit_hand[0]
        else:
            for i in range(len(no_suit)):
                agent_card_play[no_suit[i]] = no_suit[i] % 13
        if len(agent_card_play) != 0:
            min_card = min(agent_card_play.keys(), key=(lambda k: agent_card_play[k]))
            return min_card

        # if(len(agent_card_play) != 0):
        #     return random.choice(agent_card_play)
        # print(agent_card_play)

        """
        Takes a a string of the name of the player who lead the trick and
        a list of cards in the trick so far as arguments.

        Returns a two character string from the agents hand of the card to be played
        into the trick.
        """
        pass

    def new_hand(self, names):     # removes the inputted card from the hand and resets the order/turns of players
        agent_hand.remove(played_card)
        # for i in range(0, len(names) - 1):
        #     if winner == names[i]:
        #         for j in range(0, len(names) - 1):
        #             turns[j] = (i+j) % 4
        #         ordered.append(ordered[i] for i in turns)
        #         break
        """
        Takes a list of names of all agents in the game in clockwise playing order
        and returns nothing. This method is also responsible for clearing any data
        necessary for your agent to start a new round.
        """
        pass

    def add_cards_to_hand(self, cards):
        """
        Takes a list of two character strings representing cards as an argument
        and returns nothing.
        This list can be any length.
        """
        pass


cgp = CardGamePlay()
cgp.reset()
cgp.run()
