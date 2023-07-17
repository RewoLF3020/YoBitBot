import psycopg2


class BotDB:
    
    def __init__(self, host, user, password, db_name):
        """Инициализация соединения с БД"""
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        self.cursor = self.connection.cursor()
    
    def user_exists(self, user_id):
        """Проверка наличия пользователя в БД"""
        self.cursor.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
        return bool(len(self.cursor.fetchall()))
    
    def get_user_id(self, user_id):
        """Получаем id пользователя в базе по id в телеграмм"""
        self.cursor.execute("SELECT id FROM users WHERE user_id = %s", (user_id,))
        return self.cursor.fetchone()[0]
    
    def add_user(self, user_id):
        """Добавление пользователя в БД"""
        self.cursor.execute("INSERT INTO users (user_id) VALUES (%s)", (user_id,))
        return self.connection.commit()
    
    def add_record(self, user_id, operation, value):
        """Создание записи о доходах/расходах"""
        self.cursor.execute("INSERT INTO records (user_id, operation, value) VALUES (%s, %s, %s)",
            (self.get_user_id(user_id), 
             operation == "+", 
             value))
        return self.connection.commit()
    
    def get_records(self, user_id, within = "all"):
        """Получаем историю о доходах/расходах"""

        if within == "day":
            self.cursor.execute("SELECT * FROM records WHERE user_id = %s AND date BETWEEN datetime('now', 'start of day') AND datetime('now', 'localtime') ORDER BY date",
                (self.get_user_id(user_id),))
        elif within == "week":
            self.cursor.execute("SELECT * FROM records WHERE user_id = %s AND date BETWEEN datetime('now', '-6 days') AND datetime('now', 'localtime') ORDER BY date",
                (self.get_user_id(user_id),))
        elif within == "month":
            self.cursor.execute("SELECT * FROM records WHERE user_id = %s AND date BETWEEN datetime('now', 'start of month') AND datetime('now', 'localtime') ORDER BY date",
                (self.get_user_id(user_id),))
        else:
            self.cursor.execute("SELECT * FROM records WHERE user_id = %s ORDER BY date",
                (self.get_user_id(user_id),))

        return self.cursor.fetchall()
    
    def close(self):
        """Закрытие соединения с БД"""
        self.cursor.close()
        self.connection.close()



# try:
#     connection = psycopg2.connect(
#         host=host,
#         user=user,
#         password=password,
#         database=db_name
#     )
#     connection.autocommit = True
    
#     # cursor = connection.cursor()
    
#     # with connection.cursor() as cursor:
#         # cursor.execute(
#             # "SELECT version();"
#         # )
# # 
#         # print(f"Server version: {cursor.fetchone()}")

# except psycopg2.Error as _er:
#     print("[INFO] Error while working with PostrgreSQL", _er)
# finally:
#         if connection:
#             # cursor.close()
#             connection.close()
#             print("INFO PostgreSQL connection closed")
