from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField


class EmployeeRecord(models.Model):
    employee_name = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    bank_account_number = EncryptedCharField(max_length=50)
    annual_salary = models.DecimalField(max_digits=12, decimal_places=2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee_name} ({self.department})"

