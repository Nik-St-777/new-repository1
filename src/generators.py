def filter_by_currency(transactions, currency):
    for x in transactions:
        if x["operationAmount"]["currency"]["code"] == currency:
            yield x
