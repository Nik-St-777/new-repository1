
        # тест на правильность работы функции, которая принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных (float).

        from unittest.mock import patch


        @patch('builtins.print')
        def test_function_with_usd(mock_print):
            # Тестовые данные для USD
            transaction = {
                'operationAmount': {
                    'amount': '100.00',
                    'currency': {'code': 'USD'}
                }
            }

            # Вызов функции
            result = function(transaction)

            # Проверка возвращаемого значения
            assert result == 100.0
            # Проверка, что напечатался правильный текст
            mock_print.assert_called_once_with("Возвращение суммы транзакции (amount) в рублях")

        @patch('builtins.print')
        def test_function_with_other_currency(mock_print):
            # Тестовые данные для другой валюты (например, GBP)
            transaction = {
                'operationAmount': {
                    'amount': '250.50',
                    'currency': {'code': 'GBP'}
                }
            }

            # Вызов функции
            result = function(transaction)

            # Проверка возвращаемого значения
            assert result == 250.50
            # Проверка, что напечатался текст про обращение к API
            mock_print.assert_called_once_with(
                "Происходит обращение к API для получения текущего курса валют и конвертации суммы операции в рубли."
            )

