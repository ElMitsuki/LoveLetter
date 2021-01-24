from .card import Card

"""
Class that represents the countess card of love letters and inherits the class Card.
"""
class Countess(Card):

    """
    Constructor of class Countess that calls the constructor of Card.
    """
    def __init__(self):
        super().__init__(7, "Countess")

    """This method implements the discardAction method of Card.
    It doesn't apply any effect because the effect of the Countess is apply when the player draw the card and not when he discards it.

    Parameters inherited from Card:
    - player : the player that discarded the card.
    - draw : the draw list of the game because some cards need it to apply their effects like the prince.
    - players : the list of all the players of the game because some cards need it to apply their effects like the king.
    """
    def discardAction(self, player, draw, players,q, renderer):
        pass
