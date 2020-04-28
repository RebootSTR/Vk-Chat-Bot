import sqlite3


class DataBase:
    def __init__(self, name):
        self.conn = sqlite3.connect(name)

    def create(self, table, *values):
        cursor = self.conn.cursor()
        cursor.execute("create table if not exists {} ({})".format(table, ("?," * len(values))[:-1]), values)
        cursor.close()

    def append(self, table, *values):
        cursor = self.conn.cursor()
        cursor.execute("insert into {} values ({})".format(table, ("?," * len(values))[:-1]), values)
        cursor.close()
        self.save()

    def delete_all(self, table):
        cursor = self.conn.cursor()
        cursor.execute("delete from {}".format(table))
        cursor.close()
        self.save()

    def get(self, table, column, search):
        cursor = self.conn.cursor()
        data = cursor.execute("SELECT {} FROM {} where {}".format(column, table, search)).fetchone()
        if data is not None:
            data = data[0]
        cursor.close()
        return data

    def get_all(self, table):
        cursor = self.conn.cursor()
        data = cursor.execute("SELECT * FROM {}".format(table)).fetchall()
        cursor.close()
        return data

    def edit(self, table, column, value, search):
        cursor = self.conn.cursor()
        cursor.execute("update {} set {}=? where {}".format(table, column, search), [value])
        cursor.close()
        self.save()

    def delete(self, table, column, value):
        cursor = self.conn.cursor()
        cursor.execute("delete from {} where {}=?".format(table, column), [value])
        cursor.close()
        self.save()

    def count(self, table):
        cursor = self.conn.cursor()
        result = cursor.execute(f"select count(*) from {table}").fetchone()[0]
        cursor.close()
        return result

    def save(self):
        self.conn.commit()
