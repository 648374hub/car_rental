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

    def update_userdata(self, username, password):
        self.cursor.execute(
            "INSERT INTO MPS_USERS(username,password) VALUES (?,?)",
            (username, password),
        )
        self.conn.commit()

    def login_user(self, username, password):
        self.cursor.execute(
            "SELECT * FROM MPS_USERS WHERE username =? AND password = ?",
            (username, password),
        )
        data = self.cursor.fetchall()
        return data
