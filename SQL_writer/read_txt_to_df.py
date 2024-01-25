import pandas as pd
import datetime 

# блок переменных, предполагается, что будут вноситься input'ом
#date_period = "Сентябрь 2023 г."
#segment = "ЕАЭС"
# конец блока переменных

# блок инициализации DateFrame, первичная агрегация и очистка

df_1C_sales_include_VAT = pd.read_csv('C:/Users/vorotintsev/Desktop/Проекты PYTHON/Input_data/Sales_Include_VAT.csv', header=0, sep='\t', on_bad_lines="skip",
                                        engine='python')
df_1C_sales_without_VAT = pd.read_csv('C:/Users/vorotintsev/Desktop/Проекты PYTHON/Input_data/Sales_WIthout_VAT.csv', header=0, sep='\t', on_bad_lines="skip",
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
        new_val = str(val).replace(',','.').replace('\xa0', '')
        # преобразуем в число с плавающей точкой
        return float(new_val)
    else:
        return val

# Ф-я преобразования строки с датой в дату
def convert_date(date_string):
    # Разделяем строку на  месяц, год
    month, year = date_string[:-3].split(' ')
    
    # Создаем словарь для соответствия числового значения месяца его названию по-русски
    month_dict = {
        'Январь': '01',
        'Февраль': '02',
        'Март': '03',
        'Апрель': '04',
        'Май': '05',
        'Июнь': '06',
        'Июль': '07',
        'Август': '08',
        'Сентябрь': '09',
        'Октябрь': '10',
        'Ноябрь': '11',
        'Декабрь': '12'
    }
    
    # Получаем числовое значение месяца
    month = month_dict[month]
    
    # Преобразуем день, месяц и год в числовой формат
    month, year = int(month), int(year)
    day = 1
    # Создаем новую дату с заданным днем, месяцем и годом
    new_date = datetime.date(year, month, day)
    
    return new_date.strftime("%d.%m.%Y")

def slice_str(val):
    if val !='':
        space_index = val.find(' ')
        if space_index < 0:
            return val
        else:
            new_val = val[:space_index]
            return new_val
    else:
        return val

# функция преобразования входных df' ом
def df_convert_currency(df_list):   
    i = 0
    for df in df_list:
        # удаляем "NaN"
        df = df.dropna(subset=['Период, месяц'])
        df = df.dropna(subset=['Сегмент'])
        df = df.dropna(subset=['Группа доступа'])
        # преобразуем столбцы
        df['Головное предприятие']=df['Головное предприятие'].fillna(df['Клиент'])
        df['Количество'] = df['Количество'].apply(convert_currency)
        df['Выручка'] = df['Выручка'].apply(convert_currency)
        df[['Выручка', 'Количество']] = df[['Выручка', 'Количество']].fillna(0)
        df['График оплаты'] = df['График оплаты'].fillna('')
        df['График оплаты'] = df['График оплаты'].apply(slice_str)
        df['Период, месяц'] = df['Период, месяц'].apply(convert_date)
        
        df_list[i]=df
        #df_List_ID[i] = df
        i = i + 1
# преобразование входных Df
df_convert_currency(df_List_ID)
#print(df_List_ID[0].info())
#print(df_List_ID[0].head())
# рабочий код после фильтрации по "Период, месяц", ниже тестовая область
# переименовываем столбцы

# оригинальный список имен столбцов
column_name_list = df_List_ID[0].columns.values.tolist()
# тот, на который хотим менять
new_col_names = ['Segment', 'Access_group', 'Main_manager', 'Reduction factor', 'Doc_number', 'Payment schedule', 'Client', 'Parent_company', 'Type_of_Nom', 'Nom', 'Art', 'Period', 'Count', 'Billing']
# ['Сегмент', 'Группа доступа', 'Основной менеджер', 'Понижающий коэф(Общие)', 'Заказ клиента / Реализация', 'График оплаты', 'Клиент', 'Головное предприятие', 'Вид номенклатуры', 'Номенклатура', 'Артикул', 'Период, месяц', 'Количество', 'Выручка']
# ['Segment', 'Access_group', 'Main_manager', 'Reduction factor', 'Doc_number', 'Payment schedule', 'Client', 'Parent_company', 'Type_of_Nom', 'Nom', 'Art', 'Period', 'Count', 'Billing']
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
#json_sales_wout_VAT = df_sales_wout_VAT.to_json(orient='table')
#with open('SQL_writer/DATA/sales_wout_VAT.json', 'w') as file:
#    file.write(json_sales_wout_VAT)
    
#print(df_sales_incl_VAT.head())
#print(df_sales_wout_VAT.info())
print(len(df_sales_wout_VAT))