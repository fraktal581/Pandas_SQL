import pandas as pd

# блок переменных, предполагается, что будут вноситься input'ом
#date_period = "Сентябрь 2023 г."
#segment = "ЕАЭС"
# конец блока переменных

# блок инициализации DateFrame, первичная агрегация и очистка

df_1C_sales_include_VAT = pd.read_csv('C:/Users/vorotintsev/Desktop/Проекты PYTHON/Входные_данные/Sales_Include_VAT.csv', header=0, sep='\t', on_bad_lines="skip",
                                      engine='python')
df_1C_sales_without_VAT = pd.read_csv('C:/Users/vorotintsev/Desktop/Проекты PYTHON/Входные_данные/Sales_WIthout_VAT.csv', header=0, sep='\t', on_bad_lines="skip",
                                      engine='python')
df_List_ID = [df_1C_sales_without_VAT, df_1C_sales_include_VAT]

# функция первичной очистки данных: фильрация DateFrame по периоду и сегменту 
# для каждой таблицы в списке применяем маски согласно введенным переменным сегмента и отчетного месяца
""" def prim_cln_df(df_list):
    i = 0
    for df in df_list:
        # создаем маски по входным данным "Период" и "Сегмент"
        mask_date = df['Период, месяц'] == date_period
        mask_segment = df['Сегмент'] == segment
        df_list[i] = df.loc[(mask_date & mask_segment)]
        i += 1 """
# вызов функции для фильтрации таблицы
#prim_cln_df(df_List_ID)
# конец блока инициализации DateFrame

# рабочий код после фильтрации по "Период, месяц"

# ф-я удаления неделимого пробела
def convert_currency(val):                      
    if val != 0:
        # новое значение с заменой символов
        new_val = val.replace(',','.').replace('\xa0', '')
        # преобразуем в число с плавающей точкой
        return float(new_val)
    else:
        return val


# функция преобразования входных df' ом
def df_convert_currency(df_list):   
    i = 0
    for df in df_list:
        # удаляем "NaN"
        df = df.dropna(subset=['Период, месяц'])
        # преобразуем столбцы
        df['Головное предприятие']=df['Головное предприятие'].fillna(df['Клиент'])
        df['Количество'] = df['Количество'].apply(convert_currency)
        df['Выручка'] = df['Выручка'].apply(convert_currency)
        df_list[i]=df
        #df_List_ID[i] = df
        i = i + 1
# преобразование входных Df
df_convert_currency(df_List_ID)

# рабочий код после фильтрации по "Период, месяц", ниже тестовая область
# переименовываем столбцы

# оригинальный список имен столбцов
column_name_list = df_List_ID[0].columns.values.tolist()
# тот, на который хотим менять
new_col_names = ['Segment', 'Access_group', 'Main_manager', 'Doc_number', 'Client', 'Parent_company', 'Type_of_Nom', 'Nom', 'Art', 'Period', 'Count', 'Billing']
# ['Сегмент', 'Группа доступа', 'Основной менеджер', 'Заказ клиента / Реализация', 'Клиент', 'Головное предприятие', 'Вид номенклатуры', 'Номенклатура', 'Артикул', 'Период, месяц', 'Количество', 'Выручка']
# ['Segment', 'Access_group', 'Main_manager', 'Doc_number', 'Client', 'Parent_company', 'Type_of_Nom', 'Nom', 'Art', 'Period', 'Count', 'Billing']
# ф-я для изменения имен столбцов в DF
def comp_columns_dict(col_list1, col_list2, df):
    i = 0
    col_dict = {}
    for i in range(len(col_list1)):
        col_dict.update({col_list1[i] : col_list2[i]})
    df.rename(columns = col_dict, inplace = True)
# Ф-я перебора списка DF и применение функции - comp_columns_dict к каждому DF
def rename_df(df_list):
    for df in df_list:
        comp_columns_dict(column_name_list, new_col_names, df)
    return df_list


rename_df(df_List_ID)

df_sales_wout_VAT = df_List_ID[0].copy()
df_sales_incl_VAT = df_List_ID[1].copy()
#print(df_sales_incl_VAT.head())
#print(df_sales_wout_VAT.info())

""" for row in df_sales_incl_VAT.itertuples(index=False):
    for value in row:
        print(value)
        print(value.find('Ноябрь')) """
        