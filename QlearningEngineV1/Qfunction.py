from .io import DBAccess

db = DBAccess()

def setNodeExpectation(node):
    '''Return the expectation for the given node.

    Keyword arguments:
        node = object state wich contains two card values.
    '''
    node.setCurrentExpectation(db.getExpectation(node.getCurrentState(),node.getCurrentAction()))


def updateQTable(node,r):
    '''Update the value of the expectation in the Qtable according to the formula of the Q-learning.

    Keyword arguments:
        node = object state wich contains two card values.
        r = a reward given by the current state.
    '''
    if( node.getParentExpectation() is not None ) : 
        newExpectation = node.getParentExpectation() + 0.1*( r + 0.9*node.getCurrentExpectation() - node.getParentExpectation() )
        db.updateExpectation(node.getParentState(),node.getParentAction(),newExpectation)
    else : 
        newExpectation = 0.1*( r + 0.9*node.getCurrentExpectation() )
        db.updateExpectation(node.getCurrentState(),node.getCurrentAction(),newExpectation)
    return True