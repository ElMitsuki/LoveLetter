from .card import Card

class Princess(Card):
      
      def __init__(self):
        super().__init__(8, "Princess")

    
      def discardAction(self, player, draw, players,q, renderer):
        """Knock out the current player.
    
        Keyword arguments:
        player -- the current player

        """
        if not renderer.getSimuMod():
          renderer.displayMessage(['La princesse est posée ... Vous perdez la manche !'])  
        player.setIsKnockedOut(True)
