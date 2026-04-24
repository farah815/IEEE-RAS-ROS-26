class Book:
    def __init__(self,title,author):
        self.title=title
        self.author=author
        self.is_available=True
    def borrow_book(self):
        if self.is_available ==True:
            self.is_available=False
            print(f'You borrowed "{self.title}" by {self.author}')

        else:
             print(f'Sorry, "{self.title}" is already out.')
            
book1 = Book("1984", "George Orwell")
book1.borrow_book()
book1.borrow_book()