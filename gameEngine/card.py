from abc import ABC, abstractmethod

"""
Abstract class that represents a template for all the cards of the game.
"""
class Card(ABC):

    """Constructor of class Card.
    Parameters :
    - value : the value of a card which represents it's power. The higher the value, the better it is (from 1 to 8).
    - name : the name of the card which can be : Countess, Handmaid, King, Prince, Princess, Priest, Guard or Baron.
    """
    def __init__(self, value, name):
        self._value = value
        self._name = name

    """Return the value of the card.
    """
    def getValue(self):
        return self._value

    """Change the value of the card with the value given in parameter.
    Parameter :
    - v : the new value.
    """
    def setValue(self, v):
        self._value = v

    """Return the name of the card.
    """
    def getName(self):
        return self._name

    """Change the name of the card with the name given in parameter.
    Parameter :
    - n : the new name.
    """
    def setName(self, n):
        self._name = n

    """Abstract method that will be implemented by the cards.
    This method applies the effect of a card when it is discarded.
    Parameters :
    - player : the player that discarded the card.
    - draw : the draw list of the game because some cards need it to apply their effects like the prince.
    - players : the list of all the players of the game because some cards need it to apply their effects like the king.
    """
    @abstractmethod
    def discardAction(self, player, draw, players,q, renderer):
        pass
