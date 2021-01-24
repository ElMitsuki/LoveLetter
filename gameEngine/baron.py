from .card import Card

class Baron(Card):
      
      def __init__(self):
        super().__init__(3, "Baron")

      
      def getOpponent(self,player, players):
        """Find the opponent.

        Keyword arguments:
        player -- the current player

        """
        return players[0] if players[0].getId() != player.getId() else players[1]
      
      
      def discardAction(self, player, draw, players,q, renderer):
        """Check if the opponnentCard is higher than the current playerCard.
        Then CHEH

        Keyword arguments:
        player -- the current player

        """  
        opponent = self.getOpponent(player, players)
        opponentCard = opponent.getHand()[0]
        if opponent.getIsImmune() == False :
            if not renderer.getSimuMod():
              if callable(getattr(player, "getSpecial", None)):
                renderer.showCard(player.getId(), player.getHand()[0]._name)
              else:
                renderer.showCard(opponent.getId(), opponentCard._name)
            if  opponentCard._value < player.getHand()[0]._value :
                opponent.setIsKnockedOut(True)
                if not renderer.getSimuMod():
                  renderer.displayMessage([f"{player.getName()} a la carte  {player.getHand()[0]._name}",f"{opponent.getName()} a la carte  {opponentCard._name}",f"{player.getName()} gagne le duel !"])
            elif opponentCard._value > player.getHand()[0]._value :
                player.setIsKnockedOut(True)
                if not renderer.getSimuMod():
                  renderer.displayMessage([f"{player.getName()} a la carte  {player.getHand()[0]._name}",f"{opponent.getName()} a la carte  {opponentCard._name} ",f"{opponent.getName()} gagne le duel !"])
            else :
              if not renderer.getSimuMod():
                renderer.displayMessage([f"{player.getName()} a la carte  {player.getHand()[0]._name}",f"{opponent.getName()} a la carte  {opponentCard._name}",f"Ouch, les deux joueurs ont la même carte..."])
              if callable(getattr(player, "setMemorizedOpponentCard", None)):
                player.setMemorizedOpponentCard(opponentCard._value)
              elif callable(getattr(opponent, "setMemorizedOpponentCard", None)):
                opponent.setMemorizedOpponentCard(player.getHand()[0]._value) 
        else :
          if not renderer.getSimuMod():
            renderer.displayMessage(["Votre adversaire est immunisé !"])
