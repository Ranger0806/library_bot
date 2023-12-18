import sqlite3

class LibraryDB:
    def __init__(self):
        self.conn = sqlite3.connect('lib.db')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(
                "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, name TEXT, status TEXT, role TEXT, folder TEXT)")
            self.conn.commit()
        except sqlite3.OperationalError:
            "Unexpected error"

    async def cheker_user(self, user_id):
        self.cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
        if self.cursor.fetchone()[0] == 0:
            return False
        else:
            return True

    async def get_new_user(self, user_id, name, status, role, folder):
        self.cursor.execute("INSERT INTO 'users' ('user_id', 'name', 'status', 'role', 'folder') VALUES (?, ?, ?, ?, ?)",
                    (user_id, name, status, role, folder,))
        self.conn.commit()

    async def get_status(self, user_id):
        self.cursor.execute("SELECT status FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()[0]

    async def set_status(self, status, user_id):
        self.cursor.execute("UPDATE users SET status = ? WHERE user_id = ?", (status, user_id,))
        self.conn.commit()

    async def get_role(self, user_id):
        self.cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()[0]

    async def get_folder(self, user_id):
        self.cursor.execute("SELECT folder FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()[0]

    async def set_folder(self, folder, user_id):
        self.cursor.execute("UPDATE users SET folder = ? WHERE user_id = ?", (folder, user_id,))
        self.conn.commit()