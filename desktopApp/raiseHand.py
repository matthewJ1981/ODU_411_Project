import os, sys
sys.path.insert(0, os.path.abspath("../database"))

from database import database

if __name__ == "__main__":
    db = database()
    try:
        id = db.child.add("Fred", 4, 1)
    except:
        id = db.child.getID(("Fred", 4, 1))

    db.child.setRaisedHand(id, 1)
    db.close()