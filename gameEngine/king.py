from .card import Card

"""
Class that represents the king card of love letters and inherits the class Card.
"""
class King(Card):

    """
    Constructor of class King that calls the constructor of Card.
    """
    def __init__(self):
        super().__init__(6, "King")

    """This method implements the discardAction method of Card and applies the effect of the King card.
    The effect of this card is to allow the player to choose another player who's not immunize and to swap hand.
    
    Parameters inherited from Card:
    - player : the player that discarded the card.
    - draw : the draw list of the game because some cards need it to apply their effects like the prince.
    - players : the list of all the players of the game because some cards need it to apply their effects like the king.
    """
    def discardAction(self, player, draw, players,q, renderer):
        players = players
        opponent = None

        for p in players:
            if (p.getId() != player.getId()) and (p.getIsImmune() is False):
                opponent = p

        if opponent is not None:
            if callable(getattr(player, "setMemorizedOpponentCard", None)):
                player.setMemorizedOpponentCard(player.getHand()[0]._value)
            elif callable(getattr(opponent, "setMemorizedOpponentCard", None)):
                opponent.setMemorizedOpponentCard(opponent.getHand()[0]._value) 
            tmp = opponent.getHand()[0]
            opponent.getHand()[0] = player.getHand()[0]
            player.getHand()[0] = tmp
