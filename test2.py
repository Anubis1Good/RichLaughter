from datetime import date, timedelta

# Получаем текущую дату
today = date.today()

# Вычитаем один день, чтобы получить вчерашнюю дату
yesterday = today - timedelta(days=1)

print(yesterday)
