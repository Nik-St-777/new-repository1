from src.masks  import get_mask_card_number, get_mask_account


class TestMasks:
    def test_get_mask_card_number(self):
        raw = "1234567890123456"
        expected = "123456****3456"
        assert get_mask_card_number(raw) == expected

    def test_get_mask_account(self):
        raw = "40817810123456789012"
        # последние 4: 9012
        expected = "****************9012"
        assert get_mask_account(raw) == expected
