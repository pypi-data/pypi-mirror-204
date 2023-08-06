class Discount:
    def __init__(self, percentage):
        self.percentage = percentage
        
    def apply_discount(self, category):
        for item in category.items:
            item.price = item.price * (1 - self.percentage / 100)

def apply_discount_to(category, discount):
    discount.apply_discount(category)



