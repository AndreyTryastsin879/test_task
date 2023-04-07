TXT_WITH_RECEPIENT_FOR_RANDOM_SENDING = 'etherscan_adresses.txt'

TXT_WITH_PRIVATE_KEYS = 'private_keys.txt'

REPORT_TABLE_NAME = 'report_table.csv'

#количество вариаций в диапазоне min_amount_for_sending и max_amount_for_sending в chain_settings
NUMBER_OF_VARIATIONS_BETWEEN_SENDING_AMOUNT = 50

#интервал для рандомного выбора таймслип между транзакциями
MIN_TIMESLEEP_BETWEEN_TRANSACTIONS = 25

MAX_TIMESLEEP_BETWEEN_TRANSACTIONS = 50

#количество потоков
NUMBER_OF_MULTIPROCESSINGS = 4

#интервал для рандомного выбора таймслип для отсложенного старта потоков
MIN_TIMESLEEP_BETWEEN_MULTIPROCESSING = 5

MAX_TIMESLEEP_BETWEEN_MULTIPROCESSING = 10

#CHAIN_TNX_COUNTER_STRING = '================={} Поток №{} сделано {} транзакций================='