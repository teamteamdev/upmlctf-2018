from db import *

db.connect()
db.create_tables([Link])

Link.create(id="hHk2l", url="https://ctf.upml.tech/secret_flag_124EHx.html")

