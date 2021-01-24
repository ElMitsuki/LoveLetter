from .card import Card

"""
Class that represents the handmaid card of love letters and inherits the class Card.
"""
class Handmaid(Card):

    """
    Constructor of class Handmaid that calls the constructor of Card.
    """
    def __init__(self):
        super().__init__(4, "Handmaid")

    """This method implements the discardAction method of Card and applies the effect of the Handmaid card.
    The effect of this card is to immunize the player against the effect of cards from other players.
    
    Parameters inherited from Card:
    - player : the player that discarded the card.
    - draw : the draw list of the game because some cards need it to apply their effects like the prince.
    - players : the list of all the players of the game because some cards need it to apply their effects like the king.
    """
    def discardAction(self, player, draw, players,q, renderer):
        if not renderer.getSimuMod():
            renderer.displayMessage(["{0} est immunisé".format(player.getName())])
        player.setIsImmune(True)
