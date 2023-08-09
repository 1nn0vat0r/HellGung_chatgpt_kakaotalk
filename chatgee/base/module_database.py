# -*- coding: utf-8 -*-
"""ChatGee Database Moduel Class Object"""

import sqlite3
import os

class ChatGee_DB:
    """ChatGee Database Moduel Class Object"""

    def __init__(self):
        self.db_prefix = "ChatGee"
        self.user_db_name = "_User.db"
        self.chat_db_name = "_Chat.db"
        self.token_db_name = "_Tokens.db"

    def init_db(self, db_prefix):
        """Initialize ChatGee Database"""
        self.db_prefix = db_prefix
        self.user_db_name = db_prefix + "_User.db"
        self.chat_db_name = db_prefix + "_Chat.db"
        self.token_db_name = db_prefix + "_Tokens.db"

        # User databasse
        if os.path.isfile(self.user_db_name):
            print("ChatGee DB : User Database exists!")
        else:
            # create a connection to the database 없는경우 생성됨!!!!!
            conn_init = sqlite3.connect(self.user_db_name)

            # create a new table to store conversation data
            cursor_init = conn_init.cursor()
            cursor_init.execute("CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                    room TEXT NOT NULL, member BOOL NOT NULL, count INTEGER NOT NULL, \
                    total_count INTEGER NOT NULL, myAge INTEGER NULL, \
                    myGender TEXT NULL, myHeight REAL NULL, myWeight REAL NULL)")
            conn_init.commit()

            # close the database connection when finished
            cursor_init.close()
            conn_init.close()

        # Prompt database
        if os.path.isfile(self.chat_db_name):
            print("ChatGee DB : Chat History Database exists!")
        else:
            # create a connection to the database
            conn_init = sqlite3.connect(self.chat_db_name)

            # create a new table to store conversation data
            cursor_init = conn_init.cursor()
            cursor_init.execute("CREATE TABLE conversation (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                speaker TEXT NOT NULL, room TEXT NOT NULL, message TEXT NOT NULL, \
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
            conn_init.commit()

            # close the database connection when finished
            cursor_init.close()
            conn_init.close()

        if os.path.isfile(self.token_db_name):
            print("ChatGee DB : Token Usage Database exists!")
        else:
            # create a connection to the database
            conn_init = sqlite3.connect(self.token_db_name)
            # create a new table to store conversation data
            cursor_init = conn_init.cursor()
            cursor_init.execute("CREATE TABLE data (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                prompt_tokens INTEGER NULL, response_tokens INTEGER NULL, \
                                total_tokens INTEGER NULL, \
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
            conn_init.commit()
            # close the database connection when finished
            cursor_init.close()
            conn_init.close()

    # Define a function to save conversation data
    def save_conversation_data(self, speaker, room, message):
        """Save conversation data"""
        conn = sqlite3.connect(self.chat_db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO conversation (speaker, room, message) \
                       VALUES (?, ?, ?)",  (speaker, room, message))
        cursor.execute("DELETE FROM conversation WHERE id NOT IN \
                       (SELECT id FROM conversation ORDER BY id DESC LIMIT 20)")
        conn.commit()
        cursor.close()
        conn.close()

    # Define a function to save conversation data not at the end but somewhere in the middle
    def save_conversation_one_above(self, speaker, room, message):
        """Define a function to save conversation data not at the end but somewhere in the middle"""
        conn = sqlite3.connect(self.chat_db_name)
        cursor = conn.cursor()

        # Get the id of the last row
        cursor.execute("SELECT id FROM conversation ORDER BY id DESC LIMIT 1")
        last_id = cursor.fetchone()

        new_id = last_id[0] + 2 if last_id else 1

        # Shift the ids of all rows with an id >= new_id
        cursor.execute("UPDATE conversation SET id = id + 2 WHERE id >= ?", (new_id,))

        # Insert the new row with the desired id
        cursor.execute("INSERT INTO conversation (id, speaker, room, message) \
                       VALUES (?, ?, ?, ?)", (new_id, speaker, room, message))

        conn.commit()
        cursor.close()
        conn.close()

    def delete_conversation_data(self, room):
        """Delete conversation data"""
        conn = sqlite3.connect(self.chat_db_name)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM conversation WHERE room=?", (room,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_conversation_data(self, room, limit=100):
        """Get conversation data"""
        conn = sqlite3.connect(self.chat_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversation WHERE room=? \
                       ORDER BY id ASC LIMIT ?", (room, limit))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_conversation_latest(self, room, limit=1):
        """Get latest conversation data"""
        conn = sqlite3.connect(self.chat_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM conversation WHERE room=? \
                       ORDER BY id DESC LIMIT ?", (room, limit))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    # # Define a function to save user data
    # def save_user_data(self, room, member, count, total_count):
    #     """Save user data"""
    #     conn = sqlite3.connect(self.user_db_name)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT COUNT(*) FROM data WHERE room=?", (room,))
    #     count_row = cursor.fetchone()
    #     if count_row[0] == 0:
    #         cursor.execute("INSERT INTO data (room, member, count, total_count) \
    #                        VALUES (?, ?, ?, ?)", (room, member, count, total_count))
    #     else:
    #         cursor.execute("UPDATE data SET member=?, count=?, total_count=? \
    #                        WHERE room=?", (member, count, total_count, room))
    #     conn.commit()
    #     cursor.close()
    #     conn.close()

    def save_user_data(self, room, member, count, total_count, myAge=None, myGender=None, myHeight=None, myWeight=None):
        """Save user data"""
        conn = sqlite3.connect(self.user_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM data WHERE room=?", (room,))
        count_row = cursor.fetchone()
        if count_row[0] == 0:
            cursor.execute("INSERT INTO data (room, member, count, total_count, myAge, myGender, myHeight, myWeight) \
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (room, member, count, total_count, myAge, myGender, myHeight, myWeight))
        else:
            cursor.execute("UPDATE data SET member=?, count=?, total_count=?, myAge=?, myGender=?, myHeight=?, myWeight=? \
                        WHERE room=?", (member, count, total_count, myAge, myGender, myHeight, myWeight, room))
        conn.commit()
        cursor.close()
        conn.close()

    def save_user_age(self, room, member, count, total_count, myAge):
        """Save user data"""
        conn = sqlite3.connect(self.user_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM data WHERE room=?", (room,))
        count_row = cursor.fetchone()
        if count_row[0] == 0:
            cursor.execute("INSERT INTO data (room, member, count, total_count, myAge) \
                        VALUES (?, ?, ?, ?, ?)",
                        (room, member, count, total_count, myAge))
        else:
            cursor.execute("UPDATE data SET member=?, count=?, total_count=?, myAge=? \
                        WHERE room=?", (member, count, total_count, myAge, room))
        # cursor.execute("INSERT INTO data (room, member, count, total_count, myAge) \
        #             VALUES (?, ?, ?, ?, ?)",
        #             (room, member, count, total_count, myAge))
        conn.commit()
        cursor.close()
        conn.close()

    def save_user_gender(self, room, myGender):
        """Save user data"""
        conn = sqlite3.connect(self.user_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM data WHERE room=?", (room,))
        count_row = cursor.fetchone()
        cursor.execute("UPDATE data SET myGender=? \
                    WHERE room=?", (myGender, room))
        conn.commit()
        cursor.close()
        conn.close()

    def save_user_height(self, room, myHeight):
        """Save user data"""
        conn = sqlite3.connect(self.user_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM data WHERE room=?", (room,))
        count_row = cursor.fetchone()
        cursor.execute("UPDATE data SET myHeight=? \
                    WHERE room=?", (myHeight, room))
        conn.commit()
        cursor.close()
        conn.close()

    def save_user_weight(self, room, myWeight):
        """Save user data"""
        conn = sqlite3.connect(self.user_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM data WHERE room=?", (room,))
        count_row = cursor.fetchone()
        cursor.execute("UPDATE data SET myWeight=? \
                    WHERE room=?", (myWeight, room))
        conn.commit()
        cursor.close()
        conn.close()
    # # Define a function to save user data 나이 성별 키 몸무게 추가했습니다
    # def save_user_age(self, room, age, gender, height, weight):
    #     """Save user data"""
    #     conn = sqlite3.connect(self.user_db_name)
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT COUNT(*) FROM data WHERE room=?", (room,))
    #     count_row = cursor.fetchone()
    #     # if count_row[0] == 0:
    #     #     cursor.execute("INSERT INTO data (room, age) \
    #     #                    VALUES (?, ?)", (room, member, count, total_count, age, gender, height, weight))
    #     if age and gender and height and weight:
    #         cursor.execute("UPDATE data SET member=?, count=?, total_count=? age=?, gender=?, height=?, weight=?\
    #                        WHERE room=?", (member, count, total_count, age, gender, height, weight, room))
    #     else:
    #         cursor.execute("UPDATE data SET member=?, count=?, total_count=? \
    #                        WHERE room=?", (member, count, total_count, room))
    #     conn.commit()
    #     cursor.close()
    #     conn.close()

    # Define a function to retrieve user data
    def get_user_data_by_room(self, room):
        """Get user data by room"""
        conn = sqlite3.connect(self.user_db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM data WHERE room=?", (room,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def save_token_usage(self, prompt_tokens, response_tokens):
        """Save token usage"""
        conn = sqlite3.connect(self.token_db_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (prompt_tokens, response_tokens, total_tokens) \
                       VALUES (?, ?, ?)",
                       (prompt_tokens, response_tokens, prompt_tokens + response_tokens))
        cursor.close()
        conn.commit()
        conn.close()
