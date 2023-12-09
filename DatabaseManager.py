import mysql.connector
import hashlib


def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False


class DatabaseManager:
    def __init__(self, db_user, db_password, host, database) -> None:
        self.conn = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=host,
            database=database,
        )

        self.cursor = self.conn.cursor()

    def create_usertable(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)"
        )

    def update_userdata(self, username, password):
        self.cursor.execute(
            "INSERT INTO userstable(username,password) VALUES (?,?)",
            (username, password),
        )
        self.conn.commit()

    def login_user(self, username, password):
        self.cursor.execute(
            "SELECT * FROM userstable WHERE username =? AND password = ?",
            (username, password),
        )
        data = self.cursor.fetchall()
        return data
