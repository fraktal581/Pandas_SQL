import pyodbc as dbc
import pandas as pd
from read_txt_to_df import df_sales_wout_VAT

# входные константы и переменные: продумать пути записи через инпут, форму, окно
SERVER = 'SQL-srv-01'   # Имя сервера
DATABASE = 'analytica'  # Имя DB
USER_NAME = 'SA'        # login
PASSWORD = '1QAzxSW2'   # pwd
table_name = 'sales_without_vat'    # имя целевой таблицы

# строка с данными запроса
connection_data_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};UID={USER_NAME};PWD={PASSWORD};TrustServerCertificate=yes'

#####       БЛОК ФУНКЦИЙ        #####

# функция подключения к BD с проверкой существования таблицы
def create_connection_check_table(conn_data: str, table_name: str):
    try:
        # Создаем объект подключения к DB
        connection_DB = dbc.connect(conn_data)
        # Инициализируем функцию - курсор
        cursor=connection_DB.cursor()
        # Формируем SQL-запрос для создания таблицы
        check_table_query = "SELECT 1 FROM sys.tables WHERE name = '" + table_name + "'"
        # Проверяем существование таблицы
            # если на выходе получаем "1": выводим соответствующий print
            # если None - создаем таблицу, выводим print
        if cursor.execute(check_table_query).fetchone(): 
            print(f"Таблица '{table_name}' уже существует")
        else:
            # Формируем SQL-запрос для создания таблицы
            sql_query = f"""
                        CREATE TABLE {DATABASE}.dbo.{table_name}
                        (Id INT PRIMARY KEY IDENTITY,
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
                        count INT,
                        billings SMALLMONEY)"""
            cursor.execute(sql_query)
            print(f"таблица '{table_name}' создана")    
        # фиксация изменений
        connection_DB.commit
        # закрытие соединения
        connection_DB.close
    except dbc.Error as err:
        print(f'Произошла ошибка при создании таблицы {table_name}. \nКод ошибки: {err}')

# Функция проверки существования данных
def record_exist(conn_data: str, table_name, tuple):
    #try:
        # Создаем объект подключения к DB
        connection_DB = dbc.connect(conn_data)
        # Инициализируем функцию - курсор
        cursor=connection_DB.cursor()
        cursor.execute(f"""SELECT 1 FROM {table_name} 
                                WHERE realisation = '{tuple[4]}' AND
                                    vendor = '{str(tuple[10])}' AND
                                    nomenclature = '{tuple[9].replace("'","")}' AND
                                    date_period = '{tuple[11]}' AND
                                    count = {tuple[12]} AND
                                    billings = {tuple[13]};""")
        result = cursor.fetchone()
        return result
    #except dbc.Error as err:
        #print(f'Произошла ошибка при поиске строки \n{tuple} \nв таблицы {table_name}. \nКод ошибки: {err}')


# функция внесения данных в таблицу DB с проверкой данных
def insert_data_to_table(conn_data: str, df):
    try:
        # Создаем объект подключения к DB
        connection_DB = dbc.connect(conn_data)
        # Инициализируем функцию - курсор
        cursor=connection_DB.cursor()
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
        for row in df.itertuples(index=False):
            if record_exist(connection_data_string, table_name, row):
                print(f'realisation = {row[4]}, vendor = {str(row[10])}, nomenclature = {row[9]}, date_period = {row[11]}, count = {row[12]}, billing = {row[13]}')
                count_block +=1
                df_block_rows.loc[len(df_block_rows)] = row
            else:
                sql_query = f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                cursor.execute(sql_query, row)
                count_add +=1
                # фиксация изменений
                connection_DB.commit
                # закрытие соединения
                connection_DB.close
        print(f'В таблицу {table_name} добавлено {count_add} записей(си)\nЗаблокировано {count_block} записей(си)')
        # Запись не вошедших строк
        df_block_rows.to_csv('SQL_writer/DATA/block_rows_in_SQL_Server_sales_wout_VAT.csv', encoding='utf-8')
    except dbc.Error as err:
        print(f'Произошла ошибка при внесении строки в таблицу {table_name}. \n\n Строка: {row} \n\nКод ошибки: {err}')



#####       БЛОК ИСПОЛНЯЕМОГО КОДА        #####

create_connection_check_table(connection_data_string, table_name)

insert_data_to_table(connection_data_string, df_sales_wout_VAT)



# Устанавливаем соединение с БД
#connection_DB = dbc.connect(connectionString)

""" # Инициализация курсора
cursor = connection_DB.cursor()

# Формируем SQL-запрос для создания таблиц
check_table_query = "SELECT 1 FROM sys.tables WHERE name = '" + table_name + "'"

# Проверяем существование таблицы
    # если на выходе получаем "1": выводим соответствующий print
    # если None - создаем таблицу, выводим print
if cursor.execute(check_table_query).fetchone(): 
    print("Таблица", table_name, "уже существует")
else:
    # Формируем SQL-запрос для создания таблицы """
#    sql_query = f"""
#                CREATE TABLE {DATABASE}.dbo.{table_name}
#                (id INT, segment VARCHAR(255), access_group VARCHAR(255), main_meneger VARCHAR(255), reduction_factor VARCHAR(255), realisation VARCHAR(255), payment_schedule VARCHAR(255), client_name VARCHAR(255), main_organisation VARCHAR(255), type_of_nomenclature VARCHAR(255), nomenclature VARCHAR(255), vendor VARCHAR(255), date_period DATE, count INT, billings SMALLMONEY)"""
"""     cursor.execute(sql_query)
    print(f'таблица dbo.{table_name} создана')
    
# фиксация изменений
connection_DB.commit

# закрытие соединения
connection_DB.close
 """
