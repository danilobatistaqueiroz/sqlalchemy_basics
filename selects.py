# tutorial
# http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
# https://stackoverflow.com/questions/2048084/sql-alchemy-what-is-wrong
# step before: firststeps.py

from sqlalchemy import *

# Let's re-use the same database as before
db = create_engine('sqlite:///tutorial.db')

db.echo = True  # We want to see the SQL we're creating

metadata = MetaData(db)

# The users table already exists, so no need to redefine it. Just
# load it from the database using the "autoload" feature.
users = Table('users', metadata, autoload=True)

def run2(stmt):
    rs = stmt.execute()
    for row in rs:
        print (row.name)


# Extra underscore after "in" to avoid conflict with Python keyword
s = users.select(users.c.name.in_(['Mary', 'Susan']))
run2(s)
