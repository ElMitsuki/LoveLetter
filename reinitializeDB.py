from QlearningEngineV3.io import DBAccess as DBAccessV3
from QlearningEngineV1.io import DBAccess as DBAccessV1

if __name__ == "__main__":
    dbV3 = DBAccessV3()
    # dbV1 = DBAccessV1()

    # dbV1.initializeTable()
    # dbV3.initialize()

    """Reinitialize statistics table"""
    dbV3.initializeStatTable()
