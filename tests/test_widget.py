from src.widget import mask_account_card, get_date


class TestWidget:
    def test_mask_account_card(self):
        account = "40817810123456789012"
        card = "1234567890123456"
        result = mask_account_card(account, card)
        assert "account" in result
        assert "card_number" in result

    def test_get_date(self):
        date_str = get_date()
        # простая проверка формата: YYYY-MM-DD
        assert len(date_str) == 10
        assert date_str[4] == "-"
        assert date_str[7] == "-"
