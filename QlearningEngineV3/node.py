from .state import State

"""
Class that represents a node of the tree which contains a state with the parent of the state, their expectations
and also the size of the draw. It also contains the player choosen by playing a Prince (True = AI, False = Player)
"""
class Node:

    def __init__(self, parent_card1, parent_card2, parent_action, parent_expectation, current_card1, current_card2, current_action, draw_size, choosenPlayer):
        if (parent_card1 is None) or (parent_card2 is None):
            self.__parent_state = None
        else:
            self.__parent_state = State(parent_card1, parent_card2)
        self.__parent_action = parent_action
        self.__parent_expectation = parent_expectation
        self.__current_state = State(current_card1, current_card2)
        self.__current_action = current_action
        self.__current_expectation = 0
        self.__draw_size = draw_size
        self.__choosenPlayer = choosenPlayer

    def getParentState(self):
        return self.__parent_state

    def getParentAction(self):
        return self.__parent_action

    def getParentExpectation(self):
        return self.__parent_expectation

    def getCurrentState(self):
        return self.__current_state

    def getCurrentAction(self):
        return self.__current_action

    def getCurrentExpectation(self):
        return self.__current_expectation

    def setCurrentExpectation(self, new_expectation):
        self.__current_expectation = new_expectation

    def getDrawSize(self):
        return self.__draw_size

    def getChoosenPlayer(self):
        return self.__choosenPlayer
