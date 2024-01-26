import datetime

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
