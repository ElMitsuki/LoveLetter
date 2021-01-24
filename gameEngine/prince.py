from .card import Card
from .input import input_int
import time

"""
Class that represents the prince card of love letters and inherits the class Card.
"""
class Prince(Card):

    """
    Constructor of class Prince that calls the constructor of Card.
    """
    def __init__(self):
        super().__init__(5, "Prince")

    """This method implements the discardAction method of Card and applies the effect of the Prince card.
    The effect ot this card is to allow the player to choose a player (including himself) who's not immunize
    and make this player discard his hand and draw a new card.
    
    Parameters inherited from Card:
    - player : the player that discarded the card.
    - draw : the draw list of the game because some cards need it to apply their effects like the prince.
    - players : the list of all the players of the game because some cards need it to apply their effects like the king.
    """
    def discardAction(self, player, draw, players,q, renderer):
        if len(draw) > 0:
            if(callable(getattr(player, "getSpecial", None))):
                id = player.getSpecial()
                choosen_player = 0 if players[0].getId() == id else 1
            else:
                if not renderer.getSimuMod():
                    time.sleep(0.2)
                    renderer.askPlayer(players)
                choosen_player=q.get()
                q.task_done()
                q.join()
            if players[choosen_player].getIsImmune():
                if not renderer.getSimuMod():
                    renderer.displayMessage(["Votre adversaire est immunisé... dommage !"])
            elif not players[choosen_player].getHand():
                if not renderer.getSimuMod():
                    renderer.displayMessage(["Le joueur choisi n'a plus de carte en main... dommage !"])
            else:
                choosen_player = players[choosen_player]
                choosen_player.discardCard(draw, player.getId(), players, q, renderer)
                if choosen_player.getId() != player.getId():
                    if(callable(getattr(player, "forgetOpponentCard", None))):
                        player.forgetOpponentCard(choosen_player.getDiscard())
                if(callable(getattr(player, "forgetOpponentCard", None))) and renderer.getOneSide():
                    choosen_player.draw(draw, renderer, False)
                else:
                    choosen_player.draw(draw, renderer, False if choosen_player == player else True)
