import psycopg2
from read_txt_to_df import df_sales_wout_VAT

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
               CREATE TABLE IF NOT EXISTS Sales_without_VAT
               (
                   id SERIAL PRIMARY KEY,
                   segment VARCHAR(255),
                   access_group VARCHAR(255),
                   main_meneger VARCHAR(255),
                   realisation VARCHAR(255),
                   client_name VARCHAR(255),
                   main_organisation VARCHAR(255),
                   type_of_nomenclature VARCHAR(255),
                   nomenclature VARCHAR(255),
                   vendor VARCHAR(255),
                   date_period VARCHAR(255),
                   count INTEGER,
                   billings FLOAT
               )
""")

# Вставка данных в таблицу
for row in df_sales_wout_VAT.itertuples(index=False):
    cursor.execute("""
                INSERT INTO Sales_without_VAT(segment, access_group, main_meneger, realisation, client_name, main_organisation, type_of_nomenclature, nomenclature, vendor, date_period, count, billings) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    (row)
                    )
                )


# Фиксация изменений в БД
connection_BD.commit()

# Закрытие курсора и соединения
cursor.close()
connection_BD.close()