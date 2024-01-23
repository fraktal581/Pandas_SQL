import psycopg2

# подключение к базе

connection_BD = psycopg2.connect(
    host = "localhost",
    database = 'postgres',
    user = 'postgres',
    password = '12345w!'
)
# создание курсора для выполнения SQL-запроса
cursor = connection_BD.cursor()
# создание таблицы
cursor.execute("""
               CREATE TABLE IF NOT EXISTS Competitor_price(
                   id SERIAL PRIMARY KEY,
                   vendor VARCHAR(255),
                   nomination VARCHAR(255),
                   price FLOAT,
                   category VARCHAR(255),
                   sub_category VARCHAR(255)
               )
""")

# Вставка данных в таблицу
cursor.execute("""
               INSERT INTO Competitor_price(vendor, nomination, price, category, sub_category) VALUES (%s, %s, %s, %s, %s);
               """, (
                   ('0103252', 'Кран шаровой для воды 1/2" г/г бабочка ГАЛЛОП ПРАКТИК 130', 173.13, 'Трубопроводная арматура', 'Краны шаровые')
                   )
               )


# Фиксация изменений в БД
connection_BD.commit()

# Закрытие курсора и соединения
cursor.close()
connection_BD.close()