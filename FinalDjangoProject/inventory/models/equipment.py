from django.db import models

class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Equipment Name")
    serial_number = models.CharField(max_length=255, unique=True, verbose_name="Serial Number")
    category = models.CharField(max_length=100, default="General", verbose_name="Category")
    cpu = models.CharField(max_length=100, verbose_name="CPU")
    status = models.CharField(max_length=50, default='Available', choices=(
        ('Available', 'Available'),
        ('Reserved', 'Reserved'),
        ('Unavailable', 'Unavailable')
    ), verbose_name="Status")
    image_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="Image URL")

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipments"