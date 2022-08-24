import sqlite3
import cassiopeia as cass

class DBHelper():

    def __init__(self) -> None:
        self.__connection = sqlite3.connect('chad.db', isolation_level=None)


    def get_cursor(self):
        return self.__connection.cursor()

        

    def is_in_databse(self, cursor: sqlite3.Cursor, id):

        cursor.execute('SELECT summoner FROM users where id = ?', (int(id),))
        # cursor.execute('SELECT id FROM summoners where puuid = ?', ('JKdQjbjJEFCEjDSaZEIsMHaCfQfxH7sbt4pJRnU5YWz32eYMtpP18MuSVs8MkuG7dU_5B8fSm1hOow',))
        result = cursor.fetchone()

        if result != None:
            return result[0]

        return result


    def add_to_db_new(self, cursor: sqlite3.Cursor, id, summ_name, summ_region):

        summoner = cass.get_summoner(name=summ_name, region=summ_region)

        if self.check_if_summoner_in_db(cursor, summoner.puuid) == None:
            cursor.execute('INSERT INTO summoners (puuid, name, region) VALUES (?, ?, ?)', (summoner.puuid, summoner.name, summ_region))

        cursor.execute('SELECT id FROM summoners where puuid = ?', (summoner.puuid, ))
        cursor.execute('INSERT INTO users (id, summoner) VALUES (?, ?)', (int(id), cursor.fetchone()[0]))


    def overwrite(self, cursor: sqlite3.Cursor, id, summ_name, summ_region):

        summoner = cass.get_summoner(name=summ_name, region=summ_region)

        if self.check_if_summoner_in_db(cursor, summoner.puuid) == None:
            cursor.execute('INSERT INTO summoners (puuid, name, region) VALUES (?, ?, ?)', (summoner.puuid, summoner.name, summ_region))

        cursor.execute('SELECT id FROM summoners where puuid = ?', (summoner.puuid, ))

        cursor.execute('UPDATE users SET summoner = ? WHERE id = ?', (cursor.fetchone()[0], int(id)))



    def check_if_summoner_in_db(self, cursor: sqlite3.Cursor, puuid):
        
        cursor.execute('SELECT id FROM summoners where puuid = ?', (puuid, ))

        result = cursor.fetchone()

        if result != None:
            return result[0]

        return result
