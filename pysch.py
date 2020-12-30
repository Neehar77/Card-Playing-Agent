import itertools
import random
import cards


class Player(object):
    def __init__(self):
        global agent_hand, sensible_card, win, ordered, suit, rank
        rank = {'A': 13, 'K': 12, 'Q': 11, 'J': 10, '10': 9, '9': 8, '8': 7, '7': 6, '6': 5, '5': 4, '4': 3, '3': 2, '2': 1}
        suit = []
        ordered = []
        agent_hand = []
        sensible_card = ""
        win = ""
        pass

    def get_name(self):  # gets the name of the agent
        name = input("Enter the name of the agent: ")
        print("Hi", name)
        return name
        """
        Returns a string of the agent's name
        """
        pass

    def get_hand(self):  # gets the list of 13 unique cards from an unbiased deck
        card = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        deck = list(itertools.product(range(1, 13), ['S', 'H', 'D', 'C']))
        random.shuffle(deck)
        for i in range(13):
            temp = deck[i][0]
            agent_hand.append(card[temp] + deck[i][1])
        return agent_hand
        """
        Returns a list of two character strings representing cards in the agent's hand
        """
        pass

    def new_hand(self, names):  # removes the inputted card from the hand and resets the order/turns of players
        turns = []
        agent_hand.remove(sensible_card)
        for i in range(0, len(names) - 1):
            if win == names[i]:
                for j in range(0, len(names) - 1):
                    turns[j] = (i + j) % 4
                ordered.append(ordered[i] for i in turns)
                break
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

    def play_card(self, lead, trick):  # This function will be called once in every trick
        if lead == "p1":
            sensible_card = random.choice(agent_hand)
            trick.append(sensible_card)  # agent_hand = agent_hand - sensible_card
            return sensible_card
        elif lead == "p2":
            if len(trick) == 3:
                for i in range(len(agent_hand)):
                    while (any(i in trick) for i in
                           agent_hand[i]):  # checks if the same suit is available in the hand or not
                        agent_hand.append(agent_hand[i])
                    break
                sensible_card = random.choice(
                    agent_hand)  # In this case trick would consist of three cards and our agent would be last to play
                trick.append(sensible_card)  # agent_hand = agent_hand - sensible_card
                return sensible_card
            else:
                print("other player has not enter there cards yet")
        elif lead == "p3":
            if len(trick) == 2:
                for i in range(len(agent_hand)):
                    while (any(i in trick) for i in
                           agent_hand[i]):  # checks if the same suit is available in the hand or not
                        agent_hand.append(agent_hand[i])
                    break  # In case of no suit it will pass random values of any suit
                sensible_card = random.choice(
                    agent_hand)  # In this case trick would consist of two cards and our agent would be third to play
                trick.append(sensible_card)  # agent_hand = agent_hand - sensible_card
                return sensible_card
            else:
                print("")
        elif lead == "p4":
            if len(trick) == 2:
                for i in range(len(agent_hand)):
                    while (any(i in trick) for i in
                           agent_hand[i]):  # checks if the same suit is available in the hand or not
                        agent_hand.append(agent_hand[i])
                    break  # In case of no suit it will pass random values of any suit
                sensible_card = random.choice(
                    agent_hand)  # In this case trick would consist of one card and our agent would be second to play
                trick.append(sensible_card)  # agent_hand = agent_hand - sensible_card
                return sensible_card
            else:
                print("")
        """
        Takes a a string of the name of the player who lead the trick and
        a list of cards in the trick so far as arguments.

        Returns a two character string from the agents hand of the card to be played
        into the trick.
        """
        pass

    def collect_trick(self, lead, winner, trick):
        if len(trick) == 4:
            winner = max(trick)
            lead = winner

        """
        Takes three arguments. Lead is the name of the player who led the trick.
        Winner is the name of the player who won the trick. And trick is a four card
        list of the trick that was played. Should return nothing.
        """
        pass

    def score(self):

        """
        Calculates and returns the score for the game being played.
        """
        pass


def main():
    names = ["p1", "p2", "p3", "p4"]
    cards_played = []
    cards = []
    p1 = Player()
    p1.play_card("p2", cards_played)
    p1.collect_trick("p2", "p1", cards)
    p1.score()


main()