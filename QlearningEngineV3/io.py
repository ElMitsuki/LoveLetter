import sqlite3 
from .exceptionDB import log, create_logger

class DBAccess:
    
    active_log = False
    logger = create_logger

    def __init__(self, file='QlearningEngineV3/db/data.db'):
        """The constructor initializes the path to the database and the different names
        to use to access the data.
        """
        self.__db_file = file
        # Expectation table
        self.__Qlearning_table = 'Qlearning'
        self.__card1_col = 'card1'
        self.__card2_col = 'card2'
        self.__action_col = 'action'
        self.__prince_col = 'prince_targets_AI'
        self.__draw_col = 'draw_size'
        self.__expectation_col = 'expectation'

        # Statistics table
        self.__stat_table = 'statistics'
        self.__agent1_col = 'agent1'
        self.__agent2_col = 'agent2'
        self.__winner_col = 'winner'
        self.__rounds_col = 'rounds_won'
        self.__games_col = 'games_won'

        # Journal mode
        self.__journal_mode = "OFF"
  
    @log(active_log, logger)
    def initialize(self):
        """Initializes QLearning and Statistics tables. 
        """
        self.initializeQlearningTable()
        self.initializeStatTable()

    @log(active_log, logger)
    def initializeQlearningTable(self):
        """Initializes or reinitializes the expectation table with all expectation with a value of 0.
        """
        self.__open()
        expectation_table = self.__cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'".format(self.__Qlearning_table)) 
        if not expectation_table.fetchone():
            self.__createQlearningTable()
        else:
            self.__resetQlearningTable()
        self.__close()
    
    @log(active_log, logger)
    def initializeStatTable(self):
        """Initializes or reinitializes the statistic table with numbers of rounds and games won set to 0.
        """
        self.__open()
        stat_table = self.__cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'".format(self.__stat_table)) 
        if not stat_table.fetchone():
            self.__createStatTable()
        else:
            self.__resetStatTable()
        self.__close()

    @log(active_log, logger)
    def __open(self):
        """Open a connection with the database setting a connection variable and a cursor variable
        belonging to the class.
        """
        self.__connection = sqlite3.connect(self.__db_file) 
        self.__connection.execute("PRAGMA journal_mode = {0}".format(self.__journal_mode))
        self.__cursor = self.__connection.cursor() 
    
    @log(active_log, logger)
    def __close(self):
        """Close the connection.
        """
        self.__connection.close()

    @log(active_log, logger)
    def getExpectation(self, state, action, draw_size, prince_targets_AI = None):
        """Returns an expectation value of a specific row of the Qlearning table.

        Keyword arguments:
        state = object state wich contains two card values.
        action = value of the card played.
        draw_size = number of remaining cards in the draw.
        prince_targets_AI = boolean parameter set in case of prince played.
            set to True if the prince target the AI and False otherwise.

        """
        self.__open()
        query = "SELECT {0} FROM {1} WHERE {2} = {3} AND {4} = {5} AND {6} = {7} AND {8} = {9}".format(
            self.__expectation_col, self.__Qlearning_table, self.__card1_col, state.getCard1(), 
            self.__card2_col, state.getCard2(), self.__action_col, action, self.__draw_col, draw_size) 
        if prince_targets_AI is not None:
            query += " AND {0} = {1}".format(self.__prince_col, self.__setTargetPrince(prince_targets_AI)) 
        else:
            query += " AND {0} IS {1}".format(self.__prince_col, self.__setTargetPrince(prince_targets_AI)) 
        self.__cursor.execute(query)
        expectation = self.__cursor.fetchone()[0]
        self.__close()
        return expectation

    @log(active_log, logger)
    def updateExpectation(self, state, action, draw_size, expectation, prince_targets_AI = None):
        """update the expectation in the Qlearning table for a specific row.

        Keyword arguments:
        state = object state wich contains two card values.
        action = value of the card played.
        draw_size = number of remaining cards in the draw.
        expecation = value of the expectation to update for the state and action.
        prince_targets_sAI = boolean parameter set in case of prince played.
            set to True if the prince target the AI and False otherwise.

        """
        self.__open()
        query = "UPDATE {0} SET {1} = {2} WHERE {3} = {4} AND {5} = {6} AND {7} = {8} AND {9} = {10}".format(
            self.__Qlearning_table, self.__expectation_col, expectation, self.__card1_col, state.getCard1(), 
            self.__card2_col, state.getCard2(), self.__action_col, action, self.__draw_col, draw_size)
        if prince_targets_AI is not None:
            query += " AND {0} = {1}".format(self.__prince_col, self.__setTargetPrince(prince_targets_AI)) 
        else:
            query += " AND {0} IS {1}".format(self.__prince_col, self.__setTargetPrince(prince_targets_AI))
        self.__cursor.execute(query)
        self.__connection.commit()
        self.__close()

    
    @log(active_log, logger)
    def incrementStat(self, winner, looser, increment_round = True):
        """Increment the number of won rounds in the statistics table considering a winner and a looser and 
        what is the statistics to increment.

        Keyword arguments:
        winner = object (Player or AI) representing the winner.
        looser = object (Player or AI) representing the looser.
        increment_round = boolean which indicate if the number of round is the statistic to update,
            if false, the number of games won is the statistic to update.

        """
        stat_to_increment = self.__games_col
        if increment_round:
            stat_to_increment = self.__rounds_col
        winner_col = winner.getVersion()
        agent1, agent2 = self.defineAgentOrder(winner, looser)

        self.__open()
        stat_request = self.__cursor.execute("SELECT {0} FROM {1} WHERE {2}='{3}' AND {4} = '{5}' AND {6} = '{7}'".format(
            stat_to_increment, self.__stat_table, self.__agent1_col, agent1, self.__agent2_col, agent2, self.__winner_col, winner_col))
        stat = 0
        fetch = stat_request.fetchone()
        if not fetch:
            query = "INSERT INTO {0} ({1},{2},{3},{4},{5}) VALUES ('{6}','{7}','{8}',0,0)".format(
                self.__stat_table, self.__agent1_col, self.__agent2_col, self.__winner_col, self.__rounds_col, 
                self.__games_col, agent1, agent2, winner_col)
            self.__cursor.execute(query)
        else:
            stat = fetch[0]
        query = "UPDATE {0} SET {1} = {2} WHERE {3}='{4}' AND {5} = '{6}' AND {7} = '{8}'".format(
            self.__stat_table, stat_to_increment, stat + 1, self.__agent1_col, agent1, 
            self.__agent2_col, agent2, self.__winner_col, winner_col)
        self.__cursor.execute(query)
        self.__connection.commit()
        self.__close()

    def defineAgentOrder(self, agent1, agent2):
        """Return two string corresponding to the two agents in parameter.
        The return order depend of the order in which you want to encounter them in the statistic table.
        (first column as agent1 or second as agent two). Arbitrarily set as AI before player and old AI version
        before newer.

        Keyword arguments:
        agent1 = The first agent to return the string for.
        agent2 = The second agent to return the string for.

        """
        agent1_col = agent1.getVersion()
        agent2_col = agent2.getVersion()
        if (agent1_col == "AIv1") or (agent1_col == "AIv3" and agent2_col == "Player"):
            return agent1_col, agent2_col
        if (agent2_col == "AIv1") or (agent2_col == "AIv3" and agent1_col == "Player"):
            return agent2_col, agent1_col

    @log(active_log, logger)
    def __createQlearningTable(self):
        """Creates the table with all expectation set to 0.
        """
        query = "CREATE TABLE {0}({1} TINYINT UNSIGNED,{2} TINYINT UNSIGNED,{3} TINYINT UNSIGNED,".format(
            self.__Qlearning_table, self.__card1_col, self.__card2_col, self.__action_col)
        query += " {0} BOOLEAN, {1} TINYINT UNSIGNED,{2} FLOAT)".format(
            self.__prince_col , self.__draw_col, self.__expectation_col)
        self.__cursor.execute(query) 
        for value_first_card in range(1,8):
            for value_second_card in range(value_first_card, 8):
                if (value_first_card < 6) or (value_first_card >= 6 and value_first_card != value_second_card):
                    if not(value_first_card == 6 and value_second_card == 7) and not(
                            value_first_card == 5 and value_second_card == 7):
                        for draw_size in range(0, 11):  
                            if value_first_card != 5:
                                self.__createRowQtable(value_first_card, value_second_card, value_first_card, draw_size)
                            else:
                                self.__createRowQtable(value_first_card, value_second_card, value_first_card, draw_size, False)
                                self.__createRowQtable(value_first_card, value_second_card, value_first_card, draw_size, True)
                        if value_first_card != value_second_card:
                            for draw_size in range(0, 11):
                                if value_second_card != 5:
                                    self.__createRowQtable(value_first_card, value_second_card, value_second_card, draw_size)
                                else:
                                    self.__createRowQtable(value_first_card, value_second_card, value_second_card, draw_size, False)
                                    self.__createRowQtable(value_first_card, value_second_card, value_second_card, draw_size, True)
        self.__connection.commit()

    @log(active_log, logger)
    def __createRowQtable(self, value_first_card, value_second_card, action, draw_size, prince_targets_AI = None):
        """Create and execute a query in order to insert a new row in the Qlearning table.

        Keyword arguments:
        value_first_card = value of the first card in the hand.
        value_second_card = value of the second card in the hand.
        action = value of the card played.
        draw_size = number of remaining cards in the draw.
        prince_targets_AI = boolean parameter set in case of prince played.
            equal to True if the prince target the AI and False otherwise.

        """
        prince_target = self.__setTargetPrince(prince_targets_AI)
        query = "INSERT INTO {0} ({1},{2},{3},{4},{5},{6}) VALUES ({7},{8},{9},{10},{11},0)".format(
            self.__Qlearning_table, self.__card1_col, self.__card2_col, self.__action_col, self.__prince_col, self.__draw_col, 
            self.__expectation_col, value_first_card, value_second_card, action, prince_target, draw_size)
        self.__cursor.execute(query)

    def __setTargetPrince(self, prince_targets_AI):
        """Returns a value which indicates who is tageted by the prince condidering the boolean in parameter.

        The returned value is meant to be insert in the Qlearning table in the prince_targets_AI column.
        The returned value is 0 if the AI is not the target, 1 otherwise and NULL if the prince is not the action
        (parameter equal to None).

        Keyword arguments:
        prince_targets_AI = boolean parameter set in case of prince played.
            equal to True if the prince target the AI and False otherwise.
            equal to None if a prince is not the action.

        """
        if prince_targets_AI is None:
            return "NULL"
        elif prince_targets_AI:
            return 1
        return 0

    @log(active_log, logger)
    def __resetQlearningTable(self):
        """Reinitializes the table setting all expectation to 0.
        """
        query = "UPDATE {0} SET {1} = 0".format(self.__Qlearning_table, self.__expectation_col)
        self.__cursor.execute(query)
        self.__connection.commit()

    @log(active_log, logger)
    def __createStatTable(self):
        """Creates the statistic table with all numbers of rounds and games won set to 0.
        """
        query = "CREATE TABLE {0}({1} TINYTEXT, {2} TINYTEXT, {3} TINYTEXT, {4} TINYINT UNSIGNED, {5} TINYINT UNSIGNED)".format(
            self.__stat_table, self.__agent1_col, self.__agent2_col, self.__winner_col, self.__rounds_col, self.__games_col)
        self.__cursor.execute(query)  
        self.__connection.commit()

    @log(active_log, logger)
    def __resetStatTable(self):
        """Reinitializes the statistic table with all numbers of rounds and games won set to 0.
        """
        query = "UPDATE {0} SET {1} = 0, {2} = 0".format(self.__stat_table, self.__rounds_col, self.__games_col)
        self.__cursor.execute(query)
        self.__connection.commit()
