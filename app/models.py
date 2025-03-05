class Product:
    """Mahsulot obyektini yaratish uchun klass."""
    
    def __init__(self, id, title, price, image, link, shipping):
        self.id = id
        self.title = title
        self.price = float(price)  # Narxni son shaklida saqlaymiz
        self.image = image
        self.link = link
        self.shipping = shipping
        self.final_price = self.calculate_price()  # Ustama qo‘shilgan narx
    
    def calculate_price(self):
        """Narx ustiga 30% ustama qo‘shish."""
        markup = 1.3  # 30% ustama
        return round(self.price * markup, 2)  # Narxni yaxlitlash
    
    def to_dict(self):
        """Mahsulot obyektini JSON formatga o'tkazish."""
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "final_price": self.final_price,
            "image": self.image,
            "link": self.link,
            "shipping": self.shipping
        }

# Mustaqil funksiya - mahsulot narxiga ustama qo‘shish
def calculate_price(original_price):
    """Mahsulot narxiga 30% ustama qo‘shish."""
    markup = 1.3  # 30% ustama
    return round(original_price * markup, 2)  # Narxni yaxlitlash