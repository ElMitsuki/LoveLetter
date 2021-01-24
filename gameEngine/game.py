import random, threading, time
from .player import Player
from .prince import Prince
from .princess import Princess
from .countess import Countess
from .guard import Guard
from .baron import Baron
from .priest import Priest
from .handmaid import Handmaid
from .king import King
from QlearningEngineV3.AIV3 import AIV3
from QlearningEngineV1.AIV1 import AIV1
from QlearningEngineV3.io import DBAccess

db = DBAccess()

class Game(threading.Thread):

    """
    Class representing a game of two players.
    """

    def __init__(self,renderer,q):
        threading.Thread.__init__(self)
        self.daemon=True
        self.__q=q
        self.__draw = []
        self.__players = []
        self.__discard = []
        self.__renderer=renderer
        self.__nb_simulation = 1
        self.learning = 0
        self.start()

    def getQ(self):
        return self.__q
    def getDraw(self):
        return self.__draw
    def getPlayers(self):
        return self.__players
    def getDiscard(self):
        return self.__discard
    def getRenderer(self):
        return self.__renderer

    def run(self):
        """Starts and play a game of two player."""
        infos=self.__q.get()
        self.__q.task_done()
        self.__q.join()
        num_player=1
        self.__nb_simulation = 1
        self.__renderer.setOneSide(infos[0][1] == 0 and infos[1][1] == 1 or infos[0][1] == 1 and infos[1][1] == 0)
        for info in infos:
            if info[1] == 0:
                self.__players.append(Player(num_player,info[0]))
            else:
                if info[2] == 1:
                    self.__players.append(AIV3(num_player,0))
                else:
                    self.__players.append(AIV1(num_player,0))
            num_player+=1
        #if(infos[0][2] == 1 or infos[1][2] == 1):
        #    self.__renderer.askNbSimu()
        #    self.__nb_simulation = int(self.__q.get())
        #    self.__q.task_done()
        #    self.__q.join()
        random.shuffle(self.__players)
        if not self.__renderer.getSimuMod():
            self.__renderer.displayMessage(["{0} commence !".format(self.__players[0].getName())])
        while self.__nb_simulation > 0:
            if self.__renderer.getSimuMod():
                self.__renderer.showNbSimu(self.__nb_simulation)
            while (self.__players[0].getScore() != 7 and self.__players[1].getScore() != 7):
                self.initRound()
                while not self.endRoundCondition():
                    self.turn()
                self.endRound()
            winner = self.__players[1]
            looser = self.__players[0]
            if (self.__players[0].getScore() == 7):    
                winner = self.__players[0]
                looser = self.__players[1]
            if (callable(getattr(self.__players[0], "lastUpdate", None)) or callable(getattr(self.__players[1], "lastUpdate", None))) and self.learning == 0:
                db.incrementStat(winner, looser, False)
            else:
                if not self.__renderer.getSimuMod():
                    self.__renderer.displayMessage(["{0} a gagné !".format(self.__players[1].getName())])
            self.__players[0].setScore(0)
            self.__players[1].setScore(0)
            self.__nb_simulation-=1
        self.__renderer.end()
    
    def turn(self):
        """Play a turn, meaning both player play a card."""
        for player in self.__players:
            if (not self.endRoundCondition()):
                if not self.__renderer.getSimuMod():
                    self.__renderer.swapPlayer(player.getName())
                player.setIsImmune(False)
                player.draw(self.__draw, self.__renderer)
                player.playCard(self)
                if not self.__renderer.getSimuMod():
                    self.__renderer.initTurn(self.__players, player, self.__draw)

    def initRound(self):
        """Initializes __draw, __discard, player's hands and boolean's __players status for a new round."""
        #self.__renderer.displayMessage(["Nouveau round"])
        self.__draw = [Princess(), Countess(), King(), Prince(), Prince(), Handmaid(), Handmaid(), 
            Baron(), Baron(), Priest(), Priest(), Guard(), Guard(), Guard(), Guard(), Guard()]
        random.shuffle(self.__draw)
        self.__discard = [self.__draw.pop(0), self.__draw.pop(0), self.__draw.pop(0)]
        self.swapPlayersOrder()
        if not self.__renderer.getSimuMod():
            self.__renderer.initRound(self.__draw, self.__discard, self.__players)
        p=0
        for player in self.__players:
            hide = False if p == 0 else True
            player.setHand([])
            player.setDiscard([])
            player.setIsImmune(False)
            player.setIsKnockedOut(False)
            if callable(getattr(player, "setMemorizedOpponentCard", None)):
                player.setMemorizedOpponentCard(None)
                player.updateRemainingCards(self.__discard)
            if not self.__renderer.getSimuMod():
                if self.__renderer.getOneSide() and not callable(getattr(player,"getSpecial",None)):
                    hide = False
            player.draw(self.__draw, self.__renderer, hide)
            p+=1

    def endRoundCondition(self):
        """Return True if the conditions to finish the round if the conditions are gathered.""" 
        for player in self.__players:
            if player.getIsKnockedOut():
                return True
        if not self.__draw:
            return True
        return False
    
    def endRound(self):
        """To call at the end of a round, determine the winner and set his score.""" 
        winner = self.__players[0]
        looser = self.__players[1]
        if (self.__players[1].getIsKnockedOut() or self.__players[0].getHand()[0].getValue() > self.__players[1].getHand()[0].getValue() and not self.__players[0].getIsKnockedOut()):
            self.__players[0].setScore(self.__players[0].getScore() + 1)
        elif (self.__players[0].getIsKnockedOut() or self.__players[1].getHand()[0].getValue() > self.__players[0].getHand()[0].getValue() and not self.__players[1].getIsKnockedOut()):
            self.__players[1].setScore(self.__players[1].getScore() + 1)
            winner = self.__players[1]
            looser = self.__players[0]
        elif (self.__players[1].calcTie() > self.__players[0].calcTie()):
            self.__players[1].setScore(self.__players[1].getScore() + 1)
            winner = self.__players[1]
            looser = self.__players[0]
        if callable(getattr(winner, "lastUpdate", None)):
            winner.lastUpdate(1)
        if callable(getattr(looser, "lastUpdate", None)):
            looser.lastUpdate(-1)
        if (callable(getattr(self.__players[0], "lastUpdate", None)) or callable(getattr(self.__players[1], "lastUpdate", None))) and self.learning == 0:
            db.incrementStat(winner, looser, True)
        if not self.__renderer.getSimuMod():
            self.__renderer.displayMessage(["{0} a gagné le round !".format(winner.getName()),
                                            "Scores :\n{0} : {1}\n{2} : {3}".format(self.__players[0].getName(), self.__players[0].getScore(),
                                                                                    self.__players[1].getName(), self.__players[1].getScore())])
    def swapPlayersOrder(self):
        """Swap the order of the players in the list of players to make them play first alternately.
        Swap only if it is not the first round.
        """ 
        if self.__players[0].getScore() != 0 or self.__players[1].getScore() != 0:
            tmp_player = self.__players[0]
            self.__players[0] = self.__players[1]
            self.__players[1] = tmp_player
