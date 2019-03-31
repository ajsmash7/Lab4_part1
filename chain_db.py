import sqlite3
from model import Juggler

db_file = "jugglers.sqlite"


class Database:

    """ Use a singleton to create an instance of the database
    ensures code will only have one instance writing to database
    at one time """

    instance = None

    class __Database:
        def __init__(self):
            self._db = sqlite3.connect(db_file)
            self._db.row_factory = sqlite3.Row

            with self._db as db:
                cur = db.cursor()
                cur.execute('CREATE TABLE IF NOT EXISTS jugglers (name TEXT UNIQUE, country TEXT, catches INT)')

        # show all jugglers, throw exception if error
        def get_jugglers(self):
            try:
                cur = self._db.cursor()
                cur.execute('SELECT rowid, * FROM jugglers')
                return self._cursor_to_recordlist(cur)
            except sqlite3.Error as e:
                raise JugglerError(f'Error getting Juggler Records') from e

        # add a new juggler record to the database. Raise exception if juggler already exists
        def add_record(self, juggler):
            try:
                with self._db as db:
                    cur = db.cursor()
                    cur.execute('INSERT INTO jugglers values (?, ?, ?)', (juggler.name, juggler.country, juggler.catches))
                    juggler.id = cur.lastrowid
            except sqlite3.IntegrityError:
                raise JugglerError('Juggler Record already exists')
            except sqlite3.Error as e:
                raise JugglerError(f'error adding juggler {juggler}') from e

        # update catches by name, raise exception if juggler does not exist
        def update_catches(self, name, catches):

            try:
                with self._db as db:
                    cur = db.cursor()
                    cur.execute('UPDATE jugglers SET catches = ? WHERE name = ?', (catches, name))
                    if not cur.rowcount:
                        raise JugglerError('Juggler does not exist')
            except sqlite3.Error as e:
                raise JugglerError(f'Error updating catches for {name}') from e

        # gets the matches for the user entry search term, raise exception if no match found
        def search_records(self, entry):

            try:
                cur = self._db.cursor()
                search = f'%{entry.upper()}%'
                cur.execute('SELECT rowid, * FROM jugglers WHERE UPPER(name) like ?', (search, ))
                return self._cursor_to_recordlist(cur)
            except sqlite3.Error as e:
                raise JugglerError(f'No Juggler Match Found for {entry}') from e

        # delete juggler, raise exception if no juggler found to delete
        def delete_juggler(self, name):

            try:
                with self._db as db:
                    cur = db.cursor()
                    cur.execute('DELETE FROM jugglers WHERE name = ?', (name, ))
                    if not cur.rowcount:
                        raise JugglerError('DELETE FAILED: Juggler does not exist')
            except sqlite3.Error as e:
                raise JugglerError('Error Deleting Juggler') from e

        # turn the database record into a Juggler object, return none if parameter is empty
        def _row_to_juggler(self, row):
            if not row:
                return None
            juggler = Juggler(row['name'], row['country'], row['catches'], row['rowid'])
            return juggler

        def _cursor_to_recordlist(self, cur):
            return [self._row_to_juggler(row) for row in cur]

        # get id by name, raise exception if no juggler found
        def get_id(self, name):
            try:
                cur = self._db.cursor()
                id = cur.execute('SELECT rowid FROM jugglers WHERE name = ?', (name, ))
                return id
            except sqlite3.Error as e:
                raise JugglerError(f'{name} does not exist!') from e

    # method to validate and instantiate a new instance of a database session
    def __new__(cls, *args, **kwargs):
        if not Database.instance:
            Database.instance = Database.__Database()
        return Database.instance

    # override the getter and setter with each instantiation
    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)

class JugglerError(Exception):
    # for raise errors
    pass
