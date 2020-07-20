import datetime as dt

class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.comment = comment
        if date == '':
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record : Record):
        self.records.append(record)

    def get_today_stats(self): 
        res = 0
        for item in self.records:
            delt = (dt.datetime.now().date() - item.date).days
            if delt == 0:
                res += item.amount
        return res

    def get_week_stats(self):
        res = 0
        for item in self.records:
            delt = (dt.datetime.now().date() - item.date).days
            if delt >= 0 and delt <= 7:
                res += item.amount
        return res

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_today = self.get_today_stats()
        if calories_today < self.limit:
            cal_remained = self.limit - calories_today
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                +f'калорийностью не более {cal_remained} кКал')
        else:
            return ('Хватит есть!')
         
class CashCalculator(Calculator):
    USD_RATE = 2.40
    EURO_RATE = 2.73

    def convert_num(self, num, currency):
        if currency == 'rub':
            return round(num, 2)
        elif currency == 'usd':
            return round(num / self.USD_RATE, 2)
        elif currency == 'eur':
            return round(num / self.EURO_RATE, 2)

    def get_today_cash_remained(self, currency):
        currency_dict = {
            'usd': 'USD',
            'eur': 'Euro',
            'rub': 'руб'
        }
        sum_today = self.get_today_stats()
        if sum_today < self.limit:
            sum_remained = self.limit - sum_today
            result_sum = self.convert_num(sum_remained, currency)
            return(f'На сегодня осталось {result_sum} '
                 f'{currency_dict[currency]}')
        elif (sum_today == self.limit):
            return('Денег нет, держись')
        else:
            res = self.convert_num(sum_today - self.limit, currency)
            return(f'Денег нет, держись: твой долг - {res} '
                 f'{currency_dict[currency]}')


period = dt.timedelta(hours=3)


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)
        
# дата в параметрах не указана, 
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
                
print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# На сегодня осталось 555 руб

cal_calculator = CaloriesCalculator(100)
cal_calculator.add_record(Record(amount=20, comment="кофе", date="20.07.2020"))
cal_calculator.add_record(Record(amount=30, comment="[хлеб]", date="18.07.2020"))
cal_calculator.add_record(Record(amount=20, comment="сало", date="18.07.2020"))             
print(cal_calculator.get_calories_remained())

date_before = (dt.datetime.now() - dt.timedelta(days=7)).date()
print(date_before)