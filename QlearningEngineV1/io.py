import sqlite3 
from .exceptionDB import log, create_logger

active_log = False
logger = create_logger

class DBAccess:

    def __init__(self, file='QlearningEngineV1/db/data.db'):
        """The constructor initializes the path to the database and the different names
        to use to access the data.
        """
        self.__db_file = file
        self.__expectation_table = 'expectation_table'
        self.__card1_col = 'card1'
        self.__card2_col = 'card2'
        self.__action_col = 'action'
        self.__expectation_col = 'expectation'

        # Journal mode
        self.__journal_mode = "OFF"


    @log(active_log, logger)
    def initializeTable(self):
        """Initializes or reinitializes the expectation table with all expectation with a value of 0.
        """
        self.__open()
        expectation_table = self.__cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='{0}'".format(self.__expectation_table)) 
        if not expectation_table.fetchone():
            self.__createTable()
        else:
            self.__initTable()
        self.__close()

    @log(active_log, logger)
    def getExpectation(self, state, action):
        """Returns an expectation value from the table condisdering the state and the action.

        Keyword arguments:
        state = object state wich contains two card values.
        action = value of the card played.

        """
        self.__open()
        query = "SELECT {0} FROM {1} WHERE {2} = {3} AND {4} = {5} AND {6} = {7}".format(
            self.__expectation_col, self.__expectation_table, 
            # replaced state.card1 and state.card2 later
            self.__card1_col, state.getCard1(), self.__card2_col, state.getCard2(), self.__action_col, action) 
        self.__cursor.execute(query)
        expectation = self.__cursor.fetchone()[0]
        self.__close()
        return expectation

    @log(active_log, logger)
    def updateExpectation(self, state, action, expectation):
        """update the expectation in the table for a state and the action.

        Keyword arguments:
        state = object state wich contains two card values.
        action = value of the card played.
        expecation = value of the expectation to update for the state and action.

        """
        self.__open()
        query = "UPDATE {0} SET {1} = {2} WHERE {3} = {4} AND {5} = {6} AND {7} = {8}".format(
            self.__expectation_table, self.__expectation_col, expectation,
            self.__card1_col, state.getCard1(), self.__card2_col, state.getCard2(), self.__action_col, action)
        self.__cursor.execute(query)
        self.__connection.commit()
        self.__close()

    @log(active_log, logger)
    def __open(self):
        """Open a connection with the database setting a connection variable and a cursor
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
    def __createTable(self):
        """Creates the table with all expectation set to 0.
        """
        query = "CREATE TABLE {0}({1} TINYINT UNSIGNED,{2} TINYINT UNSIGNED,{3} TINYINT UNSIGNED,{4} FLOAT)".format(
            self.__expectation_table, self.__card1_col, self.__card2_col, self.__action_col, self.__expectation_col)
        self.__cursor.execute(query) 
        for value_first_card in range(1,8):
                for value_second_card in range(value_first_card, 8):
                    if (value_first_card < 6) or (value_first_card >= 6 and value_first_card != value_second_card):
                        if not(value_first_card == 6 and value_second_card == 7) and not(
                                value_first_card == 5 and value_second_card == 7):  
                            query = "INSERT INTO {0} ({1},{2},{3},{4}) VALUES ({5},{6},{7},0)".format(
                                self.__expectation_table, self.__card1_col, self.__card2_col, self.__action_col, 
                                self.__expectation_col, value_first_card, value_second_card, value_first_card)
                            self.__cursor.execute(query) 
                            if value_first_card != value_second_card:
                                query = "INSERT INTO {0} ({1},{2},{3},{4}) VALUES ({5},{6},{7},0)".format(
                                    self.__expectation_table, self.__card1_col, self.__card2_col, self.__action_col,
                                    self.__expectation_col, value_first_card, value_second_card, value_second_card)
                                self.__cursor.execute(query) 
        self.__connection.commit()

    @log(active_log, logger)
    def __initTable(self):
        """Reinitializes the table setting all expectation to 0.
        """
        query = "UPDATE {0} SET {1} = 0".format(self.__expectation_table, self.__expectation_col)
        self.__cursor.execute(query)
        self.__connection.commit()

if __name__ == "__main__":
    db = DBAccess()
    db.initializeTable()
