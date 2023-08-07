class Discount:
    def __init__(self, percentage):
        self.percentage = percentage

    def apply_discount(self, item):
        percentage = float(self.percentage)
        item.price = item.price * (1 - percentage / 100)


def apply_discount_to(item, discount_code):
    try:
        discount = Discount.objects.get(code=discount_code)
        item.price = item.price - Decimal(item.price * (discount.value / 100))
    except Discount.DoesNotExist:
        pass
    
    return item.price
