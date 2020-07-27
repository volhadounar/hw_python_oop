import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record: Record):
        self.records.append(record)

    def get_period_stats(self, delt_day):
        today = dt.date.today()
        date_before = today - dt.timedelta(days=delt_day)
        return sum([item.amount for item in self.records
                   if date_before < item.date <= today])

    def get_today_stats(self):
        return self.get_period_stats(1)

    def get_week_stats(self):
        return self.get_period_stats(7)

    def get_remained_sum(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        cal_remained = self.get_remained_sum()
        if cal_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    + f'калорийностью не более {cal_remained} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 2.40
    EURO_RATE = 2.73

    def get_today_cash_remained(self, currency):
        sum_remained = self.get_remained_sum()

        if (sum_remained == 0):
            return('Денег нет, держись')

        currency_dict = {
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro'],
            'rub': [1, 'руб']
        }

        str_currency = currency_dict[currency][1]
        if sum_remained > 0:
            result_sum = sum_remained/currency_dict[currency][0]
            return(f'На сегодня осталось {result_sum:.2f} '
                   f'{str_currency}')
        res = abs(sum_remained)/currency_dict[currency][0]
        return(f'Денег нет, держись: твой долг - {res:.2f} '
               f'{str_currency}')


def main():
    # создадим калькулятор денег с дневным лимитом 1000
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    # и к этой записи тоже дата должна добавиться автоматически
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    # а тут пользователь указал дату, сохраняем её
    cash_calculator.add_record(
        Record(amount=3000, comment='бар в Танин др', date='08.11.2019'))
    print(cash_calculator.get_today_cash_remained('rub'))
    # должно напечататься
    # На сегодня осталось 555 руб
    cal_calculator = CaloriesCalculator(100)
    cal_calculator.add_record(
        Record(amount=20, comment='кофе', date='20.07.2020'))
    cal_calculator.add_record(
        Record(amount=30, comment='[хлеб]', date='18.07.2020'))
    cal_calculator.add_record(
        Record(amount=20, comment='сало', date='18.07.2020'))
    print(cal_calculator.get_calories_remained())
    date_before = (dt.datetime.now() - dt.timedelta(days=7)).date()
    print(date_before)
    print(dt.date.today().day)
    print('Here\'s a single-quote escape')
    print('This is an "escape" of a double-quote')


if __name__ == '__main__':
    main()
