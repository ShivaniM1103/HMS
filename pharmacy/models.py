from django.db import models

# Create your models here.
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    expiry_date = models.DateField()

    def __str__(self):
        return self.name