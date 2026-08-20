from .services_page import ServicesPage
class BookingPage(ServicesPage):
    def book_first_available(self):self.choose_first();self.click(self.BOOK);return self
