from .card import Card
from .input import input_int

class Guard(Card):
      
  def __init__(self):
    super().__init__(1, "Guard")

  
  def getOpponent(self, player, players):
    """Find the opponent.

    Keyword arguments:
    player -- the current player

      """
    return players[0] if players[0].getId() != player.getId() else players[1]
      
      
  def discardAction(self, player, draw, players,q, renderer):
    """Ask to the current player to try to find the oppenent card. If he success, the opponent is knocked out.

    Keyword arguments:
    player -- the current player

        """
    opponent = self.getOpponent(player, players)
    opponentCard = opponent.getHand()[0]
    if opponent.getIsImmune() == False :
      if(callable(getattr(player, "getSpecial", None))):
        guessedOppenentCard = player.getSpecial()
      else:
        renderer.askCard()
        guessedOppenentCard=q.get()
        q.task_done()
        q.join()
      if ( opponentCard._value == guessedOppenentCard ) :
        opponent.setIsKnockedOut(True)
        if not renderer.getSimuMod():
          renderer.displayMessage(['Bravo, c\'est la bonne carte ! '])
      else :
        if not renderer.getSimuMod():
          renderer.displayMessage(['Dommage ... ce n\'est pas la bonne carte ! '])
    else:
      if not renderer.getSimuMod():
        renderer.displayMessage(["Votre adversaire est immunisé !"])
