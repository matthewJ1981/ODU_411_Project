
import os
import sys

import os, sys
sys.path.insert(0, os.path.abspath("../database"))
from database import database


db = database('localhost')
db.createTestDB()
db.useDB()

file = open ("../images/login_logo.png", "rb")
b = file.read()
file.close()

clid = db._class.add("Class", "Teacher")
aid = db.activity.add("Writing", clid)
mid = db.macroElement.add(orderNum = 1, activity_id = aid, img = b)

file = open("../images/Test.png", "wb")
img = db.macroElement.getImage(mid)
file.write(img)
file.close()

db.close()