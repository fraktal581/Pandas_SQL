import psycopg2
import pandas as pd
from read_txt_to_df import df_sales_wout_VAT

# имя таблицы
table_name = 'sts.sales_without_vat'

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
cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {table_name}
                (
                    id SERIAL PRIMARY KEY,  
                    segment VARCHAR(255),
                    access_group VARCHAR(255),
                    main_meneger VARCHAR(255),
                    reduction_factor VARCHAR(255),
                    realisation VARCHAR(255),
                    payment_schedule VARCHAR(255),
                    client_name VARCHAR(255),
                    main_organisation VARCHAR(255),
                    type_of_nomenclature VARCHAR(255),
                    nomenclature VARCHAR(255),
                    vendor VARCHAR(255),
                    date_period DATE,
                    count INTEGER,
                    billings FLOAT
                )
""")

# функция проверки данных в DB
def record_exist(connection, tuple):
    cursor.execute(f"""
                        SELECT EXISTS(
                            SELECT * FROM {table_name} 
                            WHERE realisation = %s AND
                                vendor = %s AND
                                nomenclature = %s AND
                                date_period = %s AND
                                count = %s AND
                                billings = %s)""", (tuple[4], str(tuple[10]), tuple[9], tuple[11], tuple[12], tuple[13]))
    result = cursor.fetchall()[0][0]
    return result

# Вставка данных в таблицу
block_row_dict = {'segment':[],
                    'access_group':[],
                    'main_manager':[],
                    'reduction_factor':[],
                    'realisation_doc':[],
                    'payment_shedule':[],
                    'client_name':[],
                    'main_organisation':[],
                    'type_of_nom':[],
                    'nomenclature':[],
                    'vendor':[],
                    'date':[],
                    'count':[],
                    'billing':[]}
df_block_rows = pd.DataFrame(block_row_dict)    # датафрей для записи заблокированных результатов
count_block = 0     # счетчик заблокированных данных
count_add = 0       # счетчик добавленных данных
# цикл проверки данных:
# вызов функции проверки данных в BD
# Если возвращает TRUE - вносим в DF плюсуем счетчик заблокированных строк
# Иначе - вносим данные в BD
for row in df_sales_wout_VAT.itertuples(index=False):
    if record_exist(connection_BD, row):
        #print(f'realisation = {row[4]}, vendor = {str(row[10])}, nomenclature = {row[9]}, date_period = {row[11]}, count = {row[12]}, billing = {row[13]}')
        count_block +=1
        df_block_rows.loc[len(df_block_rows)] = row
    else:
        cursor.execute(f"""
                INSERT INTO {table_name}(segment, 
                                                access_group,
                                                main_meneger,
                                                reduction_factor,
                                                realisation,
                                                payment_schedule,
                                                client_name,
                                                main_organisation,
                                                type_of_nomenclature,
                                                nomenclature,
                                                vendor,
                                                date_period,
                                                count,
                                                billings) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    (row)
                    )
                )
        count_add +=1
# Вывод результата:
# количество добавленных
# количество заблокированных
# запись заблокированных данных в CSV - файл
print(f'В таблицу {table_name} добавлено {count_add} записей(си)\nЗаблокировано {count_block} записей(си)')
df_block_rows.to_csv('SQL_writer/DATA/block_rows_sales_wout_VAT.csv', encoding='utf-8')
#print(df_block_rows)



# Фиксация изменений в БД
connection_BD.commit()

# Закрытие курсора и соединения
cursor.close()
connection_BD.close()