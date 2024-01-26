import pyodbc as dbc
import pandas as pd
from read_txt_to_df import df_sales_wout_VAT

server = 'SQL-srv-01'
data_base = 'analytica'
user_name = 'SA'
password = '1QAzxSW2'
table_name = 'sales_without_vat'
connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={data_base};UID={user_name};PWD={password};TrustServerCertificate=yes'
# Устанавливаем соединение с БД
connection_DB = dbc.connect(connectionString)
# Инициализация курсора
cursor = connection_DB.cursor()
# Формируем SQL-запрос для создания таблицы
check_table_query = "SELECT 1 FROM sys.tables WHERE name = '" + table_name + "'"
# Проверяем существование таблицы
if cursor.execute(check_table_query).fetchone():
    print("Таблица", table_name, "уже существует")
else:
    # Формируем SQL-запрос для создания таблицы
    #  sql_query = 'CREATE TABLE ' + table + ' (' + ', '.join(columns) + ')'
    sql_query = f"""
                CREATE TABLE {data_base}.dbo.{table_name}
                (id INT, segment VARCHAR(255), access_group VARCHAR(255), main_meneger VARCHAR(255), reduction_factor VARCHAR(255), realisation VARCHAR(255), payment_schedule VARCHAR(255), client_name VARCHAR(255), main_organisation VARCHAR(255), type_of_nomenclature VARCHAR(255), nomenclature VARCHAR(255), vendor VARCHAR(255), date_period DATE, count INT, billings SMALLMONEY)"""
    cursor.execute(sql_query)
    print(f'таблица dbo.{table_name} создана')
connection_DB.commit
connection_DB.close

