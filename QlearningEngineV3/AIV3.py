import math
import random
import time
from gameEngine.player import Player
from QlearningEngineV3.node import Node
from QlearningEngineV3.Qfunction import setNodeExpectation, updateQTable

class AIV3(Player):

    def __init__(self, id, exploration_coeff):
        super().__init__(id, "IAv3")
        self.__memorized_opponent_card = None
        self.__previous_node = None
        self.__special = None
        self.__exploration_coeff = exploration_coeff
        self.__remaining_cards = [5,2,2,2,2,1,1,1]
        self.__probas = [0,0,0,0,0,0,0,0]
        self._version = "AIv3"
    
    def getSpecial(self):
        return self.__special
    
    def draw(self, draw, renderer, hide=False):
        """Same of player draw but counts remainging cards

        draw = list of cards
        """
        drawn_card = draw.pop(0)
        if not renderer.getSimuMod():
            renderer.draw(self._id, "back", len(self._hand), True)
        self._hand.append(drawn_card)
        self.__remaining_cards[drawn_card.getValue()-1]-=1

    def setMemorizedOpponentCard(self, card_value):
        self.__memorized_opponent_card = card_value

    def updateRemainingCards(self, discard):
        """Update remainging unkonwn cards in game

        discard = list of cards
        """
        for card in discard:
            self.__remaining_cards[card.getValue()-1]-=1
        self.__updateProba()

    def __updateProba(self):
        """Update probabilities of what card can has the opponent
        """
        nb_cards = 0
        for remaining_card in self.__remaining_cards:
            nb_cards+=remaining_card
        if nb_cards != 0:
            index_proba = 0
            for remaining_card in self.__remaining_cards:
                if remaining_card != 0:
                    self.__probas[index_proba] = remaining_card/nb_cards
                index_proba+=1

    def forgetOpponentCard(self, opponent_discard):
        """Check if memorized card was played.

        opponent_discard = opponent discard
        """
        self.__memorized_opponent_card = None if opponent_discard[len(opponent_discard)-1] == self.__memorized_opponent_card else self.__memorized_opponent_card

    def _chooseCard(self, game):
        """Choose a card to play thanks to Q-Learning.

        game = game object

        Return : index of card to play
        """
        self.__special = None
        choosen_card = None
        opponent = game.getPlayers()[1] if game.getPlayers()[0].getId() == self._id else game.getPlayers()[0]
        if len(opponent.getDiscard()) != 0:
            self.forgetOpponentCard(opponent.getDiscard())
        nodes=[]
        have_princess = self.__playPrincess()
        if have_princess:
            choosen_card = 1 if self._hand[0].getValue() == 8 else 0
            if self._hand[choosen_card].getValue() == 5 :
                self.__special = opponent._id
        else:
            for card in self._hand:
                node = None
                if(self.__previous_node != None):
                    if card.getValue() == 5:
                        node = Node(self.__previous_node.getCurrentState().getCard1(), self.__previous_node.getCurrentState().getCard2(), self.__previous_node.getCurrentAction(), self.__previous_node.getCurrentExpectation(), self._hand[0].getValue(), self._hand[1].getValue(), card.getValue(), len(game.getDraw()), False)
                        setNodeExpectation(node)
                        nodes.append(node)
                        node = Node(self.__previous_node.getCurrentState().getCard1(), self.__previous_node.getCurrentState().getCard2(), self.__previous_node.getCurrentAction(), self.__previous_node.getCurrentExpectation(), self._hand[0].getValue(), self._hand[1].getValue(), card.getValue(), len(game.getDraw()), True)
                    else:
                        node = Node(self.__previous_node.getCurrentState().getCard1(), self.__previous_node.getCurrentState().getCard2(), self.__previous_node.getCurrentAction(), self.__previous_node.getCurrentExpectation(), self._hand[0].getValue(), self._hand[1].getValue(), card.getValue(), len(game.getDraw()), None)
                else:
                    if card.getValue() == 5:
                        node = Node(None, None, None, None, self._hand[0].getValue(), self._hand[1].getValue(), card.getValue(), len(game.getDraw()), False)
                        setNodeExpectation(node)
                        nodes.append(node)
                        node = Node(None, None, None, None, self._hand[0].getValue(), self._hand[1].getValue(), card.getValue(), len(game.getDraw()), True)
                    else:
                        node = Node(None, None, None, None, self._hand[0].getValue(), self._hand[1].getValue(), card.getValue(), len(game.getDraw()), None)
                setNodeExpectation(node)
                nodes.append(node)
                    
            choosen_card = self.__instaPlay(opponent, have_princess)
            choosen_node = None
            if self.__exploration_coeff > random.random():
                choosen_card = 0 if self._hand[random.randint(0,1)].getValue() == self._hand[0].getValue() else 1
            elif choosen_card == -1:
                if len(nodes) > 2:
                    real_prince_expectation = 0
                    prince_nodes=[]
                    other_node = None
                    for node in nodes:
                        if node.getCurrentAction() == 5:
                            real_prince_expectation+=node.getCurrentExpectation()
                            prince_nodes.append(node)
                        else:
                            other_node = node
                    if other_node != None and other_node.getCurrentExpectation() > real_prince_expectation:
                        choosen_node = other_node
                    else:
                        for prince_node in prince_nodes:
                            if choosen_node == None or choosen_node.getCurrentExpectation() < prince_node.getCurrentExpectation():
                                choosen_node = prince_node
                    choosen_card = 0 if choosen_node.getCurrentAction() == self._hand[0].getValue() else 1
                else:
                    for node in nodes:
                        if(choosen_node == None or choosen_node.getCurrentExpectation() < node.getCurrentExpectation()):
                            choosen_node = node
                            choosen_card = 0 if node.getCurrentAction() == self._hand[0].getValue() else 1
            if choosen_node is None:
                if len(nodes) == 1:
                    choosen_node = nodes[0]
                else:
                    if self._hand[choosen_card].getValue() == 5:
                        if nodes[0].getCurrentAction() == 5 :
                            choosen_node = nodes[random.randint(0,1)]
                        else:
                            choosen_node = nodes[random.randint(1,2)]
                    else:
                        if len(nodes) == 3:
                            choosen_node = nodes[0] if nodes[0].getCurrentAction() != 5 else nodes[2]
                        else:
                            choosen_node = nodes[0] if nodes[0].getCurrentAction() == self._hand[choosen_card].getValue() else nodes[1]
            if(self.__previous_node != None):
                updateQTable(choosen_node, 0)
            self.__previous_node = choosen_node
            self.__chooseSpecial(choosen_node, opponent)
        time.sleep(1)
        if not game.getRenderer().getSimuMod():
            game.getRenderer().removeCardHand(self._id, 0, len(self._hand))
        return choosen_card

    def __chooseSpecial(self, choosen_node, opponent):
        """Ai choose how to play prince and guard

        choosen_node = choosen node by Qlearning
        """
        if choosen_node.getCurrentAction() == 1 and self.__special == None:
            best_proba = 0
            card_value = 1
            equality = True
            value_remaining_cards=[]
            for proba in self.__probas:
                if proba != 0 and card_value != 1:
                    if best_proba != proba:
                        equality = False
                    value_remaining_cards.append(card_value)
                if best_proba < proba and card_value != 1:
                    best_proba = proba
                    self.__special = card_value
                card_value+=1
            if equality :
                self.__special = value_remaining_cards[0 if len(value_remaining_cards) == 1 else random.randint(0, len(value_remaining_cards)-1)]
            if best_proba == 0:
                self.__special = 2
        elif choosen_node.getCurrentAction() == 5 and self.__special == None:
            self.__special= self._id if choosen_node.getChoosenPlayer() else opponent._id


    def lastUpdate(self, r):
        """Update reward of last node

        r = rewards of last node
        """
        if self.__previous_node != None:
            updateQTable(self.__previous_node, r)

    def __instaPlay(self, opponent, have_princess):
        """Check if a the A.I can instant play

        return = card choose if A.I can else -1
        """
        have_guard = False
        have_baron = False
        have_prince = False
        for card in self._hand:
            have_guard = False if not have_guard and card.getValue() != 1 else True
            have_baron = False if not have_baron and card.getValue() != 3 else True
            have_prince = False if not have_prince and card.getValue() != 5 else True
        if self.__memorized_opponent_card != None and not opponent.getIsImmune():
            if have_guard and self.__memorized_opponent_card > 1:
                self.__special = self.__memorized_opponent_card
                return 0 if self._hand[0].getValue() == 1 else 1
            if have_baron :
                if self._hand[0].getValue() == 3 and self.__memorized_opponent_card < self._hand[1].getValue():
                    return 0
                elif self._hand[1].getValue() == 3 and self.__memorized_opponent_card < self._hand[0].getValue():
                    return 1
            if have_prince:
                other_card_value = self._hand[0].getValue() if self._hand[1].getValue() == 5 else self._hand[1].getValue()
                if self.__memorized_opponent_card == 8 or have_princess or other_card_value >= 5:
                    self.__special = 1 if self._id == 2 else 2
                return 0 if self._hand[0].getValue() == 1 else 1
        return -1

    def __playPrincess(self):
        """Check if a the A.I can play princess

        return = have_princess
        """
        have_princess = False
        for card in self._hand:
            have_princess = False if not have_princess and card.getValue() != 8 else True
        return have_princess
