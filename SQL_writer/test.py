import datetime
x = "Заглушка  M   3/4''"
print(x.replace("'",""))
sql_query = 'INSERT INTO ' + ' VALUES (' + ', '.join(['%s']*5) + ')'
print(sql_query)
""" 
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

date_string = "Декабрь 2021 г."
converted_date = convert_date(date_string)
print(converted_date)
"""


""" Segment='Дальневосточный ФО', 
Access_group='СФО Тактонова', 
Main_manager='Тактонова Наталья', 
_3=nan, 
Doc_number='Заказ клиента Ст00-009866 от 03.06.2019 6:14:15', 
_5='14', 
Client='Ким НЭ, ИП, Уссурийск', 
Parent_company='Ким НЭ, ИП, Уссурийск', 
Type_of_Nom='Резьба никелированная', 
Nom='Заглушка  M   3/4', 
Art='02585', 
Period='01.06.2019', 
Count=40.0, 
Billing=918.84 """