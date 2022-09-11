from unittest import TestCase

from app.utils import get_monthly_payment

TEST_DATA_CORRECT = {
    'price': 10_000_000,
    'deposit': 1_000_000,
    'term': 20
}
rate = 6.0
TEST_DATA_INCORRECT = {}


class CalculateTestCase(TestCase):
    """Test https://mortgage-calculator.ru/"""

    def test_calculate_true(self) -> None:
        """Correct input data"""
        result = get_monthly_payment(req_params=TEST_DATA_CORRECT, rate=rate)
        self.assertEqual(64479, round(result))  # rounded into serializer

    def test_calculate_false(self) -> None:
        """Incorrect input data"""
        result = get_monthly_payment(req_params=TEST_DATA_INCORRECT, rate=rate)
        self.assertEqual(0, result)
