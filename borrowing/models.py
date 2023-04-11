from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return = models.DateField()
    actual_return = models.DateField(null=True)
    book = models.ForeignKey('book.Book', on_delete=models.DO_NOTHING, related_name='borrowings')
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, related_name='borrowings')

    def __str__(self):
        return f'{self.user.get_full_name()} {self.book}'
