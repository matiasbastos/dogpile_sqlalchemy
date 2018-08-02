"""helloworldredis.py

Illustrate how to load some data, and cache the results with redis.

"""

import pudb; pu.db
from environment import Session
from model import Person
from caching_query import FromCache

# load Person objects.  cache the result in the "redis" cache region
print("loading people....")
people = Session.query(Person).options(FromCache("redis")).all()

# remove the Session.  next query starts from scratch.
Session.remove()

# load again, using the same FromCache option. now they're cached,
# so no SQL is emitted.
print("loading people....again!")
people = Session.query(Person).options(FromCache("redis")).all()

# Specifying a different query produces a different cache key, so
# these results are independently cached.
print("loading people two through twelve")
people_two_through_twelve = Session.query(Person).\
                            options(FromCache("redis")).\
                            filter(Person.name.between("person 02", "person 12")).\
                            all()

# the data is cached under string structure of the SQL statement, *plus*
# the bind parameters of the query.    So this query, having
# different literal parameters under "Person.name.between()" than the
# previous one, issues new SQL...
print("loading people five through fifteen")
people_five_through_fifteen = Session.query(Person).\
                            options(FromCache("redis")).\
                            filter(Person.name.between("person 05", "person 15")).\
                            all()


# ... but using the same params as are already cached, no SQL
print("loading people two through twelve...again!")
people_two_through_twelve = Session.query(Person).\
                            options(FromCache("redis")).\
                            filter(Person.name.between("person 02", "person 12")).\
                            all()


# invalidate the cache for the three queries we've done.  Recreate
# each Query, which includes at the very least the same FromCache,
# same list of objects to be loaded, and the same parameters in the
# same order, then call invalidate().
print("invalidating everything")
Session.query(Person).options(FromCache("redis")).invalidate()
Session.query(Person).\
            options(FromCache("redis")).\
            filter(Person.name.between("person 02", "person 12")).invalidate()
Session.query(Person).\
            options(FromCache("redis", "people_on_range")).\
            filter(Person.name.between("person 05", "person 15")).invalidate()

