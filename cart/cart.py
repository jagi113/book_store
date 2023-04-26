from django.conf import settings

from books.models import Book


class Cart(object):
    def __init__(self, request):
        """Initializing Cart"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            self.cart = self.session[settings.CART_SESSION_ID] = {}
        else:
            self.cart = cart

    def add(self, book, quantity=1, override=False):
        book_id = str(book.id)
        if book_id not in self.cart.keys():
            self.cart[book_id] = {"quantity": quantity, "price": float(book.price)}
        elif override:
            self.cart[book_id]["quantity"] = quantity
        else:
            self.cart[book_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, book):
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def __iter__(self):
        book_ids = self.cart.keys()
        books = Book.objects.filter(id__in=book_ids)

        cart = self.cart.copy()
        for book in books:
            cart[str(book.id)]["book"] = book

        for book in cart.values():
            yield book

    def __len__(self):
        return sum(int(item["quantity"]) for item in self.cart.values())

    def __str__(self):
        return " | ".join(list(self.cart.keys()))

    @property
    def total_price(self):
        return round(
            sum(float(item["price"] * item["quantity"]) for item in self.cart.values()),
            2,
        )

    @property
    def notax_price(self):
        return round(
            sum(
                float(item["price"]) / 1.2 * item["quantity"]
                for item in self.cart.values()
            ),
            2,
        )

    @property
    def tax(self):
        return round(
            self.total_price
            - sum(
                float(item["price"]) / 1.2 * item["quantity"]
                for item in self.cart.values()
            ),
            2,
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
