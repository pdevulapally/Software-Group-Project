from .inventory import Inventory
from .equipment import Equipment
from django.db import models

class InventoryEquipmentStorage(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)