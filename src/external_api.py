def function(transaction):
    amount = float(transaction['operationAmount']['amount'])
    if transaction['operationAmount']['currency']['code'] in ['USD', 'EUR']:
        print("Возвращение суммы транзакции (amount) в рублях")
    else:
        print("Происходит обращение к API для получения текущего курса валют и конвертации суммы операции в рубли.")

    return amount

