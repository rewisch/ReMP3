import sqlite3 as sql

class Database():
    def __init__(self):
        self.connection = sql.connect('_db/db.db')

    def set_song(self, file_name, blob):
        cursor = self.connection.cursor()
        sql = """INSERT INTO Song (Title, Blob) VALUES (?, ?)"""
        parameters = (file_name, blob)
        cursor.execute(sql, parameters)
        self.connection.commit()
        cursor.close()

    def get_song(self, title):
        cursor = self.connection.cursor()
        sql = f"SELECT Blob FROM Song WHERE Title = '{title}'"
        cursor.execute(sql)
        song = cursor.fetchone()[0]
        cursor.close()
        return song

    def get_songs(self):
        cursor = self.connection.cursor()
        sql = f'SELECT Title FROM Song'
        cursor.execute(sql)
        songs = cursor.fetchall()
        result = [n[0] for n in songs]
        cursor.close()
        return result

    def del_song(self, title):
        cursor = self.connection.cursor()
        sql = f"""Delete From Song where Title = '{title}'"""
        cursor.execute(sql)
        self.connection.commit()
        cursor.close()

