from .card import Card

class Priest(Card):
      
      def __init__(self):
        super().__init__(2, "Priest")

      
      def getOpponent(self, player, players):
        """Find the opponent.

        Keyword arguments:
        player -- the current player

        """
        return players[0] if players[0].getId() != player.getId() else players[1]  
      
      
      def discardAction(self, player, draw, players,q, renderer):
        """Give the name and the value of the opponent card.

        Keyword arguments:
        player -- the current player

        """  
        opponent = self.getOpponent(player, players)
        opponentCard = opponent.getHand()[0]
        if opponent.getIsImmune() == False :
          if callable(getattr(player, "setMemorizedOpponentCard", None)):
              player.setMemorizedOpponentCard(opponentCard._value)
          else:
            if not renderer.getSimuMod():
              renderer.showCard(opponent.getId(),opponentCard._name)
        else :
          if not renderer.getSimuMod():
            renderer.displayMessage(["Votre adversaire est immunisé !"])
