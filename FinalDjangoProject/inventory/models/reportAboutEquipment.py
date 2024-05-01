from inventory import models
from inventory.models.equipment import Equipment
from inventory.models.report import Report


class ReportAboutEquipment(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
 