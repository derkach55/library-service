from django.core.exceptions import ValidationError
from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return = models.DateField()
    actual_return = models.DateField(null=True, default=None)
    book = models.ForeignKey('book.Book', on_delete=models.DO_NOTHING, related_name='borrowings')
    user = models.ForeignKey('user.User', on_delete=models.DO_NOTHING, related_name='borrowings')

    def validate_borrowing(self):
        if self.expected_return < self.borrow_date:
            raise ValidationError('Expected return date should be after the borrow date.')
        if self.actual_return and self.borrow_date < self.actual_return:
            raise ValidationError('Actual return date should be after the borrow date.')

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.validate_borrowing()
        return super(Borrowing, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.user.get_full_name()} {self.book}'
