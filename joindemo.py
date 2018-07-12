# tutorial
# http://www.rmunn.com/sqlalchemy-tutorial/tutorial.html
# https://stackoverflow.com/questions/33053241/sqlalchemy-if-table-does-not-exist
# https://stackoverflow.com/questions/42079419/truncate-table-not-working-with-sql-server-sqlalchemy-engine-and-pandas

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


db = create_engine('sqlite:///joindemo.db')
Session = sessionmaker(bind=db)

# db.echo = True
db.echo = False

metadata = MetaData(db)

users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('age', Integer),
)
if not db.dialect.has_table(db, 'users'):
    users.create()

emails = Table('emails', metadata,
    Column('email_id', Integer, primary_key=True),
    Column('address', String),
    Column('user_id', Integer, ForeignKey('users.user_id')),
)
if not db.dialect.has_table(db, 'emails'):
    emails.create()
    
    
session = Session()
session.execute('''DELETE FROM emails''')
session.commit()
session.execute('''DELETE FROM users''')
session.commit()
session.close()

i = users.insert()
i.execute(
    {'name': 'Mary', 'age': 30},
    {'name': 'John', 'age': 42},
    {'name': 'Susan', 'age': 57},
    {'name': 'Carl', 'age': 33}
)
i = emails.insert()
i.execute(
    # There's a better way to do this, but we haven't gotten there yet
    {'address': 'mary@example.com', 'user_id': 1},
    {'address': 'john@nowhere.net', 'user_id': 2},
    {'address': 'john@example.org', 'user_id': 2},
    {'address': 'carl@nospam.net', 'user_id': 4},
)

def run(stmt):
    pass
    # rs = stmt.execute()
    # for row in rs:
    #    print (row)
    
def run2(stmt):
     rs = stmt.execute()
     for row in rs:
        print (row)

# This will return more results than you are probably expecting.
s = select([users, emails])
run(s)

# The reason is because you specified no WHERE clause, so a full join was
# performed, which returns every possible combination of records from
# tables A and B. With an appropriate WHERE clause, you'll get the
# restricted record set you really wanted.
s = select([users, emails], emails.c.user_id == users.c.user_id)
run(s)

# If you're interested in only a few columns, then specify them explicitly
s = select([users.c.name, emails.c.address], emails.c.user_id == users.c.user_id)
run(s)

# There are also "smart" join objects that can figure out the correct join
# conditions based on the tables' foreign keys
s = join(users, emails).select()
print("inner join")
run2(s)

# If you want all the users, whether or not they have an email address,
# then you want an "outer" join.
s = outerjoin(users, emails).select()
print("left outer join")
run2(s)

# Order of outer joins is important! Default is a "left outer join", which
# means "all records from the left-hand table, plus their corresponding
# values from the right-hand table, if any". Notice how this time, Susan's
# name will *not* appear in the results.
s = outerjoin(emails, users).select()
run(s)