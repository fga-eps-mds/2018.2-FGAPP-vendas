from django.db import models

class Order(models.Model):
    date = models.DateTimeField(auto_now_add= True)
    fk_product = models.IntegerField(default= '0')
    fk_buyer = models.IntegerField(default= '0')
    buyer_message = models.TextField()
    quantity = models.IntegerField(default= '0')
    total_price = models.FloatField(default= '0.0')
    closed = models.BooleanField(default= False)

    class Meta:
        ordering = ('date',)