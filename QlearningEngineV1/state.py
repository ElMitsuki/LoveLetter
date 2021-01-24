"""
Class that represent a state.
A state can be represented by the two cards a player can play.
"""
class State:

    def __init__(self, card1, card2):
        if card1 <= card2:
            self.__card1 = card1
            self.__card2 = card2
        else:
            self.__card1 = card2
            self.__card2 = card1

    def getCard1(self):
        return self.__card1

    def getCard2(self):
        return self.__card2
