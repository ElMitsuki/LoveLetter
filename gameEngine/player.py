import time

class Player:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._hand = []
        self._discard = []
        self._score = 0
        self._is_knocked_out = False
        self._is_immune = False
        self._version = "Player"
    
    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getHand(self):
        return self._hand
    def setHand(self, hand):
        self._hand = hand

    def getDiscard(self):
        return self._discard
    def setDiscard(self,discard):
        self._discard=discard

    def getScore(self):
        return self._score
    def setScore(self, score):
        self._score = score

    def getIsKnockedOut(self):
        return self._knocked_out
    def setIsKnockedOut(self, state):
        self._knocked_out = state
    
    def getIsImmune(self):
        return self._is_immune
    def setIsImmune(self, state):
        self._is_immune = state

    def getVersion(self):
        return self._version

    def draw(self, draw, renderer, hide=False):
        """Draw a card and put it in player's hand

        Keyword arguments:
        draw -- the draw stack of the game
        """
        card=draw.pop(0)
        if not renderer.getSimuMod():
            renderer.draw(self._id, card.getName() if not hide else "back", len(self._hand), hide)
        self._hand.append(card)

    def playCard(self, game):
        """Play a card and use its power
        
        Keywords arguments:
        game -- current game
        """
        choosen_card = None
        king_or_prince = False
        countess = False
        card_index = 0
        opponent = game.getPlayers()[0] if game.getPlayers()[0]._id != self._id else game.getPlayers()[1]
        for card in self._hand:
            king_or_prince = card.getName() == "King" or card.getName() == "Prince" if not king_or_prince else king_or_prince
            if card.getName() == "Countess":
                countess = True
                choosen_card = card_index
            card_index += 1
        if not king_or_prince or not countess:
            choosen_card = self._chooseCard(game)
        else :
            time.sleep(1)
            if not game.getRenderer().getSimuMod():
                game.getRenderer().removeCardHand(self._id, choosen_card, len(self._hand))
        
        choosen_card = self._hand.pop(choosen_card)
        y = 537 if self._id != opponent._id else 179
        if not game.getRenderer().getSimuMod():
            if game.getRenderer().getOneSide():
                if game.getRenderer().getOneSide():
                    if callable(getattr(self, "getSpecial", None)):
                        y = 179
                    else:
                        y = 537
            game.getRenderer().updateDiscard(choosen_card.getName(), self._id, len(self._discard), y)
        self._discard.append(choosen_card)
        if callable(getattr(opponent, "updateRemainingCards", None)):
            opponent.updateRemainingCards([choosen_card])
        choosen_card.discardAction(self, game.getDraw(), game.getPlayers(), game.getQ(), game.getRenderer())

    def _chooseCard(self, game):
        """Ask a card to play

        Return : index of card
        """
        if not game.getRenderer().getSimuMod():
            game.getRenderer().chooseCard(self)
        ret = game.getQ().get()
        game.getQ().task_done()
        game.getQ().join()
        return ret

    def discardCard(self, draw, current_player_id, players, q, renderer):
        """Force to discard
        
        Keywords arguments:
        draw -- the draw stack of game
        players -- players in game
        """
        card = self._hand.pop(0)
        if not renderer.getSimuMod():
            renderer.removeCardHand(self._id, 0, len(self._hand))
            y = 537 if current_player_id == self._id else 179
            if renderer.getOneSide():
                if renderer.getOneSide():
                    if callable(getattr(self, "getSpecial", None)):
                        y = 179
                    else:
                        y=537
            renderer.updateDiscard(card.getName(), self._id, len(self._discard), y)
        self._discard.append(card)
        opponent = players[0] if players[0].getId() != self._id else players[1]
        if card.getValue() == 8 :
            card.discardAction(self, draw, players, q, renderer)
        if callable(getattr(opponent, "updateRemainingCards", None)):
            opponent.updateRemainingCards([card])
        
    def calcTie(self):
        """Calculate points in case of tie
        
        Return : result
        """
        res = 0
        for card in self._discard:
            res += card.getValue()
        return res

    def __findCard(self, num):
        """Find index of a card in player hand thanks to it num
        
        Keyword arguments:
        num -- num of a Card

        Return : index of Card or None
        """
        for card_index, card in enumerate(self._hand):
            if num == card.getValue():
                return card_index
        return False
