def calculate_discounted_price(name, price, discount_percent):
    discount_amount = price * (discount_percent / 100)
    discounted_price = price - discount_amount
    return name,discounted_price, discount_percent, price
