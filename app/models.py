from django.db import models


# Create your models here.
class MortgageOffer(models.Model):
    bank_name = models.CharField(max_length=255, verbose_name='Название банка')
    term_min = models.PositiveIntegerField(verbose_name='Срок ипотеки, ОТ')
    term_max = models.PositiveIntegerField(verbose_name='Срок ипотеки, ДО')
    rate_min = models.DecimalField(max_digits=3, decimal_places=1,  verbose_name='Ставка, ОТ')
    rate_max = models.DecimalField(max_digits=3, decimal_places=1, verbose_name='Ставка, ДО')
    payment_min = models.PositiveIntegerField(verbose_name='Сумма кредита, ОТ')
    payment_max = models.PositiveIntegerField(verbose_name='Сумма кредита, ДО')

    def __str__(self):
        return self.bank_name

    class Meta:
        verbose_name = 'Кредитное предложение'
        verbose_name_plural = 'Кредитные предложения'
