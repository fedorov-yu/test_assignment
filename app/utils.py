def get_monthly_payment(req_params: dict, rate: float) -> float | int:
    """
    Function to calculate the monthly payment
    guide: https://mortgage-calculator.ru/
    """
    price = req_params.get('price')
    deposit = req_params.get('deposit')
    term = req_params.get('term')
    if price and deposit and term:
        monthly_rate = rate / 12 / 100
        total_rate = (1 + monthly_rate) ** (int(term) * 12)
        payment = (int(price) - int(deposit)) * total_rate * monthly_rate / (total_rate - 1)
        return payment
    return 0
